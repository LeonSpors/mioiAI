import socket
import threading
import logging
import queue
import time

from client import Client
from socketHelper import SocketHelper

class Worker(threading.Thread):
    clients = None #see self.__init__
    logger = None
    workerThreads = []
    pipeline = None
    dead = False
    stopRequest = False

    def __init__(self, clients):
        threading.Thread.__init__(self)

        self.clients = clients
        self.pipeline = queue.Queue()
        self.logger = logging.getLogger("worker")
        self.logger.debug("Initialization successful")  

    def run(self):
        t = threading.Thread(target=self.recviever)
        t.start()
        self.workerThreads.append(t)

        t = threading.Thread(target=self.sender)
        t.start()
        self.workerThreads.append(t)

        t = threading.Thread(target=self.predrecviever)
        t.start()
        self.workerThreads.append(t)

    # From Video Server    
    def recviever(self):
        self.logger.debug("Reciever started.")

        while not self.stopRequest:
            client = None
            if len(self.clients) > 0:
                clientId = Client.find(self.clients, 0)
                
                if clientId != None:
                    client = self.clients[clientId]

            if client != None:
                #print(client.dead)

                while not client.dead:
                    try:
                        length = SocketHelper.recv(client.sock, 16)
                        if length != None:
                            stringData = SocketHelper.recv(client.sock, int(length))

                            if stringData != None:
                                #self.logger.debug(stringData)
                                self.pipeline.put(stringData, block=False)
                    except socket.timeout:
                        client.dead = True
            
            Client.cleanup(self.clients)
            time.sleep(1/40)
        self.logger.debug("Reciever stopped.")

    # From Pred Server
    def predrecviever(self):
        self.logger.debug("Predreciever started.")

        while not self.stopRequest:
            client = None
            if len(self.clients) > 0:
                clientId = Client.find(self.clients, 1)
                
                if clientId != None:
                    client = self.clients[clientId]

            if client != None:
                #print(client.dead)

                while not client.dead:
                    try:
                        length = SocketHelper.recv(client.sock, 16)
                        if length != None:
                            print(length)       
                            stringData = SocketHelper.recv(client.sock, int(length))
                            print(stringData)
                            if stringData != None:
                                data = int(stringData.decode("ascii"))
                                self.doAction(data)
                    except socket.timeout:
                        client.dead = True
            
            Client.cleanup(self.clients)
            time.sleep(1/40)

        self.logger.debug("Predreciever stopped.")

    # To Pred Server
    def sender(self):
        self.logger.debug("Sender started.")

        while not self.stopRequest:
            client = None
            if len(self.clients) > 0:
                clientId = Client.find(self.clients, 1)
                
                if clientId != None:
                    client = self.clients[clientId]

            if client != None:
                while not client.dead:
                    item = self.pipeline.get(block=True)

                    if item != None:
                        try:
                            SocketHelper.send(client.sock, item, True)
                        except socket.timeout:
                            client.dead = True

                    self.pipeline.task_done()
            
            Client.cleanup(self.clients)
            time.sleep(1/40)
        self.logger.debug("Sender stopped.")

    def doAction(self, id):
        print(id)    