import socket
import os
import time
import shutil

expiration_time_for_cached_file = 120

# this function takes fileName and
# returns True if the file exists in the proxyCache folder, otherwise it returns False
def fileExistsInCache(fileName):
    path_to_cache_directory = os.getcwd() + "\proxyCache"
    path_to_file = path_to_cache_directory + fileName
    fileExists = os.path.exists(path_to_file)
    return fileExists, path_to_file

# This function gets the file_path (path to a file in proxyCache folder) and
# returns True if the last access to the file was before 120 seconds ago (i.e. the file in cache has expired)
# otherwise it returns False  
def file_in_cache_expired(file_path):
    last_access_time = os.path.getatime(file_path)
    if time.time() - last_access_time > expiration_time_for_cached_file:
        return True
    else:
        return False
# This function gets a file name and creates a copy that file
# with the same name inside proxyCache folder 
def copy_file_to_proxy_cache(file_name):
    path_to_cache_directory = os.getcwd() + "\proxyCache"
    destination = path_to_cache_directory + fileName
    shutil.copy(file_name[1:], destination)

def received_304_from_remote_server(response_from_remote_server):
    response_first_line = response_from_remote_server.split('\n')[0]
    if "304" in response_first_line:
        return True
    else:
        return False

def readFile(filePath):
    fin = open(filePath)
    content = fin.read()
    fin.close()
    return content
# --------------------------------- End of Helper Functions ----------------------------------------------------

PROXY_HOST = '0.0.0.0'
PROXY_PORT = 8001

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8004

# Create sockets 
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))

proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server_socket.connect((SERVER_HOST, SERVER_PORT))


proxy_socket.listen(1)
print('Proxy Server is listening on port %s ...' % PROXY_PORT)
client_connection, client_address = proxy_socket.accept()

# Get the client request
request = client_connection.recv(1024).decode()
headers = request.split('\n')
fileName = headers[0].split()[1]

fileIsInCache, path_to_file_in_cache = fileExistsInCache(fileName)


if fileIsInCache and not file_in_cache_expired(path_to_file_in_cache):
    print("------------- file is in cache and it is not expired, responding to the request from proxy cache ---------------")
    content = readFile(path_to_file_in_cache)
    response = 'HTTP/1.0 200 OK\n\n' + content
    response = response.encode()
elif fileIsInCache and file_in_cache_expired(path_to_file_in_cache):
    print("------------- file is in cache, but it has expired, need to double check with remote server if the file in cache is still good to use ---------------")
    proxy_server_socket.send(request.encode())
    # receive message from remote server 
    response_from_server = proxy_server_socket.recv(1024).decode()
    response_is_304 = received_304_from_remote_server(response_from_server)
    if response_is_304:
        print("-------- received 304 from the remote server, the expired file is good to use ---------------")
        content = readFile(path_to_file_in_cache)
        response = 'HTTP/1.0 200 OK\n\n' + content
        response = response.encode()
    else:
        print("-------- Don't use the expired file, need to get a new copy from server ---------------")
        response = response_from_server.encode()
        copy_file_to_proxy_cache(fileName)
elif not fileIsInCache:
    print("------------- file is NOT in cache, need to ask remote server for a copy of the file ---------------")
    copy_file_to_proxy_cache(fileName)
    proxy_server_socket.send(request.encode())
    # receive message from remote server 
    response_from_server = proxy_server_socket.recv(1024).decode()
    response = response_from_server.encode()
    
  
# sending response to client (browser)
print(response)
client_connection.sendall(response)
client_connection.close()








# import sys

# if len(sys.argv) <= 1:

#     print ('Usage: "python S.py port"\n[port : It is the port of the Proxy Server')

#     sys.exit(2)

# # Server socket created, bound and starting to listen

# Serv_Port = int(sys.argv[1]) # sys.argv[1] is the port number entered by the user

# Serv_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket function creates a socket.

# # Prepare a server socket

# print ("starting server ....")

# Serv_Sock.bind(('', Serv_Port))

# Serv_Sock.listen(5)

# def caching_object(splitMessage, Cli_Sock):

#     #this method is responsible for caching

#     Req_Type = splitMessage[0]

#     Req_path = splitMessage[1]

#     Req_path = Req_path[1:]

#     print ("Request is ", Req_Type, " to URL : ", Req_path)

#     #Searching available cache if file exists

#     file_to_use = "/" + Req_path

#     print (file_to_use)

#     try:

#         file = open(file_to_use[1:], "r")

#         data = file.readlines()

#         print ("File Present in Cache\n")

#         #Proxy Server Will Send A Response Message

#         #Cli_Sock.send("HTTP/1.0 200 OK\r\n")

#         #Cli_Sock.send("Content-Type:text/html")

#         #Cli_Sock.send("\r\n")

#         #Proxy Server Will Send Data

#         for i in range(0, len(data)):

#             print (data[i])

#             Cli_Sock.send(data[i])

#         print ("Reading file from cache\n")

#     except IOError:

#         print ("File Doesn't Exists In Cache\n fetching file from server \n creating cache")

#         serv_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         host_name = Req_path

#         print ("HOST NAME:", host_name)

#         try:

#             serv_proxy.connect((host_name, 80))

#             print ('Socket connected to port 80 of the host')

#             fileobj = serv_proxy.makefile('r', 0)

#             fileobj.write("GET " + "http://" + Req_path + " HTTP/1.0\n\n")

#             # Read the response into buffer

#             buffer = fileobj.readlines()

#             # Create a new file in the cache for the requested file.

#             # Also send the response in the buffer to client socket

#             # and the corresponding file in the cache

#             tmpFile = open("./" + Req_path, "wb")

#             for i in range(0, len(buffer)):

#                 tmpFile.write(buffer[i])

#                 Cli_Sock.send(buffer[i])

#         except:

#             print (')Illegal Request')

#     Cli_Sock.close()

# while True:

#     # Start receiving data from the client

#     print ('Initiating server... \n Accepting connection\n')

#     Cli_Sock, addr = Serv_Sock.accept() # Accept a connection from client

#     #print addr

#     print (' connection received from: ', addr)

#     message = Cli_Sock.recv(1024).decode() #Recieves data from Socket

#     splitMessage = message.split()

#     if len(splitMessage) <= 1:

#         continue

#     caching_object(splitMessage, Cli_Sock)