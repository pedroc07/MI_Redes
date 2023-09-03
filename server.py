from fastapi import FastAPI
from pydantic import *
import json
from typing import *
import socket
import threading

class Produto(BaseModel):
    id: str 
    nome: str
    preco: float
    estoque: int


with open('produtos.json', 'r') as arq:
    produtos = json.load(arq)

def cria_headers(status_code: int, status_text: str, msg="") -> bytes:
    response_protocol = "HTTP/1.1"
    response_status_code = status_code
    response_status_text = status_text
    response_content_type = "application/json; encoding=utf8"
    response_connection = "close"
    message_body_bytes = msg.encode('utf-8')
    response_content_length = len(message_body_bytes)

    # Create seções
    status_line = f"{response_protocol} {response_status_code} {response_status_text}\r\n"
    connection = f"Connection: {response_connection}\r\n"
    content_type = f"Content-Type: {response_content_type}\r\n"
    content_length = f"Content-Length: {response_content_length}\r\n"
    empty_line = "\r\n"

    # Concatenar string
    response_header = (
        status_line +
        connection +
        content_type +
        content_length +
        empty_line
    )

    # Concatenar header e corpo da mensagem
    response = response_header.encode('utf-8') + message_body_bytes

    return response

# GET
def get_byid(produto_id:str):
    produto = [p for p in produtos if p['id'] == produto_id]
    return produto[0] if len(produto) > 0 else {}

def do_GET(produto_id:str):
    produto = get_byid(produto_id)
    if produto:
        response_body = json.dumps(produto)
        return cria_headers(200, "OK", response_body)
    else:
        return cria_headers(404, "Not Found")

# POST
def do_POST(produto):
    print(produto)
    p = json.loads(produto)
    produto_novo = {
            "id": p['id'],
            "nome": p['nome'],
            "preco": p['preco'],
            "estoque": p['estoque']
    }
    produtos.append(produto_novo)
    with open('produtos.json', 'w') as arq:
        json.dump(produtos, arq)
        
    response_body = json.dumps({"status": "ok"})
    return cria_headers(200, "OK", response_body)

# PUT
def do_PUT(produto: list):
    produto_novo = {
        "id": produto['id'],
        "nome": produto['nome'],
        "preco": produto['preco'],
        "estoque": produto['estoque']
    }
    produto_lista = [p for p in produtos if p['id'] == produto['id']]
    if len(produto_lista) > 0:
        produtos.remove(produto_lista[0])
        produtos.append(produto_novo)
    with open('produtos.json', 'w') as arq:
        json.dump(produtos, arq)

# DELETE
def do_DELETE(produto_id:str):
    produto = get_byid(produto_id)
    if len(produto) > 0:
        produtos.remove(produto)
        with open('produtos.json', 'w') as arq:
            json.dump(produtos, arq)
        response_body = json.dumps({"status": "ok"})
        return cria_headers(200, "OK", response_body)
    else:
        return cria_headers(404, "Not Found")

#host = socket.gethostbyname(socket.gethostname())
host = 'localhost'
port=8102
max_dados = 2048 #Máximo de dados recebidos de uma vez
# protocolo TCP
sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
print (f"Esperando por uma mensagem em {host}, {port}")
sock.bind((host, port))
max_conexoes = 5
sock.listen(max_conexoes)
bloqueados = []

def connect(cliente):
    msg = cliente.recv(max_dados).decode('utf-8')
    if msg[0:3] == 'GET':  
        print(f"Produto de ID {msg[5:29]} detectado")
        res = do_GET(msg[5:29])
        cliente.send(res)
    elif msg[0:3] == 'PUT':
        res = do_PUT(msg)
        cliente.send(res)
    elif msg[0:4] == 'POST':
        res = do_POST(msg[137:])
        cliente.send(res)
    elif msg[0:6] == 'DELETE':
        res = do_DELETE(msg[8:32])
        cliente.send(res)
        print(f"Produto de ID {msg[8:32]} deletado.")
    cliente.close()

while True:
    cliente, cliente_end = sock.accept()
    for b in bloqueados:
        if b == cliente_end:
            cliente.close()
    print(f"Conectado a {cliente_end}")
    t1 = threading.Thread(target=connect, args=(cliente,))
    t1.start()