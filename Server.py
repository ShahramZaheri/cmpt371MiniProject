import socket
import time
import os

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
print('Listening on port %s ...' % SERVER_PORT)

# while True:    
    # Wait for client connections
client_connection, client_address = server_socket.accept()

# Get the client request
request = client_connection.recv(1024).decode()
# print(request)
# print(type(request))
if len(request) > 0:

    # Parse HTTP headers
    headers = request.split('\n')
    # print(headers)
    filename = headers[0].split()[1]
    filename = filename[1:]
    print("file name = {}".format(filename))

    try:
        # last_access_time = os.path.getatime(filename)
        # 
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
            else:
                response = 'HTTP/1.0 304 Not Modified \n\n'
        else:
            fin = open(filename)
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 200 OK\n\n' + content

    except FileNotFoundError:

        response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()