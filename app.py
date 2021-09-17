from datetime import datetime
from flask import Flask, json, request, render_template
from detect import Predict

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = {}
    if request.method=="POST":
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

        response["filename"] = filename
        response["status"] = "OK"

        result = Predict(file)
        response['result'] = [result]

    return render_template("index.html", response=json.dumps(response))

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get('image')
    response = {}

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

    response["filename"] = filename
    response["status"] = "OK"

    result = Predict(file)
    response['result'] = [result]
    # response["result"] = result

    return json.jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")