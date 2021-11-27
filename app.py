from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy

# App 세팅하는 과정 
app = Flask(__name__);
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")
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


# s3 관련 세부 설정 
# def s3_connection():
#     '''
#     s3 bucket에 연결
#     :return: 연결된 s3 객체
#     '''
#     try:
#         s3 = boto3.client(
#             service_name='s3',
#             region_name=
#             aws_access_key_id=
#             aws_secret_access_key=
#         )
#     except Exception as e:
#         print(e)
#         exit(ERROR_S3_CONNECTION_FAILED)
#     else:
#         print("s3 bucket connected!")
#         return s3

# def s3_put_object(s3, bucket, filepath, access_key):
#     '''
#     s3 bucket에 지정 파일 업로드
#     :param s3: 연결된 s3 객체(boto3 client)
#     :param bucket: 버킷명
#     :param filepath: 파일 위치
#     :param access_key: 저장 파일명
#     :return: 성공 시 True, 실패 시 False 반환
#     '''
#     try:
#         s3.upload_file(filepath, bucket, access_key)
#     except Exception as e:
#         print(e)
#         return False
#     return True
    
# def s3_get_object(s3, bucket, object_name, file_name):
#     '''
#     s3 bucket에서 지정 파일 다운로드
#     :param s3: 연결된 s3 객체(boto3 client)
#     :param bucket: 버킷명
#     :param object_name: s3에 저장된 object 명
#     :param file_name: 저장할 파일 명(path)
#     :return: 성공 시 True, 실패 시 False 반환
#     '''
#     try:
#         s3.download_file(bucket, object_name, file_name)
#     except Exception as e:
#         print(e)
#         return False
#     return True
# # s3 관련 세부 설정 끝 
# s3 = s3_connection()

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
     db.session.commit()
     db.session.remove()
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
   
  
if __name__ == "__main__":
    db.create_all();
    app.run(host='0.0.0.0', debug=False);