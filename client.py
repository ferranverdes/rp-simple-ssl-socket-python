#!/usr/bin/python

import socket
import ssl

"""
Se crea un objeto del tipo SSLContext, el cual recibe por parametro el protocolo que
se desea utilizar en la negociacion de la seguridad para el establecimiento de la conexion.
"""
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Envuelve el socket dentro del contexto de seguridad especificado anteriormente.
Retorna un objecto del tipo SSLSocket.
"""
conn = context.wrap_socket(sock)

conn.connect(("192.168.1.183", 443))

print conn.recv(256)
conn.send("Hi Server!")

conn.close()