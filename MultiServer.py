import socket
import time
import os
import threading

# ---------------------------------------- Beginning of Helper Functions ----------------------------------------
def request_is_conditional_GET (request):
    request_array = request.split('\n')
    if "modified at:" in request_array[1]:
        time_starts_at_index = request_array[1].index(":") + 2
        modified_time = request_array[1] [time_starts_at_index: ]
        return True, float(modified_time)
    else:
        return False, " "


#  --------------------------------------- End of Helper Functions ----------------------------------------------


# Define socket host and port
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8004

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on IP %s | port %s ...' % (SERVER_HOST,SERVER_PORT))

threads = []
   
def newTCPServerThread(client_connection):
    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)
    
    currentTime = time.time()

    if len(request) > 0:
        try:
            # Parse HTTP headers
            headers = request.split('\n')
            filename = headers[0].split()[1]
            filename = filename[1:]
            print("file name = {}".format(filename))
            # time.sleep(3)
            try:
                is_conditional_get, specified_time_in_request = request_is_conditional_GET(request)
                if is_conditional_get:
                    time_file_modified_at_server = os.path.getmtime(filename)
                    print("time modified at server:{} ".format(time_file_modified_at_server))
                    print("time specified in request:{} ".format(specified_time_in_request))
                    if time_file_modified_at_server >= specified_time_in_request:
                        fin = open(filename)
                        content = fin.read()
                        fin.close()
                        response = 'HTTP/1.0 200 OK\n\n' + content
                        
                        responseTime = time.time()
                        if (responseTime - currentTime > 2):
                            response = 'HTTP/1.0 408 REQUEST TIMED OUT\n\n Request Timed Out'

                    else:
                        response = 'HTTP/1.0 304 Not Modified \n\n'
                        
                        responseTime = time.time()
                        if (responseTime - currentTime > 2):
                            response = 'HTTP/1.0 408 REQUEST TIMED OUT\n\n Request Timed Out'

                else:
                    fin = open(filename)
                    content = fin.read()
                    fin.close()
                    response = 'HTTP/1.0 200 OK\n\n' + content

                    responseTime = time.time()
                    if (responseTime - currentTime > 2):
                        response = 'HTTP/1.0 408 REQUEST TIMED OUT\n\n Request Timed Out'

            except FileNotFoundError:
                response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'
                
                responseTime = time.time()
                if (responseTime - currentTime > 2):
                    response = 'HTTP/1.0 408 REQUEST TIMED OUT\n\n Request Timed Out'

        except:
            response = 'HTTP/1.0 400 BAD REQUEST\n\n Bad Request'
            
    else:
        response = 'HTTP/1.0 400 BAD REQUEST\n\n Bad Request'
    
    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()


while True:
    client_connection, client_address = server_socket.accept()
    newServerThread = threading.Thread(target=newTCPServerThread, args=[client_connection,])
    newServerThread.start()
    threads.append(newServerThread)