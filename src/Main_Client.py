import time

from Client import SocketClient
import json
import numpy as np


# TODO: csinalj egy strategy-t ami evoluciosan tanit egy ann-t
class NaiveHunterStrategy:
    def __init__(self, **kwargs):
        self.nextAction = "0"
        self.oldpos = None
        self.oldcounter = 0

    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]

        return action

    def processObservation(self, fulljson, sendData):
        #print(fulljson)
        if fulljson["type"] == "leaderBoard":
            print("Game finished after",fulljson["payload"]["ticks"],"ticks!")
            print("Leaderboard:")
            for score in fulljson["payload"]["players"]:
                print(score["name"],score["active"], score["maxSize"])

            time.sleep(50)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))

        if fulljson["type"] == "readyToStart":
            print("Game is ready, starting in 5")
            time.sleep(5)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "start", "data": {"mapPath": None, "updateMapPath": None}}}))

        if fulljson["type"] == "started":
            print("Startup message from server.")
            print("Ticks interval is:",fulljson["payload"]["tickLength"])

        elif fulljson["type"] == "gameData":
            jsonData = fulljson["payload"]
            if "pos" in jsonData.keys() and "tick" in jsonData.keys() and "active" in jsonData.keys() and "size" in jsonData.keys() and "vision" in jsonData.keys():

                if self.oldpos is not None:
                    if tuple(self.oldpos) == tuple(jsonData["pos"]):
                        self.oldcounter += 1
                    else:
                        self.oldcounter = 0
                if jsonData["active"]:
                    self.oldpos = jsonData["pos"].copy()

                vals = []
                for field in jsonData["vision"]:
                    if field["player"] is not None:
                        if tuple(field["relative_coord"]) == (0, 0):
                            if 0 < field["value"] <= 3:
                                vals.append(field["value"])
                            elif field["value"] == 9:
                                vals.append(-1)
                            else:
                                vals.append(0)
                        elif field["player"]["size"] * 1.1 < jsonData["size"]:
                            vals.append(field["player"]["size"])
                        else:
                            vals.append(-1)
                    else:
                        if 0 < field["value"] <= 3:
                            vals.append(field["value"])
                        elif field["value"] == 9:
                            vals.append(-1)
                        else:
                            vals.append(0)

                values = np.array(vals)
                if np.max(values) <= 0 or self.oldcounter >= 3:
                    actstring = self.getRandomAction()
                    self.oldcounter = 0
                else:
                    idx = np.argmax(values)
                    actstring = ""
                    for i in range(2):
                        if jsonData["vision"][idx]["relative_coord"][i] == 0:
                            actstring += "0"
                        elif jsonData["vision"][idx]["relative_coord"][i] > 0:
                            actstring += "+"
                        elif jsonData["vision"][idx]["relative_coord"][i] < 0:
                            actstring += "-"

                sendData(json.dumps({"command": "SetAction", "name": "Nata", "payload": actstring}))


hunter = NaiveHunterStrategy()

client = SocketClient("localhost", 42069, hunter.processObservation)
client.start()
time.sleep(0.1)
client.sendData(json.dumps({"command": "SetName", "name": "Nata", "payload": None}))
# client.sendData(json.dumps({"command": "GameControl", "name": "master", "payload": {"type":"reset", "data":{"mapPath":None, "updateMapPath":None}}}))
