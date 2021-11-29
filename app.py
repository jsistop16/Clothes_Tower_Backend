import os
import io


# from google.cloud import vision
# from google.cloud.vision_v1 import AnnotateImageResponse
# from google.cloud.vision_v1.services.image_annotator import client
# from google.protobuf.json_format import MessageToJson
import pytz
import schedule
import requests 
import random
from datetime import  datetime, timedelta
from flask import Flask, json, jsonify
from flask import request as request2
from flask_restx import Api, Resource
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.wrappers import response

# =============== basic setting ===================

global list1  
list1 = [];


#====================================== App 세팅하는 과정 =========================================

app = Flask(__name__);
# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
#172.17.0.1 우분투 배포 
#host.docker.internal 윈도우에서 테스트해볼때


# ======================================== DB 세팅하는 과정 =============================================

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



#==================================== REST API 세팅하는 과정 =============================================

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



# ==================================== NUGU와 관련된 API ==========================================

@api.route("/answer-weather")
class NuguApi(Resource):
   
   # NUGU에게 적절한 응답을 내려주는 과정 
   
   def post(self):
      
      # 실시간으로 공공데이터 기상 api에서 기온 정보를 받아옴
      tz = pytz.timezone('Asia/Seoul')
      # cur_time = datetime.now(tz);
      
      now = datetime.now(tz)
      print(now.hour);
      print("지금 시간은 " + now.strftime("%H%M"));
      # 오늘
      # today = datetime.today(tz) # 현재 지역 날짜 반환
      today_date = now.strftime("%Y%m%d") # 오늘의 날짜 (연도/월/일 반환)
      print('오늘의 날짜는', today_date)

      # 어제
      yesterday = now - timedelta(days=1)
      yesterday_date=yesterday.strftime('%Y%m%d')
      print('어제의 날짜는', yesterday_date)

      # 1일 총 8번 데이터가 업데이트 된다.(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
      # 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
      if now.hour<2 or (now.hour==2 and now.minute<=10): # 0시~2시 10분 사이
        base_date=yesterday_date # 구하고자 하는 날짜가 어제의 날짜
        base_time="2300"
      elif now.hour<5 or (now.hour==5 and now.minute<=10): # 2시 11분~5시 10분 사이
        base_date=today_date
        base_time="0200"
      elif now.hour<8 or (now.hour==8 and now.minute<=10): # 5시 11분~8시 10분 사이
        base_date=today_date
        base_time="0500"
      elif now.hour<=11 or (now.minute<=11 and now.minute<=10): # 8시 11분~11시 10분 사이
        base_date=today_date
        base_time="0800"
      elif now.hour<14 or (now.hour==14 and now.minute<=10): # 11시 11분~14시 10분 사이
        base_date=today_date
        base_time="1100"
      elif now.hour<17 or (now.hour==17 and now.minute<=10): # 14시 11분~17시 10분 사이
        base_date=today_date
        base_time="1400"
      elif now.hour<20 or (now.hour==20 and now.minute<=10): # 17시 11분~20시 10분 사이
        base_date=today_date
        base_time="1700" 
      elif now.hour<23 or (now.hour==23 and now.minute<=10): # 20시 11분~23시 10분 사이
        base_date=today_date
        base_time="2000"
      else: # 23시 11분~23시 59분
        base_date=today_date
        base_time="2300"
      
      print("현재 시각 : " +base_time);
      # 실제로 공공데이터 api에서 데이터를 가지고 오는 로직 
      url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
      params ={'serviceKey' : os.environ.get("WEATHER_KEY"),
               'pageNo' : '1', 'numOfRows' : '1',
               'dataType' : 'JSON', 'base_date' : base_date,
               'base_time' :  base_time, 'nx' : '60', 'ny' : '127' }
      response = requests.get(url, params=params).json();
      
      response2 = response['response']['body']['items']['item'][0]['fcstValue'];
      
      if(int(response2) <= 10):
         answer = "현재 시각, 기온는 "+ response2 + "도 입니다. 긴 옷을 추천드립니다. 스마트 클로젯을 실행할까요?"
      elif(int(response2) > 10 and int(response2) <= 20):
         answer =  "현재 시각, 기온는 "+ response2 + "도 입니다. 환절기이니 외투를 챙기세요. 스마트 클로젯을 실행할까요?"
      elif(int(response2) > 20):
         answer =  "현재 시각, 기온는 "+ response2 + "도 입니다. 시원한 옷을 추천드립니다. 스마트 클로젯을 실행할까요?" 
      else:
        answer = "현재 시각, 기온는 " + response2 + "도 입니다."
        
      list1.append(int(response2));
      
      
      
         
      
      
      # 응답을 내려주는 json 데이터 
      data =  {
         "version": "2.0",
         "resultCode": "OK",
         "output": {
             # backend parameter
         "location" : "location",  # utterance parameter 1 
         "message":  answer
            
         },   # utterance parameter 2
            "directives": []
              }
      
      # 실제 데이터 응답 
      return jsonify(data);



# 옷을 정리하는 로직    
@api.route("/answer-arrangement")
class NuguArrangement(Resource):
    def post(self):
          
          num = len(list1)
          
          cnt1 = 0
          cnt2 = 0 
          
          # 여기서 조금 더 세분화하면 사계절 구분 가능 
          for i in range(0,num):
             if list1[i] < 5:
                print(list1[i]);
                cnt1 += 1
             else:
                cnt2 += 1
         
          if cnt1 >= num-1:
            answer = "겨울"
          elif cnt2 >= num-1:
            answer = "여름"
          else:
            answer = "환절기입니다. 여러 종류의 옷을 구비해 두시는게 좋을 것 같네요. 그래도 옷장을 정리하시겠습니까?"
          data =  {
           "version": "2.0",
           "resultCode": "OK",
            "output": {
             # backend parameter
            "location" : "location",  # utterance parameter 1 
            "message2":  answer
            
            },   # utterance parameter 2
             "directives": []
              }
          return jsonify(data);
        
        
        
# ================================== Google Image Vision을 통한 옷 이미지 인식 기능 =================================        
        
# def rgb_to_hex(r, g, b):
#     r, g, b = int(r), int(g), int(b)
#     return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
# def run_vision(file_name):
#   client = vision.ImageAnnotatorClient()
#   os.environ.get("GOOGLE_APPLICATION_CREDENTIALS");


#   with io.open(file_name, 'rb') as image_file: 
#     content = image_file.read()

#   image = vision.Image()
#   image.content = content;

#   response = client.image_properties(image = image)
  
#   labels = response.image_properties_annotation;
#   print(labels)
#   for color in labels.dominant_colors.colors:
#     print("color = " + rgb_to_hex(int(color.color.red),int(color.color.green),int(color.color.blue)) + " percentage : " +str(int(color.score * 100))+"%")
   
#   return labels;        
# @api.route("/vision")
# class Vision(Resource):
    
#   def get(self):
#     print("google vision api start...!")
#     result = run_vision("./image/cloth.png");
#     return "success";



# =======================================================

# def closest_colour(requested_colour):
#     min_colours = {}
#     for key, name in webcolors.css3_hex_to_names.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#         rd = (r_c - requested_colour[0]) ** 2
#         gd = (g_c - requested_colour[1]) ** 2
#         bd = (b_c - requested_colour[2]) ** 2
#         min_colours[(rd + gd + bd)] = name
#     return min_colours[min(min_colours.keys())]

# def get_colour_name(requested_colour):
#     try:
#         closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
#     except ValueError:
#         closest_name = closest_colour(requested_colour)
#         actual_name = None
#     return actual_name, closest_name

# requested_colour = (119, 172, 152)
# actual_name, closest_name = get_colour_name(requested_colour)


# 
# print "Actual colour name:", actual_name, ", closest colour name:", closest_name    
#==================================================================       
if __name__ == "__main__":
   
    db.create_all();
    app.run(host='0.0.0.0', debug=False);
   