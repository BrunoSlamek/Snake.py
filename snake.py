import pygame
import tkinter as tk
import random

"""
Snake_game.py
Desenvolvido com o material do bootcamp IGTI. Desenvolvedor Python.
"""

pygame.init()


class Cube(object):
    """
    Classe utilizada para desenhar os cubos
    Inicializando com o movimento na horizontal
    """
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        """
        Atulizando a movimentação, movimentos baseados no grid da tela
        e não na posição da tela
        """
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        """
        Encontrando a distancia entre cada linha do grid e desenhando o
        retangulo que representa o "cubo" definido. Os valores de +1 e -2
        são utilizados para não desenhar sobre as linhas.
        """
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    """
    Classe para desenhar e movimentar a cobra na tela, a classe recebe
    e constrói a cobra utilizando a classe cubo
    """

    body = []  # Lista que contém o corpo de cubos da cobra
    turns = {}  # dicionário utilizado para movimentar

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    """
    Função para tratar os eventos e movimentos, capturando as teclas
    e verificar se atingiu as bordas da tela
    """

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:

                # Esquerda
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                # Direita
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                # Cima
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                # Baixo
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        """
        Reseta as variáveis(reinicializa)
        """
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addcube(self):
        """
        Adicionando um novo cubo para a cauda e identificando em qual direção
        está se movimentando para adicionar o cubo
        """
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Confirmando a direção para adicionar o cubo
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        """
        Construindo a cobra e confirmando sobre a cabeça para adicionar os olhos
        """
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawgrid(w, rows, surface):
    """
    Desenhando o grid na tela, definindo a distancia entre cada uma das linhas
    e dividindo a tela em pontos para as linhas
    """
    size_btwn = w // rows

    x = 0
    y = 0

    for linhas in range(rows):
        x = x + size_btwn
        y = y + size_btwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawindow(surface):
    """
    Função utilizada para desenhar todos os elementos na tela a cada frame
    variaveis globais que são utilizadas a cada novo frame
    desenhando a cobra na tela, as comidas, as linhas e atualizando os frames
    """
    global rows, width, snake, food

    surface.fill((0, 0, 0))
    snake.draw(surface)
    food.draw(surface)
    drawgrid(width, rows, surface)
    pygame.display.update()


def randomfood(rows, item):
    """
    Adiciona a comida para o jogo
    """
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    """
    Enviando a mensagem após o erro do jogador
    """
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    message_box.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    """
    Função principal para o jogo

    Variaveis globais para o funcionamento do jogo, dimensionando a tela,
    instanciando o objeto clock para ajustar a velocidade do jogo

    Organizando o delay para deixar o jogo um pouco mais lento

    Adicionando o loop principal do jogo
    """
    global width, rows, snake, food

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    food = Cube(randomfood(rows, snake), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].pos == food.pos:
            snake.addcube()
            food = Cube(randomfood(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print("\'Pontuação: \'", len(snake.body))
                message_box("\'Você perdeu!\'", "\'Tente novamente.\'")
                snake.reset((10, 10))
                break

        redrawindow(win)


main()
