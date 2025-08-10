import socket


def run_client() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "169.254.20.99"
    server_port = 8000
    client.connect((server_ip, server_port))
    try:
        while True:
            msg = input("Enter message: ")
            client.send(msg.encode("utf-8")[:1024])
            response = client.recv(1024).decode("utf-8")
            if response.lower() == "closed":
                break
            print(f"Received: {response}")
    finally:
        client.close()
        print("Connection to server closed")


if __name__ == "__main__":
    run_client()
