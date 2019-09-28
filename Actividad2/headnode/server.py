import socket
import sys
import os
from datetime import datetime

def fileWrite(message):
    print(message)
    f = open("registro_server.txt", "a")
    f.write(message)
    f.close()

#now = datetime.now()
#current_time = now.strftime("%H:%M:%S")

fileWrite("Iniciando servidor de headnode\n")

newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("headnode", 5001)
newSocket.bind(server_address)
newSocket.listen(1)

while True:

    connection, client_address = newSocket.accept()

    try:
        data = connection.recv(1024)
        fileWrite("Se ha conectado el cliente " + client_address[0] + "\nCliente dice: {!r}".format(data) + "\n")
        
        if data:
            fileWrite("Respondiendo a cliente...\n")
            connection.sendall(b'Que tengas un buen dia')
            
        else:
            fileWrite("Cliente conectado no envia datos\n")
            break

    finally:
        fileWrite("Cerrando conexion con cliente\n\n")
        connection.close()