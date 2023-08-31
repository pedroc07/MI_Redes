#import mercury
import sys
from datetime import datetime
import socket
import threading

param = 2300

if len(sys.argv) > 1:
        param = int(sys.argv[1])

# configura a leitura na porta serial onde esta o sensor
#reader = mercury.Reader("tmr:///dev/ttyUSB0")

# para funcionar use sempre a regiao "NA2" (Americas)
#reader.set_region("NA2")

# nao altere a potencia do sinal para nao prejudicar a placa
#reader.set_read_plan([1], "GEN2", read_power=param)

# realiza a leitura das TAGs proximas e imprime na tela
# print(reader.read())
def retorna_tags():
    pass
    '''epcs = map(lambda tag: tag, reader.read())
    tags = []
    for tag in epcs:
        print(tag.epc, tag.read_count, tag.rssi, datetime.fromtimestamp(tag.timestamp))
        tags.append(tag.epc)

    return tags'''

host = 'localhost'
port=8077
max_dados = 2048 #Máximo de dados recebidos de uma vez
# protocolo TCP
sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
print (f"Esperando por uma solicitação em {host}, {port}")
sock.bind((host, port))
max_conexoes = 100
sock.listen(max_conexoes)


def connect(cliente):
    msg = cliente.recv(max_dados).decode('utf-8')
    tags = retorna_tags()
    tags = ["E20000172211011718905474", "E20000172211010218905459", "E2000017221100961890544A"]
    for tag in tags:
        cliente.send(tag.encode('utf-8'))
        print(f"Enviando tag {tag}")
    cliente.close()

while True:
    cliente, cliente_end = sock.accept()
    print(f"Conectado a {cliente_end}")
    t1 = threading.Thread(target=connect, args=(cliente,))
    t1.start()