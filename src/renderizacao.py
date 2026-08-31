from PIL import Image, ImageDraw

from src.config import IMAGE_WIDTH, IMAGE_HEIGHT
from src.individuo import Individuo


def renderizar_individuo(individuo: Individuo) -> Image.Image:
    # Cria uma nova imagem RGB com fundo branco opaco.
    imagem = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))
    # Cria um objeto que desenha cores RGBA misturando corretamente o alpha com o fundo.
    desenho = ImageDraw.Draw(imagem, "RGBA")

    #Looping que desenha todos os triangulos do individuo no desenho
    for triangulo in individuo.triangulos:
        #coordenadas na imagem
        pontos = [
            (triangulo.x1, triangulo.y1),
            (triangulo.x2, triangulo.y2),
            (triangulo.x3, triangulo.y3),
        ]

        #cor pintada na imagem
        cor = (
            triangulo.r,
            triangulo.g,
            triangulo.b,
            triangulo.alpha,
        )

        #funcao principal do Pillow que desenha efetivamente o triangulo com transparencia
        desenho.polygon(pontos, fill=cor)

    return imagem
