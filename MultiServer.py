import socket
import threading

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8004

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

threads = []

def newTCPServerThread(client_connection):
    request = client_connection.recv(1024).decode()
    print(request)
    headers = request.split('\n')
    filename = headers[0].split()[1]

    # Get the content of the file
    if filename == '/':
        filename = '/test.html'

    try:
        fin = open('hotdocs' + filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:

        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()


while True:
    client_connection, client_address = server_socket.accept()
    newServerThread = threading.Thread(target=newTCPServerThread, args=[client_connection,])
    newServerThread.start()
    threads.append(newServerThread) 