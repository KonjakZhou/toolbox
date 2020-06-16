import random
import numpy as np
import json

class Partner(object):
    def __init__(self):
        self._strategyQueue = None
        self.reset()

    def reset(self):
        self._strategyQueue = list()
        self._strategyQueue.append(random.randint(0,2))

    def appendNextGesture(self, OLG):    #opponentLastGesture
        pass

    @staticmethod
    def _numberGestureConverter(arg):
        G2N = {'Rock':0, 'Paper':1, 'Scissors':2}
        N2G = dict(zip(G2N.values(),G2N.keys()))

        if str(arg).isdigit():
            return N2G[arg]
        return G2N[arg]

    @staticmethod
    def _gestureCalculator(base, strategy):
        return (base + strategy) % 3

    @property
    def strategyQueue(self):
        return self._strategyQueue

class Repeater(Partner):    #策略永远不变
    def appendNextGesture(self, OLG):    #opponentLastGesture
        self._strategyQueue.append(self._strategyQueue[-1])

class OpponentWinner(Partner):       #永远针对对手上一个,基于对方手势针对一轮
    def appendNextGesture(self, OLG):    #opponentLastGesture
        gesture = self._gestureCalculator(OLG, 1)
        self._strategyQueue.append(gesture)

class Imitator(Partner):    #永远模仿对手上一个,基于对方手势针对两轮
    def appendNextGesture(self, OLG):    #opponentLastGesture
        self._strategyQueue.append(OLG)

class OpponentLoser(Partner):#永远出败于对手上一个，实际基于对方手势针对三轮
    def appendNextGesture(self, OLG):    #opponentLastGesture
        gesture = self._gestureCalculator(OLG, 2)
        self._strategyQueue.append(gesture)

class SelfLoser(Partner):   #永远出败于自己上一个，实际基于对方思路针对一轮
    def appendNextGesture(self, OLG):    #opponentLastGesture
        gesture = self._gestureCalculator(self._strategyQueue[-1], 2)
        self._strategyQueue.append(gesture)

class SelfWinner(Partner):  #永远出战胜自己上一个，实际基于对方思路针对两轮
    def appendNextGesture(self, OLG):    #opponentLastGesture
        gesture = self._gestureCalculator(self._strategyQueue[-1], 1)
        self._strategyQueue.append(gesture)

class Randomer(Partner):    #随机手势
    def appendNextGesture(self, OLG):
        gesture = random.randint(0,2)
        self._strategyQueue.append(gesture)

class Referee(object):
    def __init__(self, members,Format):
        self._members = members
        if Format[:2]!='BO':
            raise Exception("error: not a True game format")
        self._numOfRounds = int(Format[2:])
        self._numOfMembers = len(self._members)
        self._result = list()
        self._multiMatchResult = list()

    def match(self):
        result = list()
        for i in range(self._numOfMembers):
            current = list()
            for j in range(i):
                current.append(result[j][i])
            for j in range(i, self._numOfMembers):
                r = self._battle(self._members[i], self._members[j])
                if r>0:
                    current.append(1)
                elif r==0:
                    current.append(0)
                else:
                    current.append(-1)
            result.append(current)
            self._result = result

    @property
    def result(self):
        formatResult = list()
        winCounts, winRatio = self._statisticsOfWinning(withSelf=True)
        for i in range(self._numOfMembers):
            formatResult.append([winCounts[i], "{:.2f}%".format(winRatio[i]*100),
                                 self._result[i]])
        return formatResult

    def multiMatch(self, times, withSelf=False):
        average = np.zeros(shape=self._numOfMembers)
        for k in range(times):
            self.match()
            _, winRatio = self._statisticsOfWinning(withSelf=withSelf)
            average = np.sum([average, winRatio], axis=0)
        average = average/ times
        self._multiMatchResult = average

    @property
    def multiMatchResult(self):
        result = ["{:.2f}%".format(self._multiMatchResult[i] * 100)
                  for i in range(self._numOfMembers)]
        return result


    def _battle(self,A,B):  #A and B are two type of players of one game
        a = A()
        b = B()
        for k in range(1, self._numOfRounds):
            aLast = a.strategyQueue[-1]
            bLast = b.strategyQueue[-1]
            a.appendNextGesture(bLast)
            b.appendNextGesture(aLast)
        r = 0
        for k in range(self._numOfRounds):
            r += self._ruling(a.strategyQueue[k], b.strategyQueue[k])
        return r

    def _statisticsOfWinning(self, withSelf = False):
        winCounts = list()
        for i in range(self._numOfMembers):
            winCounts.append(self._result[i].count(1))
            if not withSelf:
                if self._result[i][i] == 1:
                    winCounts[-1] -= 1
        winRatio = np.array(winCounts)/self._numOfMembers
        return winCounts,winRatio

    @staticmethod
    def _ruling(a,b):    #1: a wins b; 0: a equals b; -1: b wins a
        result =  (a - b + 3) % 3
        if result == 2:
            result = -1
        return result

if __name__ == '__main__':
    players = {'Imitator':Imitator, 'OpponentLoser':OpponentLoser,
               'OpponentWinner':OpponentWinner, 'Repeater':Repeater,
               'SelfLoser':SelfLoser, 'SelfWinner':SelfWinner, 'Randomer':Randomer}
    arena = Referee(list(players.values()), 'BO5')
    arena.match()
    testResult = dict(zip(players.keys(),arena.result))
    print(json.dumps(testResult, sort_keys=True, indent=4))

    arena.multiMatch(10000, withSelf=False)
    testResult = dict(zip(players.keys(),arena.multiMatchResult))
    print(json.dumps(testResult, sort_keys=True, indent=4))

    arena.multiMatch(10000, withSelf=True)
    testResult = dict(zip(players.keys(),arena.multiMatchResult))
    print(json.dumps(testResult, sort_keys=True, indent=4))
