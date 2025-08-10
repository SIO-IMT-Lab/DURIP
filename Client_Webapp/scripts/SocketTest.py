import socket


def run_server() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "169.254.20.99"
    port = 8000
    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        while True:
            msg = input("Enter message: ")
            client_socket.send(msg.encode("utf-8")[:1024])
    finally:
        client_socket.close()
        print("Connection to client closed")
        server.close()


if __name__ == "__main__":
    run_server()
