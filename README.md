# cmpt371MiniProject

First, run Server.py then run proxy.py. Now, in the browser type http://localhost:8001/test2.html . If the requested file is in proxyCache folder, proxy server will respond to the request by sending the file available in proxyCache folder. However, if the requested file has not been cached (the file is not in proxyCache folder), proxy server will contact the remote server and ask for the file. 
