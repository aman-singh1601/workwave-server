from fastapi import APIRouter, HTTPException
from auth.webtoken import tokengen
import hashlib
from database.dbconn import db
from pydantic import BaseModel 
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

signup_router = APIRouter()

class SignupData(BaseModel):
    username: str
    password: str
    email: str
    firstName: str
    lastName: str

def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password

@signup_router.post("/signup")
async def signup(formdata: SignupData):
    username = formdata.username
    email = formdata.email

    existing_user = db.users.find_one({'$or': [{'username': username}, {'email': email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    try:
        password = hash_password(formdata.password)
        firstName = formdata.firstName
        lastName = formdata.lastName

        user_data = {
            'username': username,
            'password': password,
            'email': email,
            'firstName': firstName,
            'lastName': lastName
        }

        payload = {
            'userName': username,
            'email': email
        }

        token = tokengen(payload)

        inserted_id = db.users.insert_one(user_data).inserted_id
        user_data['_id'] = str(inserted_id)
        serialized_user_data = jsonable_encoder(user_data)

        return {
            'user_data': serialized_user_data,
            'token': token,
            'message': 'SIGNUP COMPLETE'
        }
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
