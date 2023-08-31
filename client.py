import socket
#from leitor import retorna_tags
# ip público caso não seja a mesma máquina
def client(host = 'localhost', port=8099):
    compras = ""
    try: 
        tags = ["E20000172211011718905474", "E20000172211010218905459", "E2000017221100961890544A"]
        for mensagem in tags:
            # protocolo tcp
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            print (f"Conectando ao {host} port {port}\n ") 
            sock.connect((host, port))
            print (f"Enviando {mensagem}\n") 
            sock.send(mensagem.encode('utf-8')) 
            data = sock.recv(2048)
            compras += data.decode('utf-8') + "\n"
    except socket.error as e: 
        print (f"Socket error: {e}") 
    except Exception as e: 
        print (f"Other exception: {e}") 
    finally:
        print ("Fechando  conexão com o servidor...\n") 
        sock.close()
        print (f"Lista de compras:\n{compras}")
        confirm = input("Deseja confirmar  compra? S/N ")
        if confirm.upper() == "S":
            # exclui tags
            pass

sair = False
while not sair:
    print("[1] Executar uma compra")
    print("[2] Sair")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        client()
    elif escolha == 2:
        sair = True
