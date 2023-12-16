from fastapi import APIRouter, HTTPException

import hashlib
from database.dbconn import db 

signup_router = APIRouter()

def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    hashed_password = sha256_hash.hexdigest()
    return hashed_password

@signup_router.post("/signup")
async def signup(formdata):
    username = formdata['username']
    password = hash_password(formdata['password'])
    email = formdata['email']
    firstName = formdata['firstName']
    lastName = formdata['lastName']
    
    user_data = {
        'username': username,
        'password': password,
        'email': email,
        'firstName': firstName,
        'lastName': lastName
    }
    
    try:
        db.users.insert_one(user_data)
    except Exception:
        return {'message':'SINGUP ERROR'}