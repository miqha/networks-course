import socket
import tkinter as tk

HOST = '127.0.0.1' 
PORT = 65433

class DrawingClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        print(f"[КЛИЕНТ] Подключено к {HOST}:{PORT}")

        self.root = tk.Tk()
        self.root.title("Клиент: Рисование")
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.last_x, self.last_y = None, None
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.root.mainloop()

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_mouse_drag(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=2)
        try:
            message = f"{self.last_x},{self.last_y},{x},{y}\n"
            self.sock.sendall(message.encode())
        except Exception as e:
            print(f"[ОШИБКА] {e}")
        self.last_x, self.last_y = x, y

if __name__ == "__main__":
    DrawingClient()
