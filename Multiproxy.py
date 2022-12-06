import socket
import os
import time
import shutil
import threading

expiration_time_for_cached_file = 120
# ------------------------------------------------- Beginning of Helper Functions -----------------------------------
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
    print("last access time = {}".format(last_access_time))
    print("time.time() = {}".format(time.time()))
    print("time.time() - last_access_time = {}".format(time.time() - last_access_time))
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

def change_http_request_to_conditional_request(request):
    request_array = request.split('\n')
    fileName = request_array[0].split()[1]
    path_to_cache_directory = os.getcwd() + "\proxyCache"
    file_path = path_to_cache_directory + fileName
    time_file_modified_in__cache = os.path.getmtime(file_path)
    request_array = request_array[:1] + ["modified at: " + str(time_file_modified_in__cache)] + request_array[1:]
    conditional_request = ('\n').join(request_array)
    return conditional_request

def response_from_remote_server_is_404(response_from_remote_server):
    response_array = response_from_remote_server.split('\n')
    if "404 NOT FOUN" in response_array[0]:
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


proxy_socket.listen(1)
print('Proxy Server is listening on IP %s | port %s ...' % (PROXY_HOST,PROXY_PORT))

threads = []

def newTCPServerThread(client_connection):
    request = client_connection.recv(1024).decode()
    headers = request.split('\n')
    fileName = headers[0].split()[1]

    fileIsInCache, path_to_file_in_cache = fileExistsInCache(fileName)

    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.connect((SERVER_HOST, SERVER_PORT))

    if fileIsInCache and not file_in_cache_expired(path_to_file_in_cache):
        print("------------- file is in cache and it is not expired, responding to the request from proxy cache ---------------")
        content = readFile(path_to_file_in_cache)
        response = 'HTTP/1.0 200 OK\n\n' + content

    elif fileIsInCache and file_in_cache_expired(path_to_file_in_cache):
        print("------------- file is in cache, but it has expired, need to double check with remote server if the file in cache is still good to use ---------------")
        request = change_http_request_to_conditional_request(request)
        proxy_server_socket.send(request.encode())
        response_from_server = proxy_server_socket.recv(1024).decode()
        response_is_304 = received_304_from_remote_server(response_from_server)
        if response_is_304:
            print("-------- received 304 from the remote server, the expired file is good to use ---------------")
            content = readFile(path_to_file_in_cache)
            response = 'HTTP/1.0 200 OK\n\n' + content
            
        else:
            print("-------- Don't use the expired file, need to get a new copy from server ---------------")
            response = response_from_server
            copy_file_to_proxy_cache(fileName)
    elif not fileIsInCache:
        print("------------- file is NOT in cache, need to ask remote server for a copy of the file ---------------")
        proxy_server_socket.send(request.encode())
        response = proxy_server_socket.recv(1024).decode()
        if not response_from_remote_server_is_404(response):
            copy_file_to_proxy_cache(fileName)

    response = response.encode()
    client_connection.sendall(response)
    client_connection.close()

while True:
    client_connection, client_address = proxy_socket.accept()
    newServerThread = threading.Thread(target=newTCPServerThread, args=[client_connection,])
    newServerThread.start()
    threads.append(newServerThread)