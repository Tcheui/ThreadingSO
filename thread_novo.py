import logging
import threading
import time
import random


# retorna um valor de duração do corte com base no tipo de cliente
def random_duracao(categoria):
    if (categoria == 'tenente'):
        return random.randint(1, 3)
    if (categoria == 'sargento'):
        return random.randint(4, 6)
    if (categoria == 'oficial'):
        return random.randint(2, 4)


def geraCliente(numeroClientes):
    categorias = ['tenente', 'sargento', 'oficial']
    clientes = []

    for _ in range(numeroClientes):
        cliente = {}
        cliente['categoria'] = random.choice(categorias)
        cliente['tempo_corte'] = int(random_duracao(cliente['categoria']))
        clientes.append(cliente)

    return clientes


def ordenaPrioridade(fila):
    """ordena a fila por prioridade"""
    categorias = {'tenente': 0, 'sargento': 1, 'oficial': 2}
    fila_ordenada = sorted(
        fila, key=lambda cliente: categorias.get(cliente['categoria'], 3))
    return fila_ordenada


def sargento(fila_cadeiras, cochilo):
    """ Tenta adicionar um cliente a fila sempre que parar de cochilar """
    while True:
        if (len(fila_cadeiras) >= 20):
            time.sleep(cochilo)
        else:
            cliente = geraCliente(1)
            fila_cadeiras.append(cliente)
            logging.info("Adicionei um cara viu?  /Sargento Tainha")
            time.sleep(cochilo)


def barbeiro(fila_cadeiras):
    while True:
        if (len(fila_cadeiras) == 0):
            logging.info("Barbearia vazia! posso descansar zzz")
            time.sleep(1)
        else:
            # fila_cadeiras = ordenaPrioridade(fila_cadeiras)
            cliente_atual = fila_cadeiras.pop(0)[0]
            atendeCliente(cliente_atual)


def atendeCliente(cliente):

    tempo_restante = int(cliente["tempo_corte"])
    while tempo_restante > 0:
        logging.info("Barbeiro cortando... Faltam %d segundos", tempo_restante)
        time.sleep(1)  # Aguarda 1 segundo
        tempo_restante -= 1

    logging.info(f"Corte de cabelo do {cliente['categoria']} concluído.")

# MAIN


# Fila de cadeiras da barbearia
fila_cadeiras = []

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
cochilo_tainha = int(
    input("Digite o tempo de Cochilo do Sargento Tainha [ENTRE 1 E 5 SEGUNDOS]: "))
Sargento_tainha = threading.Thread(
    target=sargento, args=(fila_cadeiras, cochilo_tainha))
RecrutaZero = threading.Thread(target=barbeiro, args=(fila_cadeiras,))

Sargento_tainha.start()
RecrutaZero.start()
