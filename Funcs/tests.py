# class User:
#     def __init__(self, password, login):
#         self.password = password
#         self.login = login
# from hashlib import md5
# password = 'ghdfas'
# hashed_pass = md5(password.encode()).hexdigest()
# print(hashed_pass)

# cmd = 'echo %date%'
#
# cmds_list = cmd.split(' ')
#
# print(cmds_list)

# import subprocess
#
# # Способ 2 (без shell=True)
# cmd = ["cmd", "/c", "echo", "05.04.2025"]
# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
# # Проверка вывода
# output, error = process.communicate()
# print(output.decode())  # Выведет: 05.04.2025

# import os;
# print(os.environ.get("USERNAME"))

# from webbrowser import register as browser_reg, BackgroundBrowser, open
#
# browser_path = r'C:\Users\pdsgash2a\AppData\Local\Yandex\YandexBrowser\Application\brrrrowser.exe'
# browser_reg('Yandex', None, BackgroundBrowser(browser_path))
#
# url = r'https://stackoverflow.com/questions/117014/how-to-retrieve-name-of-current-windows-user-ad-or-local-using-python'
#
# open(url)
# import os
# a = os.path.exists(r'C:\Users\pasha\AppData\Local\Yandex\YandexBrowser\Application\browser.exe')
# print(a)