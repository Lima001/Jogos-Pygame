import pygame
import random
from copy import deepcopy

class Cubo:

    def __init__(self,pos_x,pos_y,altura,largura,cor):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.cor = cor

    def atualizar_pos(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def desenhar_na_tela(self,tela):
        pygame.draw.rect(tela,self.cor,[self.pos_x,self.pos_y,self.largura,self.altura])


class Tela:

    def __init__(self,largura,altura,titulo,cor_fundo):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = cor_fundo
        self.tela_pygame = None

    def iniciar_tela(self):
        self.tela_pygame = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption("Snake V1")

    def atualizar_tela(self):
        if self.tela_pygame is not None:
            pygame.display.update()

    def preencher_fundo_tela(self):
        self.tela_pygame.fill(self.cor_fundo)

    def exibir_mensagem(self,mensagem,pos):
        self.tela_pygame.blit(mensagem,pos)

class Relogio:

    def __init__(self,tempo):
        self.tempo = tempo
        self.relogio_pygame = None

    def iniciar_relogio(self):
        self.relogio_pygame = pygame.time.Clock()
    
    def passar_ciclo(self):
        if self.relogio_pygame is not None:
            self.relogio_pygame.tick(self.tempo)

class Fonte:

    def __init__(self,nome,tamanho):
        self.nome = nome
        self.tamanho = tamanho
        self.fonte_pygame = None

    def iniciar_fonte(self):
        self.fonte_pygame = pygame.font.SysFont(self.nome, self.tamanho)

class Cobra:

    def __init__(self,cabeca,velocidade):
        self.velocidade = velocidade
        self.mover_x = 0
        self.mover_y = 0
        self.corpo = [cabeca]

    def mover_corpo(self,index,desl_x,desl_y):
        self.corpo[index].pos_x += desl_x
        self.corpo[index].pos_y += desl_y

class Jogo:

    def __init__(self,tela,fonte,relogio,cobra,comida):
        self.tela = tela
        self.relogio = relogio
        self.fonte = fonte
        self.cobra = cobra
        self.comida = comida
        self.executar = False
        self.pontos = 0

    def iniciar_elementos(self):
        pygame.init()
        self.tela.iniciar_tela()
        self.relogio.iniciar_relogio()
        self.fonte.iniciar_fonte()
        self.executar = True

    def capturar_movimento(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executar = False
        
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    self.cobra.mover_x = self.cobra.velocidade * -1
                    self.cobra.mover_y = 0

                if evento.key == pygame.K_RIGHT:
                    self.cobra.mover_x = self.cobra.velocidade
                    self.cobra.mover_y = 0

                if evento.key == pygame.K_DOWN:
                    self.cobra.mover_x = 0
                    self.cobra.mover_y = self.cobra.velocidade

                if evento.key == pygame.K_UP:
                    self.cobra.mover_x = 0
                    self.cobra.mover_y = self.cobra.velocidade * -1

                #Apenas para Testes
                #if evento.key == pygame.K_SPACE:
                #    self.cobra.mover_x = 0
                #    self.cobra.mover_y = 0

    def verificar_colisoes(self):
        if self.cobra.corpo[0].pos_x >= self.tela.largura or self.cobra.corpo[0].pos_x < 0 or self.cobra.corpo[0].pos_y >= self.tela.altura or self.cobra.corpo[0].pos_y < 0:
            self.executar = False

        if  self.cobra.corpo[0].pos_x == self.comida.pos_x and  self.cobra.corpo[0].pos_y == self.comida.pos_y:
            self.pontos += 1
            self.comida.pos_x = random.randint(1,((self.tela.largura - self.comida.largura)//10))*10
            self.comida.pos_y = random.randint(1,((self.tela.altura - self.comida.altura)//10))*10

            pos_x, pos_y = (self.cobra.corpo[-1].pos_x - self.cobra.mover_x) , (self.cobra.corpo[-1].pos_y - self.cobra.mover_y)
            cubo = Cubo(pos_x,pos_y,self.cobra.corpo[0].altura,self.cobra.corpo[0].largura,self.cobra.corpo[0].cor)

            self.cobra.corpo.append(cubo)

        for i in range(1,(len(self.cobra.corpo)-1)):
            if self.cobra.corpo[0].pos_x == self.cobra.corpo[i].pos_x and self.cobra.corpo[0].pos_y == self.cobra.corpo[i].pos_y:
                self.executar = False


    def movimentar_cobra(self):
        if len(self.cobra.corpo) > 1:
            copia = deepcopy(self.cobra.corpo)

            for i in range(len(self.cobra.corpo)-1):
                self.cobra.corpo[i+1].pos_x += copia[i].pos_x - self.cobra.corpo[i+1].pos_x
                self.cobra.corpo[i+1].pos_y += copia[i].pos_y - self.cobra.corpo[i+1].pos_y

    def desenhar_elementos_tela(self):
        for i in self.cobra.corpo:
            i.desenhar_na_tela(self.tela.tela_pygame)

        self.comida.desenhar_na_tela(self.tela.tela_pygame)

    def executar_jogo(self):

        self.iniciar_elementos()

        while self.executar:

            mensagem = self.fonte.fonte_pygame.render("Pontos: " + str(self.pontos),True,(0,0,0))
            self.tela.preencher_fundo_tela()
            self.tela.exibir_mensagem(mensagem,[0,0])
            self.capturar_movimento()
            self.cobra.mover_corpo(0,self.cobra.mover_x,self.cobra.mover_y)
            self.verificar_colisoes()
            self.desenhar_elementos_tela()
            self.movimentar_cobra()
            self.relogio.passar_ciclo()
            self.tela.atualizar_tela()
        pygame.quit()


if __name__ == "__main__":

    tela = Tela(800,600,"SnakeOO",(255,255,255))
    relogio = Relogio(10)
    fonte = Fonte(None,20)
    
    pos_x, pos_y = (random.randint(1,((800-10)//10))*10), (random.randint(1,((600-10)//10))*10) 
    comida = Cubo(pos_x,pos_y,10,10,(255,0,0))

    cabeca = Cubo(400,300,10,10,(0,255,0))
    cobra = Cobra(cabeca,10)

    jogo = Jogo(tela,fonte,relogio,cobra,comida)
    jogo.executar_jogo()