import socket
import sys

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    

f = open("respuestas.txt", "a")
print("Iniciando cliente...")
f.write("Iniciando cliente\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("0.0.0.0", 5000)
print('Conectando a servidor {} por puerto {}'.format(*server_address))
f.write('Conectando a servidor {} por puerto {}'.format(*server_address) + "\n")
newSocket.connect(server_address)
f.close()

try:

    f = open("respuestas.txt", "a")
    print("Enviando saludo al servidor...")
    f.write("Enviando saludo al servidor...\n")
    message = b'Saludos'
    newSocket.sendall(message)

    data = newSocket.recv(1024)
    print("Servidor responde: " + '{!r}'.format(data))
    f.write('Servidor responde {!r}'.format(data)+ "\n")
    f.close()

finally:

    f = open("respuestas.txt", "a")
    f.write("Cerrando socket\n\n")
    f.close()
    newSocket.close()
