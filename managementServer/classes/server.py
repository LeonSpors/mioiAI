import socket
import threading

class Server:
    sock = None
    clients = {}

    def __init__(self, addr):
        """Initializes the socket server.
            
        Args:
            addr (tuple): Host and port on which the server is listening
        """
        super().__init__()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(True)
        self.start()

    def start(self):
        """Handles incoming connections.
        """
        thread = threading.Thread(target=self.__incomingConnectionHandler__)
        thread.start()

    def __incomingConnectionHandler__(self):
        print("Server is listening for clients")
        while True:
            connection, addr = self.sock.accept()
            workerThread = threading.Thread(target=self.worker)
            workerThread.start()
            self.clients[connection] = workerThread

    def worker(self):
        print("worker")