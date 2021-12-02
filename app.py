import os
# from google.cloud import vision
# from google.cloud.vision_v1 import AnnotateImageResponse
# from google.cloud.vision_v1.services.image_annotator import client
# from google.protobuf.json_format import MessageToJson
from flask_restx import Api
from flask import Flask
from Back.back import Clothes
from DB.models import db
# from Nugu.nuguRoute import Speaker


app = Flask(__name__);
# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
db.init_app(app);

#===== REST API 세팅하는 과정 =======

api = Api(app);
# api.add_namespace(Speaker, '/nugu')
api.add_namespace(Clothes, '/clothes')      # backend 
    # nugu speaker

if __name__ == "__main__":
    
    db.create_all();
    app.run(host='0.0.0.0', debug=False);
   