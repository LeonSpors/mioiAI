from classes.server import Server
import signal

class Controller:
    server = None
    status = {}

    def __init__(self):
        super().__init__()

        signal.signal(signal.SIGINT, self.onShutdownRequest)

        self.register("imageServer", "unknown")
        self.register("mlServer", "unknown")

        self.server = Server(("localhost", 50000))

    def onShutdownRequest(self, signal, frame):
        print("Cleaning up...")
        #self.server.requestShutdown()
        exit(0)  

    def register(self, key, value):
        self.status[key] = value

    def run(self):
        pass

