from matplotlib import animation
import matplotlib.pyplot as plt
from Engine import *

engine = AdaptIOEngine("./gui/maps/base_field.txt", 5, 1.1,
                       {"Teszt1": "naivehunterbot", "Teszt2": "naivehunterbot", "Teszt3": "naivehunterbot", "Teszt4": "naivehunterbot"}, 5,
                       "static")

fig = plt.figure(figsize=(8,8))
ax = plt.axes()

def color(alive):
    if alive:
        return "r"
    else:
        return "k"

def update_points(num):
    engine.tick()
    ax.clear()

    return [ax.imshow(engine.field.T),
            ax.scatter(engine.players[0].pos[0], engine.players[0].pos[1], color=color(engine.players[0].active), label="P1: "+str(engine.players[0].size)),
            ax.scatter(engine.players[1].pos[0], engine.players[1].pos[1], color=color(engine.players[1].active), label="P2: "+str(engine.players[1].size)),
            ax.scatter(engine.players[2].pos[0], engine.players[2].pos[1], color=color(engine.players[2].active), label="P3: "+str(engine.players[2].size)),
            ax.scatter(engine.players[3].pos[0], engine.players[3].pos[1], color=color(engine.players[3].active), label="P4: "+str(engine.players[3].size)),
            ax.legend(loc='upper center',fontsize=8)]


ani = animation.FuncAnimation(fig,
                              update_points,
                              interval=10.0,
                              blit=True)

plt.show()
