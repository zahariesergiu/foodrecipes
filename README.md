# foodrecipes

git clone git@github.com:zahariesergiu/foodrecipes.git
  

# installl web app requirements
pip install -r requirements.txt
  

# start flask web app:
python web_app.py
  

# run inference.py for a demo prediction
python inference.py
  

# run a curl post command for a prediction:
curl -X POST -H "Content-Type: application/json" -d '{"1":"Mix oats with buttermilk.  Let stand for 1/2 hour.**Stir oil, egg, and brown sugar into oat mixture. Stir together flour, baking powder, soda, and salt: mix into oat mixture.  Pour batter into a greased and floured 8 1/2 x 4 1/2 inch loaf pan.**Bake at 350 degrees F (175 degrees C) for 55 to 60 minutes, or until done.**"}' http://127.0.0.1:5000/predict/



# install tensorflow_model_server
echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list && \
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -

apt-get update && apt-get install tensorflow-model-server


apt-get upgrade tensorflow-model-server


  
# Start tensorflow_model_server
tensorflow_model_server --model_base_path=/home/sergiuz/workspace/recipes/models_small/model1 --model_name=model1 --port=1234 --rest_api_port=1235
tensorflow_model_server --model_base_path=<full_path_to_model> --model_name=<model_name> --port=1234 --rest_api_port=1235
   

# Delete the comment at the lines 26-29  in inference.py to include the code that makes a request to tensorflow_model_serving
# run inference.py for a demo prediction with tensorflow model server
python inference.py

# Or run it with the REST web app to the tf model server  
curl -X POST -H "Content-Type: application/json" -d '{"1":"Mix oats with buttermilk. Let stand for 1/2 hour.**Stir oil, egg, and brown sugar into oat mixture. Stir together flour, baking powder, soda, and salt: mix into oat mixture. Pour batter into a greased and floured 8 1/2 x 4 1/2 inch loaf pan.Bake at 350 degrees F (175 degrees C) for 55 to 60 minutes, or until done."}' http://127.0.0.1:5000/predict/tfserving/
