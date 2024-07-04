from fastapi import FastAPI, UploadFile,HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import utils.data_type as data_type
import config.database as database
import utils.helping as helping
from pathlib import Path
from typing import Union
import numpy as np
import shutil
import test

origins = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_and_preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


UPLOAD_DIRECTORY = "check"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

@app.post("/autism/neuro")
async def AutismCheck(image: Union[UploadFile, None] = None,user: data_type.User = Depends(helping.get_current_user)):
    try:
       if image is None:
            return {"message": "No image provided"}
       img_path = Path(UPLOAD_DIRECTORY) / image.filename
       with img_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
       if not test.detect_human_dnn(img_path):
            return {"message": "Not a human image"}
       
       model = load_model('Facialmobile_net.keras')
       img_array = load_and_preprocess_image(img_path)
       predictions = model.predict(img_array)
       predicted_class = np.argmax(predictions, axis=-1)
       message=""
       if predicted_class == 0:
           message="Not Autistic"
       else:
           message="Autistic"
       return {"message":message, "image":image}
    except Exception as e:
        return {"message":"Error with your code"}



@app.post("/autism/facial")
async def AutismCheck(image: Union[UploadFile, None] = None, user: data_type.User = Depends(helping.get_current_user)):
    try:
       print("FDF")
       if image is None:
            return {"message": "No image provided"}
       img_path = Path(UPLOAD_DIRECTORY) / image.filename
       with img_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
       model = load_model('mobile_net.keras')
       img_array = load_and_preprocess_image(img_path)
       predictions = model.predict(img_array)
       predicted_class = np.argmax(predictions, axis=-1)
       message=""
       if predicted_class == 0:
           message="Not Autistic"
       else:
           message="Autistic"
       return {"message":message, "image":image}
    except Exception as e:
        return {"message":"Error with your code"}



@app.post("/login")
async def login(user:data_type.LoginRequest):
    try:
        userCollection=database.db.get_collection("users")
        data = userCollection.find_one({"email":user.email})
        if data:
            isPassMatch=helping.verify_password(user.password,data['password'])
            if isPassMatch:
                access_token_expires = timedelta(minutes=helping.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = helping.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
                return data_type.Token(access_token=access_token, token_type="bearer",message="Successfully Loge in")
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return {"message":e,"status":False}


@app.post("/registration")
async def registration(user: data_type.RegistrationRequest):
    try:
        userCollection=database.db.get_collection("users")
        data = userCollection.find_one({"email":user.email})
        if data:
            return {"message":"User already exists"}
        else:
            passwordHash=helping.get_password_hash(user.password)
            data={"firstName": user.firstName,"lastName": user.lastName, "email":user.email,"password":passwordHash}
            userCollection.insert_one(data)
            return {"message":"Successfully Registered"}
    except Exception as e:
        return e


@app.get("/refresh-token")
async def getToken():
    print("Refresh-Token")