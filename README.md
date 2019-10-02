# README Tarea 1 - Sistemas Distribuidos 2019-2

Integrantes:
  
  -**Juan Escalona** - 201373551-7
  
  -**Sebastián Torrico** - 201330061-8


## Actividad 1

### Desplegar arquitectura
- Para ejecutar la actividad 1, debe ingresar a la carpeta *Actividad1* y ejecutar:

  `$sudo docker-compose build`  
	`$sudo docker-compose up`

### Interacción cliente-servidor
- Para controlar el cliente, se debe abrir una nueva terminal, ingresar a *Actividad1/client* y ejecutar:

	`$sudo docker ps`  
	`$sudo docker exec -it <nombre contenedor> bash`  
	`#python3 client.py`

- **Observaciones:** 
	- *nombre contenedor* suele tener la forma ***actividad1_client_1***.
	- El último comando se puede ejecutar reiteradamente según se requiera.

- A continuación estará ejecutando el cliente quien solicitará que ingrese un mensaje para ser enviado al servidor.

### Visualización de registros
- Una vez enviado el mensaje se puede verificar la interaccion en los siguientes archivos de texto:

	> Actividad1/client/respuestas.txt  
	> Actividad1/server/log.txt


## Actividad 2
### Desplegar arquitectura
- Para ejecutar la actividad 2, debe ingresar a la carpeta *Actividad2* y ejecutar:

	`$sudo docker-compose build`  
	`$sudo docker-compose up`

### Interacción cliente-headnode
- Para controlar el cliente, se debe abrir una nueva terminal, ingresar a *Actividad2/client* y ejecutar:

	`$sudo docker ps`  
	`$sudo docker exec -it <nombre contenedor> bash`  
	`#python3 client.py`

- **Observaciones:**
	- *nombre contenedor* suele tener la forma ***actividad2_client_1***.
	- El último comando se puede ejecutar reiteradamente según se requiera.

### Visualización de registros
- Una vez enviado el mensaje se puede verificar la interaccion en los siguientes archivos de texto:

	> Actividad2/client/registro_cliente.txt  
	> Actividad2/headnode/hearbeat_server.txt  
	> Actividad2/headnode/registro_server.txt  
	>Actividad2/datanodeX/data.txt

- **Observaciones:**
	- X corresponde al número del datanode en cuestión (1, 2 o 3).

### Consideraciones generales
- ***IMPORTANTE:*** Se recomienda utilizar el comando `$sudo docker-compose down` antes de cada inicialización de arquitectura, con el objetivo de realizar un montaje limpio.

- El código esta diseñado para funcionar con carácteres ASCII, es decir, no acepta caracteres especiales (ejemplos: ñ, á, ó, ¿). 

- Ante cualquier error, reiniciar completamente la arquitectura:

	`$sudo docker-compose down`  
	`$sudo docker-compose up`

- Los registros se limpian y reinicializan al reiniciarse la arquitectura a excepción del cliente. Lo anterior se realizó para mantener simpleza y evitar confusiones.

- Para la **Actividad 2** se utilizaron Threads para correr 2 servicios en un mismo container simultaneamente. Por ejemplo el *multicast* y el servidor del headnode.

- El tiempo del log registrado en los archivos de registros se encuentra en sistema horario UTC. 

- En caso de necesitar eliminar uno de los datanodes para probar consistencia del sistema, utilizar:

	`$sudo docker kill actividad2_datanodeX_1`

	Donde X corresponde al numero del datanode a eliminar. De este modo se puede verificar el funcionamiento del sistema revisando los registros del hearbeat sin cambiar su comportamiento ante el cliente.

**Nota**:  Para encontrar el nombre de los contenedores, en caso de requerirse se puede utilizar el comando `$sudo docker ps`.

