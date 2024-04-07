import socket
import os

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

Host='127.0.0.1'
Port=8080

try:
    os.unlink(Host)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(Host))

sock.bind((Host,Port))

sock.listen(1)

while True:
    connection,client_address=sock.accept()
    try:
        print('Connection from {}'.format(client_address))

        while True:
            data=connection.recv(1024)
            data_str=data.decode('utf-8')

            print('Received {!r}'.format(data_str))

            if data:
                print('Sending data back to the client')
                connection.sendall(data)
            else:
                print('No more data from {}'.format(client_address))
                break
    finally:
        print('Closing connection with {}'.format(client_address))
        connection.close()
