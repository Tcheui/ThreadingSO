import logging
import threading
import time
import random

def random_duracao(categoria):
    """Escolhe uma duração aleatória, dependendo do tipo de patente do militar """
    if (categoria == 'tenente'):
        return random.randint(1, 3)
    if (categoria == 'sargento'):
        return random.randint(4, 6)
    if (categoria == 'cabo'):
        return random.randint(2, 4)

def geraCliente_3filas(numeroClientes):
    """ Gera novos clientes. Cada cliente é na verdade um dicionário"""
    categorias = ['tenente', 'sargento', 'oficial']
    tenentes = []
    sargentos = []
    oficiais = []

    for _ in range(numeroClientes):
        cliente = {}
        cliente['categoria'] = random.choice(categorias)
        cliente['tempo_corte'] = int(random_duracao(cliente['categoria']))
        if cliente['categoria'] == 'tenente':
            tenentes.append(cliente)
        elif cliente['categoria'] == 'sargento':
            sargentos.append(cliente)
        else:
            oficiais.append(cliente)

    return tenentes, sargentos, oficiais

def geraCliente(numeroClientes):
    """ Gera novos clientes. Cada cliente é na verdade um dicionário """
    categorias = ['tenente', 'sargento', 'cabo']
    clientes = []
    global ID

    for _ in range(numeroClientes):
        cliente = {}
        cliente ['ID'] = ID
        cliente['categoria'] = random.choice(categorias)
        cliente['tempo_corte'] = int(random_duracao(cliente['categoria']))
        clientes.append(cliente)
        ID += 1

    return clientes


def ordenaPrioridade(fila):
    """ Organiza a fila de cadeiras por prioridade de patente"""

    ordem_categorias = {'tenente': 0, 'sargento': 1, 'cabo': 2}

    def chave_de_ordenacao(dicionario):
        categoria = dicionario['categoria']
        return ordem_categorias.get(categoria, float('inf'))

    fila.sort(key=chave_de_ordenacao)


def sargento(fila_cadeiras, cochilo):
    """ Tenta adicionar um cliente a fila sempre que parar de cochilar """
    cont = 0
    cont_consecutivas = 0
    while True:
        with semaphore:
            if (len(fila_cadeiras) >= 20):
                logging.info("Tudo lotado! volto mais tarde zzz /Tainha ")
                time.sleep(cochilo)
                cont_consecutivas += 1
            else:
                cliente = geraCliente(1)
                cont += 1
                # Área de seção crítica
                fila_cadeiras.extend(cliente)
                logging.info("Adicionei um cara viu?  /Sargento Tainha")
                time.sleep(cochilo)
                cont_consecutivas = 0
        
        # Verifica as condições de parada do sargento. Se entrarem 1000 registros ou fila cheia três vezes consecutivas.
        if cont >= 1000 or cont_consecutivas == 3:
            logging.info("Sargento tainha indo embora!")
            break        

def barbeiro(fila_cadeiras, barbeiro):
    """ Dá a informação do que está fazendo todos os segundos."""
    while True:
        with semaphore:
            if len(fila_cadeiras) == 0:
                logging.info("Barbearia vazia! %s está descansando zzz", barbeiro)
                time.sleep(1)
            else:
                ordenaPrioridade(fila_cadeiras)
                # for i in fila_cadeiras:
                #     logging.info("elementos da fila: %s", i)
                cliente_atual = fila_cadeiras.pop(0)
                atendecliente(cliente_atual, barbeiro)

def atendecliente(cliente, barbeiro):
    """ Simula o tempo de corte. """
    tempo_restante = int(cliente["tempo_corte"])
    while tempo_restante > 0:
        logging.info("Barbeiro %s cortando... Faltam %d segundos",barbeiro,tempo_restante)
        time.sleep(1)  # Aguarda 1 segundo
        tempo_restante -= 1
    logging.info(f"Corte de cabelo do {cliente['categoria']} concluído.")

# MAIN

# Fila de cadeiras da barbearia
fila_cadeiras = []
ID = 0
semaphore = threading.Semaphore(4)

# Formatação
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

# Pergunta ao usuário
cochilo_tainha = int(input("Digite o tempo de Cochilo do Sargento Tainha [ENTRE 1 E 5 SEGUNDOS]: "))

# Início das threads
Sargento_tainha = threading.Thread(target=sargento, args=(fila_cadeiras, cochilo_tainha))
RecrutaZero = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Zero"))
Dentinho = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Dentinho"))
Otto = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Otto"))

# Execução delas
Dentinho.start()
Sargento_tainha.start()
RecrutaZero.start()
Otto.start()