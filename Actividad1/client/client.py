import socket
import sys
from datetime import datetime

# Creación de respuestas.txt en el almacenamiento del cliente
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def createFile():
    f = open("respuestas.txt", "w")
    f.close()

# Función para escribir mensajes en respuestas.txt
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def fileWrite(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open("respuestas.txt", "a")
    f.write("[" + current_time + "] " + message)
    f.close()

# Interacción con el usuario. El usuario manda un mensaje
accept = False
while(accept != True):
    print("Escriba el mensaje a enviar: ")
    user_input = input()

    try:
        user_input.encode('ascii')

    except UnicodeEncodeError:
        print("Ha insertado un caracter invalido. Intente nuevamente.\n")

    else:
        accept = True

# Obtención de hostname y dirección IP del cliente
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    

fileWrite("Iniciando cliente\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando cliente con servidor
server_address = ("server", 5000)
print('Conectando a {} por puerto {}'.format(*server_address))
fileWrite('Conectando a {} por puerto {}'.format(*server_address) + "\n")
newSocket.connect(server_address)

try:
    fileWrite("Usuario escribe: " + user_input + "\n")

    # Enviando el input del usuario al headnode
    fileWrite("Enviando mensaje al servidor\n")
    message = bytes(user_input, 'utf-8')
    newSocket.sendall(message)

    # Respuesta del servidor
    data = newSocket.recv(1024)
    print('Servidor responde: ' + str(data, 'utf-8'))
    fileWrite('Servidor responde: ' + str(data, 'utf-8') + "\n")

# Cerrando conexión
finally:
    print("Cerrando conexion con servidor\n")
    fileWrite("Cerrando socket\n\n")
    newSocket.close()
