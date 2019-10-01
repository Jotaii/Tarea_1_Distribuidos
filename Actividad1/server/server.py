import socket
import sys
import os
from datetime import datetime

# Creación de registro_cliente.txt en el almacenamiento del cliente
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def createFile():
    f = open("log.txt", "w")
    f.close()

# Función para escribir mensajes en registro_ciente.txt
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def fileWrite(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open("log.txt", "a")
    f.write("[" + current_time + "] " + message)
    f.close()

# Iniciación del servidor
createFile()
fileWrite("Iniciando servidor\n\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Apertura de socket
server_address = ("server", 5000)
newSocket.bind(server_address)
newSocket.listen(1)

# Espera de peticiones
while True:
    connection, client_address = newSocket.accept()

    # Conexión con un cliente
    try:
        fileWrite("Se ha conectado el cliente " + client_address[0] + " al servidor\n")
        data = connection.recv(1024)
        fileWrite("Cliente dice: " + str(data, 'utf-8') + "\n")

        # Cliente envía un mensaje
        if data:
            fileWrite("Respondiendo a cliente\n")
            connection.sendall(b'Mensaje almacenado con exito')
            
        # Cliente conectado pero no envía mensaje
        else:
            fileWrite("Cliente conectado pero no envia datos\n")
            break

    # Cerrando conexión con el cliente
    finally:
        fileWrite("Cerrando conexion con el cliente\n\n")
        connection.close()