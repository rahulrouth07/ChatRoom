import socket
import threading

chat_rooms = {}

def handle_client(client_socket, client_address, room_name):
    try:
        welcome_message = f"Welcome to {room_name} chat room! Type 'exit' to leave."
        client_socket.send(welcome_message.encode())

        broadcast(f"{client_address} has joined the chat!", room_name, client_socket)

        # Receive messages from user
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.lower() == "exit":
                client_socket.send("You have left the chat.".encode())
                chat_rooms[room_name].remove(client_socket)
                broadcast(f"{client_address} has left the chat.", room_name, client_socket)
                break
            else:
                broadcast(f"{client_address}: {msg}", room_name, client_socket)
    except:
        chat_rooms[room_name].remove(client_socket)
        broadcast(f"{client_address} has unexpectedly disconnected.", room_name, client_socket)
    finally:
        client_socket.close()

def broadcast(message, room_name, sender_socket=None):
    for client in chat_rooms[room_name]:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                chat_rooms[room_name].remove(client)

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        client_socket.send("Enter chat room name: ".encode())
        room_name = client_socket.recv(1024).decode()

        if room_name not in chat_rooms:
            chat_rooms[room_name] = []

        chat_rooms[room_name].append(client_socket)

        threading.Thread(target=handle_client, args=(client_socket, client_address, room_name)).start()

server_program() 