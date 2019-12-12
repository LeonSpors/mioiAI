from classes.client import Client
from classes.predictor import Predictor

def run():
    predictor = Predictor()

    client = Client(("localhost", 50000))
    ret = client.connect(3)
    if ret == True:
        client.register()
        client.run(predictor)

if __name__ == "__main__":
    run()