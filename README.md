## **BLACK HAT PYTHON 3**

## AUTHORS

Engineer Marcus

## LEGAL DISCLAIMER
This content is not reponsible for any of the actions taken by user or by the reader.     

## **LINCENSE**
     MIT 

## **NETWORK HACKERY**

## **TCP CLIENT**

make a script: tcp_client.py 
```sh 
import socket
target_host = "www.google.com"
target_port = 80

#create a socket object 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect to the server

client.connect((target_host,target_port))

#send some data

client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")


#receive some data 
response = client.recv(4096)
print(response.decode())
client.close()

```
**RUN THE SCRIPT**
```sh
python tcp_client.py
```
## **UDP CLIENT** 

make a script: udp_client.py
```sh
import socket

target_host = "127.0.0.1"
target_port = 9997

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# Receive data
data, addr = client.recvfrom(4096)

print(data.decode())

client.close()
```

**RUN**
```sh
python udp_client.py
```
## **TCP SERVER**

make a script: tcp_server.py
```sh
import socket
import threading 

#set the server ip and port
IP = '0.0.0.0' # 0.0.0.0 listens for connctions from all addresses
PORT = 8080

#build the main function

def main():
   #creating a socket object
   server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
   # AF_INET tells the server to use ipv4 while the SOCK_STREAM identifies the server as a tcp server

   server.bind((IP, PORT)) # bind the port and ip
   server.listen(5) # listen for incoming connections, maximum 5

   print(f'[*] server listening at:  {IP}:{PORT}')

   
   while True:
      client, address = server.accept() # accept incoming connections
      print(f'[*] accepted a connection with: {address[0]}:{address[0]}')

      # handle client connections with a thread for handling many requests simultaniously
      client_handler = threading.Thread(target=handle_client, args=(client,))
       
      # start the client handler
      client_handler.start()

# build a function to handle client requests
def handle_client(client_socket):
   with client_socket as sock:
      request = sock.recv(1024)
      print(f'[*] received: {request.decode("utf-8")}')
      sock.send(b'life is good')

if __name__=='__main__':
   main()
   
  
```
