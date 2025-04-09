# Configurações iniciais
import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 10

def gerar_comida():
    """Gera uma nova posição para a comida, alinhada à grade de 20px."""
    comida_x = random.randrange(0, largura - tamanho_quadrado, tamanho_quadrado)
    comida_y = random.randrange(0, altura - tamanho_quadrado, tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(comida_x, comida_y):
    """Desenha a comida na tela."""
    pygame.draw.rect(tela, vermelha, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])

def desenhar_cobra(pixels):
    """Desenha a cobra na tela."""
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho_quadrado, tamanho_quadrado])

def desenhar_pontuacao(pontuacao):
    """Exibe a pontuação na tela."""
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, verde)
    tela.blit(texto, [10, 10])

def selecionar_velocidade(tecla, velocidade_atual):
    """Retorna a nova velocidade com base na tecla pressionada, evitando inversão instantânea."""
    vx, vy = velocidade_atual
    if tecla == pygame.K_DOWN and vy == 0:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP and vy == 0:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and vx == 0:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT and vx == 0:
        return -tamanho_quadrado, 0
    return velocidade_atual  # Mantém a mesma direção se a tecla for inválida

def rodar_jogo():
    fim_jogo = False
    x, y = largura // 2, altura // 2
    velocidade_x, velocidade_y = tamanho_quadrado, 0  # Movimento inicial para direita
    tamanho_cobra = 1
    pixels = []
    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preta)

        # Captura eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, (velocidade_x, velocidade_y))

        # Atualizar posição da cobra
        x += velocidade_x
        y += velocidade_y

        # Verificação de colisão com as bordas
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        # Adiciona nova posição da cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # Verifica colisão com o próprio corpo
        if pixels.count([x, y]) > 1:
            fim_jogo = True

        # Desenha os elementos do jogo
        desenhar_comida(comida_x, comida_y)
        desenhar_cobra(pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        # Verifica se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        pygame.display.update()
        relogio.tick(velocidade_jogo)

rodar_jogo()
pygame.quit()
