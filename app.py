import os
from datetime import datetime
import torch
import torch.nn as nn
from flask import Flask, json, request
from detect import Predict, device

class BloodModel(nn.Module):
    def __init__(self, output_num):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(p=0.25),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(p=0.25),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(p=0.25),
        )

        x = torch.randn(3,128,128).view(-1,3,128,128)
        self._to_linear = None
        self.convs(x)

        self.classifier = nn.Sequential(
            nn.Linear(self._to_linear, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),

            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(),

            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(),

            nn.Linear(128, output_num),
            nn.LogSoftmax(dim=1)
        )
        
    def convs(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)

        if self._to_linear is None:
            self._to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return x
    
    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)
        x = self.classifier(x)
        return x

app = Flask(__name__)

net = torch.load("./saved_model/blood_model.pth", map_location=device)

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get('image')

    if not file:
        return {
            "error": "Image is required"
        }, 400

    supported_mimetypes = ["image/jpeg", "image/png"]
    mimetype = file.content_type
    if mimetype not in supported_mimetypes:
        return {
            "error": "Unsupported image type"
        }, 415

    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = current_time + '-' + file.filename

    result = Predict(filename, file, net)

    return json.dumps(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")