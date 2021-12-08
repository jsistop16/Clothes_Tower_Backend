from contextlib import nullcontext
from flask import  jsonify, request
from flask import render_template
from flask_restx import Resource, Namespace
from NUGU.answerWeather import answerWeather
from NUGU.answerArrangement import answerArrangement
from DB.models import Cloth ,db

NuguSpeaker = Namespace("NuguSpeaker")
global list1  
list1 = [];
global color
color = "디폴트"
global checked
checked = "존재안함"
@NuguSpeaker.route("/health")
class HealthCheck(Resource):
   def get(self):
      return "ok";

@NuguSpeaker.route("/answer-weather")
class NuguApi(Resource):
   
   # NUGU에게 적절한 응답을 내려주는 과정 
   
   def post(self):
      
      # Nugu에게서 기온을 받아오는 로직 
      response =  answerWeather()
      list1.append(int(response.get("response")));

      # 응답을 내려주는 json 데이터 
      data =  {
         "version": "2.0",
         "resultCode": "OK",
         "output": {
         "message":  response.get("answer")

         },   
            "directives": []
              }
      
      # 실제 데이터 응답 
      return jsonify(data);
    



# 옷을 정리하는 로직    
@NuguSpeaker.route("/answer-arrangement")
class NuguArrangement(Resource):
    def post(self):
          season = ['봄','여름','가을','겨울']
          answer = answerArrangement(list1);
          value = season.index(answer);
          print(value);
          if value == 0 :
             value = 3
          else : 
           answer2= season[value-1];
          
          print("옷 정리 가능?")
          data =  {
           "version": "2.0",
           "resultCode": "OK",
            "output": {
              
            "seasonNow":  "환절기", 
            "seasonBefore" : answer2
            },   
             "directives": []
              }
          return jsonify(data);
        
        
@NuguSpeaker.route("/answer-showByColor")
class NuguAnswerColor(Resource):
    def post(self):
       
       result = request.json;
       
       
       color = result.get("action").get("parameters").get("color").get("value");
       findClothes = Cloth.query.filter(Cloth.color == color).all();
       
       countClothes = len(findClothes);
      
       data =  {
          "version": "2.0",
          "resultCode": "OK",
          "output": {
          "color" : color,
          "count": countClothes  
            },   
             "directives": []
              }
       return jsonify(data)
       
@NuguSpeaker.route("/image")
class Image(Resource):
   def post(self):
    from PIL import Image
    from app import run_vision
    from connect_server import pickColor
    file = request.files['file']
    img = Image.open(file.stream);
    img.save("./upload/test.png");
    result = run_vision("./upload/test.png");
    result2 = result.dominant_colors.colors[0].color;
    colorResult = pickColor(int(result2.red),int(result2.green),int(result2.blue));
    if colorResult == None :
       print("다시 색상을 인식시키세요")
       return render_template('error.html')
    else :
     print(colorResult);
     global color
     global checked
     checked = "존재"
     color = colorResult;
     clothes= Cloth(top_bottom="top",
                    long_short="long",
                    color=colorResult,
                    material="ull");
     db.session.add(clothes);
     db.session.commit();
     db.session.remove();
     print("DB 입력 완료됐습니다.")
     

@NuguSpeaker.route("/close")
class Answer(Resource):
  
    def post(self):
        
     global color
     global checked
     findClothesRed = Cloth.query.filter(Cloth.color == "빨간색").all();
     findClothesGreen = Cloth.query.filter(Cloth.color == "초록색").all();
     findClothesBlue = Cloth.query.filter(Cloth.color == "파란색").all();
     
     print(color)
     print(len(findClothesRed))
     
     data =  {
          "version": "2.0",
          "resultCode": "OK",
          "output": {
          "checked" : checked,
          "colorResult": color ,
          "countred" : len(findClothesRed),
          "countgreen" : len(findClothesGreen),
          "countblue" : len(findClothesBlue)
            },   
             "directives": []
              }
     checked  = "존재안함"
     return jsonify(data);
  
  
  