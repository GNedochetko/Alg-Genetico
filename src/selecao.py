import random

from src.config import TOURNAMENT_SIZE
from src.individuo import Individuo

def selecao_torneio(populacao: list[Individuo]) -> Individuo:
    #Escolhe uma subpopulacao do tamanho escolhido para o torneio
    competidores = random.sample(populacao, TOURNAMENT_SIZE)

    #Escolhe dentre essa subpopulacao, o individuo com menor fitness
    vencedor = min(competidores, key=lambda individuo: individuo.fitness)
    return vencedor.copiar()