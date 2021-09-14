import torch
from app import BloodModel

net = torch.load("./saved_model/blood_model.pth")

print(net)