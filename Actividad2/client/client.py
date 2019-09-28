import socket
import sys

def fileWrite(message):
    f = open("registro_cliente.txt", "a")
    f.write(message)
    f.close()

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    

#Iniciando cliente
fileWrite("Iniciando cliente...\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("headnode", 5001)

fileWrite("Conectando con headnode...\n")
newSocket.connect(server_address)

try:

    fileWrite("Enviando saludo...\n")
    message = b'Saludos'
    newSocket.sendall(message)

    data = newSocket.recv(1024)
    fileWrite('Servidor responde {!r}'.format(data)+ "\n")

finally:

    fileWrite("Cerrando socket...\n\n")
    newSocket.close()
