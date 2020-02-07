import socket

class SocketHelper():
    @staticmethod
    def recv(sock, count):
        # TODO: docstring
        # recv by count
        buf = b''
        
        while count:
            newbuf = None
            try:                
                newbuf = sock.recv(count)
            except Exception:
                raise socket.timeout

            if not newbuf:
                return None

            buf += newbuf
            count -= len(newbuf)
        return buf

    @staticmethod
    def send(sock, data, lenBefore=False):
        print((str(len(data)).ljust(16)).encode("ascii"))
        try:
            if lenBefore:
                sock.send((str(len(data)).ljust(16)).encode("ascii"))
            sock.send(data)
        except Exception:
            raise socket.timeout
        
        