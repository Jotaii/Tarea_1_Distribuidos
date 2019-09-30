import socket
import sys
import os
from datetime import datetime

f = open("log.txt", "a")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

f.write("[" + current_time + "] Iniciando servidor\n")
f.close()

newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Se utiliza la ip "0.0.0.0" para que todos puedan acceder al servidor mientras estén en la misma red.
#Se utiliza el port 5000 especificado en la tarea.
server_address = ("server", 5000)
newSocket.bind(server_address)
newSocket.listen(1)

while True:
    connection, client_address = newSocket.accept()

    try:
        f = open("log.txt", "a")
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        f.write("[" + current_time + "] Se ha conectado el cliente " + client_address[0] + " al servidor\n")

        data = connection.recv(1024)
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        f.write("[" + current_time + "] " + 'Cliente dice: {!r}'.format(data) + "\n")

        if data:
            now = datetime.now()        
            current_time = now.strftime("%H:%M:%S")
            f.write("[" + current_time + "] Respondiendo a host...\n")
            connection.sendall(b'Que tengas un buen dia')
            
        else:
            now = datetime.now()        
            current_time = now.strftime("%H:%M:%S")
            f.write("[" + current_time + "] Host conectado pero no envia datos\n")
            break

    finally:
        f.write("[" + current_time + "] Cerrando conexion con el cliente\n")
        f.write(" \n")
        f.close()
        connection.close()