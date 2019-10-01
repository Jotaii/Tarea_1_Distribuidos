import socket
import sys

def fileWrite(message):
    f = open("registro_cliente.txt", "a")
    f.write(message)
    f.close()

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    

#Iniciando cliente
fileWrite("Iniciando cliente: Abriendo socket...\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

fileWrite("Conectando con headnode...\n")
server_address = ("headnode", 5001)
newSocket.connect(server_address)

try:
    print("Escriba un mensaje para un datanode: ")
    user_input = input()
    fileWrite("Usuario escribe: " + user_input + "\n")

    fileWrite("Enviando mensaje a headnode...\n")
    message = bytes(user_input, 'utf-8')
    newSocket.sendall(message)

    data = newSocket.recv(1024)
    fileWrite('Headnode responde: ' + str(data, 'utf-8') + "\n")
    print('Headnode responde: ' + str(data, 'utf-8'))

finally:
    print("Terminando conexion con headnode")
    fileWrite("Cerrando socket...\n\n")
    newSocket.close()
