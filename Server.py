from Funcs.sockFuncs import *

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = 'localhost'
    port = 8080
    server_address = (ip, port)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(server_address)
    sock.listen(1)

    while True:
        print(Fore.LIGHTGREEN_EX + 'Ожидание подключения...')
        connection, client_address = sock.accept()

        try:
            client_username = recv(connection, 1024)
            data = get_from_table('login', client_username)
            if data is not None:
                if data[2] is not None:
                    send(connection, 'need password')
                    while True:
                        password = recv(connection, 1024)
                        pass_status = pass_check(client_username, password)
                        if pass_status is True:
                            send(connection, 'correct password')
                            break
                        else:
                            send(connection, 'incorrect password')
                elif data[2] is None:
                    send(connection, 'a')
            elif data is None:
                id = uuid4()
                insert_into_table(login=client_username, UUID=id)
                send(connection, 'data_accepted')

            print(f'{current_time()} <{Fore.YELLOW}Сервер{Fore.RESET}> {Fore.GREEN}подключено к {Fore.LIGHTGREEN_EX}{client_username} {Fore.WHITE}{client_address}' + Fore.RESET)

            while True:
                incoming_data = recv(connection, 2048)
                incoming_data.lower().strip()

                if incoming_data == 'stop':
                    send(connection, 'stop')
                    break

                elif incoming_data == 'subprocess':
                    sub_process(connection)
                    continue

                elif incoming_data == 'system':
                    system(connection)
                    continue

                elif incoming_data == 'joke' or incoming_data == 'jokes':
                    jokes(connection)
                    continue


                elif incoming_data == 'url':
                    open_url(connection)
                    continue


                elif incoming_data == 'calculator' or incoming_data == 'calc':
                    calc(connection)
                    continue

                elif incoming_data == 'settings':
                    settings(connection)
                    continue

                elif incoming_data == 'cmds' or incoming_data == 'commands':
                    commands_list(connection)
                    continue

                elif incoming_data == 'reg' or incoming_data == 'register':
                    register_account(connection, client_username)
                    continue

                elif incoming_data == 'change_pass' or incoming_data == 'change_password':
                    change_account_password(connection, client_username)
                    continue

                elif incoming_data == 'system':
                    system(sock)
                    continue


                else:
                    print(f'{current_time()} <{Fore.YELLOW + client_username + Fore.RESET}> {incoming_data}')
                    config.read(config_path)
                    terminal_mode = config.getboolean('SETTINGS', 'terminal-mode')

                    if terminal_mode == True:
                        send(connection, f'{Fore.LIGHTRED_EX}*Нет ответа')
                    else:
                        sent_data = input(Fore.CYAN + 'Введите сообщение ' + Fore.WHITE + '>> ' + Fore.RESET);
                        send(connection, sent_data)

        finally:
            print(f'{current_time()} <{Fore.YELLOW}Сервер{Fore.RESET}> соединение с "{Fore.YELLOW + client_username + Fore.RESET}" {Fore.RED}закрыто!' + Fore.RESET)

            connection.close()


if __name__ == '__main__':
    main()
