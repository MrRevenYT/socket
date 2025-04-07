import configparser

config = configparser.ConfigParser()
config.add_section('SETTINGS')
config.set('SETTINGS', 'terminal-mode', 'True')
config.set('SETTINGS', 'browser-path', r'C:\Users\pasha\AppData\Local\Yandex\YandexBrowser\Application\browser.exe')

with open('../settings/config.ini', 'w') as cfg:
    config.write(cfg)