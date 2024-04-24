import socket
import sys
import threading

HOST = "localhost"
PORT = 8000
CLIENT_SOCKETS = []

def listenForConnections():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handleClient, args=(client_socket, addr))
        client_thread.start()

def handleClient(client_socket, addr):
    CLIENT_SOCKETS.append((client_socket, addr))
    # Handle client communication here
    while True:
        data = client_socket.recv(1024)
        if not data:
            client_index = CLIENT_SOCKETS.index(client_socket)
            if client_index != -1:
                CLIENT_SOCKETS.remove(client_index)
                client_socket.close()
                return
        print(f"Received from {addr}: {data.decode()}")

    

if __name__ == "__main__":
    threading.Thread(target=listenForConnections).start()