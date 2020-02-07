import socket
import random
import logging
import re

from socketHelper import SocketHelper
from dataclasses import dataclass

@dataclass(init=True)
class Client:
    id: int = random.randint(1 * 10**15, 1 * 10**16)
    typeid: int = None
    sock: socket = None
    dead: bool = False

    @staticmethod
    def find(clients, typeid):
        i = 0
        for client in clients:
            if client.typeid == str(typeid):
                #print("check")
                return i
            i += 1
        return None

    @staticmethod
    def verify(clients, conn):
        logger = logging.getLogger("client")
        logger.debug("Awaiting registration...")

        data = None
        while data == None:
            data = SocketHelper.recv(conn, 14)
        data = data.decode("ascii")

        if re.fullmatch("Registration [0-3]{1}$", data, flags=0):
            logger.debug("Registration complete.")
            
            id = data.split(" ", 1)[1]
            c = Client(typeid=id, sock=conn)
            clients.append(c)

        else:
            logger.warn("Illegal registration.")

    def cleanup(clients):
        for client in clients:
            if client.dead:
                clients.remove(client)
