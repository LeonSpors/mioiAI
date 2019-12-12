import socket
import numpy as np
import cv2

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
        self.sock.sendall("REG ml".ljust(8).encode("ascii"))
        f = self.sock.makefile()
        f.flush()

    def recvall(self, count):
        buf = b''
        while count:
            newbuf = self.sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def run(self, predictor):
        while True:
            length = self.recvall(16)
            stringData = self.recvall(int(length))
            data = np.frombuffer(stringData, dtype='uint8')

            decimg = cv2.imdecode(data, 1)
            predictor.predict(decimg)
            
            cv2.imshow("preview", decimg)
            cv2.waitKey(1)