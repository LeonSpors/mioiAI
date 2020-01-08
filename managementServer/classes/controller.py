from classes.server import Server
from classes.request import Request

import configparser
import signal

class Controller:
    server = None
    status = {}

    def onShutdownRequest(self, signal, frame):
        print("Cleaning up...")
        self.server.request(Request.Shutdown)
        exit(0)  

    def __init__(self, host, port):
        super().__init__()

        signal.signal(signal.SIGINT, self.onShutdownRequest)

        self.register("imageServer", "unknown")
        self.register("mlServer", "unknown")

        self.server = Server(host, port)

    def register(self, key, value):
        self.status[key] = value

    def run(self):
        pass

