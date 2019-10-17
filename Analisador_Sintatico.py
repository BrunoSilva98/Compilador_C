from Analisador_Lexico import AnalisadorLexico

class Regra:
    def __init__(self, variavel):
        self.naoTerminal = variavel
        self.terminais = dict()
    
    def addTerminal(self, chave, terminal):
        self.terminais[chave] = terminal 
    
    def getTerminal(self, chave):
        return self.terminais.get(chave)

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tabela = list()
        self.cadeia = tokens
        self.cadeia.append('$')
        self.pilha = list()
    
    def getNaoTerminal(self, variavel):
        for regra in self.tabela:
            if (regra.naoTerminal == variavel):
                return regra

    def empilha(self, regra):
        self.pilha.insert(0, regra[::-1])

    def desempilha(self):
        return self.pilha.pop(0)
        
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
    
    def analiseSintatica(self):
        pass


if __name__ == "__main__":
    analisadorLexico = AnalisadorLexico(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")    
    analisadorLexico.analiseLexica()

    a = AnalisadorSintatico(analisadorLexico.listaTokens)
    a.criaTabelaRegras()
    a.pilha.append(a.getNaoTerminal('E'))
