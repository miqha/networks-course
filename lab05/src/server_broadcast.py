import socket
import time

BROADCAST_IP = '255.255.255.255'  # широковещательный адрес
PORT = 37020

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        message = current_time.encode('utf-8')
        sock.sendto(message, (BROADCAST_IP, PORT))
        print(f"[SERVER] Sent: {current_time}")
        time.sleep(1)

if __name__ == "__main__":
    main()
