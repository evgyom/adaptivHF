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

TRAIN = True
ACTIONS = ["00","0-","0+","+0","+-","++","-0","--","-+"]
num_episodes= 1000
batch_size= 10
total_end_sizes = []

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
            nn.Linear(256, 128), 
            nn.ReLU(), 
            nn.Linear(128, 32), 
            nn.ReLU(), 
            nn.Linear(32, 9), 
            nn.Softmax(dim=-1))     

        self.optimizer = optim.Adam(self.network.parameters(),lr=1e-4)
        
    # Perform prediction based on agent state
    def predict(self, state):
        action_probs = self.network(torch.FloatTensor(state))
        return action_probs

    # Discount the rewards 
    def discount_rewards(self, r, gamma=0.99):
        discounted_r = np.zeros_like(r)
        running_add = 0
        for t in reversed(range(len(r))):
            running_add = running_add * gamma + r[t]
            discounted_r[t] = running_add
        return discounted_r

    # Convert the action string to one hot encoded vector
    def convert_action_string_to_one_hot(self, act_str):
        ret_val = []
        for act in ACTIONS:
            if(act == act_str):
                ret_val.append(1)
            else:
                ret_val.append(0)
        return ret_val

    # Get the state based on the JSON input
    def getState(self, jsonData):
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
        return np.array(vals)

    # Calculate the reward
    def calculate_reward(self, jsonData):
        #Calculate reward for last action
        reward = 0
        if(not jsonData["active"]):
            reward = -99
        else:
            reward = jsonData["size"] - self.oldsize
            if(self.oldpos != jsonData["pos"]):
                reward+=0.1   
        return reward

    # Do one training step
    def train_step(self):
        self.optimizer.zero_grad()

        state_tensor = torch.FloatTensor(np.array(self.batch_states))
        reward_tensor = torch.FloatTensor(np.array(self.batch_rewards))
        action_tensor = torch.LongTensor(self.batch_actions)

        pred = self.predict(state_tensor)

        selected_preds = torch.sum(pred * action_tensor,dim = 1)
        selected_logprobs = reward_tensor*torch.log(selected_preds)
        loss = -selected_logprobs.sum()
        print(self.ep_counter-1,"--- Loss:", loss.item())
        # Calculate gradients
        loss.backward()
        # Apply gradients
        self.optimizer.step()

    # Save the model
    def save_model(self):
        torch.save(self.network.state_dict(), r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\\"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S' + '.p'))

    # Send reset game message
    def reset_game(self, sendDataFunc):
        sendDataFunc(json.dumps({"command": "GameControl", "name": "master",
                                        "payload": {"type": "reset", "data": {"mapPath": None, "updateMapPath": None}}}))

    # Send interrupt game message
    def interrupt_game(self, sendDataFunc):
        sendDataFunc(json.dumps({"command": "GameControl", "name": "master","payload": {"type": "interrupt", "data": None}}))

    # Process the received data
    def processObservation(self, fulljson, sendData):

        #At the end of game
        if fulljson["type"] == "leaderBoard":
            self.ep_counter += 1
           
            for score in fulljson["payload"]["players"]:
                if(score["name"] == "RemotePlayer"):
                    print("  score:", score["maxSize"])
                    if(score["active"]):
                        total_end_sizes.append(score["maxSize"])
                    else:
                        total_end_sizes.append(0)            
            if(TRAIN):
                if(self.ep_counter % 100 == 0):
                    #Save model
                    self.save_model()

                # Add to batch data
                self.batch_counter += 1
                self.total_rewards.append(sum(self.rewards))
                self.batch_rewards.extend(self.discount_rewards(self.rewards))
                self.batch_states.extend(self.states)
                self.batch_actions.extend(self.actions)

                #Clear episode data
                self.states = []
                self.rewards = []
                self.actions = []
                self.last_action = None

                if(self.batch_counter < batch_size):
                    time.sleep(0.1)                    
                    self.reset_game(sendData)            
                else:
                    self.train_step()

                    #Clear batch data
                    self.batch_rewards = []
                    self.batch_actions = []
                    self.batch_states = []
                    self.batch_counter = 0

                    if(self.ep_counter >= num_episodes):
                        self.interrupt_game(sendData)
                        #Save the last model
                        self.save_model()
                    else:
                        self.reset_game(sendData)            
            else:
                # In eval mode
                if(self.ep_counter >= num_episodes):
                    time.sleep(0.1)
                    self.interrupt_game(sendData)
                else:
                    time.sleep(0.1)
                    self.reset_game(sendData)

        # Start game
        if fulljson["type"] == "readyToStart":
            time.sleep(0.01)
            sendData(json.dumps({"command": "GameControl", "name": "master",
                                 "payload": {"type": "start", "data": None}}))

        # Prepare action based on game data
        elif fulljson["type"] == "gameData":
            jsonData = fulljson["payload"]
            if "pos" in jsonData.keys() and "tick" in jsonData.keys() and "active" in jsonData.keys() and "size" in jsonData.keys() and "vision" in jsonData.keys():              
                # Get the state based on the JsonData
                state = self.getState(jsonData)
                # Predict the actions
                pred = self.predict(state).detach().numpy()
                
                if(TRAIN):
                    #Calculate the rewards
                    reward = self.calculate_reward(jsonData)
                    #Store the training data
                    if(self.last_action != None):
                        self.states.append(self.last_state)
                        self.rewards.append(reward)
                        self.actions.append(self.convert_action_string_to_one_hot(self.last_action))
                    # Select action
                    actstring = choice(ACTIONS, 1, p=pred/np.sum(pred))[0]
                    # Update old status values
                    self.last_state = state
                    self.last_action = actstring
                    self.oldsize = jsonData["size"]
                    self.oldpos = jsonData["pos"].copy()
                else:
                    print(pred)
                    #actstring = actions[np.argmax(pred)]
                    actstring = choice(ACTIONS, 1, p=pred/np.sum(pred))[0]
                    print(actstring)

                # Akció JSON előállítása és elküldése
                sendData(json.dumps({"command": "SetAction", "name": "RemotePlayer", "payload": actstring}))


if __name__=="__main__":
    # Példányosított stratégia objektum
    hunter = RemoteStrategy()
    try:
        hunter.network.load_state_dict(torch.load(r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\model_5___.p"))
        print("model loaded")
    except:
        print("model not found")

    #Select training or evaluation mode
    if(TRAIN):
        hunter.network.train()
    else:
        hunter.network.eval()

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