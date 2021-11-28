import os
import sys
# import urllib.request
import requests 
import random
from datetime import datetime
from flask import Flask, json, jsonify
from flask import request as request2
from flask_restx import Api, Resource
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy

# =============== basic setting ===================




#============== App 세팅하는 과정 =================

app = Flask(__name__);
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  # 환경변수를 사용해서 RDS HOST를 숨김 
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
#172.17.0.1 우분투 배포 
#host.docker.internal 윈도우에서 테스트해볼때


# =========== DB 세팅하는 과정 ==============

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



#============ REST API 세팅하는 과정 ================

api = Api(app);
@api.route("/cloth")
class GetAndPostClothes(Resource):
   
   def get(self):
    clothes = Cloth.query.all();
    
    # JSON화 해서 내보내야함
    return jsonify(clothes);

   def post(self):
     
     global todo;
     todo = request2.json;
     

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

global list
list1 = [];


# NUGU와 관련된 API 
@api.route("/answer-weather")
class NuguApi(Resource):
   
   # NUGU에게 적절한 응답을 내려주는 과정 
   def post(self):
      global todo2;
      todo2 = request2.json;
      
      # 장소에 대한 parameter를 nugu 스피커에서 post 요청으로 받아온 후 파싱 
      location = todo2.get("action").get("parameters").get("location").get("value");
      
   
         # 기상예보 서비스 
      url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
      params ={'serviceKey' : os.environ.get("WEATHER_KEY"), 'pageNo' : '1', 'numOfRows' : '1', 'dataType' : 'JSON', 'base_date' : '20211128', 'base_time' : '1700', 'nx' : '59', 'ny' : '126' }
      response = requests.get(url, params=params).json()
      response2 = response['response']['body']['items']['item'][0]['fcstValue'];
      answer = "오늘 " + location + " 의 날씨는 " + response2 + "도 입니다."
      list1.append(response2);
      if(len(list1) > 3):
         answer = "계절이 바뀌나봐요! 옷을 정리해드릴까요?"
         
      # # nugu speaker로 다시 전송할 데이터 
      
      # weather
      
      # list1.append(weather)
      
      # if len(list1)%5 == 0:
         
      #    num = len(list1)
         
      #    cnt1 = 0
      #    cnt2 = 0
            
      #       for i in range(num, num-5) :
               
      #          if list1[i] > 10 : # 온도 체크 로직 
                  
      #             cnt1 += 1
                  
      #       for i in range(num, num-5) :
               
      #          if list1[i] < 0 :   # 온도 체크 로직 
                  
      #             cnt2 += 1
            
      #       #더울 때      
      #       if cnt1 == 5 :
               
      #          print
      
      #       #추울 때      
      #       if cnt2 == 5 :
               
      #          print
         
      #    if(temp > 20)
           
      #    else if (temp < 20)
         
         
         
      
      
      # list1.append(num)
      
      
      
      
      
      
      
      # if len(list1) > 5 :
         
      #    for i in list1  :
         
      #       cnt = 0
         
      #       if i > 10 :
            
      #          cnt += 1
            
      #       if cnt >5 :
            
      #          print
       
      data =  {
         "version": "2.0",
         "resultCode": "OK",
         "output": {
             # backend parameter
         "location" : location,  # utterance parameter 1 
         "message":  answer
            
         },   # utterance parameter 2
            "directives": []
              }
      
      # 실제 데이터 응답 
      return jsonify(data);
   



  
if __name__ == "__main__":
    db.create_all();
    app.run(host='0.0.0.0', debug=False);