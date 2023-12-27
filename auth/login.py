from fastapi import APIRouter, HTTPException
from auth.webtoken import tokengen
import hashlib
from database.dbconn import db
from pydantic import BaseModel 
from fastapi.encoders import jsonable_encoder

login_router = APIRouter()

def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password

class LoginData(BaseModel):
    username: str
    password: str

@login_router.post("/login")
async def login(formdata: LoginData):
    username = formdata.username
    password = formdata.password

    # Check if user with the provided username exists
    user_data = db.users.find_one({'username': username})
    if not user_data:
        raise HTTPException(status_code=401, detail="User does not exist")

    # Verify password
    hashed_password = hash_password(password)
    if hashed_password != user_data['password']:
        raise HTTPException(status_code=401, detail="Invalid password")

    # Generate token
    payload = {
        'userName': username,
        'email': user_data['email']
    }
    token = tokengen(payload)

    user_data_return = {
        "username": username,
        "email": user_data["email"], 
        "firstName": user_data["firstName"], 
        "lastName": user_data["lastName"]
        }
    serialized_user_data = jsonable_encoder(user_data_return)

    return {
        'user_data': serialized_user_data,
        'token': token,
        'message': 'LOGIN SUCCESSFUL'
    }
