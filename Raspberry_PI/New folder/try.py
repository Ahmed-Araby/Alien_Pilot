import io       # store info in buffer in ram 
import socket   # remotly connection 
import struct   # to convert info into bytes 
import time 


print("client code running \n")

IP_Address = '192.168.1.3'
Port =  8000
W = 320
H = 160

client_socket = socket.socket()
client_socket.connect((IP_Address, Port))

# get a file object associated with the socket 
connection_file = client_socket.makefile('wb')  # write data in it and 

try:
    connection_file.write(struct.pack('<L' , 2))
    connection_file.flush()
    connection_file.write(b"#%#$")
finally:
    # close the file 
    connection_file.close()
    # close the connection 
    client_socket.close()

print("cline is Dead \n")
