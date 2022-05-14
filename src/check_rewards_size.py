import matplotlib.pyplot as plt

rewards = []
sizes = []

with open(r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\src\log\past_rewards\v11.txt","r") as f:
    for line in f:
        rewards.append(line)

with open(r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\src\log\past_sizes\v11.txt","r") as f:
    for line in f:
        rewards.append(line)

plt.plot(rewards, c="r")
plt.plot(sizes, c = "blue")
plt.show()