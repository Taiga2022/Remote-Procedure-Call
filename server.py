import socket
import os

class Socket:

    def __init__(self, host, port):
        self.host = '127.0.0.1'
        self.port = 8080
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        try:
            os.unlink(self.host)
        except FileNotFoundError:
            pass
        print('Starting up on {} port {}'.format(self.host, self.port))
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)


class Request:
    def __init__(self, sock):
        self.sock = sock
        self.connection=None
        self.client_address=None

    def getFunction(self):
        while True:
           self.connection, self.client_address = self.sock.accept()
           try:
               print('Connection from {}'.format(self.client_address))

               while True:
                   data = self.connection.recv(1024)
                   data_str = data.decode('utf-8')

                   print('Received {!r}'.format(data_str))

                   if data:
                       print('Sending data back to the client')
                       self.connection.sendall(data)
                   else:
                       print('No more data from {}'.format(self.client_address))
                       break
           finally:
               print('Closing connection with {}'.format(self.client_address))
               self.connection.close()

def main():
    sock = Socket('127.0.0.1', 8080)
    sock.bind()
    request = Request(sock.sock)
    request.getFunction()


if __name__ == '__main__':
    main()
