from os.path import exists
from os import remove
from random import randint

class GerenciadorArquivo():

    def __init__(self, path_arq):
        self.path_arq = path_arq
        self.criar_arquivo()

    def criar_arquivo(self):
        if not exists(self.path_arq):
            arquivo = open(self.path_arq, "w")
            arquivo.close()

    def adicionar_palavras(self, lista_palavras):
        arquivo = open(self.path_arq, "a")
        
        for p in lista_palavras:
            if self.pesquisar_palavra(p) is None:
                arquivo.write(p.upper() + "\n")
        
        arquivo.close()

    def remover_palavra(self, palavra):
        arquivo = open(self.path_arq,'r')
        
        lista_palavras = arquivo.read().splitlines()
        
        try:
            lista_palavras.remove(palavra.upper())
        
        except:
            return False

        arquivo.close()

        self.limpar_arquivo()
        self.adicionar_palavras(lista_palavras)

        return True

    def limpar_arquivo(self):
        arquivo = open(self.path_arq, "w")
        arquivo.close()

    def pegar_palavra_aleatoria(self):
        arquivo = open(self.path_arq,'r')
        
        lista_palavras = arquivo.read().splitlines()
        
        if len(lista_palavras) == 0:
            return None

        num_aleatorio = randint(0,len(lista_palavras)-1)
        
        arquivo.close()
        
        return lista_palavras[num_aleatorio]

    def pesquisar_palavra(self, palavra):
        arquivo = open(self.path_arq, 'r')

        lista_palavras = arquivo.read().splitlines()
        
        arquivo.close()
        if palavra.upper() in lista_palavras:
            return lista_palavras.index(palavra.upper())

        else:
            return None

    def excluir_arquivo(self):
        try:
            remove(self.path_arq)
            return True
        
        except:
            return False

if __name__ == "__main__":
    path_arquivo = input("Arquivo: ")

    arq = GerenciadorArquivo(path_arquivo)

    executar = True
    while executar:
        
        print("\n"*60)
        print("0 - Sair")
        print("1 - Adicionar Palavras")
        print("2 - Remover Palavra")
        print("3 - Limpar Arquivo")
        print("4 - Pegar Palavra Aleatória")
        print("5 - Pesquisar Palavra")
        print("6 - Excluir Arquivo")
        print()

        opcao = int(input("Digite a opção: "))

        if opcao == 0:
            executar = False

        elif opcao == 1:
            lista_palavras =[]
            palavra = input("Digite uma palavra para adicionar: ")

            while palavra != "":
                lista_palavras.append(palavra)
                palavra = input("Digite uma palavra para adicionar, ou pressione enter para sair: ")
                
            arq.adicionar_palavras(lista_palavras)

        elif opcao == 2:
            palavra = input("Digite uma palavra para remover: ")

            if arq.remover_palavra(palavra):
                print("Palavra Removida com Sucesso!")
            
            else:
                print("Palavra não Encontrada!")

        elif opcao == 3:
            arq.limpar_arquivo()

        elif opcao == 4:
            palavra = arq.pegar_palavra_aleatoria()
            
            if palavra is not None:
                print(f"Palavra: {palavra}")
            
            else:
                print("Arquivo sem palavras!")

        elif opcao == 5:
            palavra = input("Digite uma palavra para localizar: ")
            linha = arq.pesquisar_palavra(palavra) 
            
            if linha is not None:
                print(f"A palavra está na linha {linha}")

            else:
                print("Palavra não encontrada!")

        elif opcao == 6:
            if arq.excluir_arquivo():
                print("Arquivo excluído...")
                executar = False
            
            else:
                print("Erro na exclusão do arquivo!")

        else:
            print("Opção Inválida!")

        print()
        trava = input("Pressione Enter para continuar...")