import socket  
import struct
import sys
import time

def fileWrite(message):
    f = open("hearbeat_server.txt", "a")
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
    print("Enviando multicast")

    try:

        # Send data to the multicast group
        #print >>sys.stderr, 'sending "%s"' % message
        sent = sock.sendto(message, multicast_grp)

        # Look for responses from all recipients
        while True:
            fileWrite("Esperando respuestas\n")
            print("Esperando respuestas")
            #print >>sys.stderr, 'waiting to receive'
            
            try:
                data, server = sock.recvfrom(16)
            
            except socket.timeout:
                #print >>sys.stderr, 'timed out, no more responses'
                fileWrite("No llegaron respuestas\n")
                print("No llegaron respuestas")
                break
            
            else:
                print("Recibido ", data, " desde ", server)
                fileWrite("Recibido " + data.decode("utf-8")  + " desde " + server[0] + "\n")
                #print >>sys.stderr, 'received "%s" from %s' % (data, server)

    finally:
        #print >>sys.stderr, 'closing socket'
        print("Cerrando socket")
        fileWrite("Cerrando socket\n\n")
        sock.close()

    time.sleep(5.0 - ((time.time() - starttime) % 5.0))



  

