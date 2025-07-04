import socket
import json
import datetime
#from leitor import retorna_tags
# ip público caso não seja a mesma rede
def client(host = '192.168.88.123', port=8102):
	try: 
        	# protocolo tcp
        	db = []
        	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        	print (f"Conectando ao {host} port {port}\n ") 
        	sock.connect((host, port))
        	rfid = int(input("Insira o cartão.."))
        	data_hora = datetime.datetime.now()
        	data_hora = data_hora.strftime('%Y-%m-%d %H:%M:%S')
        	mensagem = f"GET /{str(rfid)} HTTP/1.1\r\nHost: 172.16.103.3:8102\r\n\r\n"
        	sock.send(mensagem.encode('utf-8'))
        	data = sock.recv(2048)
        	item = data.decode('utf-8')
        	it = json.loads(item[105:])[0]
        	res = (data_hora, it[3], it[0], 1, rfid)
        	sock.close()
        	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        	print (f"Conectando ao {host} port {port}\n ") 
        	sock.connect((host, port))
        	db.append(res)
        	response_body = json.dumps(res)
        	with open('db.json', 'w') as arq:
            		json.dump(db, arq)
        	print (f"Enviando {res}\n")
        	mensagem = f"POST HTTP/1.1\r\nHost: 172.16.103.3:8102\r\n\r\n" +  response_body
	       	sock.send(mensagem.encode('utf-8')) 
        	data = sock.recv(2048)    
        	item = data.decode('utf-8')
        	#it = json.loads(item[105:])[0]
        	#print(f"Código: {it[0]}\nNome: {it[1]}\nEndereço: {it[2]}\nLatitude: {it[3]}\nLongitude: {it[4]}") 
        	print(item)
	except socket.error as e: 
        	print (f"Socket error: {e}") 
	except Exception as e: 
		print (f"Other exception: {e}") 
	finally:
		print ("Fechando  conexão com o servidor...\n") 
		sock.close()

sair = False
while not sair:
    '''print("[1] Registrar caixa")
    print("[2] Sair")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        client()
    elif escolha == 2:
        sair = True'''
    client()
