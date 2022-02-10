from matplotlib import animation
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes()

def update_points(num):
    print(num)
    return [ax.scatter([0, 0], [1, (num*0.01)%1], s=10,c='r')]


ani = animation.FuncAnimation(fig,
                              update_points,
                              interval=0.01,
                              blit=True)

plt.show()