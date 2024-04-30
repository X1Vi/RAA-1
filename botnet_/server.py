import socket
import sys
import threading
import signal

HOST = "localhost"
PORT = 8002
CLIENT_SOCKETS = []
TOTAL_CONNECTIONS = 10

SOCK : None


def listenForConnections():
    try: 
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable socket reuse

        sock.bind((HOST, PORT))
        SOCK = sock
        sock.listen()
        print(f"Listening on {HOST}:{PORT}")
        


        while True:
            client_socket, addr = sock.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handleClient, args=(client_socket, addr), daemon=True).start()
            
    except KeyboardInterrupt:
        sock.close()
        # Loop through CLIENT_SOCKETS and close each client socket
        for client_socket, _ in CLIENT_SOCKETS:
            client_socket.close()

def handleClient(client_socket, addr):
    CLIENT_SOCKETS.append((client_socket, addr))
    try:
        while True:
            print(f"Listening on {addr}")
            data = client_socket.recv(1024)
            print(data)
            if not data:
                client_entry = (client_socket, addr)
                if client_entry in CLIENT_SOCKETS:
                    CLIENT_SOCKETS.remove(client_entry)
                client_socket.close()
                print(f"client_removed -> {client_socket}, {addr}")
                return
            print(f"Received from {addr}: {data.decode()}")
    except Exception as e:
        client_entry = (client_socket, addr)
        if client_entry in CLIENT_SOCKETS:
            CLIENT_SOCKETS.remove(client_entry)
        client_socket.close()
        print(f"Error: {e}")
        print(f"client_removed -> {client_socket}, {addr}")
        close_all_client_sockets()

def close_all_client_sockets():
    for c_sock in CLIENT_SOCKETS:
        client_sock, addr = c_sock
        client_sock.close()
        
def displayLiveConnections():
    if len(CLIENT_SOCKETS) == 0:
        print("No connections established")
        return 
    for idx, client in enumerate(CLIENT_SOCKETS):
        client_socket, addr = client
        print(f"{client_socket}, {addr}, {idx}")

def handleTerminal(thread_):
    try:
        while True:
            print("1 -> Displaying live connections ")
            print("2 -> Send messages ")
            print("3 -> Send Commands")

            input_ = input("Enter Command:")
            if int(input_) == 1:
                displayLiveConnections()
            elif int(input_) == 2:
                displayLiveConnections()
                getSocketIndex = input("Enter the socket index (it is displayed at the end of line): ")
                getSocketIndex = int(getSocketIndex)
                if len(CLIENT_SOCKETS) >= getSocketIndex:
                    client_socket , addr = CLIENT_SOCKETS[getSocketIndex]
                    toSendMsgToClientSocket : str = input("Enter message to send: ")
                    toSendMsgToClientSocket = f"MSG:{toSendMsgToClientSocket}"
                    client_socket.send(toSendMsgToClientSocket.encode())
            elif int(input_) == 3:
                displayLiveConnections()
                getSocketIndex = input("Enter the socket index (it is displayed at the end of line): ")
                getSocketIndex = int(getSocketIndex)
                command_arr = []
                if len(CLIENT_SOCKETS) >= getSocketIndex:
                    client_socket , addr = CLIENT_SOCKETS[getSocketIndex]
                    numberOfCommands = input("Enter the number of commands: ")
                    for _ in range(int(numberOfCommands)):
                        command = input("Enter commands : ")
                        command_arr.append(command)
                    commands = f"CMD:{command_arr}"
                    client_socket.send(commands.encode()) 
                print(command_arr)
    except KeyboardInterrupt:
       close_all_client_sockets()
       

       print("shutting down server")
if __name__ == "__main__":
    listen_thread = threading.Thread(target=listenForConnections, daemon=True).start()
    handleTerminal(listen_thread)
