import socket

PORT = 37020
BUFFER_SIZE = 1024

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))  # слушаем на всех интерфейсах

    print("[CLIENT] Listening for broadcast messages...")
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode('utf-8')
        print(f"[CLIENT] Received from {addr}: {message}")

if __name__ == "__main__":
    main()
