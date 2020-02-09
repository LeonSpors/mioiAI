import socket
import numpy as np
import cv2

from socketHelper import SocketHelper

class Client:
    addr = None
    sock = None


    def __init__(self, address):
        self.addr = address
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    def connect(self, n):
        for retry in range(0, n):
            try:
                self.sock.connect(self.addr)
                return True
            except Exception as e:
                print(f"{e}. Retry.")
        
        return False

    def register(self):
        self.sock.sendall("Registration 1".encode("ascii"))
        f = self.sock.makefile()
        f.flush()

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def run(self, predictor):
        while True:
            length = SocketHelper.recv(self.sock, 16)
            
            if length != None:
                length = length.decode("ascii")

                stringData = SocketHelper.recv(self.sock, int(length))
                data = np.frombuffer(stringData, dtype='uint8')

                decimg = cv2.imdecode(data, 1)
                p = predictor.predict(decimg)
                
                SocketHelper.send(self.sock, data, True, True)

                cv2.imshow("preview", decimg)
                cv2.waitKey(1)