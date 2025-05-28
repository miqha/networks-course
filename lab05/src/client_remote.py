import socket

HOST = '127.0.0.1'  # Или IP сервера
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[КЛИЕНТ] Подключено к {HOST}:{PORT}")
        while True:
            command = input("Введите команду (или 'exit'): ")
            if command.lower() == 'exit':
                break
            s.sendall(command.encode('utf-8'))
            data = s.recv(65536).decode('utf-8', errors='replace')
            print(f"[ОТВЕТ СЕРВЕРА]:\n{data}")

if __name__ == "__main__":
    main()
