import random
import copy

from src.individuo import Individuo


def crossover_uniforme(pai1: Individuo, pai2: Individuo) -> Individuo:
    triangulos_filho = []

    # Para cada camada, escolhe aleatoriamente o triangulo do pai1 ou do pai2.
    for triangulo_pai1, triangulo_pai2 in zip(pai1.triangulos, pai2.triangulos):
        if random.random() < 0.5:
            triangulos_filho.append(copy.deepcopy(triangulo_pai1))
        else:
            triangulos_filho.append(copy.deepcopy(triangulo_pai2))

    return Individuo(triangulos=triangulos_filho)


def crossover_por_ponto(pai1: Individuo, pai2: Individuo) -> Individuo:
    return crossover_uniforme(pai1, pai2)
