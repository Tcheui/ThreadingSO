import logging
import threading
import time
import random
import datetime

tt_acumulado = [0, 0, 0] # [oficial, sargento, cabo]
tw_acumulado = [0, 0, 0]
numAtendimentos = [0, 0, 0] #mudar para 0, 0, 0. to so testando o relatorio
numClientes = [0, 0, 0]

def random_duracao(categoria):
    """Escolhe uma duração aleatória, dependendo do tipo de patente do militar """
    if (categoria == 'cabo'):
        return random.randint(1, 3)
    if (categoria == 'oficial'):
        return random.randint(4, 6)
    if (categoria == 'sargento'):
        return random.randint(2, 4)
    
def incrementaCategoriaTotal(categoria):
    if(categoria == 'oficial'):
        numClientes[0] += 1
    elif(categoria == 'sargento'):
        numClientes[1] += 1
    else: #se for cabo
        numClientes[2] += 1

def geraCliente_3filas(numeroClientes):
    """ Gera novos clientes. Cada cliente é na verdade um dicionário"""
    categorias = ['oficial', 'sargento', 'cabo']
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
    categorias = ['oficial', 'sargento', 'cabo']
    clientes = []
    global ID

    for _ in range(numeroClientes):
        cliente = {}
        cliente ['ID'] = ID
        cliente['categoria'] = random.choice(categorias)
        incrementaCategoriaTotal(cliente['categoria'])
        cliente['tempo_corte'] = int(random_duracao(cliente['categoria']))
        cliente['tempo_chegada'] = datetime.datetime.now()
        clientes.append(cliente)
        ID += 1

    return clientes


def ordenaPrioridade(fila):
    """ Organiza a fila de cadeiras por prioridade de patente"""

    ordem_categorias = {'oficial': 0, 'sargento': 1, 'cabo': 2}

    def chave_de_ordenacao(dicionario):
        categoria = dicionario['categoria']
        return ordem_categorias.get(categoria, float('inf'))

    fila.sort(key=chave_de_ordenacao)

def arrumaDivisaoPorZero(a, b):
    if(b == 0):
        return float('inf')
    else:
        return a/b

def geraRelatorio(fila_cadeiras, contagem_categorias):
    ttm = [arrumaDivisaoPorZero(tt_acumulado[0], numAtendimentos[0]), 
           arrumaDivisaoPorZero(tt_acumulado[1], numAtendimentos[1]), 
           arrumaDivisaoPorZero(tt_acumulado[2], numAtendimentos[2])] #turnaround médio
    twm = [arrumaDivisaoPorZero(tw_acumulado[0], numAtendimentos[0]), 
           arrumaDivisaoPorZero(tw_acumulado[1], numAtendimentos[1]), 
           arrumaDivisaoPorZero(tw_acumulado[2], numAtendimentos[2])] #waiting médio
    if numAtendimentos[0] > 0 or numAtendimentos[1] > 0 or numAtendimentos[2] > 0:
        logging.info("""Relatório, General!!!
        Ocupação de oficiais: %.0f %%
        Ocupação de sargentos: %.0f %%
        Ocupação de cabos: %.0f %%
        Livre: %.0f %%
        Comprimento médio das filas: %.3f
        Tempo de atendimento médio para oficiais: %.3f
        Tempo de atendimento médio para sargentos: %.3f 
        Tempo de atendimento médio para cabos: %.3f 
        Tempo de espera médio para oficiais: %.3f 
        Tempo de espera médio para sargentos: %.3f 
        Tempo de espera médio para cabos: %.3f
        Número de atendimentos de oficiais: %.0f
        Número de atendimentos de sargentos: %.0f
        Número de atendimentos de cabos: %.0f
        Número de total de oficiais: %.0f
        Número de total de sargentos: %.0f
        Número de total de cabos: %.0f
        """,
          contagem_categorias['oficial']*5,
          contagem_categorias['sargento']*5,
          contagem_categorias['cabo']*5,
          (20 - contagem_categorias['oficial'] - contagem_categorias['sargento'] - contagem_categorias['cabo'])*5,
          (contagem_categorias['oficial'] + contagem_categorias['sargento'] + contagem_categorias['cabo'])/3,
          ttm[0],
          ttm[1],
          ttm[2],
          twm[0],
          twm[1],
          twm[2],
          numAtendimentos[0],
          numAtendimentos[1],
          numAtendimentos[2],
          numClientes[0],
          numClientes[1],
          numClientes[2])
        #print("Tempo médio de espera: ")

def tenente(fila_cadeiras, intervalo = 3): #gerador do relatório
    while True:
        with semaphore:
            contagem_categorias = {'oficial': 0, 'sargento': 0, 'cabo': 0}

            for item in fila_cadeiras:
                if item['categoria'] in contagem_categorias:
                    contagem_categorias[item['categoria']] += 1
                else:
                    print("Erro: categoria não conhecida!")

            geraRelatorio(fila_cadeiras, contagem_categorias)
            time.sleep(intervalo)

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
                logging.info("Adicionei um %s, viu?  /Sargento Tainha", cliente[0]['categoria'])
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
                #logging.info("Barbearia vazia! %s está descansando zzz", barbeiro)
                time.sleep(1)
            else:
                ordenaPrioridade(fila_cadeiras)
                # for i in fila_cadeiras:
                #     logging.info("elementos da fila: %s", i)
                cliente_atual = fila_cadeiras.pop(0)
                atendecliente(cliente_atual, barbeiro)

def incrementaTempo(cliente, tempo_corte):
    if(cliente['categoria'] == 'oficial'):
        numAtendimentos[0] += 1
        tt_acumulado[0] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds()
        tw_acumulado[0] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds() - tempo_corte
    elif(cliente['categoria'] == 'sargento'):
        numAtendimentos[1] += 1
        tt_acumulado[1] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds()
        tw_acumulado[1] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds() - tempo_corte
    else:
        numAtendimentos[2] += 1
        tt_acumulado[2] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds()
        tw_acumulado[2] += (datetime.datetime.now() - cliente["tempo_chegada"]).total_seconds() - tempo_corte


def atendecliente(cliente, barbeiro):
    """ Simula o tempo de corte. """
    tempo_restante = int(cliente["tempo_corte"])
    aux = tempo_restante #auxiliar pra obter o tempo de espera acumulado
    logging.info("Barbeiro %s cortando %s...",barbeiro, cliente['categoria'])
    while tempo_restante > 0:
        #logging.info("Barbeiro %s cortando... Faltam %d segundos",barbeiro,tempo_restante)
        time.sleep(1)  # Aguarda 1 segundo
        tempo_restante -= 1
    logging.info(f"Corte de cabelo do {cliente['categoria']} concluído.")
    incrementaTempo(cliente, aux) #incrementa numero de atendimentos e os tempos acumulados

# MAIN

# Fila de cadeiras da barbearia
fila_cadeiras = []
ID = 0
semaphore = threading.Semaphore(5)

# Formatação
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


# Pergunta ao usuário
cochilo_tainha = int(input("Digite o tempo de Cochilo do Sargento Tainha [ENTRE 1 E 5 SEGUNDOS]: "))

# Início das threads
Sargento_tainha = threading.Thread(target=sargento, args=(fila_cadeiras, cochilo_tainha))
RecrutaZero = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Zero"))
Dentinho = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Dentinho"))
Otto = threading.Thread(target=barbeiro, args=(fila_cadeiras,"Otto"))
Escovinha = threading.Thread(target=tenente, args=(fila_cadeiras, 3))

# Execução delas
Dentinho.start()
Sargento_tainha.start()
RecrutaZero.start()
Otto.start()
Escovinha.start()