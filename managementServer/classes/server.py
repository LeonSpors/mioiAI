from classes.request import Request

import socket
import threading

class Server:
    sock = None
    clients = {}
    shutdownRequest = False

    def __init__(self, addr):
        """Initializes the socket server.
            
        Args:
            addr (tuple): Host and port on which the server is listening
        """
        super().__init__()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(True)
        self._start_()

    def request(self, request):
        if request == Request.Shutdown:
            self.shutdownRequest = True

    def _start_(self):
        """Handles incoming connections.
        """
        thread = threading.Thread(target=self.__incomingConnectionHandler__)
        thread.start()

    def __incomingConnectionHandler__(self):
        print("Server is listening for clients")
        while not self.shutdownRequest:
            connection, addr = self.sock.accept()
            workerThread = threading.Thread(target=self.__worker__)
            workerThread.start()
            self.clients[connection] = workerThread

    def __worker__(self):
        print("worker")