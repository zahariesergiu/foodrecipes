import json

from flask import Flask, request

from predict_ingredients import ModelPredict


app = Flask(__name__)


MODEL_PATH = "./models_big/model1/1/"
LABEL_BINARIZER_PATH = "./models_small/model1/1/model1_mbl.pkl"
    

@app.route('/predict/', methods=["POST"])
def predict():
    dataa = json.loads(request.data)
    return model.predict(dataa)

@app.route('/predict/tfserving/', methods=["POST"])
def predict_tfserving():
    dataa = json.loads(request.data)
    return model.predict_tfserving(dataa)


if __name__ == '__main__':
    model = ModelPredict(MODEL_PATH, LABEL_BINARIZER_PATH)
    app.run()
