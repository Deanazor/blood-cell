import cv2
import vortex.runtime as vrt
import numpy as np

export_path = "./saved_model/blood_model.onnx"
runtime_device = 'cpu'
model = vrt.create_runtime_model(model_path=export_path,
                                 runtime=runtime_device)

class_names = model.class_names

def normalize(img):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    img = np.array([(img[:,:,i] - mean[i]) / std[i] for i in range(len(mean))])

    return img

def Predict(file):
    response = {}

    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (128,128), interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    img = img[:,:,::-1]
    img = normalize(img)
    img = np.expand_dims(img, 0)

    preds = model(img)

    class_pred = preds[0]['class_label'][0][0].astype('int')
    response["label"] = class_names[class_pred]
    response["confidence"] = str(preds[0]['class_confidence'][0][0])
    
    return response