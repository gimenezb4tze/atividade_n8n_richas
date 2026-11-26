from PIL import Image
import turtle


def desenhar_retangulo(caneta, x, y, largura, altura, cor):
    """Desenha um retângulo preenchido."""
    caneta.penup()
    caneta.goto(x, y)
    caneta.setheading(0)
    caneta.color(cor)
    caneta.begin_fill()

    for distancia, angulo in [
        (largura, 90),
        (altura, 90),
        (largura, 90),
        (altura, 90)
    ]:
        caneta.forward(distancia)
        caneta.right(angulo)

    caneta.end_fill()


def carregar_imagem(caminho, remover_preto=False):
    """Carrega a imagem e prepara seus pixels."""

    imagem = Image.open(caminho).convert("RGBA")

    # Remove o fundo preto do símbolo
    if remover_preto:
        pixels = imagem.load()

        for y in range(imagem.height):
            for x in range(imagem.width):
                r, g, b, a = pixels[x, y]

                if r < 35 and g < 35 and b < 35:
                    pixels[x, y] = (0, 0, 0, 0)

    # Recorta as áreas transparentes
    caixa = imagem.getbbox()

    if caixa:
        imagem = imagem.crop(caixa)

    return imagem


def desenhar_imagem(
    caneta,
    caminho,
    x,
    y,
    tamanho_pixel=4,
    largura_maxima=150,
    remover_preto=False
):
    """Transforma uma imagem em pixels desenhados pelo Turtle."""

    imagem = carregar_imagem(caminho, remover_preto)

    # Redimensiona preservando a proporção
    proporcao = min(
        largura_maxima / imagem.width,
        largura_maxima / imagem.height
    )

    nova_largura = max(1, int(imagem.width * proporcao))
    nova_altura = max(1, int(imagem.height * proporcao))

    imagem = imagem.resize(
        (nova_largura, nova_altura),
        Image.Resampling.NEAREST
    )

    pixels = imagem.load()

    # Desenha os pixels agrupando cores iguais na horizontal
    for linha in range(nova_altura):
        coluna = 0

        while coluna < nova_largura:
            cor = pixels[coluna, linha]

            if cor[3] == 0:
                coluna += 1
                continue

            inicio = coluna

            while (
                coluna < nova_largura
                and pixels[coluna, linha] == cor
            ):
                coluna += 1

            largura = (coluna - inicio) * tamanho_pixel

            cor_rgb = (
                cor[0] / 255,
                cor[1] / 255,
                cor[2] / 255
            )

            desenhar_retangulo(
                caneta,
                x + inicio * tamanho_pixel,
                y - linha * tamanho_pixel,
                largura,
                tamanho_pixel,
                cor_rgb
            )

    return (
        nova_largura * tamanho_pixel,
        nova_altura * tamanho_pixel
    )
