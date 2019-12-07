from classes.server import Server
from classes.predictor import Predictor

def run():
    predictor = Predictor()

    server = Server(("localhost", 50000), predictor)
    server.run()

if __name__ == "__main__":
    run()