import socket
import os
import json
import math
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

    def receive(self):
        while True:
           self.connection, self.client_address = self.sock.accept()
           try:
               print('Connection from {}'.format(self.client_address))

               while True:
                   data = self.connection.recv(1024)
                   data_str = data.decode('utf-8')

                   print('Received {!r}'.format(data_str))

                   return data_str
           except Exception as e:
               print(e)


    def send(self, data):
        try:
            if data:
                print('Sending data back to the client')
                sendData = json.dumps(data)
                self.connection.sendall(sendData.encode('utf-8'))
            else:
                print('No more data from {}'.format(self.client_address))
        finally:
            print('Closing connection with {}'.format(self.client_address))
            self.connection.close()




class Function:
    def __init__(self, requestJson):
        self.method = requestJson['method']
        self.params = requestJson['params']
        self.param_types = requestJson['param_types']
        self.id=requestJson['id']
        self.result = self.call()
        self.result_type = type(self.result).__name__

    def call(self):
        if self.method == 'floor':
            return math.floor(self.params)
        elif self.method == 'nroot':
            return math.floor(self.params[0]**(1/self.params[1]))
        elif self.method == 'reverse':
            return self.params[::-1]
        elif self.method == 'validAnagram':
            return sorted(self.params[0]) == sorted(self.params[1])
        elif self.method == 'sort':
            return sorted(self.params)
        else:
            return print("Method not found")

    def response(self):
        return {
            'result': self.result,
            'result_type': self.result_type,
            'id': self.id
        }




def main():
    sock = Socket('127.0.0.1', 8080)
    sock.bind()
    request = Request(sock.sock)
    data = request.receive()
    response=Function(json.loads(data)).response()
    request.send(response)


if __name__ == '__main__':
    main()
