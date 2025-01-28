import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))

    try:
        while True:
            message = input("Введите сообщение для отправки ('exit' для выхода): ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"Ответ от сервера {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
