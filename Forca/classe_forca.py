class JogoDaForca():

    def __init__(self,qtd_vidas,palavra):
        self.qtd_vidas = qtd_vidas
        self.palavra = palavra
        self.lista_letras_certas = self.gerar_palavra_descoberta()
        self.lista_letras_erradas = []

    def gerar_palavra_descoberta(self):
        return ['' for i in range(len(self.palavra))]

    def verificar_jogada(self,letra):
        letra = letra.upper()

        if letra in self.palavra:
            self.substituir_letra(letra)
            return True

        else:
            self.aplicar_punicao(letra)
            return False

    def substituir_letra(self,letra):
        posicoes = [i for i,char in enumerate(self.palavra) if char == letra]

        for i in posicoes:
            self.lista_letras_certas[i] = letra
        
    def aplicar_punicao(self,letra):
        if letra not in self.lista_letras_erradas:
            self.lista_letras_erradas.append(letra)
            self.qtd_vidas -= 1

    def verificar_fim(self):
        if self.qtd_vidas == 0:
            return (True, -1)
        
        elif len(self.palavra) == len(''.join(self.lista_letras_certas)):
            return (True, 1)

        else:
            return (False,0)