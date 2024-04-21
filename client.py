import socket
import random
from threading import Thread
from datetime import datetime
from time import sleep

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

socket = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
socket.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

def listen_for_messages():
    try:
        while True:
            message = socket.recv(1024).decode()
            print("\n" + message)
    except Exception as e:
        print(f"Error listening: {e}")

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

def print_usage():
    print("Usage:")
    print("\t/add -> add a video.")
    print("\t/select -> select a video.")
    print("\t/play -> play a video.")
    print("\t/quit -> exit the program.")

print_usage()

while True:
    data = input(f"Enter a command: ")
    cmd = data.strip().lower()

    if cmd == '/quit':
        socket.send(cmd.encode())
        break

    if cmd == "/add":
        video_file_path = input("Enter a video file path: ")
        to_send = "INPUT_VIDEO|" + video_file_path
        print("adding " + to_send + "...")
        socket.send(to_send.encode())    
    elif cmd == '/select':
        video_file_path = input("Enter a video file path: ")
        to_send = "SELECT_VIDEO|" + video_file_path
        print("selecting " + to_send + "...")
        socket.send(to_send.encode())    

    elif cmd == '/play':
        to_send = "PLAY_VIDEO"
        print("playing...")
        socket.send(to_send.encode())    

    sleep(0.5)

socket.close()