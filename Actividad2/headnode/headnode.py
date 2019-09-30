import socket  
import struct
import sys
import time
from threading import Thread
from random import randint

def headnode_process():

    f = open("hearbeat_server.txt", "w")
    f.close()

    def fileWrite(message):
        f = open("hearbeat_server.txt", "a")
        print(message)
        f.write(message)
        f.close()

    starttime=time.time()

    while True:

        message = b'hola'
        multicast_grp = ('224.3.29.71', 5000)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        fileWrite("Enviando multicast\n")

        try:

            # Send data to the multicast group
            #print >>sys.stderr, 'sending "%s"' % message
            sent = sock.sendto(message, multicast_grp)

            # Look for responses from all recipients
            while True:
                fileWrite("Esperando respuestas\n")
                
                try:
                    data, server = sock.recvfrom(16)
                
                except socket.timeout:
                    fileWrite("No llegaron respuestas\n")
                    break
                
                else:
                    fileWrite("Recibido " + data.decode("utf-8")  + " desde " + server[0] + "\n")
                    #print >>sys.stderr, 'received "%s" from %s' % (data, server)

        finally:        
            fileWrite("Cerrando socket\n\n")
            sock.close()

        time.sleep(5.0 - ((time.time() - starttime) % 5.0)) 

def client_process():

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


def server_process():

    def fileWrite(message):
        print(message)
        f = open("registro_server.txt", "a")
        f.write(message)
        f.close()

    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")

    fileWrite("Iniciando servidor de headnode\n")

    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("headnode", 5001)
    newSocket.bind(server_address)
    newSocket.listen(1)

    while True:

        connection, client_address = newSocket.accept()

        try:
            data = connection.recv(1024)
            fileWrite("Se ha conectado el cliente " + client_address[0] + "\nCliente dice: {!r}".format(data) + "\n")
            
            #Aqui se tiene que seleccionar el datanode a utilizar random
            datanode_a_utilizar = randint(0,2)
            
            #
            if data:
                fileWrite("Respondiendo a cliente...\n")
                connection.sendall(b'Que tengas un buen dia')
                
            else:
                fileWrite("Cliente conectado no envia datos\n")
                break

        finally:
            fileWrite("Cerrando conexion con cliente\n\n")
            connection.close()

Thread(target = headnode_process).start()
Thread(target = server_process).start()