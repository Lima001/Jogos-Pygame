import pygame
from classe_arquivo import *
from classe_forca import *

class Fonte:

    def __init__(self,nome,tamanho,cor):
        self.nome = nome
        self.tamanho = tamanho
        self.cor = cor
        self.fonte_pygame = None

    def iniciar_fonte(self):
        self.fonte_pygame = pygame.font.SysFont(self.nome, self.tamanho)

class Relogio:

    def __init__(self,tempo):
        self.tempo = tempo
        self.relogio_pygame = None

    def iniciar_relogio(self):
        self.relogio_pygame = pygame.time.Clock()
    
    def passar_ciclo(self):
        if self.relogio_pygame is not None:
            self.relogio_pygame.tick(self.tempo)

class Tela:

    def __init__(self,largura,altura,titulo,cor_fundo):
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.cor_fundo = cor_fundo
        self.tela_pygame = None

    def iniciar_tela(self):
        self.tela_pygame = pygame.display.set_mode((self.largura,self.altura))
        pygame.display.set_caption(self.titulo)

    def atualizar_tela(self):
        pygame.display.update()

    def preencher_fundo_tela(self):
        self.tela_pygame.fill(self.cor_fundo)

    def exibir_mensagem(self,mensagem,pos):
        self.tela_pygame.blit(mensagem,pos)


class ModoGrafico():

    def __init__(self,path_arquivo, qtd_vidas, tela, relogio, fonte):
        self.arquivo = GerenciadorArquivo(path_arquivo)
        self.qtd_vidas = qtd_vidas
        self.tela = tela
        self.relogio = relogio
        self.fonte = fonte
        self.forca = None
        self.executar = False

    def criar_jogo(self):
        palavra = self.arquivo.pegar_palavra_aleatoria()
        return JogoDaForca(self.qtd_vidas,palavra)

    def limpar_tela(self):
        self.tela.preencher_fundo_tela()
    
    def exibir_informacoes(self):
        msg_vida = (f"Vidas: {self.forca.qtd_vidas}",True,self.fonte.cor)
        msg_palavra = (f"Palavra: {self.forca.lista_letras_certas}",True,self.fonte.cor)
        msg_tentativas = (f"Tentativas: {self.forca.lista_letras_erradas}",True,self.fonte.cor)

        mensagens = (msg_vida,msg_palavra,msg_tentativas)

        pos = 0
        for i in mensagens:
            self.tela.exibir_mensagem(self.fonte.fonte_pygame.render(*i),(0,pos))
            pos += self.fonte.tamanho + self.fonte.tamanho//2

    def exibir_cabecalho(self):
        self.limpar_tela()
        self.exibir_informacoes()
    
    def exibir_resultado(self, resultado):
        if resultado == -1:
            msg = ("Você Perdeu! Todas as suas vidas acabaram!",True,self.fonte.cor)
        
        else:
            msg = ("Parabéns, Você ganhou!",True,self.fonte.cor)


        msg_palavra = (f'A palavra era: {self.forca.palavra}',True,self.fonte.cor)

        altu = self.tela.altura//3
        larg = self.tela.largura//2 - (len(msg[0]) * 10)
        
        self.limpar_tela()
        self.tela.exibir_mensagem(self.fonte.fonte_pygame.render(*msg),(larg,altu))
        self.tela.exibir_mensagem(self.fonte.fonte_pygame.render(*msg_palavra),(larg,altu*2))
        self.tela.atualizar_tela()

        if pygame.get_init() is True:
            exe = True
            while exe:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.executar = False
                        exe = False

    def pegar_jogada(self):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                letra = pygame.key.name(evento.key)

                if letra.isalpha():
                    return letra

                else:
                    return None

            elif evento.type == pygame.QUIT:
                self.executar = False
                return None

    def finalizar_jogo(self):
        fim = self.forca.verificar_fim()
        if fim[0]:
            self.exibir_resultado(fim[1])

    def inicializar_pygame(self):
        pygame.init()
        self.tela.iniciar_tela()
        self.relogio.iniciar_relogio()
        self.fonte.iniciar_fonte()

    def jogar(self):
        self.inicializar_pygame()
        self.executar = True
        self.forca = self.criar_jogo()

        while self.executar:
            self.exibir_cabecalho()

            letra = self.pegar_jogada()

            if letra is not None:
                self.forca.verificar_jogada(letra)

            self.relogio.passar_ciclo()
            self.tela.atualizar_tela()
            self.finalizar_jogo()
        
        pygame.quit()
        
        jogar_novamente = int(input("Deseja jogar Novamente? 0-Não \ 1-Sim ..."))

        if jogar_novamente == 1:
            self.jogar()

if __name__ == "__main__":
    fonte = Fonte(None,50,(0,0,0))
    relogio = Relogio(10)
    tela = Tela(800,600,"JOGO DA FORCA",(255,255,255))
    
    qtd_vidas = 5
    path_arquivo = "palavras.txt"
    
    jogo = ModoGrafico(path_arquivo,qtd_vidas,tela,relogio,fonte)
    jogo.jogar()