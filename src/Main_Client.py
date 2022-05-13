#encoding: utf-8
from datetime import datetime

import time
from Client import SocketClient
import json
import numpy as np
from numpy.random import choice

import torch
from torch import nn
from torch import optim

TRAIN = False
PATH = r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\model_4.p"

actions = ["00","0+","0-","+0","+-","++","-0","--","-+"]
num_episodes= 2000
batch_size= 10
total_end_sizes = []

# NaiveHunter stratégia implementációja távoli eléréshez.
class RemoteStrategy:

    def __init__(self):
        # Dinamikus viselkedéshez szükséges változók definíciója
        self.oldpos = None
        self.oldcounter = 0
        # Game params
        self.oldsize = 5
        self.last_action = None
        self.last_state = None

        self.total_rewards = []
        self.batch_rewards = []
        self.batch_actions = []
        self.batch_states = []

        self.states = []
        self.rewards = []
        self.actions = []

        self.batch_counter = 0
        self.ep_counter = 1

        self.network = nn.Sequential(
            nn.Linear(81, 256), 
            nn.ReLU(),
            nn.Linear(256, 256), 
            nn.ReLU(), 
            nn.Linear(256, 128), 
            nn.ReLU(), 
            nn.Linear(128, 32), 
            nn.ReLU(), 
            nn.Linear(32, 9), 
            nn.Softmax(dim=-1))     

        self.optimizer = optim.Adam(self.network.parameters(),lr=0.001)
        
    #
    def predict(self, state):
        action_probs = self.network(torch.FloatTensor(state))
        return action_probs

    def discount_rewards(self, rewards_in, gamma=0.99):
        r = np.array([gamma**i * rewards_in[i] for i in range(len(rewards_in))])
            # Reverse the array direction for cumsum and then
            # revert back to the original order
        r = r[::-1].cumsum()[::-1]
        return r - r.mean()

    def convert_action_string_to_one_hot(self, act_str):
        ret_val = []
        for act in actions:
            if(act == act_str):
                ret_val.append(1)
            else:
                ret_val.append(0)
        return ret_val

    # Egyéb függvények...
    def getRandomAction(self):
        actdict = {0: "0", 1: "+", 2: "-"}
        r = np.random.randint(0, 3, 2)
        action = ""
        for act in r:
            action += actdict[act]
        return action

    # Az egyetlen kötelező elem: A játékmestertől jövő információt feldolgozó és választ elküldő függvény
    def processObservation(self, fulljson, sendData):
        # Játék rendezéssel kapcsolatos üzenetek lekezelése
        if fulljson["type"] == "leaderBoard":
            #print("-- Game finished after",fulljson["payload"]["ticks"],"ticks! --")
            #print("Leaderboard:")

            self.ep_counter += 1
           
            for score in fulljson["payload"]["players"]:
                if(score["name"] == "RemotePlayer"):
                    print("  score:", score["maxSize"])
                    if(score["active"]):
                        total_end_sizes.append(score["maxSize"])
                    else:
                        total_end_sizes.append(0)            
            if(TRAIN):
                if(self.ep_counter % 20 == 0):
                    torch.save(self.network.state_dict(), r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\\"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S' + '.p'))
                    with open("end_sizes.txt","w") as f:
                        for element in total_end_sizes:
                            f.write(str(element) + ";")

                self.batch_counter += 1
                self.total_rewards.append(sum(self.rewards))
                self.batch_rewards.extend(self.discount_rewards(self.rewards))
                self.batch_states.extend(self.states)
                self.batch_actions.extend(self.actions)
                #Clear
                self.states = []
                self.rewards = []
                self.actions = []
                self.last_action = None

                if(self.batch_counter < batch_size):
                    time.sleep(0.1)                    
                    sendData(json.dumps({"command": "GameControl", "name": "master",
                                        "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))            
                else:
                    self.optimizer.zero_grad()
                    state_tensor = torch.FloatTensor(np.array(self.batch_states))
                    reward_tensor = torch.FloatTensor(np.array(self.batch_rewards))
                    #print("rewards", reward_tensor)
                    
                    # Actions are used as indices, must be 
                    # LongTensor
                    action_tensor = torch.LongTensor(self.batch_actions)
                    #print("action tensor", action_tensor)
                    pred = self.predict(state_tensor)
                    #print("preds", pred)
                    selected_preds = torch.sum(pred * action_tensor,dim = 1)
                    #print("selected_preds", selected_preds)
                    selected_logprobs = reward_tensor*torch.log(selected_preds)
                    #print("selected_logprobs", selected_logprobs)
                    loss = -selected_logprobs.sum()
                    print(self.ep_counter,"--- Loss:", loss.item())

                    # Calculate gradients
                    loss.backward()

                    grads = []
                    for param in self.network.parameters():
                        grads.append(param.grad)

                    # Apply gradients
                    self.optimizer.step()

                    self.batch_rewards = []
                    self.batch_actions = []
                    self.batch_states = []
                    self.batch_counter = 0

                    if(self.ep_counter >= num_episodes):
                        sendData(json.dumps({"command": "GameControl", "name": "master","payload": {"type": "interrupt", "data": None}}))
                        #Save the last model as well
                        torch.save(self.network.state_dict(), r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\\"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S' + '.p'))
                        with open("end_sizes.txt","w") as f:
                            for element in total_end_sizes:
                                f.write(str(element) + ";")
                    else:
                        sendData(json.dumps({"command": "GameControl", "name": "master",
                                        "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))
            else:
                if(self.ep_counter >= num_episodes):
                    time.sleep(0.1)
                    sendData(json.dumps({"command": "GameControl", "name": "master","payload": {"type": "interrupt", "data": None}}))
                else:
                    time.sleep(0.1)
                    sendData(json.dumps({"command": "GameControl", "name": "master",
                                        "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))

        if fulljson["type"] == "readyToStart":
            time.sleep(0.1)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "start", "data": None}}))

        if fulljson["type"] == "started":
            pass
            #print("Startup message from server.")
            #print("Ticks interval is:",fulljson["payload"]["tickLength"])

        # Akció előállítása bemenetek alapján
        elif fulljson["type"] == "gameData":
            jsonData = fulljson["payload"]
            if "pos" in jsonData.keys() and "tick" in jsonData.keys() and "active" in jsonData.keys() and "size" in jsonData.keys() and "vision" in jsonData.keys():
                if self.oldpos is not None:
                    if tuple(self.oldpos) == tuple(jsonData["pos"]):
                        self.oldcounter += 1
                    else:
                        self.oldcounter = 0
                

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
                            vals.append(-1*field["player"]["size"])
                    else:
                        if 0 < field["value"] <= 3:
                            vals.append(field["value"])
                        elif field["value"] == 9:
                            vals.append(-1)
                        else:
                            vals.append(0)
                
                #Vision
                state = np.array(vals)
                pred = self.predict(state).detach().numpy()
                
                if(TRAIN):
                    #Calculate reward for last action
                    reward = 0
                    if(not jsonData["active"]):
                        reward = -99
                    else:
                        reward = jsonData["size"] - self.oldsize

                    if jsonData["active"]:
                        if(self.oldpos != jsonData["pos"]):
                            reward+=0.1
                        self.oldpos = jsonData["pos"].copy()
                    

                    #print("last_action:", self.last_action, "reward:", reward)

                    #Store the training data
                    if(self.last_action != None):
                        self.states.append(self.last_state)
                        self.rewards.append(reward)
                        self.actions.append(self.convert_action_string_to_one_hot(self.last_action))

                    actstring = choice(actions, 1, p=pred/np.sum(pred))[0]
                    self.last_state = state
                    self.last_action = actstring
                    self.oldsize = jsonData["size"]
                else:
                    print(pred)
                    #actstring = actions[np.argmax(pred)]
                    actstring = choice(actions, 1, p=pred/np.sum(pred))[0]
                    print(actstring)

                # Akció JSON előállítása és elküldése
                sendData(json.dumps({"command": "SetAction", "name": "RemotePlayer", "payload": actstring}))


if __name__=="__main__":
    # Példányosított stratégia objektum
    hunter = RemoteStrategy()
    try:
        hunter.network.load_state_dict(torch.load(PATH))
        print("loaded model")
    except:
        pass
    hunter.network.train()

    # Socket kliens, melynek a szerver címét kell megadni (IP, port), illetve a callback függvényt, melynek szignatúrája a fenti
    # callback(fulljson, sendData)
    client = SocketClient("localhost", 42069, hunter.processObservation)

    # Kliens indítása
    client.start()
    # Kis szünet, hogy a kapcsolat felépülhessen, a start nem blockol, a kliens külső szálon fut
    time.sleep(0.1)
    # Regisztráció a megfelelő névvel
    client.sendData(json.dumps({"command": "SetName", "name": "RemotePlayer", "payload": None}))

    # Nincs blokkoló hívás, a főszál várakozó állapotba kerül, itt végrehajthatók egyéb műveletek a kliens automata működésétől függetlenül.