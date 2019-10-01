import socket
import struct
import sys
from threading import Thread

# Creación de data.txt en el almacenamiento del datanode
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def createFile():
    f = open("data.txt", "w")
    f.close()

# Función para escribir mensajes en data.txt
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def fileWrite(message):
    f = open("data.txt", "a")
    f.write(message)
    f.close()

# Función para que el datanode reciba y responda los mensajes multicast que envía el headnode
def multicast_response():
    # Informacion del grupo multicast
    multicast_group = '224.3.29.71'
    server_address = ('', 5000)

    # Creación del socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enlace con el headnode
    sock.bind(server_address)

    # Se le avisa al SO que se va a añadir el grupo de multicast en todas las interfaces
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Loop de respuesta al headnode
    while True:
        data, address = sock.recvfrom(1024)
        sock.sendto(b'2', address)

# Función para que el datanode actúe como servidor para escuchar las peticiones del headnode (cliente)
def server_process():
    # Iniciación del servicio
    fileWrite("Iniciando servidor\n")
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)

    # Apertura de socket en el puerto 5000 del datanode
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IPAddr, 5000)

    # Enlace del socket a la dirección especificada
    newSocket.bind(server_address)
    newSocket.listen(1)

    # Loop de escucha y respuesta
    while True:
        connection, client_address = newSocket.accept()
        
        # Probar en caso de que el headnode se conecte al datanode
        try:
            fileWrite("Se ha conectado headnode " + client_address[0] + " al datanode\n")          
            data = connection.recv(1024)

            # Si headnode manda un mensaje por parte de un cliente externo           
            if data:
                fileWrite("Headnode dice por parte de un cliente externo: " + str(data, 'utf-8') + "\n")
                fileWrite("Enviando confirmacion al headnode\n")
                connection.sendall(b'Mensaje del cliente externo registrado exitosamente')
                
            # Si headnode se conecta pero no envía un mensaje
            else:
                fileWrite("No se recibe mensaje por parte del headnode\n")
                break

        # Se cierra la conexión con el headnode
        finally:
            fileWrite("Cerrando conexion con el headnode\n\n")
            connection.close()

# Ejecución de ambos procesos como threads
createFile()
Thread(target = multicast_response).start()
Thread(target = server_process).start()