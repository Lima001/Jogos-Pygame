from modulo_velha import *
import pygame

#Variaveis Globais

#Tela
largura = 800
altura = 600

#Quadrantes
pos_inicial_quadrante1 = (70,75)
pos_final_quadrante1 = (730,75)

pos_final_quadrante2 = (70,555)

largura_quadranete = 220
altura_quadrante = 160

#Linha Cabeçalho
pos_inicial_cabecalho = (0,30)
pos_final_cabecalho = (800,30)

#Cores
preto = (0,0,0)
branco = (255,255,255)
azul = (0,0,255)
vermelho = (255,0,0)
cinza_claro = (212,212,212)

#Fonte
tamanho_fonte_padrao = 20
tamanho_fonte_simbolos = 100

#Funções
def gerar_quadrantes():
    quadrantes = [[],[],[]]

    y = pos_inicial_quadrante1[1]
    for i in quadrantes:
        for j in range(0,3):
            x = pos_inicial_quadrante1[0] + j*largura_quadranete
            posicao = (x,y)
            
            i.append(posicao)
        
        y += altura_quadrante

    return quadrantes

def carregar_cabecalho(tela, simbolo, map_simbolos, aviso, fonte):
    if simbolo == -1:
        cor = vermelho
    else:
        cor = azul
    
    mensagem1 = fonte.render(f"Vez de ", True, (0,0,0))
    mensagem2 = fonte.render(f"{map_simbolos[simbolo]}", True, cor)
    
    aviso = fonte.render(aviso, True, (0,0,0))

    tela.blit(mensagem1, [0,10])
    tela.blit(mensagem2, [50,10])
    tela.blit(aviso, [600,10])

    pygame.draw.line(tela, preto, pos_inicial_cabecalho, pos_final_cabecalho, 1)

def carregar_tabuleiro(tela, tabuleiro, map_simbolos, quadrantes, fonte):

    #Linhas Horizontais    
    for i in range(4):
        xi = pos_inicial_quadrante1[0] 
        xf = pos_final_quadrante1[0]

        y = pos_inicial_quadrante1[1] + i * altura_quadrante

        pygame.draw.line(tela, preto, (xi,y), (xf,y), 1)

    #Linhas Verticais
    for i in range(4):
        x = pos_inicial_quadrante1[0] + i * largura_quadranete

        yi = pos_inicial_quadrante1[1]
        yf = pos_final_quadrante2[1]

        pygame.draw.line(tela, preto, (x,yi), (x,yf), 1)

    #Simbolos
    for linha in range(len(tabuleiro)):
        for coluna in range(len(tabuleiro)):
            if tabuleiro[linha][coluna] == -1:
                cor = vermelho
            
            elif tabuleiro[linha][coluna] == 1:
                cor = azul
            
            else:
                cor = branco

            elemento = tabuleiro[linha][coluna]
            desenho = fonte.render(f"{map_simbolos[elemento]}", True, cor)
        
            x = quadrantes[linha][coluna][0] + (largura_quadranete//11) * 4
            y = quadrantes[linha][coluna][1] + (altura_quadrante//4) * 1
            
            tela.blit(desenho, [x,y])

def destacar_quadrante(tela, posicao_mouse, quadrantes):
    xm,ym = posicao_mouse
    
    for linha in quadrantes:
        for i in linha:
            if xm >= i[0]+1 and xm <= i[0] + largura_quadranete-1 and ym >= i[1]+1 and ym <= i[1]+altura_quadrante-1:
                retangulo = pygame.Rect((i[0]+1, i[1]+1), (largura_quadranete-1, altura_quadrante-1))
                tela.fill(cinza_claro, retangulo)
                return None

def exibir_parte_grafica(tela, fonte1, fonte2, quadrantes, tabuleiro, map_simbolos, simbolo, resultado=""):
    tela.fill(branco)

    posicao_mouse = pygame.mouse.get_pos()
    destacar_quadrante(tela, posicao_mouse, quadrantes)

    carregar_cabecalho(tela, simbolo, map_simbolos, resultado, fonte1)
    carregar_tabuleiro(tela, tabuleiro, map_simbolos, quadrantes, fonte2)

    pygame.display.update()

def mapear_quadrante_tabuleiro(posicao_mouse, quadrantes):
    xm = posicao_mouse[0]
    ym = posicao_mouse[1]

    for linha in range(3):
        for coluna in range(3):
            if xm+1 >= quadrantes[linha][coluna][0] and xm <= quadrantes[linha][coluna][0]+largura_quadranete-1:
                if ym+1 >= quadrantes[linha][coluna][1] and ym <= quadrantes[linha][coluna][1]+altura_quadrante-1:
                    return (linha, coluna)

    return None 

def pegar_jogada_jogador(quadrantes):
    posicao = None
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

        elif evento.type == pygame.MOUSEBUTTONUP:
            posicao_mouse_click = pygame.mouse.get_pos()
            posicao = mapear_quadrante_tabuleiro(posicao_mouse_click, quadrantes)
            return posicao

    return posicao

def pegar_jogada(simbolo, maquina, quadrantes):
    if maquina is not None and simbolo == maquina:
        return pegar_jogada_maquina()
    else:
        return pegar_jogada_jogador(quadrantes)

def executar_partida(tela, fonte1, fonte2, quadrantes, tabuleiro, pos_restantes, map_simbolos, simbolo, maquina):
    vencedor = 0
    executar = True
    while executar and pygame.get_init():
        
        exibir_parte_grafica(tela, fonte1, fonte2, quadrantes, tabuleiro, map_simbolos, simbolo)
        posicao = pegar_jogada(simbolo, maquina, quadrantes)
        
        if posicao is not None:
            if realizar_jogada(tabuleiro, simbolo, posicao, pos_restantes):
                pos_restantes -= 1
                resultado_round = finalizar_jogo(tabuleiro, simbolo, pos_restantes)
                
                if resultado_round is not None:
                    vencedor = resultado_round
                    break
                
                simbolo *= -1

    return vencedor

def imprimir_resultado(tela, fonte1, fonte2, quadrantes, tabuleiro, map_simbolos, simbolo, vencedor):
    if pygame.get_init() is True:
        resultado = interpretar_resultado(vencedor, map_simbolos, tabuleiro)
        
        while True:
            exibir_parte_grafica(tela, fonte1, fonte2, quadrantes, tabuleiro, map_simbolos, simbolo, resultado)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return None

def main():
    #Inicialização Pygame
    pygame.init()

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jogo da Velha")

    fonte1 = pygame.font.SysFont(None, tamanho_fonte_padrao)
    fonte2 = pygame.font.SysFont(None, tamanho_fonte_simbolos)

    #Variaveis do Jogo
    tabuleiro = [[0,0,0], [0,0,0], [0,0,0]]
    pos_restantes = 9
    map_simbolos = {-1:"O", 0:" ", 1:"X"}
    simbolo = definir_simbolo()
    maquina = definir_maquina(simbolo)
    quadrantes = gerar_quadrantes()

    vencedor = executar_partida(tela, fonte1, fonte2, quadrantes, tabuleiro, pos_restantes, map_simbolos, simbolo, maquina)
    imprimir_resultado(tela, fonte1, fonte2, quadrantes, tabuleiro, map_simbolos, simbolo, vencedor)

if __name__ == "__main__":
    main()
