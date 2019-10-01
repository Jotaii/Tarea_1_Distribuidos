import socket  
import struct
import sys
import time
import random
from threading import Thread

ips = []

def fileWrite(file, message):

    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    f = open(file, "a")
    #print(message)
    f.write(message)
    f.close()

def multicast():
    ips.clear()

    message = b'hola'
    multicast_grp = ('224.3.29.71', 5000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    fileWrite("hearbeat_server.txt","Enviando multicast\n")

    try:
        # Send data to the multicast group
        #print >>sys.stderr, 'sending "%s"' % message
        sent = sock.sendto(message, multicast_grp)

        # Look for responses from all recipients
        while True:
            fileWrite("hearbeat_server.txt", "Esperando respuestas\n")
            
            try:
                data, server = sock.recvfrom(16)
            
            except socket.timeout:
                fileWrite("hearbeat_server.txt", "No llegaron respuestas\n")
                break
            
            else:
                fileWrite("hearbeat_server.txt", "Recibido ack desde " + server[0] + "(datanode" + data.decode("utf-8") + ")\n")
                
                if data.decode("utf-8") not in ips:
                    ips.append(data.decode("utf-8"))
                    
    finally:        
        fileWrite("hearbeat_server.txt", "Cerrando socket\n\n")
        sock.close()
        

def headnode_process():
    starttime=time.time()
    while True:
        multicast()
        time.sleep(5.0 - ((time.time() - starttime) % 5.0)) 

def server_process():
    fileWrite("registro_server.txt", "Iniciando servidor de headnode\n")

    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("headnode", 5001)
    newSocket.bind(server_address)
    newSocket.listen(1)

    while True:
        connection, client_address = newSocket.accept()
        fileWrite("registro_server.txt", "Se ha conectado el cliente " + client_address[0] + "\n")

        try:
            data = connection.recv(1024)
               
            if data:
                if len(ips) != 0:
                    fileWrite("registro_server.txt", "Cliente envia: " + str(data, 'utf-8') + "\n")

                    random_datanode = random.choice(ips)
                    fileWrite("registro_server.txt", "AAAAAAAAAAA" + random_datanode + "\n")

                    #TODO: condicion lista vacia


                    fileWrite("registro_server.txt", "Se ha escogido aleatoriamente el datanode " + random_datanode + "\n")

                    newDatanode_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_address1 = ("datanode" + random_datanode, 5000)
                    newDatanode_Socket.connect(server_address1)
                    
                    try:
                        fileWrite("registro_server.txt", "Enviando mensaje a datanode " + random_datanode + "\n")
                        newDatanode_Socket.sendall(data)

                        datanode_data = newDatanode_Socket.recv(1024)
                        fileWrite("registro_server.txt", 'Datanode responde: ' + str(datanode_data, 'utf-8') + "\n")

                    finally:
                        fileWrite("registro_server.txt", "Cerrando conexion con datanode " + random_datanode + "\n")
                        newDatanode_Socket.close()

                    fileWrite("registro_server.txt", "Confirmando a cliente sobre la recepcion de su mensaje...\n")
                    response = bytes("Datanode " + random_datanode + " confirma recepcion de su mensaje", 'utf-8')
                    connection.sendall(response)

                else:
                    fileWrite("registro_server.txt", "No hay datanodes disponibles\n")
                    response = bytes("No hay datanodes disponibles", 'utf-8')
                    connection.sendall(response)

            else:
                fileWrite("registro_server.txt", "Cliente conectado no envia datos\n")
                break

        finally:
            fileWrite("registro_server.txt", "Cerrando conexion con cliente\n\n")
            connection.close()

#Iniciación de entorno y configuración del headnode
f = open("hearbeat_server.txt", "w")
f.close()

f = open("registro_server.txt", "w")
f.close()

#Inicio del primer multicast para almacenar las direcciones IP de los datanodes reconocidos
multicast()

#Inicio de ambos servicios del headnode. 
Thread(target = headnode_process).start()             
Thread(target = server_process).start()