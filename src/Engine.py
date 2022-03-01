import numpy as np
from collections import Counter
import random


class RandBotStrategy:
    def __init__(self):
        self.nextAction = 0

    def setObservations(self, ownPos, fieldDict):
        pass

    def getNextAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action


class NaiveStrategy:
    def __init__(self):
        self.nextAction = "0"

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def setObservations(self, ownPos, fieldDict):
        values = np.array([field["value"] for field in fieldDict["vision"]])
        values[values > 3] = 0
        values[values < 0] = 0
        if np.max(values) == 0:
            self.nextAction = self.getRandomAction()
        else:
            idx = np.argmax(values)
            actstring = ""
            for i in range(2):
                if fieldDict["vision"][idx]["relative_coord"][i] == 0:
                    actstring += "0"
                elif fieldDict["vision"][idx]["relative_coord"][i] > 0:
                    actstring += "+"
                elif fieldDict["vision"][idx]["relative_coord"][i] < 0:
                    actstring += "-"

            self.nextAction = actstring

    def getNextAction(self):
        return self.nextAction


class Player:
    strategies = {"randombot": RandBotStrategy, "naivebot": NaiveStrategy}

    def __init__(self, name, playerType, startingSize):
        self.name = name
        self.playerType = playerType
        self.pos = np.zeros((2,))
        self.size = startingSize
        self.strategy = Player.strategies[playerType]()
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

    def __init__(self, mapPath, startingSize, minRatio, strategyDict, visionRange, updateMode):
        self.mapPath = mapPath
        self.field, self.size = self.prepareField(self.mapPath)
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

        diffFromSide = 2
        self.players[0].pos = np.array([0 + diffFromSide, 0 + diffFromSide])
        self.players[1].pos = np.array([self.size - diffFromSide, 0 + diffFromSide])
        self.players[2].pos = np.array([0 + diffFromSide, self.size - diffFromSide])
        self.players[3].pos = np.array([self.size - diffFromSide, self.size - diffFromSide])

    def genVisibilityMask(self):
        coordlist = []
        for i in np.arange(-self.visionRange, self.visionRange + 1):
            for j in np.arange(-self.visionRange, self.visionRange + 1):
                if np.sqrt(i ** 2 + j ** 2) <= self.visionRange:
                    coordlist.append((i, j))

        return coordlist

    def prepareField(self, mapPath):
        field = np.transpose(np.loadtxt(mapPath))
        size = field.shape[0]
        return field, size
        # ertekek self.field-be, initben setelje valahogy, ugy hogy 0-4 kaja ertek, -1 fal
        # assertelni lehetne, hogy a size jo, vagy lehet helyette path/mapstring beadas is
        # self.size is legyen megfelelo

    def checkBound(self, pos):
        if not 0 <= pos[0] < self.size or not 0 <= pos[1] < self.size:
            return False
        if self.field[pos[0], pos[1]] == 9:
            return False
        else:
            return True

    def makeAction(self, action, pos):
        oldpos = pos.copy()
        if action == "0":
            return pos
        if action[0] == "-":
            pos[0] -= 1
        if action[0] == "+":
            pos[0] += 1
        if action[1] == "-":
            pos[1] -= 1
        if action[1] == "+":
            pos[1] += 1

        if not self.checkBound(pos):
            pos = oldpos
        return pos

    def handleCollision_randomized(self, positions, oldPositions, valueToHandle):
        newpos = positions.copy()
        displacements = list(self.neighbourDifferencies.values())
        random.shuffle(displacements)

        colliding = []
        for i in range(len(positions)):
            if positions[i] == valueToHandle:
                colliding.append(i)

        sizes = np.array([self.players[i].size for i in colliding])
        idx = np.argsort(sizes)
        if sizes[idx[0]] >= sizes[idx[1]] * self.minRatio:
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

    def handleCollision_oldpos(self, positions, oldPositions, valueToHandle):
        newpos = positions.copy()

        colliding = []
        for i in range(len(positions)):
            if tuple(positions[i]) == tuple(valueToHandle):
                colliding.append(i)

        sizes = np.array([self.players[i].size for i in colliding])
        idx = np.argsort(sizes)
        if sizes[idx[0]] >= sizes[idx[1]] * self.minRatio:
            newsize = np.sum(sizes)
            colliding.remove(colliding[idx[0]])
            for dead in colliding:
                self.players[dead].die()

            self.players[idx[0]].size = newsize

        else:
            j = 0
            for i in colliding:
                newpos[i] = oldPositions[i].copy()
                j += 1
        return newpos

    def surveyArea(self, pos):
        observation = {"pos": pos, "vision": []}
        playerpos = [tuple(player.pos) for player in self.players]
        for diffcoord in self.visibilityMask:
            vispos = pos + np.array(diffcoord)
            if tuple(vispos) in playerpos:
                playerDict = {}
                playerDict["size"] = self.players[playerpos.index(tuple(vispos))].size
                playerDict["name"] = self.players[playerpos.index(tuple(vispos))].name
            else:
                playerDict = None

            if not 0 <= vispos[0] < self.size or not 0 <= vispos[1] < self.size:
                val = 9
            else:
                val = self.field[int(vispos[0]), int(vispos[1])]
            observation["vision"].append({"relative_coord": diffcoord, "value": val, "player": playerDict})

        return observation

    def updatePlayers(self, newpos):
        for i in range(len(self.players)):
            self.players[i].pos = newpos[i]
            if 0 < self.field[newpos[i][0], newpos[i][1]] <= 3:
                self.players[i].size += self.field[newpos[i][0], newpos[i][1]]
                self.field[newpos[i][0], newpos[i][1]] = 0

    def updateFood(self):
        if self.updateMode == "static":
            return
        else:
            pass

    def checkCollision(self, newpos, oldpos):
        checked = False
        while not checked:
            checked = True
            counts = Counter([tuple(n) for n in newpos])
            for collisionTile, cnt in counts.items():
                if cnt > 1:
                    newpos = self.handleCollision_oldpos(newpos, oldpos, collisionTile)
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

        self.updateFood()

        for i in range(len(self.players)):
            self.players[i].strategy.setObservations(self.players[i].pos, self.surveyArea(self.players[i].pos))
