import socket

class VideoServer:
    def __init__(self, host, port):
        # Initialize VideoServer with host and port
        self.host = '0.0.0.0'  # Use '0.0.0.0' to listen on all available interfaces
        self.port = port
        self.video_list = []  # Initialize an empty list to store video names

    def start_server(self):
        # Create a socket, bind it to host and port, and start listening for incoming connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Allow up to 5 queued connections
        print("Server is listening...")

        while True:
            # Accept incoming connection
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            # Handle client requests
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        # Receive and handle client requests
        while True:
            # Receive request from client
            request = client_socket.recv(1024).decode()
            if not request:  # If no data is received, break the loop
                break

            # Parse request
            request_parts = request.split("|")
            operation = request_parts[0]

            # Perform requested operation
            if operation == "INPUT_VIDEO":
                response = self.input_new_video(request_parts[1])
            elif operation == "SELECT_VIDEO":
                response = self.select_video_to_stream(request_parts[1])
            elif operation == "PLAY_VIDEO":
                response = self.play_video()
            elif operation == "PAUSE_VIDEO":
                response = self.pause_video()
            elif operation == "FAST_FORWARD_VIDEO":
                response = self.fast_forward_video()
            elif operation == "REWIND_VIDEO":
                response = self.rewind_video()
            elif operation == "NAME_VIDEO":
                old_name, new_name = request_parts[1], request_parts[2]
                response = self.name_video(old_name, new_name)
            elif operation == "DELETE_VIDEO":
                response = self.delete_video(request_parts[1])
            else:
                response = "Invalid operation."

            # Send response back to client
            client_socket.send(response.encode())

        # Close client socket after handling requests
        client_socket.close()

    def input_new_video(self, video_name):
        # Add new video to the video list
        self.video_list.append(video_name)
        return f"Video '{video_name}' added successfully."

    def select_video_to_stream(self, video_name):
        # Check if requested video exists in the video list
        if video_name in self.video_list:
            return f"Streaming video '{video_name}'."
        else:
            return f"Video '{video_name}' not found."
        
    def play_video(self):
        # Method to indicate playing a video
        return "Playing video."

    def pause_video(self):
        # Method to indicate pausing a video
        return "Pausing video."

    def fast_forward_video(self):
        # Method to indicate fast-forwarding a video
        return "Fast-forwarding video."

    def rewind_video(self):
        # Method to indicate rewinding a video
        return "Rewinding video."

    def name_video(self, old_name, new_name):
        # Method to rename a video
        if old_name in self.video_list:
            # If the old video name exists in the list, rename it to the new name
            self.video_list.remove(old_name)
            self.video_list.append(new_name)
            return f"Video '{old_name}' renamed to '{new_name}'."
        else:
            # If the old video name is not found, return a message indicating so
            return f"Video '{old_name}' not found."

    def delete_video(self, video_name):
        # Method to delete a video
        if video_name in self.video_list:
            # If the video to be deleted is found in the list, remove it
            self.video_list.remove(video_name)
            return f"Video '{video_name}' deleted successfully."
        else:
            # If the video to be deleted is not found, return a message indicating so
            return f"Video '{video_name}' not found."

if __name__ == "__main__":
    # Create an instance of VideoServer and start the server
    server = VideoServer(host='server_ip_here', port=5000)  # Replace 'server_ip_here' with actual server IP
    server.start_server()


