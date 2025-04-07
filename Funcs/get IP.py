import socket

host_name = socket.gethostname()
host_info = socket.gethostbyname_ex(host_name)
ip = host_info[-1][-1]

print('IP устройства >> ' + ip)