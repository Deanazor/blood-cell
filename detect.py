import torch
from torchvision import transforms
from PIL import Image

labelexp = ['parasitized', 'uninfected']

device = torch.device("cuda:0")\
         if torch.cuda.is_available()\
         else torch.device("cpu")

data_transforms = transforms.Compose([
                        transforms.Resize((128, 128)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])                                    
                ])

def predict(X, model):
    with torch.no_grad():
        model.eval()
        output = model(X)
        preds = output.argmax(1)

    return preds

def Predict(filename, file, net):
    img = Image.open(file)
    response = {}

    img = data_transforms(img).view(-1, 3, 128, 128)
    net, img = net.to(device), img.to(device)
    res = predict(img, net)
    response[filename] = labelexp[res[0]]
    
    return response