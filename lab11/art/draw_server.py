import socket
import threading
import tkinter as tk

HOST = '0.0.0.0'
PORT = 65433

class DrawingServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сервер: Холст")
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.last_x, self.last_y = None, None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        print(f"[СЕРВЕР] Ожидание подключения на {HOST}:{PORT}...")
        self.conn, _ = self.sock.accept()
        print(f"[СЕРВЕР] Клиент подключен.")

        threading.Thread(target=self.receive_coords, daemon=True).start()
        self.root.mainloop()

    def receive_coords(self):
        while True:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                coords = data.strip().split(',')
                if len(coords) == 4:
                    x1, y1, x2, y2 = map(float, coords)
                    self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            except Exception as e:
                print(f"[ОШИБКА] {e}")
                break

if __name__ == "__main__":
    DrawingServer()
