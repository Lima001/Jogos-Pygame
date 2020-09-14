from random import randint

def verificar_posicao_valida(tabuleiro, posicao):
    if posicao[0] in [0,1,2] and posicao[1] in [0,1,2]:
        return tabuleiro[posicao[0]][posicao[1]] == 0
    
    return False
        
    
def verificar_colunas(tabuleiro, simbolo):
    for i in range(3):
        if tabuleiro[0][i] + tabuleiro[1][i] + tabuleiro[2][i] == simbolo*3:
            return True

    return False

def verificar_linhas(tabuleiro, simbolo):
    for linha in tabuleiro:
        if sum(linha) == simbolo*3:
            return True

    return False

def verificar_diagonais(tabuleiro, simbolo):
    diagonal1 = 0
    diagonal2 = 0

    tamanho = len(tabuleiro) -1

    for i in range(3):
        diagonal1 += tabuleiro[i][i]
        diagonal2 += tabuleiro[i][tamanho-i]

    return diagonal1 == simbolo * 3 or diagonal2 == simbolo * 3 

def verificar_vencedor(tabuleiro, simbolo):
    return verificar_colunas(tabuleiro, simbolo) or verificar_linhas(tabuleiro, simbolo) or verificar_diagonais(tabuleiro, simbolo)

def marcar_simbolo_tabuleiro(tabuleiro, simbolo, posicao):
    tabuleiro[posicao[0]][posicao[1]] = simbolo

def definir_simbolo():
    if randint(1,10) % 2 == 0:
        return 1
    return -1

def definir_maquina(simbolo):
    modo = int(input("(1)Contra Pessoa / (-1)Contra Máquina : "))
    
    if modo == -1:
        maquina = simbolo * -1
        return maquina
    
    return None

def pegar_jogada_maquina():
    linha = randint(0,2)
    coluna = randint(0,2)

    return (linha, coluna)

def realizar_jogada(tabuleiro, simbolo, posicao, pos_restantes):
    if verificar_posicao_valida(tabuleiro, posicao):
        marcar_simbolo_tabuleiro(tabuleiro, simbolo, posicao)
        return True

    return False

def finalizar_jogo(tabuleiro, simbolo, pos_restantes):
    if pos_restantes == 0:
        return 0

    elif verificar_vencedor(tabuleiro,simbolo):
        return simbolo
    
    else:
        return None

def interpretar_resultado(vencedor, map_simbolos, tabuleiro):
    if vencedor == 0:
        return "O JOGO EMPATOU!"
    else:
        return f"O vencedor foi {map_simbolos[vencedor]}"