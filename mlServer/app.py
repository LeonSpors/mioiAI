from classes.client import Client
from classes.predictor import Predictor

import configparser

def run():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")

    predictor = Predictor()

    client = Client((host, port))
    ret = client.connect(3)
    if ret == True:
        client.register()
        client.run(predictor)

if __name__ == "__main__":
    run()