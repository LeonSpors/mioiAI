from classes.controller import Controller

import configparser

def main():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")

    Controller(host, port).run()

if __name__ == "__main__":
    main()