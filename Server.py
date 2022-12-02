import socket


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
if len(request) > 0:

    # Parse HTTP headers
    headers = request.split('\n')
    # print(headers)
    filename = headers[0].split()[1]
    filename = filename[1:]
    print("file name = {}".format(filename))

    try:
        fin = open(filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:

        response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()