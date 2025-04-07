from Funcs.sockFuncs import *

def main():
    username = CheckUserName()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = 'localhost'
    server_port = 8080
    server_address = (server_ip, server_port)


    sock.connect(server_address)


    try:
        CheckPassword(sock, username)
        while True:
            sent_data = input(Fore.CYAN + 'Введите команду/сообщение ' + f'{Fore.RESET}>> ')

            send(sock, sent_data)
            incoming_data = recv(sock, 4096)

            if incoming_data == 'stop':
                send(sock, 'stop')
                break

            else:
                print(f'{current_time()} <{Fore.YELLOW}Сервер{Fore.RESET}> {incoming_data}')

    finally:
        sock.close()
        print(f'<{Fore.YELLOW}Сервер{Fore.RESET}> Соединение с сервером ' + Fore.RED + 'закрыто!' + Fore.RESET)

    k = input(Fore.WHITE + 'Нажмите Enter для продолжения...')

if __name__ == '__main__':
    main()