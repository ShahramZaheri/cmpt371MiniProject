import socket
serverPort = 12016
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverName = socket.gethostname()
serverIpAddress = socket.gethostbyname(serverName)
print("server IP address = {}".format(serverIpAddress))

serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print(" server is ready ")
connectionSocket, clientAddress = serverSocket.accept()
print("client address = {}".format(clientAddress))

msg = connectionSocket.recv(1024).decode()
print("msg is : {}".format(msg))
print("----------------------------------- msg ends here ---------------------------------------------")
# modifiedMessage = msg.upper()

fileName = msg.split()[1]
fileName = fileName[1:]
f = open(fileName)
outputData = f.read()
f.close()
outputData = 'HTTP/1.0 200 OK\n\n' + outputData 
print("outputData = {}".format(outputData))
print(type(outputData))
# for i in range(len(outputData)):
# connectionSocket.send("HTTP/1.1 200 OK \r\n\r\n")
# for i in range(len(outputData)):
connectionSocket.sendall(outputData.encode())
# connectionSocket.send("\r\n")
connectionSocket.close()



# Python 3 server example
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time

# hostName = "localhost"
# serverPort = 8080

# class MyServer(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
#         self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
#         self.wfile.write(bytes("<body>", "utf-8"))
#         self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
#         self.wfile.write(bytes("</body></html>", "utf-8"))

# if __name__ == "__main__":        
#     webServer = HTTPServer((hostName, serverPort), MyServer)
#     print("Server started http://%s:%s" % (hostName, serverPort))

#     try:
#         webServer.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     webServer.server_close()
#     print("Server stopped.")