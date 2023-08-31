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

app = FastAPI()

with open('produtos.json', 'r') as arq:
    produtos = json.load(arq)

@app.get('/produto/{produto_id}')
def get_produto(produto_id:str):
    produto = [p for p in produtos if p['id'] == produto_id]
    return produto[0] if len(produto) > 0 else {}

@app.post('/NovoProduto', status_code=201)
def novo_produto(nome, preco, estoque=0):
    produto_id = max(p['id'] for p in produtos) + 1
    produto_novo = {
        "id": produto_id,
        "nome": nome,
        "preco": preco,
        "estoque": estoque
    }
    produtos.append(produto_novo)
    with open('produtos.json', 'w') as arq:
        json.dump(produtos, arq)

    return produto_novo

@app.put('/EditaProduto', status_code=202)
def edita_produto(produto: Produto):
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

@app.delete('/DeleteProduto/{produto_id}')
def deleta_produto(produto_id:str):
    produto = [p for p in produtos if p['id'] == produto_id]
    if len(produto) > 0:
        produtos.remove(produto[0])
        with open('produtos.json', 'w') as arq:
            json.dump(produtos, arq)

    return produto
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
    if msg[0] == 'R':  
        msg = msg[1:]
        print(f"Produto de ID {msg} detectado")
        produto = get_produto(msg)
        cliente.send(("Produto identificado:" + str(produto)).encode('utf-8'))
    elif msg[0] == 'W':
        msg = msg[1:]
        produto = get_produto(msg)
        produto['estoque'] -= 1
        edita_produto(produto)
        print(f"{produto['nome']} foi comprado")
    cliente.close()

while True:
    cliente, cliente_end = sock.accept()
    '''for b in bloqueados:
        if b == cliente_end:
            cliente.close()'''
    print(f"Conectado a {cliente_end}")
    t1 = threading.Thread(target=connect, args=(cliente,))
    t1.start()