import socket
import pyaudio
import threading
import uuid

# Конфигурация аудио
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Генерация уникального ID
user_id = str(uuid.uuid4())

# Инициализация сокета
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 0))  # Привязываем к любому свободному порту

# Получение собственного IP-адреса
local_ip = socket.gethostbyname(socket.gethostname())
local_port = sock.getsockname()[1]

# Вывод информации о пользователе
print(f"Ваш уникальный ID: {user_id}")
print(f"Ваш IP: {local_ip}")
print(f"Ваш порт: {local_port}")

# Ввод IP и порта другого пользователя
server_ip = input("Введите IP другого пользователя для подключения: ")
server_port = int(input("Введите порт для подключения: "))

# Инициализация PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, output=True,
                    frames_per_buffer=CHUNK)

# Функция для отправки ID
def send_id():
    sock.sendto(user_id.encode(), (server_ip, server_port))

# Функция для отправки аудио
def send_audio():
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (server_ip, server_port))

# Функция для получения данных (ID или аудио) и обработки
def receive_data():
    while True:
        data, addr = sock.recvfrom(1024 * 10)
        # Если данные меньше определенного размера, считаем, что это ID
        if len(data) < 50:
            received_id = data.decode()
            print(f"Получен ID другого пользователя: {received_id}")
        else:
            # Воспроизведение аудио
            stream.write(data)

# Отправка ID другому пользователю
send_id()

# Создание потоков для отправки и получения аудио и ID
send_thread = threading.Thread(target=send_audio)
receive_thread = threading.Thread(target=receive_data)

send_thread.start()
receive_thread.start()

# Ожидание завершения потоков
send_thread.join()
receive_thread.join()
