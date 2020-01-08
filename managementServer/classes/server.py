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
        thread = threading.Thread(target=self._incomingConnectionHandler_)
        thread.start()

    def _incomingConnectionHandler_(self):
        # TODO: Docstring
        logging.debug("Awaiting connection requests")

        while not self.shutdownRequest:
            connection, addr = self.sock.accept()
            connection.settimeout(1)
            print(connection.gettimeout())
            logging.debug("Connection {0} etablished. Starting worker...".format(addr))

            workerThread = threading.Thread(target=self._worker_, args=(connection,))
            workerThread.start()

    def recvall(self, sock, count):
        # TODO: docstring
        buf = b''
        while count:
            newbuf = None
            try:                
                newbuf = sock.recv(count)
            except Exception as err:
                logging.error(err)


            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def _recvImageWorker_(self):
        logging.debug("recv image worker started")

        client = self.clients["img"]

        t = threading.currentThread()
        while getattr(t, "do_run", True):
            length = self.recvall(client, 16)
            if length != None:
                stringData = self.recvall(client, int(length))
            else:
                logging.debug("recv image worker stopped")
                self.clients["img"] = None
                t.do_run = False

            self.data = stringData

    def _echoWorker_(self):
        # TODO: Clean up
        #   Docstring
        logging.debug("echo worker started")

        mlClient = self.clients.get("ml")

        lastSend = 0
        try:
            while self.clients.get("ml") != None and self.clients.get("img") != None:
                datac = self.data
                if datac != None:
                    currLen = len(datac)
                    if lastSend != currLen:
                        logging.info(f"Sent {currLen}")
                        lastSend = currLen                    
                        mlClient.send((str(lastSend).ljust(16)).encode("ascii"))
                        mlClient.send(datac)
        except Exception as e:
            self.clients["ml"] = None
            print(e)

        logging.debug("echo worker stopped")

    def _statusWorker_(self):
        echoWorkerThread = None

        while echoWorkerThread == None:
            for w in self.workers:
                if w.name == "echo_thread":
                    echoWorkerThread = w
            time.sleep(1)

        while True:
            #print(echoWorkerThread.isAlive())

            if echoWorkerThread.isAlive():
                for c in self.clients:
                    if self.clients.get(c) == None:
                        logging.debug(f"Stopping echo worker. Reason: {c.getsockname()} connection lost")
                        echoWorkerThread.do_run = False        
            else:
                if self.clients.get("img") != None and self.clients.get("ml") != None:
                    logging.debug(f"Start echo worker. All clients connected.")
                    echoWorkerThread.start()

            time.sleep(1)
    
    def _worker_(self, client):
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
            self.clients["img"] = client
            for w in self.workers:
                if w.getName() == "recvImage_thread":
                    w.start()
        elif data[0] == "REG" and data[1] == "ml":
            self.clients["ml"] = client
            logging.debug("Registration complete.")
            pass
        else:
            logging.debug("Registration failed. Closing connection.")
            client.close()
            
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

        logging.debug("Threads initialization...")
        t = threading.Thread(target=self._recvImageWorker_, args=(), name="recvImage_thread")
        t.daemon = True
        self.workers.append(t)

        #self.workers.append(threading.Thread(target=self._recvImageWorker_, args=(), name="recvPred_thread"))        
        t = threading.Thread(target=self._echoWorker_, args=(), name="echo_thread")
        t.daemon = True
        self.workers.append(t)

        t = threading.Thread(target=self._statusWorker_, args=(), name="status_thread")
        t.start()
        self.workers.append(t)
