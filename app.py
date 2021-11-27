from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy


# App 세팅하는 과정 
app = Flask(__name__);
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  # 환경변수를 사용해서 RDS HOST를 숨김 
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
#172.17.0.1 우분투 배포 
#host.docker.internal 윈도우에서 테스트해볼때

# DB 세팅하는 과정 
db = SQLAlchemy(app);

# Cloth 데이터 직렬화를 위해서 @dataclass 데코레이터를 사용함 
@dataclass
class Cloth(db.Model):
   
   # 이거 설정 안해주면 데이터 출력이 안됩니다..
   id: int 
   top_bottom: str
   long_short: str
   color: str
   material: str
   
   # DB COLUMN 설정 
   id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
   top_bottom = db.Column(db.String(20))
   long_short = db.Column(db.String(50))
   color = db.Column(db.String(20))
   material = db.Column(db.String(20))



# REST API 세팅하는 과정 
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
     

     clothes= Cloth(top_bottom=todo.get("top_bottom"),long_short=todo.get("long_short"),color=todo.get("color"),material=todo.get("material"));
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


# NUGU와 관련된 API 
@api.route("/answer-weather")
class NuguApi(Resource):
   
   # NUGU에게 적절한 응답을 내려주는 과정 
   def post(self):
      global todo2;
      todo2 = request.json;
      print(todo2);
      data =  {
         "version": "2.0",
         "resultCode": "OK",
         "output": {
         "date" : "오늘",     # backend parameter
         "location" : "명동",  # utterance parameter 1 
         "message": "맑아"},   # utterance parameter 2
            "directives": []
              }
      
      return jsonify(data);
   



  
if __name__ == "__main__":
    db.create_all();
    app.run(host='0.0.0.0', debug=False);