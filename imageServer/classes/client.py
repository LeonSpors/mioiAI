import socket

class Client:
    addr = None
    sock = None

    # data = sock.recv(1024)
    # data = data.decode('ascii')

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


    # def register(self):
    #     self.sock.sendall("8 {0}".format(ServerType.IMAGE).encode('ascii'))
    #     f = self.sock.makefile()
    #     f.flush()

    def send(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()