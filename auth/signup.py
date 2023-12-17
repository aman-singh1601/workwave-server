from fastapi import APIRouter
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
    password = hash_password(formdata.password)
    email = formdata.email
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

    try:
        # Insert user_data into the database
        db.users.insert_one(user_data)

        # Convert user_data to a Pydantic model for serialization
        user_data_model = SignupData(**user_data)
        
        # Use jsonable_encoder to ensure correct serialization
        serialized_user_data = jsonable_encoder(user_data_model)

        return {
            'user_data': serialized_user_data,
            'token': token,
            'message': 'SIGNUP COMPLETE'
        }
    except Exception:
        return {'message': 'SIGNUP ERROR'}
