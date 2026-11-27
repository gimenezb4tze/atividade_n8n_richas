
from PIL import Image
from collections import deque


def remover_fundo_preto(imagem, tolerancia=12):
    """
    Remove pixels escuros conectados às bordas.
    Preserva contornos pretos que estejam dentro da imagem.
    """

    imagem = imagem.convert("RGBA")
    largura, altura = imagem.size
    pixels = imagem.load()

    visitados = bytearray(largura * altura)
    fila = deque()

    def eh_fundo(x, y):
        r, g, b, a = pixels[x, y]
        return a > 0 and max(r, g, b) <= tolerancia

    # Procura pixels pretos nas bordas
    for x in range(largura):
        for y in (0, altura - 1):
            if eh_fundo(x, y):
                fila.append((x, y))

    for y in range(altura):
        for x in (0, largura - 1):
            if eh_fundo(x, y):
                fila.append((x, y))

    # Percorre apenas regiões conectadas ao fundo
    while fila:
        x, y = fila.popleft()
        indice = y * largura + x

        if visitados[indice]:
            continue

        visitados[indice] = 1
        pixels[x, y] = (0, 0, 0, 0)

        vizinhos = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for nx, ny in vizinhos:
            if 0 <= nx < largura and 0 <= ny < altura:
                if not visitados[ny * largura + nx] and eh_fundo(nx, ny):
                    fila.append((nx, ny))

    return imagem



def carregar_imagem(caminho, recortar=True):
    """Abre e prepara uma imagem."""

    imagem = Image.open(caminho).convert("RGBA")

    imagem = remover_fundo_preto(imagem)

    # Recorta apenas quando solicitado
    if recortar:
        caixa = imagem.getbbox()

        if caixa:
            imagem = imagem.crop(caixa)

    return imagem



def transformar_em_retangulos(
    caminho,
    centro_x,
    centro_y,
    largura_maxima,
    altura_maxima,
    max_pixels=180,
    recortar=True
):
    """
    Converte uma imagem em pequenos retângulos.
    Agrupa pixels consecutivos da mesma cor.
    """

    imagem = carregar_imagem(caminho, recortar=recortar)

    # Reduz a imagem preservando o pixel art
    imagem.thumbnail(
        (max_pixels, max_pixels),
        Image.Resampling.NEAREST
    )

    largura, altura = imagem.size

    # Calcula escala para posicionamento no Canvas
    escala = min(
        largura_maxima / largura,
        altura_maxima / altura
    )

    largura_final = largura * escala
    altura_final = altura * escala

    inicio_x = centro_x - largura_final / 2
    inicio_y = centro_y - altura_final / 2

    pixels = imagem.load()
    retangulos = []

    # Percorre cada linha da imagem
    for y in range(altura):
        x = 0

        while x < largura:
            cor = pixels[x, y]

            # Ignora transparência
            if cor[3] == 0:
                x += 1
                continue

            inicio = x

            # Agrupa pixels consecutivos da mesma cor
            while x < largura and pixels[x, y] == cor:
                x += 1

            quantidade = x - inicio

            r, g, b, a = cor

            cor_css = (
                f"rgba({r},{g},{b},{a / 255:.3f})"
            )

            retangulos.append({
                "x": round(inicio_x + inicio * escala, 2),
                "y": round(inicio_y + y * escala, 2),
                "w": round(quantidade * escala, 2),
                "h": round(escala, 2),
                "cor": cor_css
            })

    return retangulos
