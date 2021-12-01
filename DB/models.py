from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
db = SQLAlchemy()

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