import socket, datetime, sqlite3, configparser, os, subprocess
from pyjokes import get_joke
from uuid import uuid4
from colorama import Fore, init
from webbrowser import register as browser_reg, open as open_url2, BackgroundBrowser
from hashlib import md5

init()

config = configparser.ConfigParser()
config_path = 'settings/config.ini'

db_path = 'settings/database.db'
db_table_name = 'users'

commands_list_path = 'settings/commands_list.txt'

def send(sock, text):
    sock.send(text.encode(encoding='utf-8', errors='ignore'))

def recv(sock, size):
    return sock.recv(size).decode(encoding='utf-8', errors='ignore')

def current_time():
    time = datetime.datetime.today()
    return Fore.WHITE + '[' + str(time.strftime('%H:%M')) + ']' + Fore.RESET

def system(sock):
    send(sock, 'Введите команду.')
    cmd = recv(sock, 1024)
    result = os.system(cmd)
    if result == 1:
        send(sock, 'Команда успешно выполнена')
    else:
        send('Операция не выполнена')

def jokes(sock):
    def joke(count=None):
        if count < 0:
            abs(count)
        if count > 10:
            return 'TooMuch'
        joke = get_joke('ru')
        if count != None:
            jokes = ''
            counter = 1
            for i in range(0, count):
                joke = get_joke('ru')
                jokes = jokes + '\n' + Fore.WHITE + f'[{counter}/{count}] ' + Fore.LIGHTGREEN_EX + joke + Fore.RESET
                counter += 1
            return jokes
        return '\n' + joke
    send(sock, 'Введите кол-во шуток')
    count = recv(sock, 1024)
    try:
        count = int(count)
    except:
        joke()
    jokes = joke(count)
    if jokes == 'TooMuch':
        send(sock, (Fore.RED + 'ОШИБКА! Слишком много.'))
    else:
        send(sock, jokes)

def sub_process(sock):
    send(sock, (Fore.CYAN + 'Введите команду' + Fore.RESET))
    cmd = (recv(sock, 1024))
    cmds_list = ['cmd', '/c', cmd]

    try:
        process = subprocess.Popen(cmds_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()

        send(sock, 'Реузльтат >> ' + output.decode())

    except subprocess.CalledProcessError:
        send(sock, (Fore.RED + f"Ошибка команды {subprocess.CalledProcessError.cmd}!" + Fore.RESET))


def system(sock):
    send(sock, (Fore.CYAN + 'Введите команду' + Fore.RESET))
    cmd = recv(sock, 1024)
    try:
        result = os.system(cmd)
        if result == 1:
            send(sock, (Fore.CYAN + 'Операция не выполнена' + Fore.RESET))
        else:
            send(sock, (Fore.CYAN +'Операция выполнена успешно' + Fore.RESET))
    except:
        send(sock, (Fore.RED + 'ОШИБКА!'))

def calc(sock):
    send(sock, (Fore.CYAN + f'Введите математическую задачу.' + Fore.RESET))
    math = recv(sock, 1024)
    try:
        result = eval(math)
        send(sock, (Fore.LIGHTGREEN_EX + "Ответ >> " + Fore.LIGHTYELLOW_EX + str(result)))
    except:
        send(sock, (Fore.RED + 'ОШИБКА!'))

def open_url(sock):
    config.read(config_path)
    browser = config.get('SETTINGS', 'browser-path')
    browser_reg('Custom', None, BackgroundBrowser(browser))
    send(sock, 'Вставьте ссылку.')
    url = recv(sock, 1024)
    try:
        open_url2(url)
    except:
        send(sock, 'Ошибка! Не удалось проверить ссылку.')

def commands_list(sock):
    with open(commands_list_path) as cmds_list:
        cmds = cmds_list.read()
        cmds = Fore.CYAN + '\n=----------< ' + Fore.LIGHTCYAN_EX + 'Список команд' + Fore.CYAN + ' >----------=\n' + Fore.LIGHTYELLOW_EX + cmds + Fore.CYAN + '\n=-------------------------------------=\n'
        send(sock, cmds)

# Датабаза

def pass_check(username, user_password):
    original_password = get_from_table('login', username)[2]

    if user_password == original_password:
        return True
    else:
        return False

with sqlite3.connect('../settings/database.db') as db:
    cursor = db.cursor()

    # cursor.execute('''create table if not exists
    # users(login PRIMARY KEY, UUID TEXT, password TEXT)''')

    # cursor.execute('''alter table users add column password 'text' ''')


def insert_into_table(**columns):
    def render(value):
        return f'"{value}"'

    keys = ', '.join(list(columns.keys()))
    values = ', '.join(map(render, list(columns.values())))

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(f'''INSERT INTO {db_table_name}({keys}) VALUES({values})''')

def update_table(*where, **updated_columns):
    updated_columns = list(updated_columns.items())

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        for column in updated_columns:
            cursor.execute(f'''UPDATE {db_table_name} SET {column[0]}="{column[1]}" 
                           WHERE {where[0]}="{where[1]}"''')

def get_from_table(*where):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        if len(where) != 0:
            cursor.execute(f'''SELECT * FROM {db_table_name} WHERE {where[0]}="{where[1]}"''')

            return cursor.fetchone()

        cursor.execute(F'''SELECT * FROM {db_table_name}''')

        return cursor.fetchall()

def delete_from_table(*where):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        if len(where) != 0:
            cursor.execute(f'''DELETE FROM {db_table_name} WHERE {where[0]}="{where[1]}"''')

        else:
            cursor.execute(f'''DELETE FROM {db_table_name}''')

#   НАСТРОЙКИ
def settings(sock):
    send(sock, f'''
{Fore.CYAN}=----------< {Fore.LIGHTCYAN_EX}Выберете настройку {Fore.CYAN}>----------=
{Fore.YELLOW}0. Выйти.
1. (ВКЛ/ВЫКЛ) Режим терминала.
2. (ПУТЬ) браузера
{Fore.CYAN}=------------------------------------------={Fore.RESET}
''')
    mode = recv(sock, 1024)
    try:
        mode = int(mode)
    except:
        send(sock, (Fore.RED + 'Ошибка! Нужно выбрать цифру нужной вам настройке.'))

    if mode == 0:
        send(sock, (Fore.RED + 'Вы успешно вышли из редактирования настроек.'))
    elif mode == 1:
        terminal_mode_edit(sock)
    elif mode == 2:
        change_browser_path(sock)

def change_browser_path(sock):
    config.read(config_path)
    old_browser_path = config.get('SETTINGS', 'browser-path')
    send(sock, (Fore.LIGHTGREEN_EX + f'Текущий путь до браузера: "{Fore.YELLOW + str(old_browser_path) + Fore.LIGHTGREEN_EX}". Вы хотите изменить путь?' + Fore.WHITE + ' (Да/Нет)' + Fore.RESET))
    confirm = recv(sock, 1024)
    confirm = str(confirm).lower().strip()
    if confirm == 'да' or confirm == 'lf':
        send(sock, (Fore.CYAN + 'Введите новый путь для браузера'))
        new_browser_path = recv(sock, 1024)
        check_path = os.path.exists(new_browser_path)
        if check_path == True:
            if old_browser_path == new_browser_path:
                send(sock, (Fore.RED + 'ОШИБКА! Данный путь до браузера уже установлен'))
            else:
                send(sock, (Fore.LIGHTGREEN_EX + f'Вы уверенны что хотите изменить путь до браузера на "{Fore.YELLOW + str(new_browser_path) + Fore.LIGHTGREEN_EX}"?'  + Fore.WHITE + ' (Да/Нет)' + Fore.RESET))
                confirm = recv(sock, 1024)
                confirm = str(confirm).lower().strip()
                if confirm == 'да' or confirm == 'lf':
                    config.set('SETTINGS', 'browser-path', new_browser_path)
                    send(sock, (Fore.LIGHTGREEN_EX + 'Вы успешено изменили путь до браузера.' + Fore.RESET))
                    with open(config_path, 'w') as cfg:
                        config.write(cfg)
                else:
                    send(sock, (Fore.RED + 'Отменено.' + Fore.RESET))
        else:
            send(sock, (Fore.RED + 'ОШИБКА! По данному пути ничего не найдено'))
    else:
        send(sock, (Fore.RED + 'Отменено.' + Fore.RESET))
def terminal_mode_edit(sock):
    config.read(config_path)
    terminal_mode = config.getboolean('SETTINGS', 'terminal-mode')
    send(sock, f'{Fore.LIGHTGREEN_EX}Текущее значение "{Fore.YELLOW}Режим терминала{Fore.LIGHTGREEN_EX}": "{Fore.YELLOW + str(terminal_mode) + Fore.RESET}". {Fore.LIGHTGREEN_EX}Вы уверенны что хотите изменить на значение: "{Fore.YELLOW + str(not terminal_mode) + Fore.LIGHTGREEN_EX}" {Fore.WHITE}(Да/Нет){Fore.RESET}')
    confirm = recv(sock, 1024)
    confirm = str(confirm).lower().strip()
    if confirm == 'да' or confirm == 'lf':
        config.set('SETTINGS', 'terminal-mode', str(not terminal_mode))
        send(sock, f'{Fore.LIGHTGREEN_EX}Вы успешно изменили значение "{Fore.YELLOW}Режим терминала{Fore.LIGHTGREEN_EX}" на "{Fore.YELLOW + str(not terminal_mode) + Fore.LIGHTGREEN_EX}"{Fore.RESET}')
        with open(config_path, 'w') as cfg:
            config.write(cfg)
    else:
        send(sock, (Fore.RED + 'Отменено.' + Fore.RESET))

def CheckUserName():
    allowed_chars = ['_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                     'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
                     'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    while True:
        a = True
        username = input(Fore.CYAN + 'Введите логин ' + Fore.WHITE + '>> ' + Fore.RESET)

        counter = 0
        for i in range(0, len(username)):
            for ii in allowed_chars:
                if username[i] == ii:
                    counter += 1
        if counter != len(username):
            print(current_time() + Fore.RED + 'Ошибка! Ваш логин содержит недопустимые символы.')
            continue

        if len(username) < 3:
            print(current_time() + Fore.RED + 'Ошибка! Ваш логин должен содержать 3-х или более символов')
            continue
        elif len(username) > 12:
            print(current_time() + Fore.RED + 'Ошибка! Ваш логин должен содержать 12-и или менее символов')
            continue

        with open('settings/username_blacklist.txt', 'r') as f:
            data = f.read()
            data = data.split('\n')
            for i in data:
                if i == username:
                    print(current_time() + Fore.RED + 'Ошибка! Ваш никнейм содержит запрещенные слова.')
                    a = False
        if a is True:
            return username
        else: continue

def CheckPassword(sock, username):
    send(sock, username)
    check_pass = recv(sock, 1024)
    if check_pass == 'need password':
        print(current_time() + Fore.RED + ' Для данного логина уже зарегистрирован аккаунт. Требуется пароль.' + Fore.RESET)
        pass_status = None
        while pass_status != 'correct password':
            password = input(Fore.CYAN + 'Введите пароль ' + Fore.WHITE + '>> ' + Fore.RESET)

            hash_pass = md5(password.encode())
            password = hash_pass.hexdigest()

            send(sock, password)
            pass_status = recv(sock, 1024)
            if pass_status == 'incorrect password':
                print(f'{current_time()} {Fore.RED}Ошибка! Неверный пароль')
        print(
            f'{current_time()} {Fore.LIGHTGREEN_EX}Вы успешно вошли в систему. Приветствуем вас {Fore.YELLOW + username}!')

def password_allowed_chars():
    allowed_chars = ['.', ',', '/', '\\', '|', ']', '[', '{', '}', '>', '<', '~', '`'
                     '!', '@', '#', '$', '%', '^', '&', '*', ')', '(', '+', '=', '-', '?',
                     ':', ';', '№', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                     'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
                     'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    return allowed_chars

def change_account_password(sock, username):
    allowed_chars = password_allowed_chars()
    data = get_from_table('login', username)
    current_password = data[2]
    if current_password is None:
        send(sock, (Fore.RED + 'Вы еще не авторизированны в системе. Вы хотите авторизоваться? ' + Fore.WHITE + '(Да/Нет)' + Fore.RESET))
        confirm = recv(sock, 1024)
        confirm = str(confirm).strip().lower()
        if confirm == 'да' or confirm == 'lf':
            register_account(sock, username)
        else:
            send(sock, (Fore.RED + 'Отменено!' + Fore.RESET))
    else:
        send(sock, (Fore.LIGHTYELLOW_EX + 'Введите текущий пароль.' + Fore.RESET))
        user_current_password = recv(sock, 1024)
        hashed_user_current_password = md5(user_current_password.encode()).hexdigest()
        if current_password == hashed_user_current_password:
            send(sock, (Fore.LIGHTYELLOW_EX + 'Введите новый пароль.'))
            new_password = recv(sock, 1024)
            if len(new_password) > 24:
                send(sock, (Fore.RED + 'Ошибка! Ваш пароль должен состоять из 24-х или менее символов.' + Fore.RESET))
            elif len(new_password) < 6:
                send(sock, (Fore.RED + 'Ошибка! Ваш пароль должен состоять 6-и или более символов' + Fore.RESET))
            counter = 0
            for i in range(0, len(new_password)):
                for ii in allowed_chars:
                    if new_password[i] == ii:
                        counter += 1
            if counter != len(new_password):
                send(sock, (Fore.RED + 'Ошибка! Ваш пароль содержит недопустимые символы.' + Fore.RESET))
            send(sock, (Fore.LIGHTRED_EX + f'Вы уверенны что хотите изменить пароль на "{Fore.RESET + str(new_password) + Fore.RED}"?' + Fore.WHITE + ' (Да/Нет)' + Fore.RESET))
            confirm = recv(sock, 1024)
            confirm = str(confirm).strip().lower()
            if confirm == 'да' or confirm == 'lf':
                new_password = md5(new_password.encode()).hexdigest()
                update_table('login', username, password=new_password)
                send(sock, (Fore.LIGHTRED_EX + 'Вы успешно изменили пароль аккаунта.' + Fore.RESET))
            else:
                send(sock, (Fore.RED + 'Отменено!' + Fore.RESET))
        else:
            send(sock, (Fore.RED + 'Неверный пароль.' + Fore.RESET))



def register_account(sock, username):
    allowed_chars = password_allowed_chars()
    data = get_from_table('login', username)
    if data[2] is None:
        send(sock, (Fore.LIGHTYELLOW_EX + 'Придумайте пароль.'))
        password = recv(sock, 1024)
        if len(password) > 24:
            send(sock, (Fore.RED + 'Ошибка! Ваш пароль должен состоять из 24-х или менее символов.' + Fore.WHITE + '\n(Введите любое сообщение чтобы продолжить.)' + Fore.RESET))
        elif len(password) < 6:
            send(sock, (Fore.RED + 'Ошибка! Ваш пароль должен состоять 6-и или более символов' + Fore.WHITE + '\n(Введите любое сообщение чтобы продолжить.)' + Fore.RESET))
        else:
            counter = 0
            for i in range(0, len(password)):
                for ii in allowed_chars:
                    if password[i] == ii:
                        counter += 1
            if counter != len(password):
                send(sock, (Fore.RED + 'Ошибка! Ваш пароль содержит недопустимые символы.' + Fore.RESET))
            else:
                send(sock, (Fore.LIGHTYELLOW_EX + 'Подтвердите пароль.' + Fore.RESET))
                confirm = recv(sock, 1024)
                if confirm == password:
                    send(sock, (Fore.LIGHTRED_EX + f'Вы уверенны что хотите зарегистрировать аккаунт {username}?' + Fore.WHITE + '(Да/Нет)' + Fore.RESET))
                    confirm = recv(sock, 1024)
                    confirm = str(confirm).lower().strip()
                    if confirm == 'lf' or confirm == 'да':
                        send(sock, (Fore.LIGHTRED_EX + f'Вы успешно зарегистрировали аккаунт {username}' + Fore.RESET))
                        hashed_pass = md5(password.encode()).hexdigest()
                        update_table('login', username, password=hashed_pass)

                    else:
                        send(sock, (Fore.RED + 'Ошибка! Неверный пароль!' + Fore.RESET))
    else:
        send(sock, (Fore.RED + 'Данный аккаунт уже зарегистрирован. Хотите ли вы сменить пароль на нем? ' + Fore.WHITE + '(Да/Нет)'))
        confirm = recv(sock, 1024)
        confirm = str(confirm).strip().lower()
        if confirm == 'да' or confirm == 'lf':
            change_account_password(sock, username)
        else:
            send(sock, (Fore.RED + 'Отменено!' + Fore.WHITE + '\n(Введите любое сообщение чтобы продолжить.) ' + Fore.RESET))
            recv(sock, 1024)