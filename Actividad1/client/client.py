import socket
import sys

def fileWrite(message):
    print(message)
    f = open("respuestas.txt", "a")
    f.write(message)
    f.close()

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    


fileWrite("Iniciando cliente\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("server", 5000)
print('Conectando a servidor {} por puerto {}'.format(*server_address))
fileWrite('Conectando a servidor {} por puerto {}'.format(*server_address) + "\n")
newSocket.connect(server_address)


try:
    
    fileWrite("Enviando saludo al servidor...\n")
    
    message = b'Saludos'
    newSocket.sendall(message)

    data = newSocket.recv(1024)
    print("Servidor responde: " + '{!r}'.format(data))
    fileWrite('Servidor responde {!r}'.format(data)+ "\n")
    

finally:

    fileWrite("Cerrando socket\n\n")
    newSocket.close()
