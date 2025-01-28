import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Новый клиент {client_address} подключен")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Получено сообщение от {client_address} {message.decode()}")
            client_socket.send(message)
        except ConnectionResetError:
            break
    print(f"Клиент отключен {client_address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5555))
    server_socket.listen(5)
    print("Сервер запущен / oжидание подключения клиентов")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"Активные потоки {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
