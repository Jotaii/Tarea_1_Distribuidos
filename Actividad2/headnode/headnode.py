import socket  
import struct
import sys
import time
import random
from datetime import datetime
from threading import Thread

# Definición de variables compartidas entre threads
ips = []

# Función para escribir mensajes en los registros
# Se usa así para que los archivos no queden bloqueados una vez que se apaguen los containers
def fileWrite(file, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open(file, "a")
    f.write("[" + current_time + "] " + message)
    f.close()

def headnode_process():
    fileWrite("hearbeat_server.txt","Iniciando servicio de multicast\n\n")

    # Se define el tiempo de inicio para el hearbeat
    starttime=time.time()

    while True:
        # Limipieza del arreglo compartido que almacena los datanodes activos
        ips.clear()

        # Definición de mensaje multicast y características del grupo
        # Se utiliza una IP de broadcast y el puerto 5000
        message = b'hola'
        multicast_grp = ('224.3.29.71', 5000)

        # Apertura de socket y definición de timeout para escuchar respuestas
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)

        # Seteo de tiempo de vida en 1 para que los mensajes no pasen por el segmento
        # de area local
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        fileWrite("hearbeat_server.txt","Enviando multicast\n")

        try:
            # Envío de mensaje al grupo multicast
            sent = sock.sendto(message, multicast_grp)

            # Loop de espera para respuesta por parte de los datanodes
            while True:
                fileWrite("hearbeat_server.txt", "Esperando respuestas\n")
                
                # Búsqueda de respuestas
                try:
                    data, server = sock.recvfrom(16)
                
                # En caso de que se termine el plazo establecido para la respuesta
                # se asume que el datanodo está caido
                except socket.timeout:
                    fileWrite("hearbeat_server.txt", "No llegaron respuestas\n")
                    break
                
                # En caso de que llegue una respuesta por parte de un datanode
                else:
                    fileWrite("hearbeat_server.txt", "Recibido ack desde " + server[0] + "(datanode" + data.decode("utf-8") + ")\n")
                    
                    # Almacenamiento del datanode que respondió en el arreglo compartido para threads
                    if data.decode("utf-8") not in ips:
                        ips.append(data.decode("utf-8"))

        # No se reciben más respuestas, se cierra el socket.                
        finally:        
            fileWrite("hearbeat_server.txt", "Cerrando socket\n\n")
            sock.close()

        # Se esperan 5 segundo para volver a repetir el multicast
        time.sleep(5.0 - ((time.time() - starttime) % 5.0)) 

# Función para el thread que inicia al headnode como servidor para recibir mensajes de clientes externos
def server_process():
    fileWrite("registro_server.txt", "Iniciando servidor de headnode\n\n")

    # Apertura de socket para recibir peticiones. Se utiliza el 5001, ya que el 5000 está reservado para el multicast
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("headnode", 5001)
    newSocket.bind(server_address)
    newSocket.listen(1)

    # Loop para escuchar peticiones de clientes externos
    while True:
        # Se conecta un cliente
        connection, client_address = newSocket.accept()
        fileWrite("registro_server.txt", "Se ha conectado el cliente " + client_address[0] + "\n")

        try:
            # Se recibe la información por parte del cliente
            data = connection.recv(1024)
               
            if data:
                # Si hay datanodes activos, se envía el mensaje del cliente a un datanode aleatorio
                if len(ips) != 0:
                    fileWrite("registro_server.txt", "Cliente envia: " + str(data, 'utf-8') + "\n")

                    # Se escoge un datanode aleatorio de la lista
                    random_datanode = random.choice(ips)
                    fileWrite("registro_server.txt", "Se ha escogido aleatoriamente el datanode " + random_datanode + "\n")

                    # Socket para conexión con el datanode escogido
                    newDatanode_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_address1 = ("datanode" + random_datanode, 5000)
                    newDatanode_Socket.connect(server_address1)
                    
                    # Intento de conexión con el datanode
                    try:
                        # Se envía mensaje del cliente al datanode
                        fileWrite("registro_server.txt", "Enviando mensaje a datanode " + random_datanode + "\n")
                        newDatanode_Socket.sendall(data)

                        # Se confirma recepción por parte del datanode
                        datanode_data = newDatanode_Socket.recv(1024)
                        fileWrite("registro_server.txt", 'Datanode responde: ' + str(datanode_data, 'utf-8') + "\n")

                    # Cierre de conexión con el datanode.
                    finally:
                        fileWrite("registro_server.txt", "Cerrando conexion con datanode " + random_datanode + "\n")
                        newDatanode_Socket.close()

                    # Respuesta de parte del headnode al cliente externo sobre que datanode guardó su mensaje
                    fileWrite("registro_server.txt", "Confirmando a cliente sobre la recepcion de su mensaje...\n")
                    response = bytes("Datanode " + random_datanode + " confirma recepcion de su mensaje", 'utf-8')
                    connection.sendall(response)

                # Si no hay datanodes activos, se avisa inmediatamente al cliente externo
                else:
                    fileWrite("registro_server.txt", "No hay datanodes disponibles\n")
                    response = bytes("No hay datanodes disponibles", 'utf-8')
                    connection.sendall(response)

            # Cliente externo no envìa datos
            else:
                fileWrite("registro_server.txt", "Cliente conectado no envia datos\n")
                break

        # Cierre de conexión con cliente externo
        finally:
            fileWrite("registro_server.txt", "Cerrando conexion con cliente\n\n")
            connection.close()

#Iniciación de entorno y configuración del headnode
f = open("hearbeat_server.txt", "w")
f.close()

f = open("registro_server.txt", "w")
f.close()

#Inicio de ambos servicios del headnode. 
Thread(target = headnode_process).start()             
Thread(target = server_process).start()