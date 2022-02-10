import numpy as np
from collections import Counter
import random


class RandBotStrategy:
    def __init__(self):
        self.nextAction = 0

    def setObservations(self, ownPos, fieldDict):
        pass

    def getNextAction(self):
        pass

class Player:
    strategies = {"randombot":RandBotStrategy,}

    def __init__(self, name, playerType, startingSize):
        self.name = name
        self.playerType = playerType
        self.pos = np.zeros((2,))
        self.size = startingSize
        self.strategy = Player.strategies[playerType]
        self.active = True


class AdaptIOEngine:
    def __init__(self, mapstring, startingSize, minRatio, strategyDict, visionRange, updateMode):
        self.mapstring = mapstring
        self.field = self.prepareField()
        self.startField = self.field
        self.startingSize = startingSize
        self.minRatio = minRatio
        self.visionRange = visionRange
        self.updateMode = updateMode


        ids = list(range(4))
        random.shuffle(ids)

        self.players = [Player(list(strategyDict.keys())[ids[i]], list(strategyDict.values())[ids[i]], self.startingSize) for i in range(4)]

    def prepareField(self):
        # ertekek self.field-be, initben setelje valahogy, ugy hogy 0-4 kaja ertek, -1 fal
        # assertelni lehetne, hogy a size jo, vagy lehet helyette path/mapstring beadas is
        # self.size is legyen megfelelo
        pass

    def generateQuarterField(self):
        pass

    def makeAction(self, action, pos):
        pass

    def handleCollision(self, positions, oldPositions, valueToHandle):
        pass

    def surveyArea(self, pos):
        pass

    def updatePlayers(self, newpos):
        pass

    def updateFood(self):
        if self.updateMode=="static":
            return
        else:
            pass

    def checkCollision(self, newpos, oldpos):
        checked = False
        while not checked:
            checked = True
            counts = Counter(newpos)
            for collisionTile, cnt in counts.items():
                if cnt > 1:
                    newpos = self.handleCollision(newpos, oldpos, collisionTile)
                    checked = False

        return newpos


    def tick(self):
        actions = [player.strategy.getNextAction() for player in self.players]
        pos = [player.pos for player in self.players]

        newpos = []
        for i in range(len(self.players)):
            newpos.append(self.makeAction(actions[i], pos[i]))

        newpos = self.checkCollision(newpos, pos)
        self.updatePlayers(newpos)

        for i in range(len(self.players)):
            self.players[i].strategy.setObservations(self.players[i].pos, self.surveyArea(self.players[i].pos))

