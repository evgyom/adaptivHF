from matplotlib import animation
import matplotlib.pyplot as plt
from Engine import *

engine = AdaptIOEngine("./gui/maps/base_field.txt", 5, 1.2,
                       {"Teszt": "naivebot", "Teszt1": "randombot", "Teszt2": "randombot", "Teszt3": "randombot"}, 5,
                       "static")

fig = plt.figure(figsize=(8,8))
ax = plt.axes()


def update_points(num):
    engine.tick()
    ax.clear()
    return [ax.imshow(engine.field),
            ax.scatter(engine.players[0].pos[1], engine.players[0].pos[0], color="r", label="P1: "+str(engine.players[0].size)),
            ax.scatter(engine.players[1].pos[1], engine.players[1].pos[0], color="r", label="P2: "+str(engine.players[1].size)),
            ax.scatter(engine.players[2].pos[1], engine.players[2].pos[0], color="r", label="P3: "+str(engine.players[2].size)),
            ax.scatter(engine.players[3].pos[1], engine.players[3].pos[0], color="r", label="P4: "+str(engine.players[3].size)),
            ax.legend(loc='upper center',fontsize=8)]


ani = animation.FuncAnimation(fig,
                              update_points,
                              interval=20.0,
                              blit=True)

plt.show()
