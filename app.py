import os
import io
# from google.cloud import vision
# from google.cloud.vision_v1 import AnnotateImageResponse
# from google.cloud.vision_v1.services.image_annotator import client
# from google.protobuf.json_format import MessageToJson
from flask_restx import Api, Resource
from flask import Flask, json, jsonify
from flask import request
from nugu.answerWeather import answerWeather
from nugu.answerArrangement import answerArrangement
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy

from DB.models import Cloth , db




#============== App 세팅하는 과정 ===============

app = Flask(__name__);
# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
db.init_app(app);

#============ REST API 세팅하는 과정 ===============

api = Api(app);
@api.route("/cloth")
class GetAndPostClothes(Resource):
   
   def get(self):
    clothes = Cloth.query.all();
   
    # JSON화 해서 내보내야함
    return jsonify(clothes);

   def post(self):
     
     global todo;
     todo = request.json;
     

     clothes= Cloth(top_bottom=todo.get("top_bottom"),
                    long_short=todo.get("long_short"),
                    color=todo.get("color"),
                    material=todo.get("material"));
     db.session.add(clothes);
     db.session.commit();
     db.session.remove();
     return jsonify(todo); 

# 데이터 삭제 
@api.route("/cloth/<int:cloth_id>")
class DeleteClothes(Resource):
    def delete(self,cloth_id):
      cloth = Cloth.query.get(cloth_id);
      db.session.delete(cloth);
      db.session.commit();
      db.session.remove();
      return "delete success";

# ============= NUGU와 관련된 API ================

global list1  
list1 = [];

@api.route("/answer-weather")
class NuguApi(Resource):
   
   # NUGU에게 적절한 응답을 내려주는 과정 
   
   def post(self):
      
      # Nugu에게서 기온을 받아오는 로직 
      response = answerWeather()  
      list1.append(int(response.get("response")));

      # 응답을 내려주는 json 데이터 
      data =  {
         "version": "2.0",
         "resultCode": "OK",
         "output": {
         "location" : "location",  
         "message":  response.get("answer")

         },   
            "directives": []
              }
      
      # 실제 데이터 응답 
      return jsonify(data);



# 옷을 정리하는 로직    
@api.route("/answer-arrangement")
class NuguArrangement(Resource):
    def post(self):
          
          answer = answerArrangement(list1);
          
          data =  {
           "version": "2.0",
           "resultCode": "OK",
            "output": {
            "location" : "location",  
            "message2":  answer
            },   
             "directives": []
              }
          return jsonify(data);
        
        
        

if __name__ == "__main__":
    
    db.create_all();
    app.run(host='127.0.0.1', debug=False);
   