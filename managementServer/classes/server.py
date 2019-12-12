from classes.request import Request

import logging
import socket
import threading
import time

class Server:
    sock = None
    clients = {}
    workers = []
    
    data = None

    shutdownRequest = False

    def __init__(self, addr):
        """Initializes the socket server.
            
        Args:
            addr (tuple): Host and port on which the server is listening
        """
        super().__init__()

        logging.basicConfig(level=logging.DEBUG)  
        logging.debug("Server initialization...")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(True)
        self._start_()

    def request(self, request):
        """[summary]
        
        Args:
            request (Request): [description]
        """
        # TODO: Docstring
        if request == Request.Shutdown:
            self.shutdownRequest = True

    def _start_(self):
        """Handles incoming connections.
        """
        thread = threading.Thread(target=self.__incomingConnectionHandler__)
        thread.start()

    def __incomingConnectionHandler__(self):
        # TODO: Docstring
        logging.debug("Awaiting connection requests")

        while not self.shutdownRequest:
            connection, addr = self.sock.accept()
            logging.debug("Connection {0} etablished. Starting worker...".format(addr))

            workerThread = threading.Thread(target=self.__worker__, args=(connection,))
            workerThread.start()
            self.clients[connection] = workerThread

    def recvall(self, sock, count):
        # TODO: docstring
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def _recvImageWorker_(self, client):
        logging.debug("recv image worker started")
        while True:
            length = self.recvall(client, 16)
            stringData = self.recvall(client, int(length))
            self.data = stringData
            self.dataChanged = time.time()

    def _echoWorker_(self):
        # TODO: Clean up
        #   Docstring
        logging.debug("echo worker started")

        # Find ml client
        client = None
        while client == None:
            client = self.clients.get("ml")
            time.sleep(0.1)

        logging.info("ml client found")

        lastSend = 0
        while True:
            currLen = len(self.data)
            if lastSend != currLen:
                logging.info(f"Sent {currLen}")
                lastSend = currLen
                client.send((str(lastSend).ljust(16)).encode("ascii"))
                client.send(data)

    def __worker__(self, client):
        # TODO: Encapsulate inner worker routine.
        # Exception handling
        # Clean up.
        # Docstring
        logging.debug("Worker started.")

        ct = None

        # Waiting for registration
        data = self.recvall(client, 8).decode("ascii")
        data = str(data).split()

        if data[0] == "REG" and data[1] == "img":
            logging.debug("Registration complete.")
            riw = threading.Thread(target=self._recvImageWorker_, args=(client,))
            riw.start()
            self.workers.append(riw)

            ew = threading.Thread(target=self._echoWorker_)
            ew.start()
            self.workers.append(ew)
        elif data[0] == "REG" and data[1] == "ml":
            logging.debug("Registration complete.")
            pass
        else:
            logging.debug("Registration failed. Closing connection.")
            client.close()
            

