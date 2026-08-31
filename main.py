from pathlib import Path
from time import perf_counter

from src.config import RESULTS_DIR
from src.genetico import criar_gif_evolucao, executar_algoritmo_genetico
from src.renderizacao import renderizar_individuo


def main():
    inicio = perf_counter()

    melhor_individuo = executar_algoritmo_genetico()

    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

    imagem_final = renderizar_individuo(melhor_individuo)
    caminho_resultado = Path(RESULTS_DIR) / "melhor_individuo.png"
    imagem_final.save(caminho_resultado)

    caminho_gif = criar_gif_evolucao()
    tempo_total = perf_counter() - inicio

    print(f"Imagem final salva em: {caminho_resultado}")
    if caminho_gif is not None:
        print(f"GIF da evolucao salvo em: {caminho_gif}")
    print(f"Fitness final: {melhor_individuo.fitness}")
    print(f"Tempo total: {tempo_total:.4f} segundos")


if __name__ == "__main__":
    main()
