import socket
import sys
import struct
import random
import os

PACKET_SIZE = 1024
HEADER_SIZE = 8
LOSS_PROBABILITY = 0.3

class StopAndWaitClient:
    def __init__(self, server_host, server_port, timeout=2.0):
        self.server_host = server_host
        self.server_port = server_port
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)
        self.sequence_number = 0
        
    def create_packet(self, seq_num, data):
        data_size = len(data)
        header = struct.pack('!II', seq_num, data_size)
        return header + data
    
    def parse_ack(self, ack_data):
        if len(ack_data) >= 4:
            ack_seq_num = struct.unpack('!I', ack_data[:4])[0]
            return ack_seq_num
        return None
    
    def simulate_packet_loss(self):
        return random.random() < LOSS_PROBABILITY
    
    def send_packet_reliable(self, data):
        packet = self.create_packet(self.sequence_number, data)
        max_retries = 5
        
        for attempt in range(max_retries):
            try:
                if not self.simulate_packet_loss():
                    print(f"Отправляем пакет {self.sequence_number} (попытка {attempt + 1})")
                    self.socket.sendto(packet, (self.server_host, self.server_port))
                else:
                    print(f"Пакет {self.sequence_number} потерян при отправке (попытка {attempt + 1})")
                    continue
                
                try:
                    ack_data, _ = self.socket.recvfrom(1024)
                    ack_seq_num = self.parse_ack(ack_data)
                    
                    if ack_seq_num == self.sequence_number:
                        print(f"Получен ACK для пакета {self.sequence_number}")
                        self.sequence_number = 1 - self.sequence_number
                        return True
                    else:
                        print(f"Получен неверный ACK: ожидался {self.sequence_number}, получен {ack_seq_num}")
                        
                except socket.timeout:
                    print(f"Таймаут при ожидании ACK для пакета {self.sequence_number}")
                    
            except Exception as e:
                print(f"Ошибка при отправке пакета: {e}")
        
        print(f"Не удалось отправить пакет {self.sequence_number} после {max_retries} попыток")
        return False
    
    def send_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден")
            return False
        
        file_size = os.path.getsize(file_path)
        print(f"Передача файла {file_path} (размер: {file_size} байт)")
        
        filename = os.path.basename(file_path).encode('utf-8')
        if not self.send_packet_reliable(filename):
            print("Не удалось отправить имя файла")
            return False
        
        with open(file_path, 'rb') as f:
            total_packets = 0
            
            while True:
                data = f.read(PACKET_SIZE)
                if not data:
                    break
                
                total_packets += 1
                if not self.send_packet_reliable(data):
                    print("Не удалось отправить пакет данных")
                    return False
        
        if self.send_packet_reliable(b''):
            print(f"Файл отправлен. Всего пакетов: {total_packets}")
            return True
        else:
            print("Не удалось отправить сигнал окончания файла")
            return False
    
    def close(self):
        self.socket.close()

def main():
    if len(sys.argv) < 3:
        print("Использование: python client.py <путь_к_файлу> <таймаут> [адрес_сервера] [порт_сервера]")
        print("Пример: python client.py test.txt 2.0 127.0.0.1 12345")
        sys.exit(1)
    
    file_path = sys.argv[1]
    timeout = float(sys.argv[2])
    server_host = sys.argv[3] if len(sys.argv) > 3 else '127.0.0.1'
    server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 12345
    
    client = StopAndWaitClient(server_host, server_port, timeout)
    
    try:
        success = client.send_file(file_path)

        if success:
            print("Передача завершена успешно")
        else:
            print("Передача файла не удалась")
            
    except KeyboardInterrupt:
        print("\nПрерывание пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()