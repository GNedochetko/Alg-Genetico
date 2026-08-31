import random

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, MUTATION_RATE, DELTA_COORDENADA, DELTA_COR, ALPHA_MAX, ALPHA_MIN, DELTA_ALPHA
from src.individuo import Individuo, Triangulo

def limitar(valor: int, minimo: int, maximo: int) -> int:
    return max(minimo, min(valor, maximo))


def mutar_valor(valor: int, delta: int, minimo: int, maximo: int) -> int:
    novo_valor = valor + random.randint(-delta, delta)
    return limitar(novo_valor, minimo, maximo)


def calcular_centro(triangulo: Triangulo) -> tuple[float, float]:
    centro_x = (triangulo.x1 + triangulo.x2 + triangulo.x3) / 3
    centro_y = (triangulo.y1 + triangulo.y2 + triangulo.y3) / 3
    return centro_x, centro_y


def mutar_posicao(triangulo: Triangulo) -> None:
    # Move o triangulo inteiro sem alterar seu formato.
    deslocamento_x = random.randint(-DELTA_COORDENADA, DELTA_COORDENADA)
    deslocamento_y = random.randint(-DELTA_COORDENADA, DELTA_COORDENADA)

    triangulo.x1 = limitar(triangulo.x1 + deslocamento_x, 0, IMAGE_WIDTH - 1)
    triangulo.y1 = limitar(triangulo.y1 + deslocamento_y, 0, IMAGE_HEIGHT - 1)
    triangulo.x2 = limitar(triangulo.x2 + deslocamento_x, 0, IMAGE_WIDTH - 1)
    triangulo.y2 = limitar(triangulo.y2 + deslocamento_y, 0, IMAGE_HEIGHT - 1)
    triangulo.x3 = limitar(triangulo.x3 + deslocamento_x, 0, IMAGE_WIDTH - 1)
    triangulo.y3 = limitar(triangulo.y3 + deslocamento_y, 0, IMAGE_HEIGHT - 1)


def mutar_formato(triangulo: Triangulo) -> None:
    # Move apenas um vertice, alterando o formato do triangulo.
    vertice = random.randint(1, 3)

    if vertice == 1:
        triangulo.x1 = mutar_valor(triangulo.x1, DELTA_COORDENADA, 0, IMAGE_WIDTH - 1)
        triangulo.y1 = mutar_valor(triangulo.y1, DELTA_COORDENADA, 0, IMAGE_HEIGHT - 1)
    elif vertice == 2:
        triangulo.x2 = mutar_valor(triangulo.x2, DELTA_COORDENADA, 0, IMAGE_WIDTH - 1)
        triangulo.y2 = mutar_valor(triangulo.y2, DELTA_COORDENADA, 0, IMAGE_HEIGHT - 1)
    else:
        triangulo.x3 = mutar_valor(triangulo.x3, DELTA_COORDENADA, 0, IMAGE_WIDTH - 1)
        triangulo.y3 = mutar_valor(triangulo.y3, DELTA_COORDENADA, 0, IMAGE_HEIGHT - 1)


def mutar_cor(triangulo: Triangulo) -> None:
    # Ajusta a cor do triangulo como uma unidade, preservando mudancas graduais.
    triangulo.r = mutar_valor(triangulo.r, DELTA_COR, 0, 255)
    triangulo.g = mutar_valor(triangulo.g, DELTA_COR, 0, 255)
    triangulo.b = mutar_valor(triangulo.b, DELTA_COR, 0, 255)


def mutar_transparencia(triangulo: Triangulo) -> None:
    # Ajusta a transparencia sem permitir triangulos totalmente opacos.
    triangulo.alpha = mutar_valor(triangulo.alpha, DELTA_ALPHA, ALPHA_MIN, ALPHA_MAX)


def mutar_escala(triangulo: Triangulo) -> None:
    # Encolhe ou expande o triangulo em torno do proprio centro.
    centro_x, centro_y = calcular_centro(triangulo)
    fator_escala = random.uniform(0.75, 1.25)

    triangulo.x1 = limitar(round(centro_x + (triangulo.x1 - centro_x) * fator_escala), 0, IMAGE_WIDTH - 1)
    triangulo.y1 = limitar(round(centro_y + (triangulo.y1 - centro_y) * fator_escala), 0, IMAGE_HEIGHT - 1)
    triangulo.x2 = limitar(round(centro_x + (triangulo.x2 - centro_x) * fator_escala), 0, IMAGE_WIDTH - 1)
    triangulo.y2 = limitar(round(centro_y + (triangulo.y2 - centro_y) * fator_escala), 0, IMAGE_HEIGHT - 1)
    triangulo.x3 = limitar(round(centro_x + (triangulo.x3 - centro_x) * fator_escala), 0, IMAGE_WIDTH - 1)
    triangulo.y3 = limitar(round(centro_y + (triangulo.y3 - centro_y) * fator_escala), 0, IMAGE_HEIGHT - 1)


def mutar_camada(individuo: Individuo) -> None:
    if len(individuo.triangulos) < 2:
        return

    # Troca dois triangulos de posicao no vetor, alterando a ordem em que eles sao desenhados.
    indice1 = random.randint(0, len(individuo.triangulos) - 1)
    indice2 = random.randint(0, len(individuo.triangulos) - 1)

    individuo.triangulos[indice1], individuo.triangulos[indice2] = (
        individuo.triangulos[indice2],
        individuo.triangulos[indice1],
    )


def mutar(individuo: Individuo) -> Individuo:
    for triangulo in individuo.triangulos:
        if random.random() < MUTATION_RATE:
            # Escolhe uma mutacao por triangulo
            operacao = random.choice([
                mutar_posicao,
                mutar_formato,
                mutar_cor,
                mutar_transparencia,
                mutar_escala,
            ])
            operacao(triangulo)

    # Muta a camada de um triangulo, mudando se ele fica mais ao fundo ou mais em cima.
    if random.random() < MUTATION_RATE:
        mutar_camada(individuo)

    # Como o individuo mudou, o fitness antigo deixa de representar essa nova imagem.
    individuo.fitness = None
    return individuo
