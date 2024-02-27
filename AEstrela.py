from pyamaze import maze, agent
from queue import PriorityQueue

#f_score = g_score + h_score
#f_score = custo do caminho + heuristica

#g_score = passsos dados até a celula
#h_score = distancia da celula até o destino

destino = (1, 1)

def h_score(celula, destino):
  linhaC = celula[0]
  colunaC = celula[1]
  linhaD = destino[0]
  colunaD = destino[1]
  return abs(linhaC - linhaD) + abs(colunaC - colunaD)

def aestrela(labirinto):
  #cria um dicionario com todas as celulas do labirinto e inicializa o f_score de todas as celulas com infinito
  f_score = {celula: float("inf") for celula in labirinto.grid}
  g_score = {}
  celula_inicial = (labirinto.rows, labirinto.cols)
  #calcula o g_score e o f_score da celula inicial
  g_score[celula_inicial] = 0
  f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial, destino)

  #cria uma fila de prioridade e adiciona a celula inicial
  fila = PriorityQueue()
  item = (f_score[celula_inicial], h_score(celula_inicial, destino), celula_inicial)
  fila.put(item)

  caminho = {}
  while not fila.empty():
    celula = fila.get()[2]

    if celula == destino:
      break

    for direcao in "NSEW":
      if labirinto.maze_map[celula][direcao] == 1:
        linha_celula = celula[0]
        coluna_celula = celula[1]
        if direcao == "N":
          proxima_celula = (linha_celula - 1, coluna_celula)
        elif direcao == "S":
          proxima_celula = (linha_celula + 1, coluna_celula)
        elif direcao == "E":
          proxima_celula = (linha_celula, coluna_celula + 1)
        elif direcao == "W":
          proxima_celula = (linha_celula, coluna_celula - 1)
        
        novo_g_score = g_score[celula] + 1
        novo_f_score = novo_g_score + h_score(proxima_celula, destino)

        if novo_f_score < f_score[proxima_celula]:
          g_score[proxima_celula] = novo_g_score
          f_score[proxima_celula] = novo_f_score
          item = (novo_f_score, h_score(proxima_celula, destino), proxima_celula)
          fila.put(item)
          caminho[proxima_celula] = celula
  caminho_final = {}
  celula_analisada = destino
  print("Celulas analisadas: ", len(caminho.keys()))
  while celula_analisada != celula_inicial:
    # converte as chaves do dicionario para os valores do dicionario
    # faz o caminho inverso do destino até a celula inicial
    caminho_final[caminho[celula_analisada]] = celula_analisada
    celula_analisada = caminho[celula_analisada]
  return caminho_final

labirinto = maze(50, 50)
labirinto.CreateMaze()

agente = agent(labirinto, filled=True, footprints=True)
caminho = aestrela(labirinto)
labirinto.tracePath({agente: caminho}, delay=10)

print("Total de células: ", len(labirinto.maze_map.keys()))

labirinto.run()