import os
import io
# from google.cloud import vision
# from google.cloud.vision_v1 import AnnotateImageResponse
# from google.cloud.vision_v1.services.image_annotator import client
# from google.protobuf.json_format import MessageToJson
from flask_restx import Api
from flask import Flask
from flask import request
from Back.back import Clothes

# from flask_sqlalchemy import SQLAlchemy

from DB.models import Cloth , db
from Nugu.nuguRoute import NuguSpeacker







#============== App 세팅하는 과정 ===============

app = Flask(__name__);
# 환경변수를 사용해서 RDS HOST를 숨김 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("FLASK_DB")  
app.config['SQLALCHEMY_ECHO'] = True;
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False;
db.init_app(app);

#============ REST API 세팅하는 과정 ===============

api = Api(app);
api.add_namespace(Clothes, '/clothes')  
api.add_namespace(NuguSpeacker, '/nugu')

# ============= NUGU와 관련된 API ================




        

if __name__ == "__main__":
    
    db.create_all();
    app.run(host='127.0.0.1', debug=True);
   