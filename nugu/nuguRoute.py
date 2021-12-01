from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
from Nugu.answerWeather import answerWeather
from Nugu.answerArrangement import answerArrangement
NuguSpeacker = Namespace('NuguSpeaker');
global list1  
list1 = [];

@NuguSpeacker.route("/answer-weather")
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
         "location" : "location",  
         "message":  response.get("answer")

         },   
            "directives": []
              }
      
      # 실제 데이터 응답 
      return jsonify(data);



# 옷을 정리하는 로직    
@NuguSpeacker.route("/answer-arrangement")
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
        
        