import socket
import os
import json
from threading import Thread

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
UPLOAD_FOLDER = "uploads"

class VideoManager:
    def __init__(self):
        self.video_dict = {}

    def check_video_existence(self, video_name):
        return video_name in self.video_dict

    def add_video(self, video_name, video_file_path):
        self.video_dict[video_name] = {"file_path": video_file_path}
        self.save_video_list()

    def delete_video(self, video_name):
        if video_name in self.video_dict:
            del self.video_dict[video_name]
            self.save_video_list()
            return True
        return False

    def save_video_list(self):
        with open("video_list.json", "w") as f:
            json.dump(self.video_dict, f)

    def load_video_list(self):
        if os.path.exists("video_list.json"):
            with open("video_list.json", "r") as f:
                self.video_dict = json.load(f)

def handle_client(client_socket, client_address, video_manager):
    print(f"[+] Accepted connection from {client_address}")

    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8')  # Explicitly decode using UTF-8
            if not command:
                break
            command = command.strip().lower()

            if command.startswith("input_video|"):
                _, video_name = command.split("|")
                video_file_path = os.path.join(UPLOAD_FOLDER, video_name)
                with open(video_file_path, "wb") as video_file:
                    while True:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        video_file.write(chunk)
                video_manager.add_video(video_name, video_file_path)
                client_socket.send("Video uploaded successfully!".encode())

            elif command.startswith("select_video|"):
                _, video_name = command.split("|")
                if video_manager.check_video_existence(video_name):
                    client_socket.send(f"Video '{video_name}' selected.".encode())
                else:
                    client_socket.send(f"Video '{video_name}' not found.".encode())
            elif command == "play_video":
                client_socket.send("Playing video...".encode())
            elif command == "quit":
                break
            else:
                client_socket.send("Invalid command.".encode())
        except UnicodeDecodeError as e:
            print(f"Error decoding client data: {e}")
            client_socket.send("Error: Invalid data received.".encode())
            break
        except Exception as e:
            print(f"Error handling client request: {e}")

    print(f"[-] Connection from {client_address} closed.")
    client_socket.close()

def accept_connections(server_socket, video_manager):
    print("[*] Waiting for incoming connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket, client_address, video_manager))
        client_thread.start()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f"[*] Listening for connections on {SERVER_HOST}:{SERVER_PORT}...")
        video_manager = VideoManager()
        video_manager.load_video_list()
        accept_connections(server_socket, video_manager)
    except Exception as e:
        print(f"Error starting server: {e}")

# Start the server
start_server()
