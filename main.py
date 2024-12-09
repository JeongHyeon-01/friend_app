from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId


app = FastAPI()

#DB연결
try:
    client = MongoClient("mongodb://localhost:27017")
    db = client['friend_list']
    friends_collection = db['friends']
except Exception as e:
    print("DB연결 실패")
    
    
#모델 정의
class Friend(BaseModel):
    name : str
    phone : str
    
    
#친구추가
@app.post("/friends")
def add_friend(friend : Friend):
    new_friend = {"name":friend.name, "phone" : friend.phone}
    result = friends_collection.insert_one(new_friend)
    return {"id": str(result.inserted_id), "message": "친구가 추가되었습니다."}


#친구 조회
@app.get("/friends")
def get_friends():
    friends = []
    for friend in friends_collection.find():
        friends.append({"id": str(friend["_id"]), "name": friend["name"], "phone": friend["phone"]})
    return friends


#친구 찾기
@app.get("/friends/search")
def search_friends(name : str):
    friends = []
    for friend in friends_collection.find({"name": {"$regex": name, "$options": "i"}}):
        friends.append({"id": str(friend["_id"]), "name": friend["name"], "phone": friend["phone"]})
    return friends

# 친구 삭제
@app.delete("/friends/{friend_id}")
def delete_friend(friend_id: str):
    result = friends_collection.delete_one({"_id": ObjectId(friend_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="친구를 찾을 수 없습니다.")
    return {"message": "친구가 삭제되었습니다."}