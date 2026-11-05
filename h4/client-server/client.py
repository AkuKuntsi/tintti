import socket

# Client configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The same port as used by the server

def send_request(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1 << 31).decode('utf-8')
        return response

def get(data: str):
    req = f"GET {data}"
    response = send_request(req)
    return response

def stats():
    req = f"STATS"
    response = send_request(req)
    return response

def echo(text: str):
    req = f"ECHO {text}"
    response = send_request(req)
    return response

# Example usage: send an ECHO request
r_get = get('test.txt')
r_echo = echo("Helllo!")
r_stats = stats()

print(f"Server response:\n{r_get}")
print(f"Server response:\n{r_echo}")
print(f"Server response:\n{r_stats}")

