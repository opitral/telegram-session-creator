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
        proxy = {
            "scheme": "socks5",
            "hostname": input("(proxy ip address) > "),
            "port": int(input("(proxy port) > ")),
            "username": input("(proxy username) > "),
            "password": input("(proxy password) > ")
        }
        session_file_path = os.path.join(account_dir, session_name)
        bot = Client(session_file_path, api_id, api_hash, ipv6=True, proxy=proxy, lang_code="ru")

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
            "blocked": False,
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
