import threading
import time
import os
from tkinter import *

root = Tk()

"""
Classe modelo da linha de produção
Essa classe define os atributos dos itens que compoeem a linha de produção de peças que compoem a
a montagem de um carro, definem também o tempo de produção e armazenamento das peças produzidas.

""" 
class linhaProducao(threading.Thread):

    nomeLinha = None
    qtdMinimaItem = None
    tempoProducao = None
    produzido     = None
    estoqueMaximo = None
    lock = None

    # Método construtor que incia o objeto(linha de produção) com os parâmetros passados
    def __init__(self,nomeLinha, qtdMinimaItem, tempoProducao, produzido, estoqueMaximo, lock):
        threading.Thread.__init__(self)
        self.nomeLinha = nomeLinha
        self.qtdMinimaItem = qtdMinimaItem
        self.tempoProducao = tempoProducao
        self.produzido = produzido
        self.estoqueMaximo = estoqueMaximo
        self.lock = "PaleGreen1"
        
    
    def run(self):
        while(True):
            if (self.lock == "PaleGreen1" and self.produzido < self.estoqueMaximo ):
                time.sleep(self.tempoProducao)
                self.produzido += 1

"""
Classe de controle das linhas de produção.
Essa classe controla os limites de produção de cada linha, controla o estoque de peças, a liberação dos itens
para a montagem dos carros e por fim a quantidade de carros que irão para a esteira.
"""
class Controle(threading.Thread):
    linhasParadas = None
    carrosProntos = 0
    poolThreads = []

    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.linhasParadas = 0
        self.poolThreads = pool

    def montarCarro(self):
        self.carrosProntos += 1
        for t in self.poolThreads:
            t.produzido = t.produzido - t.qtdMinimaItem

    def montaLinha(self, c1, c2, c3, r):
        Label(root,bg = c3, text=c1, relief=RIDGE, width=40).grid(row=r,column=0, columnspan = 2, sticky="E")
        Label(root,bg = c3, text=c2, relief=RIDGE, width=40).grid(row=r,column=2, columnspan = 2, sticky ="E")

    def run(self):
        tempo = 0
        carros = 0
        tMedio = 0

        while(True):
            time.sleep(.500)
            tempo += 0.5
            r = 1

            if carros:
                tMedio = tempo/carros

            self.montaLinha("Item", "Estoque", "white", 0)
            checkProducao = 0
            os.system('clear')
            self.montaLinha("", "", "white", 6)

            self.montaLinha("Tempo Medio de Producao: ", tMedio, "white",7)

            self.montaLinha("Carros montados: ",str(self.carrosProntos), "white",8)
            # print ("Carros montados: " + str(self.carrosProntos))
            for t in self.poolThreads:
                if (t.produzido >= t.estoqueMaximo):
                    # print ("Limite de producao atingido")
                    self.montaLinha(t.nomeLinha, t.produzido, t.lock, r)
                    # print (" # Item: " + str(t.nomeLinha) + "  @ Linha Parada: " + str(t.lock) + "  & Estoque: " + str(t.produzido) )
                    t.lock = "tomato"
                    self.linhasParadas +=1
                else:
                    self.montaLinha(t.nomeLinha, t.produzido, t.lock, r)
                    # print (" # Item: " + str(t.nomeLinha) + "  @ Linha Parada: " + str(t.lock) + "  & Estoque: " + str(t.produzido) )
                    t.lock = "PaleGreen1"
                    #self.linhasParadas -=1
                if (t.produzido >= t.qtdMinimaItem):
                    checkProducao += 1

                r = r + 1
                
            if (checkProducao == 5):
                #print("Carro enviado para montagem !!")
                carros += 1
                self.montarCarro()
            if (self.carrosProntos >= 10):
                #print("Cegonheira carregada e sendo despachada !!")
                self.carrosProntos = 0



if __name__ == '__main__':

    # Inicia cada uma das instâncias da classe linha de produção com os valores padrões.
    T_motor       = linhaProducao("Motor ",1,12,0,10,False)
    T_carroceria  = linhaProducao("Carroceria ",1,15,0,20,False)
    T_pneus       = linhaProducao("Pneus ",4,9,0,100,False)
    T_banco       = linhaProducao("Banco ",5,6,0,25,False)
    T_eletronica  = linhaProducao("Eletrônica ",1,7,0,8,False)
    

    # Cria o pool de todas as threads da aplicação.
    poolThreads = []
    poolThreads.append(T_motor)
    poolThreads.append(T_carroceria)
    poolThreads.append(T_pneus)
    poolThreads.append(T_banco)
    poolThreads.append(T_eletronica)

    #Inicia todas as threads 
    T_controle = Controle(poolThreads)
    T_controle.start()
    T_motor.start()
    T_carroceria.start()
    T_pneus.start()
    T_banco.start()
    T_eletronica.start()

    root.mainloop()
    
    for t in poolThreads:
        t.join()
    
    T_controle.join()
    print("Processo terminado !!")
      
