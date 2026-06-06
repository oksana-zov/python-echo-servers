import socket
import sys


HOST = "127.0.0.1"
PORT = 50432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((HOST, PORT))
    # Проблема 4, на случай, если сервер выключился
    except ConnectionRefusedError:
        print("Ошибка: Сервер не запущен!")
        sys.exit(1)

    while True:
        data_to_send = input('Ваше сообщение: ')
        # Проблема 3: Защита от пустого ввода (если нажали Enter)
        if not data_to_send.strip():
            print('Ошибка: Нельзя отправлять пустое сообщение!')
            continue  # Просим ввести заново, не зависая на отправке/получении

        data_bytes_to_send = data_to_send.encode()
        # Проблема 4: Обработка отправки/получения, если сервер был выключен
        try:
            sock.sendall(data_bytes_to_send)# отправляем
            data_bytes_received = sock.recv(1024) # получаем ответ
            # Если сервер разорвал соединение в этот момент
            if not data_bytes_received:
                print("Программа на вашем хост-компьютере разорвала установленное подключение")
                break

            data_received = data_bytes_received.decode()
            print(f'Получено:', data_received) # выводим ответ

            # Если мы ввели команду выхода, то ПОСЛЕ получения ответа завершаем цикл
            if data_to_send.lower() == 'exit':
                break

        except (ConnectionError, BrokenPipeError):
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break

    print("\nProcess finished with exit code 0")
    sys.exit(0)
