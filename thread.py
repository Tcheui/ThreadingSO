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

def sargento(clientes, filas, cont): #função recursiva pra fazer o trabalho do sargento
    if(cont < 3):
        if(len(clientes) > 0):
            clienteAtual = clientes.pop()
            insere_fila(filas, clienteAtual, random.randint(1, 5))
        else:
            cont+=1
        sargento(clientes, filas, cont)

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
clientes = []
for i in range(10):
    clientes.append(random.randint(1, 3))
print(clientes)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

filas = [[], [], []]

tainha = threading.Thread(target=sargento, args=(clientes, filas, 0))
barbeiro = threading.Thread(target=corteBarbeiro, args=("Zero", filas[0] + filas[1] + filas[2])) #PRECISA FAZER O barbeiro OLHAR AS FILAS NA ORDEM, E TAMBEM INSERIR NA ORDEM CERTA
tainha.start()
barbeiro.start()