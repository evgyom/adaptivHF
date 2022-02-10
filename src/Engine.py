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
    strategies = {"randombot": RandBotStrategy, }

    def __init__(self, name, playerType, startingSize):
        self.name = name
        self.playerType = playerType
        self.pos = np.zeros((2,))
        self.size = startingSize
        self.strategy = Player.strategies[playerType]
        self.active = True

    def die(self):
        pass


class AdaptIOEngine:
    neighbourDifferencies = {0: np.array([0, 1]), 1: np.array([0, -1]), 2: np.array([1, 0]), 3: np.array([-1, 0])}

    @staticmethod
    def getRandomNeighbor(pos):
        r = random.randint(0, 3)
        if r == 0:
            return pos + np.array([0, 1])
        elif r == 1:
            return pos + np.array([0, -1])
        elif r == 2:
            return pos + np.array([1, 0])
        elif r == 3:
            return pos + np.array([-1, 0])

    def __init__(self, mapstring, startingSize, minRatio, strategyDict, visionRange, updateMode):
        self.mapstring = mapstring
        self.field, self.size = self.prepareField()
        self.startField = self.field
        self.startingSize = startingSize
        self.minRatio = minRatio
        self.visionRange = visionRange
        self.updateMode = updateMode
        self.visibilityMask = self.genVisibilityMask()

        ids = list(range(4))
        random.shuffle(ids)

        self.players = [
            Player(list(strategyDict.keys())[ids[i]], list(strategyDict.values())[ids[i]], self.startingSize) for i in
            range(4)]

    def genVisibilityMask(self):
        coordlist = []
        for i in np.arange(-self.visionRange, self.visionRange+1):
            for j in np.arange(-self.visionRange, self.visionRange+1):
                if np.sqrt(i**2+j**2)<=self.visionRange:
                    coordlist.append((i, j))

        return coordlist

    def prepareField(self):
        # ertekek self.field-be, initben setelje valahogy, ugy hogy 0-4 kaja ertek, -1 fal
        # assertelni lehetne, hogy a size jo, vagy lehet helyette path/mapstring beadas is
        # self.size is legyen megfelelo
        pass

    def generateQuarterField(self):
        pass

    def makeAction(self, action, pos):
        if action=="0":
            return pos
        if action[0]=="-":
            pos[0]-=1
        if action[0]=="+":
            pos[0]+=1
        if action[1]=="-":
            pos[1]-=1
        if action[1]=="+":
            pos[1]+=1
        return pos

    def handleCollision(self, positions, oldPositions, valueToHandle):
        newpos = positions.copy()
        displacements = list(self.neighbourDifferencies.values())
        random.shuffle(displacements)

        colliding = []
        for i in range(len(positions)):
            if positions[i] == valueToHandle:
                colliding.append(i)

        sizes = np.array([self.players[i].size for i in colliding])
        idx = np.argsort(sizes)
        if sizes[idx[0]] >= sizes[idx[1]]*self.minRatio:
            newsize = np.sum(sizes)
            colliding.remove(colliding[idx[0]])
            for dead in colliding:
                self.players[dead].die()

            self.players[idx[0]].size = newsize

        else:
            j = 0
            for i in colliding:
                newpos[i] += displacements[j]
                j += 1
        return newpos

    def surveyArea(self, pos):
        observation = {"pos": pos, "vision":[]}
        playerpos = [player.pos for player in self.players]
        for diffcoord in self.visibilityMask:
            vispos = pos + np.array(diffcoord)
            if vispos in playerpos:
                playerDict = {}
                playerDict["size"] = self.players[playerpos.index(vispos)].size
                playerDict["name"] = self.players[playerpos.index(vispos)].name
            else:
                playerDict = None

            if not 0<=vispos[0]<=self.size or not 0<=vispos[1]<=self.size:
                val = -1
            else:
                val = self.field[vispos[0],vispos[1]]
            observation["vision"].append({"relative_coord":diffcoord, "value":val, "player":playerDict})

        return observation


    def updatePlayers(self, newpos):
        for i in range(len(self.players)):
            self.players[i].pos = newpos[i]

    def updateFood(self):
        if self.updateMode == "static":
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
