from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Heuristica(ABC):

    @property
    def objective(self):
        """
        FO encapsulada para permitir a contagem de chamadas nfc em cada gen
        """
        self.nfc[self.nG] = self.nfc[self.nG] + 1
        return self._objective

    def createNewPop(self, nG):
        """
        Cria e define uma pop em nG
        """
        pop_temp = np.random.uniform(self.ranges[:, 0], self.ranges[:, 1],
                                     size=(self.nPop, self.ranges.shape[0]))

        for i, p in enumerate(self.pList):
            p['ch'][nG, :] = pop_temp[i, :]

    def getDataPop(self, nParticles):
        """
        Cria uma matriz numpy (n, nVar) para um dado n
        """
        return np.random.uniform(self.ranges[:, 0], self.ranges[:, 1],
                                 size=(nParticles, self.ranges.shape[0]))

    def evalPop(self, nG):
        """
        Avalia todas particulas da nG
        """
        for p in self.pList:
            p['value'][nG] = self.objective(p['ch'][nG, :])

    def sortPop(self, nG):
        """
        Ordena a pList do melhor para o pior
        """
        if self.minimize:
            self.pList.sort(key=lambda p: p['value'][nG])
        else:
            self.pList.sort(key=lambda p: p['value'][nG], reverse=True)

    def getGen(self, nG):
        """
        Retorna um DataFrame da pop em uma dada nG que contém
        as variáveis e o valor avaliado.
        """
        df = pd.DataFrame(np.stack(
                         [self.pList[p]['ch'][nG] for p in range(self.nPop)]),
                         index=[self.pList[p]['id'] for p in range(self.nPop)]
                         )

        df['val'] = [self.pList[p]['value'][nG] for p in range(self.nPop)]
        return df

    def getPbest(self):
        """
        Retorna um DataFrame do pBest.
        """
        df = pd.DataFrame(np.stack(
                          [self.pBest['ch'][nG] for nG in range(self.nGen)]))

        df['val'] = [self.pBest['value'][nG] for nG in range(self.nGen)]
        return df

    def getBestPop(self, nG):
        """
        Retorna a referencia da melhor particula da lista em uma dada nG
        """
        if self.minimize:
            pTemp = min(self.pList, key=lambda p: p['value'][nG])
        else:
            pTemp = max(self.pList, key=lambda p: p['value'][nG])

        return pTemp

    def isPaBetterPb(self, a, b):
        """
        Retorna o booleano True se o valor da 'pA' é melhor que da 'pB'
        """
        if self.minimize and (a < b):
            return True
        elif not self.minimize and (a > b):
            return True
        else:
            return False

    def pBestUpdate(self, pTemp, nG, isEqual=False):
        """
        Verifica se a pTemp é melhor que a pBest da gen anterior,
        se sim já define
        """
        if self.isPaBetterPb(pTemp['value'][nG], self.pBest['value'][nG-1]):
            self.pBest['ch'][nG, :] = pTemp['ch'][nG, :]
            self.pBest['value'][nG] = pTemp['value'][nG]

        elif isEqual and (self.pBest['value'][nG] == pTemp['value'][nG]):
            self.pBest['ch'][nG, :] = pTemp['ch'][nG, :]
            self.pBest['value'][nG] = pTemp['value'][nG]

        else:
            self.pBest['ch'][nG, :] = self.pBest['ch'][nG-1, :]
            self.pBest['value'][nG] = self.pBest['value'][nG-1]

    def getNeighbor(self, ch, sig=0.02):
        """
        Retorna um vizinho dado um sig de x% do range
        """
        return np.random.normal(loc=ch, scale=(self.ranges[:, 1] -
                                               self.ranges[:, 0])*sig)
