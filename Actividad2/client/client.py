import socket
import sys
from datetime import datetime

# Creación de registro_cliente.txt en el almacenamiento del cliente
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def createFile():
    f = open("registro_cliente.txt", "w")
    f.close()

# Función para escribir mensajes en registro_ciente.txt
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def fileWrite(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open("registro_cliente.txt", "a")
    f.write("[" + current_time + "] " + message)
    f.close()

# Interacción con el usuario. El usuario manda un mensaje
accept = False
while(accept != True):
    print("Escriba un mensaje para un datanode: ")
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

#Iniciando cliente
fileWrite("Iniciando cliente: Abriendo socket...\n")
newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando cliente con headnode
fileWrite("Conectando con headnode...\n")
server_address = ("headnode", 5001)
newSocket.connect(server_address)

try:
    fileWrite("Usuario escribe: " + user_input + "\n")

    # Enviando el input del usuario al headnode
    fileWrite("Enviando mensaje a headnode...\n")
    message = bytes(user_input, 'utf-8')
    newSocket.sendall(message)

    # Espera de una respuesta por parte del headnode
    data = newSocket.recv(1024)
    fileWrite('Headnode responde: ' + str(data, 'utf-8') + "\n")
    print('Headnode responde: ' + str(data, 'utf-8'))

finally:
    # Cerrando conexión con el headnode
    print("Terminando conexion con headnode\n")
    fileWrite("Cerrando socket...\n\n")
    newSocket.close()