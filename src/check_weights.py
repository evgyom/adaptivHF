import torch
from Main_Client import RemoteStrategy

hunter = RemoteStrategy()
hunter.network.load_state_dict(torch.load(r"C:\Users\Misi\01_SULI\02_10_felev_MSC_2\09_adaptiv\adapt_hf\adaptivegame\models\model_7.p"))

for name, param in hunter.network.named_parameters():
    print(name)
    print(param)
    print("---")