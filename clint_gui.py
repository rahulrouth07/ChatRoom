import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print(msg)  
            else:
                break  
        except Exception as e:
            print("Error receiving message:", e)
            break

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5000)) 
    print(client_socket.recv(1024).decode())  
    room_name = input("> ") 
    client_socket.send(room_name.encode())

    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        try:
            msg = input()  
            if msg.lower() == "exit":
                client_socket.send(msg.encode())  
                print("You have left the chat.")
                break
            client_socket.send(msg.encode()) 
        except Exception as e:
            print("Error sending message:", e)
            break

    client_socket.close()

client_program()