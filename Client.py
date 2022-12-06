import socket

serverName = socket.gethostname()
serverIpAddress = socket.gethostbyname(serverName)
print("server IP address = {}".format(serverIpAddress))
serverPort = 8004
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIpAddress, serverPort))
message = input('Send HTTP Request: ')
request = message + "\nHost: " + str(serverIpAddress) + ":" + str(serverPort)
clientSocket.send(request.encode())
modifiedMessage = clientSocket.recv(1024)
print(modifiedMessage.decode())
clientSocket.close()