import socket
# ip público caso não seja a mesma máquina
def client(host = '192.168.42.137', port=8099): 
    # protocolo tcp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print (f"Conectando ao {host} port {port}") 
    sock.connect((host, port))
    try: 
        mensagem = "3" 
        print (f"Enviando {mensagem}") 
        sock.send(mensagem.encode('utf-8')) 
        data = sock.recv(2048) 
        print (f"Mensagens recebidas: {data.decode('utf-8')}") 
    except socket.error as e: 
        print (f"Socket error: {e}") 
    except Exception as e: 
        print (f"Other exception: {e}") 
    finally: 
        print ("Fechando  conexão com o servidor...") 
        sock.close() 

client()
