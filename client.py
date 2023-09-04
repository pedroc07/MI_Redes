import socket
import json
import datetime
#from leitor import retorna_tags
# ip público caso não seja a mesma máquina
#host = '172.16.103.3'
def client(host = 'localhost', port=8102):
    tags = []
    '''
    lido = False
    while not lido:
        # LENDO O ID DAS TAGS
        max_dados = 2048 #Máximo de dados recebidos de uma vez
        # protocolo TCP
        server = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        server.bind((host, 8077))
        max_conexoes = 100
        server.listen(max_conexoes)
        cliente, cliente_end = server.accept()
        print(f"Conectado a {cliente_end}")
        data = cliente.recv(max_dados)
        data = data.decode('utf-8')
        if data == "END":
            lido = True
        else:
            tags.append(data)
        cliente.close()
    print("Tags escaneadas com sucesso")
    print(tags)
    server.close()
    '''
    compras = []
    tags = ["E20000172211011718905474", "E20000172211010218905459", "E2000017221100961890544A"]
    try: 
        # ENVIANDO TAGS PRO SERVIDOR
        for mensagem in tags:
            # protocolo tcp
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            print (f"Conectando ao {host} port {port}\n ") 
            sock.connect((host, port))
            print (f"Enviando {mensagem}\n")
            mensagem = f"GET /{mensagem} HTTP/1.1\r\nHost: localhost:8102\r\n\r\n"
            sock.send(mensagem.encode('utf-8')) 
            data = sock.recv(2048)
            compra = data.decode('utf-8')
            c = json.loads(compra[105:])
            compras.append(c)
            
    except socket.error as e: 
        print (f"Socket error: {e}") 
    except Exception as e: 
        print (f"Other exception: {e}") 
    finally:
        print ("Fechando  conexão com o servidor...\n") 
        sock.close()
        print (f"Lista de compras: \n{compras}\n")
        confirm = input("Deseja confirmar  compra? S/N ")
        if confirm.upper() == "S":
            # REMOVENDO ITENS DO ESTOQUE
            for c in compras:
                if int(c['estoque']) > 0:
                    c['estoque'] = str(int(c['estoque']) - 1)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                print (f"Conectando ao {host} port {port}\n ") 
                sock.connect((host, port))
                print (f"Enviando {c['id']}\n")
                mensagem = f'PUT / HTTP/1.1\r\nHost: localhost:8102\r\nContent-Type: application/json\r\nAccept: */*\r\nContent-Length: 88\r\n{c}'
                sock.send(mensagem.encode('utf-8')) 
                data = sock.recv(2048)
        print (f"Compra realizada com sucesso\n")
        d = {"data":str(datetime.datetime.now())}
        compras.insert(0, d)
        with open('compras.json', 'r') as arq:
            compras_arq = json.load(arq)
        compras_arq.append(compras)
        with open('compras.json', 'w') as arq:
            json.dump(compras_arq, arq)

sair = False
while not sair:
    print("[1] Executar uma compra")
    print("[2] Sair")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        client()
    elif escolha == 2:
        sair = True
