import mercury
import sys
from datetime import datetime
import socket
import threading

param = 2300

if len(sys.argv) > 1:
        param = int(sys.argv[1])

# configura a leitura na porta serial onde esta o sensor
reader = mercury.Reader("tmr:///dev/ttyUSB0")

# para funcionar use sempre a regiao "NA2" (Americas)
reader.set_region("NA2")

# nao altere a potencia do sinal para nao prejudicar a placa
reader.set_read_plan([1], "GEN2", read_power=param)

# realiza a leitura das TAGs proximas e imprime na tela
print(reader.read())
def retorna_tags():
    epcs = map(lambda tag: tag, reader.read())
    tags = ""
    for tag in epcs:
        print(tag.epc, tag.read_count, tag.rssi, datetime.fromtimestamp(tag.timestamp))
        tags += tag.epc.decode('utf-8') + "/"

    return tags

host = '172.16.103.0'
port=8077
max_dados = 2048 #Máximo de dados recebidos de uma vez
# protocolo TCP
sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
print (f"Esperando por uma mensagem em {host}, {port}")
sock.bind((host, port))
max_conexoes = 5
sock.listen(max_conexoes)
threads = []

def connect(cliente):
    tags = retorna_tags()
    msg = cliente.recv(max_dados).decode('utf-8')
    res = tags.encode('utf-8')
    cliente.send(res)
    cliente.close()

while True:
    cliente, cliente_end = sock.accept()
    print(f"Conectado a {cliente_end}")
    t1 = threading.Thread(target=connect, args=(cliente,))
    threads.append(t1)
    t1.start()