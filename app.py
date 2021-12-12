import os
from flask import render_template
from google.cloud import vision
from google.cloud.vision_v1.services.image_annotator import client
from flask_restx import Api, Resource
from flask import Flask ,request, jsonify
from NUGU.nuguRoute import NuguSpeaker
from Back.back import Clothes
from DB.models import Cloth, db
import io
from flask_cors import CORS


app = Flask(__name__);

# 이미지 촬영 웹사이트와의 CORS 문제 해결 
CORS(app)

# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
db.init_app(app);

# GOOGLE VISION API 이미지 색상 추출 
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


# REST API 경로 세팅 
api = Api(app);

@app.route("/render")
def index():
  return render_template('main.html');

@app.route("/showDB")
def showDB():
  order = request.args.get('color')
  if order == None : 
    clothes = Cloth.query.all();
  else:
    clothes = Cloth.query.filter(Cloth.color == order).all();  
  
  return render_template('showDB.html',dataList = clothes, image_file="image/옷걸이봉.jpg");

# NUGU SPEAKER 백엔드 프록시 정상 작동 체크 
@app.route("/health")
def healthCheck():
  return "ok";

# NUGU SPEAKER 진입점 
api.add_namespace(NuguSpeaker, '/nugu')

# DB 접근 진입점 
api.add_namespace(Clothes, '/clothes')     




if __name__ == "__main__":
    
    db.create_all();
    app.run(host='0.0.0.0', debug=False);
   