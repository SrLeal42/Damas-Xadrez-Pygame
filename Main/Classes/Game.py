import pygame as PG
from Config import LARGURA, ALTURA, NUM_PECAS_DAMAS, NUM_PECAS_XADREZ

from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro

class Game:

    jogo = ""

    gameEnd = False

    colorWinner = -1

    tabuleiro = None
    PecasBrancas = None
    PecasPretas = None

    rei_PB = None
    rei_PP = None

    num_rodadas = 0
    cor_rodada = 0

    sequencia_captura = False # Significa que caso um player capture uma peça e existe a possibilidade de capturar outras ele deve continuar na sequencia de capturas

    def __init__(self,jogo:str):

        self.jogo = jogo

        # PEÇAS BRANCAS
        PB = self.CreatePecas(0)
        PP = self.CreatePecas(1)

        self.PecasBrancas = PB
        self.PecasPretas = PP

        self.tabuleiro = Tabuleiro()

        self.tabuleiro.AdicionaPecasAoTabuleiro(PB,jogo,1)
        self.tabuleiro.AdicionaPecasAoTabuleiro(PP,jogo,0)



    def CreatePecas(self, cor:int):

        if (self.jogo == ""):
            return
        
        P = []

        if (self.jogo == "damas"):
            
            for _ in range(NUM_PECAS_DAMAS):

                p = Peca(cor,0,0, escala=1.5)
                P.append(p)
        
        elif (self.jogo == "xadrez"):
            
            outros_tipos = [3] * 2 + [4] * 2 + [5] * 2 + [6, 7]

            for i, tipo in enumerate(outros_tipos):
                p = Peca(cor, 0, 0, tipo=tipo,  escala=3)

                if tipo == 7:  # O rei
                    if cor == 0:
                        self.rei_PB = p
                    else:
                        self.rei_PP = p

                P.append(p)

            for i in range(NUM_PECAS_XADREZ//2):
                p = Peca(cor, 0, 0, tipo=2, escala=3)

                if (cor == 0):
                    P.insert(0,p)
                else:
                    P.append(p)        
        
        return P

    
    def EndTurn(self):
        self.num_rodadas += 1
        if (not self.sequencia_captura):
            self.cor_rodada = 0 if self.cor_rodada == 1 else 1
        # self.sequencia_captura = False



    def WinningUpdate(self):

        response = {"gameEnd":False, "colorWinner":-1}

        if (self.jogo == "damas"):

            response["gameEnd"] = (NUM_PECAS_DAMAS <= self.tabuleiro.num_brancas_capturadas) or (NUM_PECAS_DAMAS <= self.tabuleiro.num_pretas_capturadas)
            
            if (response["gameEnd"]):
                response["colorWinner"] = 0 if NUM_PECAS_DAMAS <= self.tabuleiro.num_pretas_capturadas else 1

        elif (self.jogo == "xadrez"):

            response["gameEnd"] = self.rei_PB.capturada or self.rei_PP.capturada

            if (response["gameEnd"]):
                response["colorWinner"] = 0 if self.rei_PP.capturada else 1

        self.gameEnd = response["colorWinner"]

        self.colorWinner = response["colorWinner"]

        return response

    
    def ResetGame(self, jogo:str = None):
        
        self.jogo = jogo if jogo else self.jogo

        self.gameEnd = False

        self.colorWinner = -1

        self.PecasBrancas = None
        self.PecasPretas = None

        self.rei_PB = None
        self.rei_PP = None

        self.num_rodadas = 0
        self.cor_rodada = 0

        self.sequencia_captura = False

        PB = self.CreatePecas(0)
        PP = self.CreatePecas(1)

        self.PecasBrancas = PB
        self.PecasPretas = PP

        self.tabuleiro.ResetTabuleiro()


        # for i in range(self.tabuleiro.tamanho):
        #         for j in range(self.tabuleiro.tamanho):
        #             if (self.tabuleiro.tabuleiro[i][j] != None):
        #                 print(self.tabuleiro.tabuleiro[i][j])
        #             else:
        #                 print(None)

        self.tabuleiro.AdicionaPecasAoTabuleiro(PB,self.jogo,1)
        self.tabuleiro.AdicionaPecasAoTabuleiro(PP,self.jogo,0)


    def SomePecaCanCapture(self):
        
        peca = []

        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):

                p = self.tabuleiro.tabuleiro[linha][coluna]

                if (p == None):
                    continue

                if (self.tabuleiro.VerifyPecaCanCapture(p, True)):
                    if (p.cor == self.cor_rodada):
                        peca.append(p)
                
        
        return peca
