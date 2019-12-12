from classes.client import Client
from classes.video import Video

def run():
    client = Client(("localhost", 50000))
    ret = client.connect(3)

    if ret is True:
        client.register()        
        video = Video(client)
        video.run()

if __name__ == "__main__":
    run()