import socket
import threading
from datetime import datetime


print("Welcome to the Good Buzzer Server - Learn multiple skills while buzzing in!")
print("")

# Function to get local IP address
def get_local_ip():
    try:
        # Create a temporary socket to get the local IP address
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(('8.8.8.8', 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

# Server Configuration
HOST = '0.0.0.0'  # Use '0.0.0.0' to listen on all available interfaces
PORT = input("Select port: ")
PORT = int(PORT)

# Dictionary to store buzz timestamps and usernames
buzz_data = {}
connected_clients = {}  # Dictionary to store connected clients and their sockets

def handle_client(client_socket, username):
    # Receive and process buzz
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"\n{username} disconnected.")
                del connected_clients[username]  # Remove disconnected client from the dictionary
                break
            if message.lower() == 'buzz':
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                buzz_data[username] = timestamp
                print(f"{username} buzzed at {timestamp}")
            elif message.lower().startswith('answer:'):
                answer = message[len('answer:'):].strip()
                print(f"{username} submitted answer: {answer}")
    except ConnectionResetError as e:
        print(f"Error handling client {username} - User potentially disconnected")
        # You can add more code here to handle the error, such as logging or retrying
    finally:
        client_socket.close() # Close the socket properly

# Function to list all connected users
def list_connected_users():
    print("Connected Users:")
    for user in connected_clients:
        print(f"- {user}")

# Function to force disconnect a user
def force_disconnect_user(username):
    if username in connected_clients:
        connected_clients[username].close()
        print(f"{username} has been forcibly disconnected.")
        del connected_clients[username]
    else:
        print(f"User {username} not found.")

# Command handler thread
def command_handler():
    while True:
        command = input("Enter command (list, disconnect <username>, exit): ").strip()
        if command.lower() == 'list':
            list_connected_users()
        elif command.lower().startswith('disconnect'):
            _, username_to_disconnect = command.split(' ', 1)
            force_disconnect_user(username_to_disconnect)
        elif command.lower() == 'exit':
            print("Server shutting down, you may close the program.")
            break
        else:
            print("Invalid command. Try again.")

# Get and print the local IP address
local_ip = get_local_ip()
if local_ip:
    print(f"Server listening on {local_ip}:{PORT}")
else:
    print("Unable to determine local IP address. Check your network configuration.")

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Start the command handler thread as a daemon
command_thread = threading.Thread(target=command_handler)
command_thread.daemon = True
command_thread.start()

# Main server loop
while True:
    client_socket, addr = server.accept()
    username = client_socket.recv(1024).decode('utf-8')
    connected_clients[username] = client_socket
    import sys
    sys.stdout.write(f"\n\033[92m{username} connected\033[0m\n") # \n is for newline
    client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
    client_thread.start()
