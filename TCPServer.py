import socket
serverPort = 12015
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print(" server is ready ")
connectionSocket, clientAddress = serverSocket.accept()
msg = connectionSocket.recv(1024).decode()
modifiedMessage = msg.upper()
connectionSocket.send(modifiedMessage.encode())
connectionSocket.close()