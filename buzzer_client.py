import socket
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import threading


print("Welcome to the Good Buzzer client - Learn multiple skills while buzzing in!")
print("")

def get_server_address():
    while True:
        try:
            server_host = input("Enter the server IP address: ")
            server_port = int(input("Enter the server port: "))
            return server_host, server_port
        except ValueError:
            print("Invalid port. Please enter a valid integer.")

def listen_server():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("Disconnected from the server.")
                break
            # Process other server messages if needed
        except (socket.error, ConnectionResetError):
            print("Disconnected from the server.")
            break

# def check_connection_status():
#     if client.fileno() == -1:
#         print("Disconnected from the server.")
#         window.quit()  # Exit the Tkinter main loop if disconnected
#     else:
#         window.after(1000, check_connection_status)  # Check again after 1 second

# Get server address from the user
SERVER_HOST, SERVER_PORT = get_server_address()

# Get username from the user
username = input("Enter your username: ")

# Connect to the server with a timeout of 10 seconds
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(10)

try:
    client.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to the server.")
except (socket.error, ConnectionRefusedError, socket.timeout):
    print("Unable to connect to the server. Please try again.")
    exit()

# Send the username to the server
client.send(username.encode('utf-8'))

# Start the listener thread
listener_thread = threading.Thread(target=listen_server)
listener_thread.start()

# Set up GUI window
window = tk.Tk()
window.title("Buzz Client")

image_path = "buzz_image.gif"  # Use the converted GIF image
original_image = Image.open(image_path)
resized_image = original_image.resize((250, 250), Image.LANCZOS)  # Resize the image with antialiasing

# Convert the resized image to PhotoImage
buzz_image = ImageTk.PhotoImage(resized_image)

# Create a smaller button with the resized image
buzz_button = tk.Button(window, image=buzz_image, command=lambda: client.send("buzz".encode('utf-8')))
buzz_button.pack()

# Check connection status periodically
#window.after(1000, check_connection_status)

# Start the Tkinter main loop
window.mainloop()

def close_connection_and_exit():
    client.close()
    window.quit()

window.protocol("WM_DELETE_WINDOW", close_connection_and_exit)

