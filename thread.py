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

def insere_fila(filas, tipo, cochilo): #(lista, inteiro, inteiro), é dado o tipo de cliente e o tempo de cochilo após inseri-lo. 1 == oficial, 2 == sargento, 3 == cabo
    if((len(filas[0]) + len(filas[1]) + len(filas[2])) <= 20):
        logging.info("Sargento Tainha: inserindo", tipo)
        duracao = random_duracao(tipo)
        filas[tipo - 1].append(duracao) ## 0 é oficial, 1 é sargento, 2 é cabo
        time.sleep(cochilo)
        logging.info("Sargento Tainha: acordando")
        return 0 #se 0 for retornado, inserção completa
    elif(tipo == 0):
        logging.info("Pausa!")
        time.sleep(cochilo)
        return 1 #se retornar 1, inserção pausada
    else:
        logging.info("Fila cheia!")
        time.sleep(cochilo)
        return 2

def corteBarbeiro(nome, fila):
    logging.info("Barbeiro ", nome, ": cortando")
    clienteAtual = fila.pop() #cada cliente é representado por um inteiro (duração do corte)
    time.sleep(clienteAtual)
    logging.info("Barbeiro ", nome, ": livre")

#main
clientes = []
for i in range(10):
    clientes.append(random.randint(1, 3))
print(clientes)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

filas = [[], [], []]
cont = 0
while(cont < 3): 
    sargento = threading.Thread(target=insere_fila, args=(filas, clientes.pop(), random.randint(1, 5)))
    sargento.start()

    barbeiro = threading.Thread(target=corteBarbeiro, args=("Zero", filas[0]))
    barbeiro.start()
