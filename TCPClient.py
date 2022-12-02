import socket

serverName = socket.gethostname()
serverIpAddress = socket.gethostbyname(serverName)
print("server IP address = {}".format(serverIpAddress))
serverPort = 12015
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIpAddress, serverPort))
message = input('Input lowercase sentence: ')
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(1024)
print(modifiedMessage.decode())
clientSocket.close()