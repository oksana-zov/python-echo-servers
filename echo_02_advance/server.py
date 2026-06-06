import socket
import sys

HOST = "127.0.0.1"
PORT = 50432

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        # Позволяет повторно использовать порт сразу после перезапуска сервера
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_socket.bind((HOST, PORT))
        serv_socket.listen()
        while True:
            print('Ожидаю соединения...')
            sock, addr = serv_socket.accept()
            with sock:
                print('Подключение по адресу:', addr)
                while True:
                    try:
                        data = sock.recv(1024)
                    except ConnectionError:
                        print(f'Клиент внезапно отключился')
                        break
                    # Проблема 2: Клиент закрыл соединение стандартным способом (передал пустоту)
                    if not data:
                        print(f'Клиент {addr} штатно закрыл соединение')
                        break

                    # переводим байты в текст, тут будет храниться строка
                    message = data.decode().strip()

                    # Проблема 1: Отключение клиента по команде exit
                    if message.lower() == 'exit':
                        print(f'Клиент {addr} запросил отключение через "exit"')
                        try:
                            sock.sendall(b'Goodbye!')# пытаемся отправить данные
                        except ConnectionError:
                            pass # Если связь оборвалась, игнорируем и идем дальше
                        break

                    # Проблема 4: Выключение сервера по команде stop server
                    if message.lower() == 'stop server':
                        print(f'Получена команда stop server от {addr}. Выключаем сервер...')
                        try:
                            sock.sendall(b'Server is shutting down...')
                        except ConnectionError:
                            pass
                        sys.exit(0)# просто всё закроем

                    print(f'Получено: {data}, от {addr}')
                    data = data.upper()
                    print(f'Отправлено: {data}, по адресу: {addr}')

                    try:
                        sock.sendall(data)
                    except ConnectionError:
                        print(f'Клиент внезапно отключился не могу отправить данные')

            print("Отключение по")
