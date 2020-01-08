from classes.client import Client
from classes.video import Video

def run():
    client = Client(("localhost", 50000))
    ret = client.connect(3)
    #client.register()

    if ret is True:
        video = Video(client)
        video.run()

if __name__ == "__main__":
    run()