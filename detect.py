from torchvision import transforms
from PIL import Image
import vortex.runtime as vrt
import numpy as np

export_path = "./saved_model/blood_model.onnx"

data_transforms = transforms.Compose([
                        transforms.Resize((128, 128)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])                                    
                ])

def Predict(file):
    response = {}
    img = Image.open(file).convert("RGB")

    img = data_transforms(img).view(-1, 3, 128, 128)
    img = np.array(img).astype(np.float32)

    runtime_device = 'cpu'
    model = vrt.create_runtime_model(model_path=export_path,
                                      runtime=runtime_device)

    class_names = model.class_names
    preds = model(img)

    class_pred = preds[0]['class_label'][0][0].astype('int')
    response["label"] = class_names[class_pred]
    response["confidence"] = str(preds[0]['class_confidence'][0][0])
    
    return response