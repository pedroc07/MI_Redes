import socket
import json
import datetime
#from leitor import retorna_tags
# ip público caso não seja a mesma rede
def client(host = '172.16.103.3', port=8102):
    try:
        # LENDO O ID DAS TAGS
        # protocolo TCP
        sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        sock.connect(('172.16.103.0', 8077))
        print (f"Conectando ao {host} port {8077}\n ")
        mensagem = "teste"
        print (f"Enviando {mensagem}")
        sock.send(mensagem.encode('utf-8'))
        data = sock.recv(2048)
        tags = data.decode('utf-8')
        tags = tags.split("/")
    
    except socket.error as e: 
        print (f"Socket error: {e}") 
    except Exception as e: 
        print (f"Other exception: {e}") 
    finally:
        print("Tags escaneadas com sucesso")
        print(tags)
        sock.close()

    compras = []
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
