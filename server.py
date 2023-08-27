from fastapi import FastAPI
from pydantic import *
import json
from typing import *
import socket
import threading
import time

class Produto(BaseModel):
    id: int 
    nome: str
    preco: float

app = FastAPI()

with open('produtos.json', 'r') as arq:
    produtos = json.load(arq)

'''@app.get('/produtos')
def get_produtos():
    return produtos'''

@app.get('/produto/{produto_id}')
def get_produto(produto_id:int):
    produto = [p for p in produtos if p['id'] == produto_id]
    return produto[0] if len(produto) > 0 else {}

@app.post('/NovoProduto', status_code=201)
def novo_produto(nome, preco):
    produto_id = max(p['id'] for p in produtos) + 1
    produto_novo = {
        "id": produto_id,
        "nome": nome,
        "preco": preco
    }
    produtos.append(produto_novo)
    with open('produtos.json', 'w') as arq:
        json.dump(produtos, arq)

    return produto_novo

@app.delete('/DeleteProduto/{produto_id}')
def deleta_produto(produto_id:int):
    produto = [p for p in produtos if p['id'] == produto_id]
    if len(produto) > 0:
        produtos.remove(produto[0])
        with open('produtos.json', 'w') as arq:
            json.dump(produtos, arq)

    return produto

host = 'localhost'
port=8099
max_dados = 2048 #Máximo de dados recebidos de uma vez
# protocolo TCP
sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
print (f"Esperando por uma mensagem em {host}, {port}")
sock.bind((host, port))
max_conexoes = 5
sock.listen(max_conexoes)

def connect(cliente):
    msg = cliente.recv(max_dados).decode('utf-8')
    print(f"Produto de ID {msg} detectado")
    produto = get_produto(int(msg))
    cliente.send(("Produto identificado:" + str(produto)).encode('utf-8'))
    cliente.close()

while True:
    cliente, cliente_end = sock.accept()
    print(f"Conectado a {cliente_end}")
    t1 = threading.Thread(target=connect, args=(cliente,))
    t1.start()