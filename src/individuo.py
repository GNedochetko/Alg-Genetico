from dataclasses import dataclass
import random
import copy

from src.config import (
    ALPHA_MAX,
    ALPHA_MIN,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
    NUM_TRIANGLES,
    TRIANGULO_GRANDE_MAX,
    TRIANGULO_GRANDE_MIN,
    TRIANGULO_MEDIO_MAX,
    TRIANGULO_MEDIO_MIN,
    TRIANGULO_PEQUENO_MAX,
    TRIANGULO_PEQUENO_MIN,
)


@dataclass
class Triangulo:
    #coordenadas do triangulo
    x1: int
    y1: int
    x2: int
    y2: int
    x3: int
    y3: int

    #cor do triangulo
    r: int
    g: int
    b: int
    alpha: int

    #criacao de um triangulo de forma aleatoria
    @staticmethod
    def aleatorio():
        centro_x = random.randint(0, IMAGE_WIDTH - 1)
        centro_y = random.randint(0, IMAGE_HEIGHT - 1)
        tamanho = sortear_tamanho_triangulo()

        return Triangulo(
            # Os vertices nascem perto de um centro para gerar triangulos pequenos, medios ou grandes.
            x1=sortear_coordenada_proxima(centro_x, tamanho, 0, IMAGE_WIDTH - 1),
            y1=sortear_coordenada_proxima(centro_y, tamanho, 0, IMAGE_HEIGHT - 1),

            x2=sortear_coordenada_proxima(centro_x, tamanho, 0, IMAGE_WIDTH - 1),
            y2=sortear_coordenada_proxima(centro_y, tamanho, 0, IMAGE_HEIGHT - 1),

            x3=sortear_coordenada_proxima(centro_x, tamanho, 0, IMAGE_WIDTH - 1),
            y3=sortear_coordenada_proxima(centro_y, tamanho, 0, IMAGE_HEIGHT - 1),

            r=random.randint(0, 255),
            g=random.randint(0, 255),
            b=random.randint(0, 255),

            alpha=random.randint(ALPHA_MIN, ALPHA_MAX),
        )


@dataclass
class Individuo:
    #Individuo sera uma lista de triangulos
    triangulos: list[Triangulo]
    #O fitness será o erro da imagem renderizada em relação a imagem-alvo
    fitness: float | None = None

    #Criar um individuo de forma aleatoria
    @staticmethod
    def aleatorio():
        return Individuo(
            triangulos=[
                Triangulo.aleatorio()
                for _ in range(NUM_TRIANGLES)
            ]
        )

    #Copiar um individuo
    def copiar(self):
        return copy.deepcopy(self)


def limitar(valor: int, minimo: int, maximo: int) -> int:
    return max(minimo, min(valor, maximo))


def sortear_coordenada_proxima(centro: int, tamanho: int, minimo: int, maximo: int) -> int:
    return limitar(centro + random.randint(-tamanho, tamanho), minimo, maximo)


def sortear_tamanho_triangulo() -> int:
    chance = random.random()

    # 70% dos triangulos nascem pequenos, ajudando a formar detalhes.
    if chance < 0.70:
        return random.randint(TRIANGULO_PEQUENO_MIN, TRIANGULO_PEQUENO_MAX)

    # 25% nascem medios, cobrindo regioes intermediarias da imagem.
    if chance < 0.95:
        return random.randint(TRIANGULO_MEDIO_MIN, TRIANGULO_MEDIO_MAX)

    # 5% nascem grandes, permitindo formar massas maiores de cor.
    return random.randint(TRIANGULO_GRANDE_MIN, TRIANGULO_GRANDE_MAX)
