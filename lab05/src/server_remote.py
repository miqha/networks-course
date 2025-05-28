import socket
import subprocess
import threading

HOST = '0.0.0.0'
PORT = 65432

def handle_client(conn, addr):
    print(f"[СЕРВЕР] Подключено к {addr}")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"[СЕРВЕР] Команда от клиента: {data}")

            try:
                result = subprocess.run(
                    data, shell=True, capture_output=True, timeout=30
                )

                # 💡 Принудительно декодируем Windows-вывод в CP866 (реально используется в cmd.exe)
                stdout = result.stdout.decode('cp866', errors='replace')
                stderr = result.stderr.decode('cp866', errors='replace')
                output = stdout + stderr

                if not output.strip():
                    output = "[СЕРВЕР] Команда выполнена, но вывода нет."

            except Exception as e:
                output = f"[ОШИБКА] {e}"

            conn.sendall(output.encode("utf-8"))
    finally:
        conn.close()
        print(f"[СЕРВЕР] Отключено от {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[СЕРВЕР] Ожидание подключения на {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
