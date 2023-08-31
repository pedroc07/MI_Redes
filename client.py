import socket
#from leitor import retorna_tags
# ip público caso não seja a mesma máquina
def client(host = 'localhost', port=8099):
    # protocolo tcp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print (f"Conectando ao {host} port {port}") 
    sock.connect((host, port))
    try: 
        tags = ["E20000172211011718905474", "E20000172211010218905459", "E2000017221100961890544A"]
        for mensagem in tags:
            print (f"Enviando {mensagem}") 
            sock.send(mensagem.encode('utf-8')) 
            data = sock.recv(2048) 
            print (f"Lista de compras:\n{data.decode('utf-8')}")
            confirm = input("Deseja confirmar  compra? ")
    except socket.error as e: 
        print (f"Socket error: {e}") 
    except Exception as e: 
        print (f"Other exception: {e}") 
    finally: 
        print ("Fechando  conexão com o servidor...") 
        sock.close() 

sair = False
while not sair:
    print("[1] Executar uma compra")
    print("[2] Sair")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        client()
    elif escolha == 2:
        sair = True
