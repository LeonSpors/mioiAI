import os
import configparser

from client import Client
from video import Video


def run():
    
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", "settings.ini"))

    host = config.get("Client", "Host")
    port = config.get("Client", "Port")


    client = Client((host, int(port)))
    ret = client.connect(3)

    if ret is True:
        client.register()        
        video = Video(client)
        video.run()

if __name__ == "__main__":
    run()