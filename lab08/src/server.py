import socket
import sys
import struct
import random
import os
import time

LOSS_PROBABILITY = 0.3

class StopAndWaitServer:
    def __init__(self, host, port, output_dir, timeout=2.0):
        self.host = host
        self.port = port
        self.output_dir = output_dir
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(self.timeout)
        self.expected_sequence = 0
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def parse_packet(self, packet_data):
        if len(packet_data) < 8:
            return None, None
        
        seq_num, data_size = struct.unpack('!II', packet_data[:8])
        data = packet_data[8:8+data_size]
        
        return seq_num, data
    
    def create_ack(self, seq_num):
        return struct.pack('!I', seq_num)
    
    def simulate_packet_loss(self):
        return random.random() < LOSS_PROBABILITY
    
    def send_ack(self, seq_num, client_address):
        ack_packet = self.create_ack(seq_num)
        
        if not self.simulate_packet_loss():
            self.socket.sendto(ack_packet, client_address)
            print(f"Отправлен ACK для пакета {seq_num}")
        else:
            print(f"ACK для пакета {seq_num} потерян при отправке")
    
    def handle_client(self, client_address):
        print(f"Новый клиент: {client_address[0]}:{client_address[1]}")
        
        filename = None
        file_handle = None
        
        try:
            while True:
                packet_data, addr = self.socket.recvfrom(2048)
                
                if addr != client_address:
                    continue
                
                seq_num, data = self.parse_packet(packet_data)
                
                if seq_num is None:
                    print("Некорректный пакет")
                    continue
                
                print(f"Получен пакет {seq_num}")
                
                if seq_num == self.expected_sequence:
                    if filename is None:
                        filename = data.decode('utf-8')
                        file_path = os.path.join(self.output_dir, filename)
                        file_handle = open(file_path, 'wb')
                        print(f"Приём файла: {filename}")
                    
                    elif len(data) == 0:
                        if file_handle:
                            file_handle.close()
                            print(f"Файл {filename} успешно получен и сохранен в {self.output_dir}")
                            self.send_ack(seq_num, client_address)
                            self.expected_sequence = 1 - self.expected_sequence
                        break
                    
                    else:
                        if file_handle:
                            file_handle.write(data)
                        print("Записаны данные размером {} байт".format(len(data)))
                    
                    self.send_ack(seq_num, client_address)
                    self.expected_sequence = 1 - self.expected_sequence
                
                else:
                    print(f"Получен дублированный пакет {seq_num} (ожидался {self.expected_sequence})")
                    self.send_ack(seq_num, client_address)

        except socket.timeout:
            print(f"Таймаут при ожидании пакета {self.expected_sequence}")

        except Exception as e:
            print(f"Ошибка при обработке клиента: {e}")
        
        finally:
            if file_handle:
                file_handle.close()
            self.expected_sequence = 0
    
    def start(self):
        print(f"Сервер запущен на {self.host}:{self.port}")
        print(f"Файлы будут сохраняться в директории: {self.output_dir}")
        print("Ожидание клиентов...")
        
        try:
            while True:
                packet_data, client_address = self.socket.recvfrom(2048)
                self.handle_client(client_address)
                
        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.socket.close()

def main():
    if len(sys.argv) < 3:
        print("Использование: python server.py <путь_для_записи> <таймаут> [адрес] [порт]")
        print("Пример: python server.py ./received_files 2.0 127.0.0.1 12345")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    timeout = float(sys.argv[2])
    host = sys.argv[3] if len(sys.argv) > 3 else '127.0.0.1'
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 12345
    
    server = StopAndWaitServer(host, port, output_dir, timeout)
    server.start()

if __name__ == "__main__":
    main()
