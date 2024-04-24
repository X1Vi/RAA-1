import socket
import time
import threading

HOST = "localhost"
PORT = 8000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectToServer():
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connection Successful -> {HOST}, {PORT}")
        handleDataTransfer(client_socket)
    except Exception as e:
        print(f"Connection to the server failed -> {e}")
        time.sleep(10)
        connectToServer()

def handleDataTransfer(client_socket_):
    while True:
        data = client_socket_.recv(1024)
        if not data:
            connectToServer()
        print(data)

# Start the initial connection attempt
threading.Thread(target=connectToServer).start()