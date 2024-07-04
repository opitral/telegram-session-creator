import configparser
from pyrogram import Client


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config["Telegram"]["api_id"]
    api_hash = config["Telegram"]["api_hash"]

    session_name = input("(session name) > ")
    bot = Client(f"results/{session_name}", api_id, api_hash)

    with bot:
        account = bot.get_me()
        print(account)


if __name__ == "__main__":
    main()
