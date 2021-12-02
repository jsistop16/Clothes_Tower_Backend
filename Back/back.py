from flask import request, jsonify
from flask_restx import Resource, Namespace
from DB.models import Cloth, db

Clothes = Namespace('Clothes')

@Clothes.route("")
class GetAndPostClothes(Resource):
   # 전체 옷 조회 
   def get(self):
    clothes = Cloth.query.all();
   
    return jsonify(clothes);
   # 옷 추가 
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
@Clothes.route("/<int:cloth_id>")
class DeleteClothes(Resource):
    def delete(self,cloth_id):
      cloth = Cloth.query.get(cloth_id);
      db.session.delete(cloth);
      db.session.commit();
      db.session.remove();
      return "delete success";