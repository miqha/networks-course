import socket

HOST = '::1'
PORT = 65432

def start_client():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("[КЛИЕНТ] Подключено к серверу.")
        try:
            while True:
                message = input("Введите сообщение (или 'exit'): ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                print(f"[КЛИЕНТ] Ответ: {data.decode()}")
        except KeyboardInterrupt:
            print("\n[КЛИЕНТ] Завершено пользователем.")

if __name__ == "__main__":
    start_client()
