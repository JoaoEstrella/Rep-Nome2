import numpy as np


class Pso:
    """Classe PSO:
        Author: João Vitor Coelho Estrela
    """

    def __init__(self, c1=2, c2=2, wMin=0.4, wMax=1.4, w=False):
        self.c1 = c1
        self.c2 = c2
        self.wMin = wMin
        self.wMax = wMax
        self.w = w

    def getParameters(self, pop):
        vRanges = (pop.ranges[:, 1] - pop.ranges[:, 0])/2
        return {'vRanges': vRanges}

    def start(self, pop):
        pop.createNewPop(0)
        pop.evalPop(0)

        for p in pop.pList:
            p['vel'] = np.empty_like(p['ch'])
            p['vel'][0, :] = np.random.uniform(-pop.parameters['vRanges'],
                                               pop.parameters['vRanges'],
                                               pop.parameters['vRanges'].shape[0])

        pTemp = pop.getBestPop(0)
        pop.pBest['ch'][0, :] = pTemp['ch'][0, :]
        pop.pBest['value'][0] = pTemp['value'][0]

        pop.pBest['vel'] = np.empty_like(pop.pBest['ch'])
        pop.pBest['vel'][0, :] = pTemp['vel'][0, :]

    def nextGen(self, pop):

        for j in pop.pList:
            w = 1
            r1 = np.random.random(j['ch'].shape[1])
            r2 = np.random.random(j['ch'].shape[1])

            persBest = j['ch'][j['value'][:pop.nG+1].argmin(), :]

            aa = (w*j['vel'][pop.nG-1, :]) + self.c1*r1*(persBest - j['ch'][pop.nG-1, :])
            bb = self.c2*r2*(pop.pBest['ch'][pop.nG-1, :] - j['ch'][pop.nG-1, :])  # trocar
            #bb = self.c2*r2*(self._getBestPop(self.pList, self.nG-1, self.minimize).ch[self.nG-1,:] -  j.ch[self.nG-1,:])

            # new Vel
            j['vel'][pop.nG, :] = np.clip(aa+bb, -pop.parameters['vRanges'], pop.parameters['vRanges'])

            # New Xvar
            j['ch'][pop.nG, :] = np.clip(j['vel'][pop.nG, :] + j['ch'][pop.nG-1, :],
                                         pop.ranges[:, 0], pop.ranges[:, 1])

        pop.evalPop(pop.nG)

        pTemp = pop.getBestPop(pop.nG)

        pop.pBestUpdate(pTemp, pop.nG)
