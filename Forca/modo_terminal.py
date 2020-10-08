from classe_arquivo import *
from classe_forca import *

class ModoTerminal():

    def __init__(self,qtd_vidas, path_arquivo):
        self.arquivo = GerenciadorArquivo(path_arquivo)
        self.qtd_vidas = qtd_vidas
        self.forca = None
        self.executar = False

    def criar_jogo(self):
        palavra = self.arquivo.pegar_palavra_aleatoria()
        return JogoDaForca(self.qtd_vidas,palavra)

    def limpar_tela(self):
        print("\n"*60)

    def exibir_informacoes(self):
        print(f"Vidas: {self.forca.qtd_vidas}")
        print(f"Palavra: {self.forca.lista_letras_certas}")
        print(f"Tentativas: {self.forca.lista_letras_erradas}")
        print()
    
    def exibir_cabecalho(self):
        self.limpar_tela()
        print("JOGO DA FORCA")
        print()
        self.exibir_informacoes()

    def pegar_jogada(self):
        letra = input("Digite uma letra: ").upper()

        if letra.isalpha():
            return letra
        
        elif letra == "":
            self.executar = False

        else:
            print("LETRA INVÁLIDA!")
        
        return None

    def finalizar_jogo(self):
        fim = self.forca.verificar_fim()
        if fim[0]:
            self.exibir_resultado(fim[1])
            self.executar = False

    def exibir_resultado(self,resultado):
        if resultado == -1:
            print("Você Perdeu! Todas as suas vidas acabaram!")
        
        else:
            print("Parabéns, Você ganhou!")

    def jogar(self):
        self.executar = True
        self.forca = self.criar_jogo()

        while self.executar:
            self.exibir_cabecalho()

            letra = self.pegar_jogada()

            if letra is not None:
                
                if self.forca.verificar_jogada(letra):
                    print(f"A letra {letra} está na palavra!", end="\n"*2)
                
                else:
                    print(f"A letra {letra} NÃO está na palavra!", end="\n"*2)

            self.finalizar_jogo()

            trava = input("Pressione Enter para continuar...")

        jogar_novamente = int(input("Deseja jogar Novamente? 0-Não \ 1-Sim ..."))

        if jogar_novamente == 1:
            self.jogar()

if __name__ == "__main__":
    qtd_vidas = 5
    path_arquivo = "palavras.txt"

    modo_terminal = ModoTerminal(qtd_vidas,path_arquivo)
    modo_terminal.jogar()