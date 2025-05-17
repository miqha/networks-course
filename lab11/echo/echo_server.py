import socket

HOST = '::1' 
PORT = 65432

def start_server():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[СЕРВЕР] Ожидание подключения на {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[СЕРВЕР] Подключено к {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = data.decode().upper().encode()
                conn.sendall(response)
                print(f"[СЕРВЕР] Принято: {data.decode()} --> Отправлено: {response.decode()}")

if __name__ == "__main__":
    start_server()
