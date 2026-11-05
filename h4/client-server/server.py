import socket

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 65432  # Port number (you can change this)

def get_file(path: str) -> str: 
    file = open(f"./{path}", "r")
    content = file.read()
    file.close()
    return content

# 0 is get, 1 is echo, 2 is stats
def save_log(index):
    new_content = ""
    parts = []
    with open("./log.txt", "r") as f:
        content = f.read()
        parts = content.split(",")
        parts[index] = f"{int(parts[index]) + 1}"
    with open("./log.txt", "w") as f:
        new_content = ",".join(parts)
        f.write(new_content)
    return parts

def handle_request(request):
    # Split the request line into method and parameter
    parts = request.strip().split(' ', 1)
    
    # Handle the "ECHO" method
    match parts[0]:
        case "GET":
            save_log(0)
            file = get_file(parts[1])
            return file
        case "ECHO":
            save_log(1)
            return parts[1]
        case "STATS":
            parts = save_log(2)
            return f"GET: {parts[0]}\nECHO: {parts[1]}\nSTATS: {parts[2]}"
        case  _:
            return "ERROR: Unknown method"

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is running on {HOST}:{PORT}...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                response = handle_request(data)
                client_socket.sendall(response.encode('utf-8'))

run_server()
