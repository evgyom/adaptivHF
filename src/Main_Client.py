from Client import SocketClient
import json
import numpy as np



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

    def processObservation(self, jsonData, sendData):
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
                if tuple(field["relative_coord"])==(0,0):
                    if 0 < field["value"] <= 3:
                        vals.append(field["value"])
                    elif field["value"] == 9:
                        vals.append(-1)
                    else:
                        vals.append(0)
                elif field["player"]["size"]*1.1<jsonData["size"]:
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
        #print(values, jsonData["vision"][np.argmax(values)]["relative_coord"], values.max())
        if np.max(values) <= 0 or self.oldcounter>=3:
            self.nextAction = self.getRandomAction()
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

            sendData(json.dumps({"command":"SetAction","name":"Nata","payload":actstring}))


hunter = NaiveHunterStrategy()


client = SocketClient("46.107.162.203",25660, hunter.processObservation)
client.start()
client.sendData(json.dumps({"command": "SetName", "name": "Nata", "payload": None}))