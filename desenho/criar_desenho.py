
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

    print("Preparando o símbolo...")

    simbolo = transformar_em_retangulos(
        caminho=ASSETS_DIR / "simbolo.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2,
        largura_maxima=590,
        altura_maxima=590
    )

    print("Preparando o personagem...")

    personagem = transformar_em_retangulos(
        caminho=ASSETS_DIR / "personagem.png",
        centro_x=LARGURA / 2,
        centro_y=ALTURA / 2 + 15,
        largura_maxima=245,
        altura_maxima=330
    )

    desenho = {
        "largura": LARGURA,
        "altura": ALTURA,
        "fundo": FUNDO,

        "cenas": [
            {
                "nome": "simbolo",
                "retangulos": simbolo
            },
            {
                "nome": "personagem",
                "retangulos": personagem
            }
        ]
    }

    destino = DOCS_DIR / "desenho.json"

    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(
            desenho,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    print("\nDesenho gerado com sucesso!")
    print(f"Símbolo: {len(simbolo)} retângulos")
    print(f"Personagem: {len(personagem)} retângulos")
    print(f"Arquivo: {destino}")


if __name__ == "__main__":
    gerar_desenho()
