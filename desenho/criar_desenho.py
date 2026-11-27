
import json
import math
from pathlib import Path

from formas import transformar_em_retangulos


# ========================================
# CONFIGURAÇÕES
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
DOCS_DIR = BASE_DIR / "docs"

DOCS_DIR.mkdir(exist_ok=True)

LARGURA = 900
ALTURA = 900

FUNDO = "#000000"


# ========================================
# ORDENAÇÃO DOS RETÂNGULOS
# ========================================

def ordenar_retangulos(retangulos, modo,
                       centro_x=450, centro_y=450):

    if modo == "circular":

        def chave(r):
            x = r["x"] + r["w"] / 2 - centro_x
            y = r["y"] + r["h"] / 2 - centro_y

            return math.atan2(x, -y) % (2 * math.pi)

    elif modo == "horizontal":

        def chave(r):
            return (
                r["y"] + r["h"] / 2,
                r["x"] + r["w"] / 2
            )

    elif modo == "baixo_para_cima":

        def chave(r):
            return -(r["y"] + r["h"] / 2)

    else:
        return retangulos

    return sorted(retangulos, key=chave)


# ========================================
# PROCESSAMENTO DE UMA CAMADA
# ========================================

def processar_camada(caminho, modo, recortar=False):

    retangulos = transformar_em_retangulos(
        caminho=caminho,
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2,
        largura_maxima=590,
        altura_maxima=590,
        max_pixels=180,
        recortar=recortar
    )

    return ordenar_retangulos(
        retangulos,
        modo,
        LARGURA / 2,
        ALTURA / 2
    )


# ========================================
# GERAÇÃO DO DESENHO
# ========================================

def gerar_desenho():

    cenas = []

    # ------------------------------------
    # 1. SÍMBOLO EXTERNO
    # ------------------------------------

    print("Preparando símbolo externo...")

    fundo = processar_camada(
        ASSETS_DIR / "simbolo" / "fundo.png",
        "circular"
    )

    cenas.append({
        "nome": "simbolo_fundo",
        "modo": "circular",
        "retangulos": fundo
    })

    # ------------------------------------
    # 2. SÍMBOLO CENTRAL
    # ------------------------------------

    print("Preparando símbolo central...")

    centro = processar_camada(
        ASSETS_DIR / "simbolo" / "centro.png",
        "horizontal"
    )

    cenas.append({
        "nome": "simbolo_centro",
        "modo": "horizontal",
        "retangulos": centro
    })

    # ------------------------------------
    # 3. PERSONAGEM
    # ------------------------------------

    print("Preparando personagem...")

    personagem = transformar_em_retangulos(
        caminho=ASSETS_DIR / "personagem.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2 + 15,
        largura_maxima=245,
        altura_maxima=330,
        max_pixels=180,
        recortar=True
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

    # ------------------------------------
    # 4. EXPORTAÇÃO
    # ------------------------------------

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

    print("\nRitual preparado com sucesso!")

    for cena in cenas:
        print(
            f"{cena['nome']}: "
            f"{len(cena['retangulos'])} retângulos"
        )


if __name__ == "__main__":
    gerar_desenho()
