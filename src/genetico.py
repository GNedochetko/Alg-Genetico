from pathlib import Path

from PIL import Image

from src.config import NUM_GENERATIONS, RESULTS_DIR
from src.crossover import crossover_uniforme
from src.fitness import carregar_imagem_alvo, calcular_fitness
from src.individuo import Individuo
from src.mutacao import mutar
from src.populacao import criar_populacao
from src.renderizacao import renderizar_individuo
from src.selecao import selecao_torneio


def avaliar_populacao(populacao: list[Individuo], imagem_alvo) -> None:
    for individuo in populacao:
        calcular_fitness(individuo, imagem_alvo)


def obter_melhor_individuo(populacao: list[Individuo]) -> Individuo:
    return min(populacao, key=lambda individuo: individuo.fitness)


def preparar_pasta_geracoes() -> Path:
    pasta_geracoes = Path(RESULTS_DIR) / "geracoes"
    pasta_geracoes.mkdir(parents=True, exist_ok=True)

    # Remove frames antigos para o novo GIF usar apenas imagens da execucao atual.
    for arquivo in pasta_geracoes.glob("geracao_*.png"):
        arquivo.unlink()

    return pasta_geracoes


def salvar_frame_geracao(individuo: Individuo, geracao: int, pasta_geracoes: Path) -> None:
    imagem = renderizar_individuo(individuo)
    imagem.save(pasta_geracoes / f"geracao_{geracao:05d}.png")


def criar_gif_evolucao(duracao_frame: int = 150) -> Path | None:
    pasta_geracoes = Path(RESULTS_DIR) / "geracoes"
    arquivos = sorted(pasta_geracoes.glob("geracao_*.png"))

    if not arquivos:
        return None

    imagens = [Image.open(arquivo).convert("RGB") for arquivo in arquivos]
    caminho_gif = Path(RESULTS_DIR) / "evolucao.gif"

    imagens[0].save(
        caminho_gif,
        save_all=True,
        append_images=imagens[1:],
        duration=duracao_frame,
        loop=0,
    )

    for imagem in imagens:
        imagem.close()

    # Depois que o GIF foi criado, remove os frames individuais das geracoes.
    for arquivo in arquivos:
        arquivo.unlink()

    return caminho_gif


def criar_nova_geracao(
    populacao: list[Individuo],
    imagem_alvo,
) -> list[Individuo]:
    nova_populacao = []

    for pai in populacao:
        # Gera um filho a partir do pai atual e de outro individuo selecionado por torneio.
        pai2 = selecao_torneio(populacao)

        filho = crossover_uniforme(pai, pai2)
        filho = mutar(filho)
        calcular_fitness(filho, imagem_alvo)

        # Modelo pai-filho: o filho so substitui o pai se tiver fitness melhor.
        if filho.fitness < pai.fitness:
            nova_populacao.append(filho)
        else:
            nova_populacao.append(pai.copiar())

    return nova_populacao


def executar_algoritmo_genetico() -> Individuo:
    imagem_alvo = carregar_imagem_alvo()
    populacao = criar_populacao()
    pasta_geracoes = preparar_pasta_geracoes()

    avaliar_populacao(populacao, imagem_alvo)
    melhor_individuo = obter_melhor_individuo(populacao).copiar()
    salvar_frame_geracao(melhor_individuo, 0, pasta_geracoes)

    for geracao in range(NUM_GENERATIONS):
        populacao = criar_nova_geracao(populacao, imagem_alvo)

        melhor_da_geracao = obter_melhor_individuo(populacao)

        if melhor_da_geracao.fitness < melhor_individuo.fitness:
            melhor_individuo = melhor_da_geracao.copiar()
            salvar_frame_geracao(melhor_individuo, geracao + 1, pasta_geracoes)

        print(
            f"Geracao {geracao + 1}: "
            f"melhor fitness = {melhor_individuo.fitness}"
        )

    return melhor_individuo
