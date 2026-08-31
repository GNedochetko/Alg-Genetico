from PIL import Image
import numpy as np

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT, TARGET_IMAGE
from src.individuo import Individuo
from src.renderizacao import renderizar_individuo


def carregar_imagem_alvo() -> Image.Image:
    imagem = Image.open(TARGET_IMAGE)
    imagem = imagem.convert("RGB")
    imagem = imagem.resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    return imagem


def calcular_fitness(individuo: Individuo, imagem_alvo: Image.Image) -> float:
    #Primeiro renderiza a imagem do individuo para comparar com a imagem-alvo
    imagem_individuo = renderizar_individuo(individuo).convert("RGB")

    #Transforma as imagens em matrizes NumPy
    alvo_array = np.array(imagem_alvo, dtype=np.int32)
    individuo_array = np.array(imagem_individuo, dtype=np.int32)

    #Primeiro ele calcula a diferença real da imagem-alvo para a imagem do individuo pixel a pixel
    diferenca = alvo_array - individuo_array
    # Media das diferencas absolutas entre todos os pixels e canais RGB.
    erro = np.mean(np.abs(diferenca))

    individuo.fitness = erro

    return erro
