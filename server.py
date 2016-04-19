#!/usr/bin/python

import socket
import ssl
import multiprocessing

def process_request(sock):
	try:
		sock.send("Hi client!")
		print sock.recv(256)
	finally:
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Cuando en una ejecucion anterior se deja el socket en un estado de timeout (TIME_WAIT), el 
flag socket.SO_REUSEADDR permite indicar al Kernel que sera posible volver a utilizar el
socket sin tener que esperar a que el timeout expire.
"""
main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""
La especificacion de 0.0.0.0 permite indicar al Kernel que se desea enlazar el socket a 
todas las direcciones disponibles, en este caso de IPv4 (AF_INET).
"""
main_socket.bind(("0.0.0.0", 443))

main_socket.listen(5)

while True:
	(client_socket, (client_ip, client_port)) = main_socket.accept()
	print "Connection accepted from %s:%s. Processing the request..." % (client_ip, client_port)

	"""
	Envolvemos el socket dentro del contexto de seguridad del protocolo TLSv1.
	Se especifica que se trata del lado servidor y por lo tanto se define la 
	ruta hacia los certificados que deben utilizarse. 
	"""
	conn = ssl.wrap_socket(client_socket, server_side=True, 
		certfile="./certificates/server.crt", keyfile="./certificates/server.key",
		ssl_version=ssl.PROTOCOL_TLSv1)

	subprocess = multiprocessing.Process(target=process_request, args=(conn,))
	subprocess.start()

main_socket.close()