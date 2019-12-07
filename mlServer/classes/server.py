from classes.predictor import Predictor
import socket
import cv2
import numpy as np

class Server:
    addr = None
    sock = None
    Predictor = None

    def __init__(self, addr, predictor):
        self.addr = addr

        if predictor is None:
            raise("Predictor is null")

        self.predictor = predictor

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen(True)

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def run(self):
        conn, addr = self.sock.accept()

        while True:
            length = self.recvall(conn, 16)
            stringData = self.recvall(conn, int(length))
            data = np.frombuffer(stringData, dtype='uint8')

            decimg = cv2.imdecode(data, 1)
            self.predictor.predict(decimg)
            
            cv2.imshow("preview", decimg)
            cv2.waitKey(1)