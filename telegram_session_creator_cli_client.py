import json
import os
import configparser
import sys
from datetime import datetime

import requests
import logging

from pyrogram import Client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("creator.log")
file_handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config["Telegram"]["api_id"]
api_hash = config["Telegram"]["api_hash"]
api_key = config["Asocks"]["api_key"]
country_code = config["Asocks"]["country_code"]


def create_proxy(country="UA", type_id=2, proxy_type_id=1, name=None, server_port_type_id=1):
    try:
        params = {
            "country_code": country,
            "state": None,
            "city": None,
            "asn": None,
            "type_id": type_id,
            "proxy_type_id": proxy_type_id,
            "name": name,
            "server_port_type_id": server_port_type_id
        }
        response = requests.post(f"https://api.asocks.com/v2/proxy/create-port?apiKey={api_key}", data=params)

        if response.status_code == 200:
            data = response.json().get("data", {})
            proxy = {
                "scheme": "socks5",
                "hostname": data["server"],
                "port": data["port"],
                "username": data["login"],
                "password": data["password"]
            }

            logger.info(f"Proxy created: {proxy['hostname']}:{proxy['port']}")

            return proxy

        else:
            logger.warning(F"Asocks return status code: {response.status_code}")

    except Exception as ex:
        logger.error(f"Error while creating proxy, details: {ex}")


def main():
    session_name = input("(session name) > ")
    account_dir = os.path.join(os.getcwd(), "results", session_name)

    if os.path.isdir(account_dir):
        logger.error(f"Session with the name \"{session_name}\" already exists")
        sys.exit(1)

    os.makedirs(os.path.dirname(account_dir), exist_ok=True)
    os.mkdir(account_dir)

    proxy = None

    try:
        proxy = create_proxy(name=session_name, country=country_code)
        session_file_path = os.path.join(account_dir, session_name)
        bot = Client(session_file_path, api_id, api_hash, proxy=proxy, lang_code="ru")

        with bot:
            account = bot.get_me()
            logger.info(account)

    except Exception as ex:
        logger.error(f"Error while creating session, details: {ex}")

    else:
        logger.info(f"Session created")

    try:
        db_name = input("(db name) > ")
        to_chat_link = input("(chat link) > ")

        session_config = {
            "session": session_name,
            "proxy": proxy,
            "db": db_name,
            "to_chat": to_chat_link,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(f"{account_dir}/{session_name}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(session_config, indent=4, ensure_ascii=False))

        logger.info(session_config)

    except Exception as ex:
        logger.error(f"Error while creating config, details: {ex}")

    else:
        logger.info("Config created")


if __name__ == "__main__":
    main()
