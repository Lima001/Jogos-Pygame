import pygame
import random

class Cubo:

    def __init__(self,pos_x,pos_y,altura,largura,cor):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.cor = cor

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

class Jogo:

    def __init__(self,passaro,modelo_tubo,gravidade,vel_cenario,forca,tela,fonte,relogio):
        self.gravidade = gravidade
        self.vel_cenario = vel_cenario
        self.forca = forca
        self.vel_queda = 0
        self.tela = tela
        self.fonte = fonte
        self.relogio = relogio
        self.passaro = passaro
        self.modelo_tubo = modelo_tubo
        self.tubos = []
        self.pontuacao = 0
        self.executar = False

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
                if evento.key == pygame.K_SPACE:
                    self.vel_queda = - self.forca

    def movimentar_elementos(self):
        self.vel_queda += self.gravidade
        self.passaro.pos_y += self.vel_queda

        for i in self.tubos:
            i[0].pos_x -= self.vel_cenario
            i[1].pos_x -= self.vel_cenario

            if i[0].pos_x + self.modelo_tubo.largura <= 0:
                self.resetar_tubo(i)

    def gerar_altura_tubos(self):
        indice_aleatoriedade = random.randint(1,2)
        if indice_aleatoriedade == 1:
            alt1 = random.randrange(80,350,10)
            alt2 = -(self.tela.altura - (alt1 + 80))
            
        else:
            alt2 = - random.randrange(80,350,10)
            alt1 = (self.tela.altura + (alt2 - 80))
        
        return (alt1,alt2)

    def resetar_tubo(self,tubo=None):

        if tubo is None:
            pos_x = 800
            for i in range(2):
                alturas = self.gerar_altura_tubos()
                cima = Cubo(pos_x,0,alturas[0],self.modelo_tubo.largura,self.modelo_tubo.cor)
                baixo = Cubo(pos_x,600,alturas[1],self.modelo_tubo.largura,self.modelo_tubo.cor)
                self.tubos.append([cima,baixo,1])
                pos_x += self.tela.largura//2 + self.modelo_tubo.largura
                
        else:
            alturas = self.gerar_altura_tubos()
            tubo[0] = Cubo(800 + self.modelo_tubo.largura,0,alturas[0],self.modelo_tubo.largura,self.modelo_tubo.cor)
            tubo[1] = Cubo(800 + self.modelo_tubo.largura,600,alturas[1],self.modelo_tubo.largura,self.modelo_tubo.cor)
            tubo[2] = 1
        

    def verificar_colisao(self):
        if self.passaro.pos_y < 0 or self.passaro.pos_y + self.passaro.altura > self.tela.altura:
            self.executar = False

        for i in self.tubos:
            if self.passaro.pos_y <= i[0].pos_y + i[0].altura:
                if (self.passaro.pos_x >= i[0].pos_x and self.passaro.pos_x <= i[0].pos_x + i[0].largura) or (self.passaro.pos_x + self.passaro.largura >= i[0].pos_x and self.passaro.pos_x + self.passaro.largura <= i[0].pos_x + i[0].largura):
                    self.executar = False

            if self.passaro.pos_y + self.passaro.altura >= i[1].pos_y + i[1].altura:
                if (self.passaro.pos_x >= i[1].pos_x and self.passaro.pos_x <= i[1].pos_x + i[1].largura) or (self.passaro.pos_x + self.passaro.largura >= i[1].pos_x and self.passaro.pos_x + self.passaro.largura <= i[1].pos_x + i[1].largura):
                    self.executar = False

    def verificar_pontuacao(self):
        if (self.tubos[0][0].pos_x + self.modelo_tubo.largura) < self.passaro.pos_x and self.tubos[0][2] == 1:
            self.pontuacao += 1
            self.tubos[0][2] = 0
        
        if (self.tubos[1][0].pos_x + self.modelo_tubo.largura) < self.passaro.pos_x and self.tubos[1][2] == 1:
            self.pontuacao += 1
            self.tubos[1][2] = 0


    def desenhar_elementos(self):
        self.passaro.desenhar_na_tela(self.tela.tela_pygame)
        for i in self.tubos:
            i[0].desenhar_na_tela(self.tela.tela_pygame)
            i[1].desenhar_na_tela(self.tela.tela_pygame)        

    def executar_jogo(self):
        self.iniciar_elementos()
        self.resetar_tubo()

        while self.executar:

            self.tela.preencher_fundo_tela()
            self.capturar_movimento()
            self.movimentar_elementos()
            self.desenhar_elementos()
            self.verificar_colisao()
            self.verificar_pontuacao()
            self.relogio.passar_ciclo()
            mensagem = self.fonte.fonte_pygame.render(str(self.pontuacao),True,(0,0,0))
            self.tela.exibir_mensagem(mensagem,[self.tela.largura//2,self.fonte.tamanho])
            self.tela.atualizar_tela()
        pygame.quit()


if __name__ == "__main__":
    
    tela = Tela(800,600,"FlappyBird",(185,185,255))
    relogio = Relogio(30)
    passaro = Cubo(400,250,20,20,(255,255,0))
    molde_tubo = Cubo(0,0,0,50,(0,255,0))
    fonte = Fonte(None,50)

    jogo = Jogo(passaro,molde_tubo,1,10,10,tela,fonte,relogio)
    jogo.executar_jogo()