
import os
from flask import render_template
from google.cloud import vision
from google.cloud.vision_v1.services.image_annotator import client
from flask_restx import Api, Resource
from flask import Flask ,request, jsonify
from NUGU.nuguRoute import NuguSpeaker
from Back.back import Clothes
from DB.models import db
import io
import ssl

from flask_cors import CORS




app = Flask(__name__);
CORS(app)
# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
db.init_app(app);

def run_vision(file_name):
  
  
  client = vision.ImageAnnotatorClient()
  os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
  

  with io.open(file_name, 'rb') as image_file: 
    content = image_file.read()

  image = vision.Image()
  image.content = content;

  response = client.image_properties(image = image)
  
  labels = response.image_properties_annotation;
 
  return labels;        


#===== REST API 세팅하는 과정 =======

api = Api(app);

@app.route("/render")
def index():
  return render_template('main.html');

api.add_namespace(NuguSpeaker, '/nugu')
api.add_namespace(Clothes, '/clothes')     


@api.route("/image")
class Image(Resource):
  
  def post(self):
    from PIL import Image
    from connect_server import pickColor
    file = request.files['file']
    img = Image.open(file.stream);
    img.save("./upload/test.png");
    result = run_vision("./upload/test.png");
    result2 = result.dominant_colors.colors[0].color;
    pickColor(int(result2.red),int(result2.green),int(result2.blue));
    
    
    return jsonify({"message" : "success"});
    






if __name__ == "__main__":
    
    db.create_all();
   

    
    app.run(host='0.0.0.0', debug=False);
   