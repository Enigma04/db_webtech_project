# main.py
from datetime import timedelta
from typing import Optional

from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status

from utils import get_password_hash, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from models import UserSignup, UserModel, Facility, FavoriteFacility
from database import (
    retrieve_kg_facility,
    retrieve_kg_facilities,
    retrieve_school_facility,
    retrieve_school_facilities,
    retrieve_scp_facility,
    retrieve_scp_facilities,
    retrieve_stp_facility,
    retrieve_stp_facilities,
    retrieve_all, get_user, add_user, authenticate_user, set_favorite_facility, get_favorite_facility, users_collection,
)

app = FastAPI()


@app.get("/kg-facilities/{id}", response_description="List a kindergarten")
async def get_kindergarten(id: str):
    kindergarten = await retrieve_kg_facility(id)
    if kindergarten:
        return kindergarten
    raise HTTPException(status_code=404, detail=f"Kindergarten with ID {id} not found")


@app.get("/kg-facilities/", response_description="List all kindergartens")
async def get_all_kindergartens():
    kindergartens = await retrieve_kg_facilities()
    return kindergartens


@app.get("/school-facilities/{id}", response_description="List a school")
async def get_school(id: str):
    school = await retrieve_school_facility(id)
    if school:
        return school
    raise HTTPException(status_code=404, detail=f"School with ID {id} not found")


@app.get("/school-facilities/", response_description="List all schools")
async def get_all_schools():
    schools = await retrieve_school_facilities()
    return schools


@app.get("/social-child-project-facilities/{id}", response_description="List a social child project")
async def get_scp(id: str):
    scp = await retrieve_scp_facility(id)
    if scp:
        return scp
    raise HTTPException(status_code=404, detail=f"Social Child Project with ID {id} not found")


@app.get("/social-child-project-facilities/", response_description="List all social child projects")
async def get_all_scp():
    scps = await retrieve_scp_facilities()
    return scps


@app.get("/social-teenage-project-facilities/{id}", response_description="List a social teenage project")
async def get_stp(id: str):
    stp = await retrieve_stp_facility(id)
    if stp:
        return stp
    raise HTTPException(status_code=404, detail=f"Social Teenage Project with ID {id} not found")


@app.get("/social-teenage-project-facilities/", response_description="List all social teenage projects")
async def get_all_stp():
    stps = await retrieve_stp_facilities()
    return stps


@app.get("/all-data/", response_model=dict)
async def get_all_data():
    all_data = await retrieve_all()
    return all_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/signup/", response_description="Register a new user")
async def signup(user: UserSignup = Body(...)):
    user_data = user.dict()
    existing_user = await users_collection.find_one(
        {"$or": [{"username": user_data["username"]}, {"email": user_data["email"]}]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
    user_data["hashed_password"] = get_password_hash(user_data["password"])
    del user_data["password"]
    new_user = await add_user(user_data)
    return new_user


@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@app.post("/users/me/favorite", response_model=Facility)
async def set_user_favorite_facility(favorite: FavoriteFacility, current_user: UserModel = Depends(get_current_user)):
    updated_user = await set_favorite_facility(current_user.username, favorite.facility_id)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Facility not found")
    favorite_facility = await get_favorite_facility(current_user.username)
    return favorite_facility


@app.get("/users/me/favorite", response_model=Optional[Facility])
async def get_user_favorite_facility(current_user: UserModel = Depends(get_current_user)):
    favorite_facility = await get_favorite_facility(current_user.username)
    if favorite_facility is None:
        raise HTTPException(status_code=404, detail="Favorite facility not found")
    return favorite_facility
