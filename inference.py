import json
import requests

import pandas as pd


DATA_PATH = "./data/"
FLASK_URL = "http://127.0.0.1:5000/predict/"
FLASK_TF_SERVING_URL = "http://127.0.0.1:5000/predict/tfserving"


# data_web_app = json.dumps({
#   "recipe1": "This is recipe 1 directions",
#   "recipe2": "This is recipe 2 directions"
# })
# text = 'Dissolve yeast in warm water.**Stir in sugar, salt, eggs, butter, and 2 cups of flour. Beat until smooth. Mix in remaining flour until smooth. Scrape dough from side of bowl. Knead dough, then cover it and let rise in a warm place until double (about 1 1/2 hours).**Punch down dough. Divide in half. Roll each half into a 12-inch circle. Spread with butter. Cut into 10 to 15 wedge. Roll up the wedges starting with the wide end. Place rolls with point under on a greased baking sheet. Cover and let rise until double (about 1 hour).**Bake at 400 degrees F (205 degrees C) for 12-15 minute or until golden brown. Brush tops with butter when they come out of the oven.**'
# data_tf_serving = json.dumps({"signature_name": "serving_default", "instances": [[text]]})
# json_response = requests.post(TF_MODEL_SERVER_URL, data=data_tf_serving, headers=headers)

headers = {"content-type": "application/json"}

clean_recipes = pd.read_csv(DATA_PATH + 'clean_recipes.csv', delimiter=';').fillna("")
data = {a[0]:a[1] for a in clean_recipes[["RecipeID", "Directions"]][:1].values.tolist()}
data_web_app = json.dumps(data)

json_response = requests.post(FLASK_TF_SERVING_URL, data=data_web_app, headers=headers)
print(json_response)
print(json_response.text)

json_response = requests.post(FLASK_URL, data=data_web_app, headers=headers)
print(json_response)
print(json_response.text)
