import socket
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def upload_video(video_file_path, socket):
    try:
        with open(video_file_path, "rb") as video_file:
            chunk = video_file.read(1024)
            while chunk:
                socket.send(chunk)
                chunk = video_file.read(1024)
            print("Upload complete.")
    except Exception as e:
        print(f"Error uploading video: {e}")
        socket.close()

def print_usage():
    print("Usage:")
    print("\t/add -> add a video.")
    print("\t/select -> select a video.")
    print("\t/play -> play a video.")
    print("\t/delete -> delete a video.")
    print("\t/quit -> exit the program.")

def main():
    # Establish connection to the server
    client_socket = socket.socket()
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")

    print_usage()

    while True:
        data = input(f"Enter a command: ")
        cmd = data.strip().lower()

        if cmd == '/quit':
            client_socket.send(cmd.encode())
            break

        if cmd == "/add":
            video_file_path = input("Enter the path to the video file: ")
            if os.path.exists(video_file_path):
                # Send command to the server to indicate video upload
                client_socket.send(f"{video_file_path}".encode())
                # Upload the video file to the server
                upload_video(video_file_path, client_socket)
            else:
                print("File not found.")

        elif cmd == '/select':
            video_name = input("Enter the name of the video: ")
            # Send command to the server to select the video
            client_socket.send(f"/select_video|{video_name}".encode())

        elif cmd == '/play':
            # Send command to the server to play the selected video
            client_socket.send("/play_video".encode())

        elif cmd == '/delete':
            video_name = input("Enter the name of the video to delete: ")
            client_socket.send(f"/delete_video|{video_name}".encode())

    client_socket.close()

if __name__ == "__main__":
    main()
