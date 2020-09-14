from modulo_velha import *

def limpar_tela():
    print("\n"*80)

def imprimir_tabuleiro(tabuleiro, map_simbolos):
    limpar_tela()
    print("-- JOGO DA VELHA --", end="\n"*2)
    print("    0   1   2")
    print("  " + "-"*13)
    
    for linha in range(len(tabuleiro)):
        string = f"{linha} | "
    
        for elemento in tabuleiro[linha]:
            string += map_simbolos[elemento] + " | "

        print(string)
        print("  " + "-"*13)
    
    print()

def impirmir_vez(simbolo, map_simbolos):
    print(f"Vez de: {map_simbolos[simbolo]}", end="\n"*2)

def pegar_jogada_jogador():
    linha = int(input("Informe a LINHA que deseja marcar: "))
    coluna = int(input("Informe a COLUNA que deseja marcar: "))

    return (linha, coluna)

def pegar_jogada(simbolo, maquina):
    if maquina is not None and simbolo == maquina:
        return pegar_jogada_maquina()
    else:
        return pegar_jogada_jogador()

def executar_partida(tabuleiro, simbolo, pos_restantes, map_simbolos, maquina):
    vencedor = 0
    executar = True
    while executar:

        imprimir_tabuleiro(tabuleiro, map_simbolos)
        impirmir_vez(simbolo, map_simbolos)
        posicao = pegar_jogada(simbolo, maquina)
    
        if realizar_jogada(tabuleiro, simbolo, posicao, pos_restantes):
            pos_restantes -= 1
            resultado_round = finalizar_jogo(tabuleiro, simbolo, pos_restantes)
        
            if resultado_round is not None:
                vencedor = resultado_round
                break

            simbolo *= -1

    return vencedor

def imprimir_resultado(tabuleiro, map_simbolos, vencedor):
    imprimir_tabuleiro(tabuleiro, map_simbolos)
    print(interpretar_resultado(vencedor, map_simbolos, tabuleiro))

def main():
    tabuleiro = [[0,0,0], [0,0,0], [0,0,0]]
    pos_restantes = 9
    map_simbolos = {-1:"O", 0:" ", 1:"X"}
    simbolo = definir_simbolo()
    maquina = definir_maquina(simbolo)

    vencedor = executar_partida(tabuleiro, simbolo, pos_restantes, map_simbolos, maquina)

    imprimir_resultado(tabuleiro, map_simbolos, vencedor)

if __name__ == "__main__":
    main()