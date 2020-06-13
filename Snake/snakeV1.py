import pygame
import random
from copy import deepcopy

#cores
branco = (255,255,255)
verde = (0,255,0)
vermelho = (255,0,0)
preto = (0,0,0)

#tela
largura = 800
altura = 600

#variaveis do jogo
executar = True

velocidade = 10
tamanho = 10
pontos = 0
texto = ""

#cobra
mover_x = 0
mover_y = 0
cobra = [[largura//2,altura//2]]

#comida
comida_pos_x = random.randint(1,((largura-tamanho)//10))*10
comida_pos_y = random.randint(1,((altura-tamanho)//10))*10

pygame.init()

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Snake V1")

relogio = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 20)

while executar:

    texto = "Pontos: " + str(pontos)
    mensagem = fonte.render(texto, True, preto)

    tela.fill(branco)
    tela.blit(mensagem,[0,0])

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executar = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                mover_x = -1*velocidade
                mover_y = 0

            if evento.key == pygame.K_RIGHT:
                mover_x = velocidade
                mover_y = 0

            if evento.key == pygame.K_DOWN:
                mover_x = 0
                mover_y = velocidade

            if evento.key == pygame.K_UP:
                mover_x = 0
                mover_y = -1*velocidade

            if evento.key == pygame.K_SPACE:
                mover_x = 0
                mover_y = 0

    cobra[0][0] += mover_x
    cobra[0][1] += mover_y

    if cobra[0][0] >= largura or cobra[0][0] < 0 or cobra[0][1] >= altura or cobra[0][1] < 0:
        executar = False
        break

    if cobra[0][0] == comida_pos_x and cobra[0][1] == comida_pos_y:
        pontos += 1
        comida_pos_x = random.randint(1,((largura-tamanho)//10))*10
        comida_pos_y = random.randint(1,((altura-tamanho)//10))*10
        cobra.append([cobra[-1][0]-mover_x,cobra[-1][1]-mover_y])

    for i in cobra[1:]:
        if i[0] == cobra[0][0] and i[1] == cobra[0][1]:
            executar = False

    for i in cobra:
        pygame.draw.rect(tela,verde,[i[0],i[1],tamanho,tamanho])

    pygame.draw.rect(tela,vermelho,[comida_pos_x,comida_pos_y,tamanho,tamanho])

    
    if len(cobra) > 1:
        copia = deepcopy(cobra)
        for i in range(len(cobra)-1):
            cobra[i+1][0] += copia[i][0] - cobra[i+1][0]
            cobra[i+1][1] += copia[i][1] - cobra[i+1][1]   
    
    relogio.tick(velocidade)
    pygame.display.update()

pygame.quit()