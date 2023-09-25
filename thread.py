import logging
import threading
import time
import random

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(10)
    logging.info("Thread %s: finishing", name)

def random_duracao(tipo): #retorna um valor de duração do corte com base no tipo de cliente
    if(tipo == 1):
        return random.randint(4, 6)
    if(tipo == 2):
        return random.randint(2, 4)
    return random.randint(1, 3)

def sargento(tipoCliente, filas, cont): #função recursiva pra fazer o trabalho do sargento
    if(cont < 3):
        if(len(tipoCliente) > 0):
            tipoAtual = tipoCliente.pop()
            insere_fila(filas, tipoAtual, random.randint(1, 4))
        else:
            cont+=1
        sargento(tipoCliente, filas, cont)

    logging.info("Sargento Tainha indo embora!")

def insere_fila(filas, tipo, cochilo): #(lista, inteiro, inteiro), é dado o tipo de cliente e o tempo de cochilo após inseri-lo. 1 == oficial, 2 == sargento, 3 == cabo
    if((len(filas[0]) + len(filas[1]) + len(filas[2])) <= 20):
        logging.info("Sargento Tainha: inserindo %d", tipo)
        duracao = random_duracao(tipo)
        filas[tipo - 1].append(duracao) ## 0 é oficial, 1 é sargento, 2 é cabo
        time.sleep(cochilo)
        logging.info("Sargento Tainha: acordando")
        return 0 #se 0 for retornado, inserção completa
    elif(tipo == 0):
        logging.info("Pausa!")
        time.sleep(cochilo)
        return 1 #se retornar 1, inserção pausada
    elif(tipo == 2):
        logging.info("Fila cheia!")
        time.sleep(cochilo)
        return 2
    else: #se a fila estiver vazia
        return 3

def ordenaPrioridade(fila):
    """ordena a fila por prioridade"""
    fila_ordenada = []
    # itera sobre os tipos
    for tipo in range(3):
        for elemento in fila:
            if elemento == tipo:
                fila_ordenada.append(elemento)
    return fila_ordenada

def corteBarbeiro(nome, fila):
    if(len(fila) > 0):
        logging.info("Barbeiro %s: cortando", nome)
        clienteAtual = fila.pop() #cada cliente é representado por um inteiro (duração do corte)
        time.sleep(clienteAtual)
        logging.info("Barbeiro %s: livre", nome)
        corteBarbeiro(nome, fila)
    else:
        logging.info("Barbeiro %s: fila vazia!", nome)
        time.sleep(1)
        corteBarbeiro(nome, fila)


#main
tipoCliente = []
for i in range(10):
    tipoCliente.append(random.randint(1, 3))
print(tipoCliente)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

filas = [[], [], []]

tainha = threading.Thread(target=sargento, args=(tipoCliente, filas, 0))
#PRECISA FAZER O barbeiro OLHAR AS FILAS NA ORDEM, E TAMBEM INSERIR NA ORDEM CERTA
barbeiro = threading.Thread(target=corteBarbeiro, args=("Zero", filas))
tainha.start()
barbeiro.start()
