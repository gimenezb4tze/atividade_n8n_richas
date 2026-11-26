from pathlib import Path
import turtle
from .gravador import Gravador
from formas import desenhar_imagem


SAIDA = Path(__file__).resolve().parent.parent / "docs" / "desenho.json"


# Configuração da janela
tela = turtle.Screen()
tela.setup(width=900, height=900)
tela.bgcolor("black")
tela.title("Meu desenho")

# Desativa atualizações automáticas
tela.tracer(0)

caneta = turtle.Turtle()
caneta.speed(0)
caneta.hideturtle()
caneta.penup()

# 1. Desenha o símbolo no centro
largura, altura = desenhar_imagem(
    caneta,
    "assets/simbolo.png",
    -300,
    300,
    tamanho_pixel=4,
    largura_maxima=150,
    remover_preto=True
)

tela.update()

# Aguarda antes de revelar o personagem
turtle.time.sleep(1)

# 2. Desenha o personagem no centro
largura_personagem, altura_personagem = desenhar_imagem(
    caneta,
    "assets/personagem.png",
    -100,
    150,
    tamanho_pixel=4,
    largura_maxima=50
)

tela.update()

turtle.done()
