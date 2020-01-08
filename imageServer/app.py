from classes.client import Client
from classes.video import Video

import configparser

def run():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")

    client = Client(host, port)
    ret = client.connect(3)

    if ret is True:
        client.register()        
        video = Video(client)
        video.run()

if __name__ == "__main__":
    run()