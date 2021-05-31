import json
import pickle
import re
import requests

from flask import Flask, request
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
import numpy as np
import tensorflow as tf
# from tensorflow_addons.losses import SigmoidFocalCrossEntropy  # Need the import if the model uses SigmoidFocalCrossEntropy loss
from tensorflow.keras.models import load_model


TF_MODEL_SERVER_URL = "http://localhost:1235/v1/models/model1:predict"



def preprocess_pipeline(text, ps, delimiter=" "):
	text = re.sub('[^A-Za-z0-9 ]+', '', text)
	tokens = []
	for token in text.split(delimiter):
	#         token = self.lemmatizer.lemmatize(token)
	    token = ps.stem(token)
	    if token:
	        tokens.append(token)
	text = delimiter.join(tokens)
	return text


class ModelPredict():

	def __init__(self, model_path, label_binarizer_path):
		nltk.download('wordnet')
		self.ps = PorterStemmer()
		self.lemmatizer = WordNetLemmatizer()
		if model_path:
			self.model = load_model(model_path)
		self.lbl = self.load_obj(label_binarizer_path)

	def load_obj(self, path):
		_file = open(path,'rb')
		obj = pickle.load(_file)
		_file.close()
		return obj
	

	def predict(self, dataa):
		data = [preprocess_pipeline(text, self.ps) for text in dataa.values()]
		data = tf.data.Dataset.from_tensor_slices(data).batch(1024)
		score = self.model.predict(data)
		predict = (score > 0.5).astype(int)
		predict = self.lbl.inverse_transform(predict)
		r = {k:v for k,v in zip(dataa.keys(), predict)}
		return r

	def predict_tfserving(self, dataa):
		data = [[preprocess_pipeline(text, self.ps)] for text in dataa.values()]
		# text = 'Dissolve yeast in warm water.**Stir in sugar, salt, eggs, butter, and 2 cups of flour. Beat until smooth. Mix in remaining flour until smooth. Scrap'
		
		data_tf_serving = json.dumps({"signature_name": "serving_default", "instances": data})
		json_response = requests.post(TF_MODEL_SERVER_URL, data=data_tf_serving, headers={"content-type": "application/json"})
		score = np.array(json.loads(json_response.text)["predictions"])
		predict = (score > 0.5).astype(int)
		predict = self.lbl.inverse_transform(predict)
		r = {k:v for k,v in zip(dataa.keys(), predict)}
		return r
