class Regra:
    def __init__(self, variavel):
        self.naoTerminal = variavel
        self.terminais = dict()
    
    def addTerminal(self, chave, terminal):
        self.terminais[chave] = terminal 
    
    def getTerminal(self, chave):
        return self.terminais.get(chave)

class AnalisadorSintatico:
    def __init__(self):
        self.tabela = list()
    
    def criaTabelaRegras(self):
        E = Regra('E')
        E.addTerminal('id', 'TS')
        E.addTerminal('num', 'TS')
        E.addTerminal('(', 'TS')
        self.tabela.append(E)

        T = Regra('T')
        T.addTerminal('id', 'FG')
        T.addTerminal('num', 'FG')
        T.addTerminal('(', 'FG')
        self.tabela.append(T)

        S = Regra('S')
        S.addTerminal('+', 'TS')
        S.addTerminal('-', 'TS')
        S.addTerminal(')', '@')
        S.addTerminal('$', '@')
        self.tabela.append(S)

        G = Regra('G')
        G.addTerminal('+', '@')
        G.addTerminal('-', '@')
        G.addTerminal('*', '*FG')
        G.addTerminal('/', '/FG')
        G.addTerminal(')', '@')
        G.addTerminal('$', '@')
        self.tabela.append(G)

        F = Regra('F')
        F.addTerminal('id', 'id')
        F.addTerminal('num', 'num')
        F.addTerminal('(', '(E)')
        self.tabela.append(F)






if __name__ == "__main__":
    a = AnalisadorSintatico()
    a.criaTabelaRegras()

    