import configparser
import logging
import os

from server import Server

def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", "settings.ini"))

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")

    Server((host, int(port)))

if __name__ == "__main__":
    main()