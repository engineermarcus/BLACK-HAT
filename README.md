## **BLACK HAT PYTHON 3**

## AUTHORS
Engineer Marcus
--
--

## LEGAL DISCLAIMER
This content is not reponsible for any of the actions taken by user or by the reader.     

## **LINCENSE**
     MIT 

## **NETWORK HACKERY**

## TCP CLIENT
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
## RUN THE SCRIPT

   python tcp_client.py

