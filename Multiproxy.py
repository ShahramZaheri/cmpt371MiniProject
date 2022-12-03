import socket
import os
import time
import sys
import threading

# this function takes fileName and
# returns True if the file exists in the proxyCache folder, otherwise it returns False
def fileExistsInCache(fileName):
    path_to_cache_directory = os.getcwd() + "\proxyCache"
    path_to_file = path_to_cache_directory + fileName
    fileExists = os.path.exists(path_to_file)
    return fileExists, path_to_file

def readFile(filePath):
    fin = open(filePath)
    content = fin.read()
    fin.close()
    return content

def saveToCache(proxy_server_socket, request, fileName):
    proxy_server_socket.send(request.encode())
    response = proxy_server_socket.recv(1024)
    res = response.decode().split('\n',1)[1]
    file = open(fileExistsInCache(fileName)[1],'w')
    file.write(res)
    file.close
    return response
# --------------------------------- End of Helper Functions ----------------------------------------------------

PROXY_HOST = '0.0.0.0'
PROXY_PORT = 8001

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8004

TIME = 120
# Create sockets 
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))

proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server_socket.connect((SERVER_HOST, SERVER_PORT))


proxy_socket.listen(1)
print('Proxy Server is listening on port %s ...' % PROXY_PORT)

threads = []

def newTCPServerThread(client_connection):

    # Get the client request
    request = client_connection.recv(1024).decode()
    headers = request.split('\n')
    fileName = headers[0].split()[1]
    # fileName = fileName[1:]

    print(fileExistsInCache(fileName)[0])
    print(fileExistsInCache(fileName)[1])

    # if the requested file is in the cache, respond to the request from cache, otherwise ask the remote server
    if fileExistsInCache(fileName)[0]:
        filetime = os.path.getmtime(fileExistsInCache(fileName)[1])
        current = time.time()
        if (current - filetime > TIME):
            print("------------- file exists in cache but needs to update, asking remote server ---------------")
            response = saveToCache(proxy_server_socket,request,fileName)
        else:
            print("------------- file exists in cache, responding from cache ---------------")
            content = readFile(fileExistsInCache(fileName)[1])
            response = 'HTTP/1.0 200 OK\n\n' + content
            response = response.encode()
    else:
        print("------------- file doesn't exist in cache, asking remote server ---------------")
        response = saveToCache(proxy_server_socket,request,fileName)

    
    # sending response to client (browser)
    client_connection.sendall(response)
    client_connection.close()

while True:
    client_connection, client_address = proxy_socket.accept()
    newServerThread = threading.Thread(target=newTCPServerThread, args=[client_connection,])
    newServerThread.start()
    threads.append(newServerThread) 