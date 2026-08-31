from src.config import POPULATION_SIZE
from src.individuo import Individuo


def criar_populacao(tamanho: int = POPULATION_SIZE) -> list[Individuo]:
    populacao = []

    for _ in range(tamanho):
        individuo = Individuo.aleatorio()
        populacao.append(individuo)

    return populacao