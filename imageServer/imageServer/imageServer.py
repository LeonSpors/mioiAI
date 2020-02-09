from client import Client
from video import Video

import configparser

def run():
    config = configparser.ConfigParser()
    config.read("../data/settings.ini")

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