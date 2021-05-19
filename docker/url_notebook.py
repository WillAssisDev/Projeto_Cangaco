from os import system, remove
from time import sleep

arquivo = open('token.txt', 'r')
url = arquivo.readlines()[1]
url = 'http://127.0.0.1:' + url[15:url.find(' ')]
arquivo.close()
sleep(1)
system('start chrome ' + url)
remove('token.txt')
