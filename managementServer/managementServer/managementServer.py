import configparser
import logging

from server import Server

def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read("../data/settings.ini")

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")

    Server((host, int(port)))

if __name__ == "__main__":
    main()