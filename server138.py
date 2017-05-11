from time import gmtime, strftime
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 1612))
sock.listen(1)

conn, addr = sock.accept()

data = conn.recv(4096).decode("utf-8")
print("Recieved: ", data)

path = data.split()[1]
print("Path: ", path)

response = "HTTP/1.1 "
body = ""
try:
    body = open("http" + path).read()
    response += "200 OK"
except IOError:
    response += "404 Not Found"
response += "\r\n"

def header(key, value):
    return key + ": " + value + "\r\n"

response += header("Date", strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
response += header("Server", "Custom Python Server")
response += header("Content-Length", str(len(body)))
response += header("Connection", "close")
response += header("Content-Type", "text/html")

response += "\r\n" + body
conn.send(response.encode("utf-8"))

print("Reponse: ", response)
conn.close()

