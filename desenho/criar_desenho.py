
import json
from pathlib import Path

from formas import transformar_em_retangulos


# Raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretórios
ASSETS_DIR = BASE_DIR / "assets"
DOCS_DIR = BASE_DIR / "docs"

DOCS_DIR.mkdir(exist_ok=True)

# Configurações
LARGURA = 900
ALTURA = 900

FUNDO = "#000000"


def gerar_desenho():

    cenas = []

    # ==================================
    # CAMADA 1 - SÍMBOLO EXTERNO
    # ==================================

    print("Preparando símbolo externo...")

    fundo = transformar_em_retangulos(
        caminho=ASSETS_DIR / "simbolo" / "fundo.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2,
        largura_maxima=590,
        altura_maxima=590,
        max_pixels=180
    )

    fundo = ordenar_retangulos(
        fundo,
        "circular",
        LARGURA / 2,
        ALTURA / 2
    )

    cenas.append({
        "nome": "simbolo_fundo",
        "modo": "circular",
        "retangulos": fundo
    })


    # ==================================
    # CAMADA 2 - SÍMBOLO CENTRAL
    # ==================================

    print("Preparando símbolo central...")

    centro = transformar_em_retangulos(
        caminho=ASSETS_DIR / "simbolo" / "centro.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2,
        largura_maxima=590,
        altura_maxima=590,
        max_pixels=180
    )

    centro = ordenar_retangulos(
        centro,
        "horizontal"
    )

    cenas.append({
        "nome": "simbolo_centro",
        "modo": "horizontal",
        "retangulos": centro
    })


    # ==================================
    # CAMADA 3 - PERSONAGEM
    # ==================================

    print("Preparando personagem...")

    personagem = transformar_em_retangulos(
        caminho=ASSETS_DIR / "personagem.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2 + 15,
        largura_maxima=245,
        altura_maxima=330,
        max_pixels=180
    )

    personagem = ordenar_retangulos(
        personagem,
        "baixo_para_cima"
    )

    cenas.append({
        "nome": "personagem",
        "modo": "baixo_para_cima",
        "retangulos": personagem
    })


    # ==================================
    # EXPORTAÇÃO
    # ==================================

    desenho = {
        "largura": LARGURA,
        "altura": ALTURA,
        "fundo": FUNDO,
        "cenas": cenas
    }

    destino = DOCS_DIR / "desenho.json"

    with open(destino, "w", encoding="utf-8") as arquivo:

        json.dump(
            desenho,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    print("\nRitual preparado!")

    for cena in cenas:

        print(
            f"{cena['nome']}: "
            f"{len(cena['retangulos'])} retângulos"
        )



if __name__ == "__main__":
    gerar_desenho()
    
elif modo == "horizontal":
    def chave(r):
        return (
            r["y"] + r["h"] / 2,
            r["x"] + r["w"] / 2
        )