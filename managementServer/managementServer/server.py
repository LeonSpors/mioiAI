import socket
import threading
import configparser
import logging

from client import Client
from worker import Worker

class Server:
    clients = []
    threads = []
    logger = None

    def __init__(self, addr):
        self.logger = logging.getLogger("server")
        self.logger.setLevel(logging.DEBUG)

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serversocket.bind(addr)
        serversocket.listen()

        self.logger.info("Server initialized")
        self.start(serversocket)

    def start(self, serversocket):
        w = Worker(self.clients)
        w.start()
        self.threads.append(w)

        self.logger.info("Listening...")     
        while True:
            try:
                (conn, addr) = serversocket.accept()
                conn.settimeout(60)

                Client.verify(self.clients, conn)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                if connection:
                    connection.close()
                self.logger.warn("CRTL-C")

        self.logger.info("Server stopped.")
        serversocket.close()