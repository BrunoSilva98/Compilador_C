from Analisador_Lexico import AnalisadorLexico
from tabulate import tabulate

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
        self.cadeia.append(['Fim','$','Identificador Final'])
        self.pilha = list()
        self.terminais = ['id','num','+','-','*','/','(',')','$']
        self.tabelaPrintar = [["Pilha", "Cadeia", "Regra"]]

    def getNaoTerminal(self, variavel):
        for regra in self.tabela:
            if (regra.naoTerminal == variavel):
                return regra

    def empilha(self, regra):
        if regra == '@':
            pass
        elif regra in self.terminais:
            self.pilha.append(regra)
        else:
            for elemento in regra[::-1]:
                self.pilha.append(elemento)

    def desempilha(self):
        return self.pilha.pop(len(self.pilha)-1)
        
    def removeFirstCharCadeia(self):
        self.cadeia = self.cadeia[1:]

    def verificaRegra(self, naoVariavel, terminal):
        regra = self.getNaoTerminal(naoVariavel)
        lista = regra.terminais.keys()
        if(terminal in lista):
            return True
        return False

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
        S.addTerminal('+', '+TS')
        S.addTerminal('-', '-TS')
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
    
    def printarCadeia(self):
        texto = ""
        for i in range(len(self.cadeia)-1):
            texto = texto + self.cadeia[i][1]
        return texto + '$'

    def analiseSintatica(self):
        topo = self.pilha[len(self.pilha)-1]
        topoCadeia = self.cadeia[0][1]

        while (topo != '$'):
            topo = self.pilha[len(self.pilha)-1]
            topoCadeia = self.cadeia[0][1]
            if(topo in self.terminais):
                if(topo == topoCadeia):
                    self.tabelaPrintar.append([list(self.pilha), self.printarCadeia(), 'RECONHECE'])
                    self.desempilha()
                    self.removeFirstCharCadeia()
                else:
                    self.tabelaPrintar.append([list(self.pilha), self.printarCadeia(), 'ERRO'])
                    break
            
            elif(self.verificaRegra(topo,topoCadeia)):
                regra = self.getNaoTerminal(topo)
                self.tabelaPrintar.append([list(self.pilha), self.printarCadeia(), topo + '->' + regra.terminais[topoCadeia]])
                self.desempilha() 
                self.empilha(regra.terminais[topoCadeia])
            
            else:
                self.tabelaPrintar.append([list(self.pilha), self.cadeia, 'ERRO'])
                break
    
    def mostrarTabela(self):
        print(tabulate(self.tabelaPrintar))

                

if __name__ == "__main__":
    analisadorLexico = AnalisadorLexico(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")    
    analisadorLexico.analiseLexica()

    a = AnalisadorSintatico(analisadorLexico.listaTokens)
    a.criaTabelaRegras()
    a.pilha.append('$')
    a.pilha.append(a.getNaoTerminal('E').naoTerminal)
    a.analiseSintatica()
    a.mostrarTabela()