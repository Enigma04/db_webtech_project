import uuid

from fastapi import HTTPException
from pymongo import ASCENDING
from bson import ObjectId, Binary
from models import KinderGartenFacilityModel, SchoolFacilityModel, SPFacilityModel
from motor.motor_asyncio import AsyncIOMotorClient
from utils import verify_password

from schemas import kg_facility_helper, school_facility_helper, sp_facility_helper

uri = "mongodb+srv://rohitv0604:admin12345@cluster01.8hg0car.mongodb.net/"

client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
database = client["ChemnitzFacilities"]
users_collection = database["users"]

users_collection.create_index([("username", ASCENDING)], unique=True)
users_collection.create_index([("email", ASCENDING)], unique=True)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("You have successfully connected to MongoDB!")
except Exception as e:
    print(f"Error: ${e}")

kindergarten = database["kindergarten"]
school = database["school"]
social_child_project = database["social_child_projects"]
social_teenage_project = database["social_teenage_project"]
user_collection = database["users"]


async def retrieve_kg_facilities():
    facilities = []
    async for facility in kindergarten.find():
        facilities.append(kg_facility_helper(facility))
    return facilities


async def retrieve_kg_facility(id: str) -> dict:
    facility = await kindergarten.find_one({"_id": ObjectId(id)})
    if facility:
        return kg_facility_helper(facility)


async def retrieve_school_facilities():
    school_facilities = []
    async for facility in school.find():
        school_facilities.append(school_facility_helper(facility))
    return school_facilities


async def retrieve_school_facility(id: str) -> dict:
    facility = await school.find_one({"_id": ObjectId(id)})
    if facility:
        return school_facility_helper(facility)


async def retrieve_scp_facilities():
    scp_facilities = []
    async for facility in social_child_project.find():
        scp_facilities.append(sp_facility_helper(facility))
    return scp_facilities


async def retrieve_scp_facility(id: str) -> dict:
    facility = await social_child_project.find_one({"_id": ObjectId(id)})
    if facility:
        return sp_facility_helper(facility)


async def retrieve_stp_facilities():
    stp_facilities = []
    async for facility in social_teenage_project.find():
        stp_facilities.append(sp_facility_helper(facility))
    return stp_facilities


async def retrieve_stp_facility(id: str) -> dict:
    facility = await social_teenage_project.find_one({"_id": ObjectId(id)})
    if facility:
        return sp_facility_helper(facility)


async def retrieve_all():
    try:
        kindergartens = await retrieve_kg_facilities()
        schools = await retrieve_school_facilities()
        social_child_projects = await retrieve_scp_facilities()
        social_teenage_projects = await retrieve_stp_facilities()

        return {
            "kindergartens": kindergartens,
            "schools": schools,
            "social_child_projects": social_child_projects,
            "social_teenage_project": social_teenage_projects
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_user(user_data: dict) -> dict:
    user_data["favorite_facility"] = None
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"id": user.inserted_id})
    return new_user


async def get_user(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    return user


async def authenticate_user(username: str, password: str) -> dict:
    user = await get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


async def set_user_favorite(username: str, facility_id: str):
    collections = [
        kindergarten,
        school,
        social_child_project,
        social_teenage_project
    ]
    facility = None
    for collection in collections:
        facility = await collection.find_one({"_id": ObjectId(facility_id)})
        if facility:
            break
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    facility = convert_objectid_to_str(facility)

    # Infer the facility type based on the presence of specific fields
    if 'KITA' in facility or 'HORT' in facility:
        facility = KinderGartenFacilityModel(**facility)

    elif 'TYP' in facility or 'ART' in facility:
        if 'global_uuid' in facility:
            facility['global_uuid'] = Binary.from_uuid(uuid.UUID(facility['global_uuid']))
        facility = SchoolFacilityModel(**facility)

    elif 'LEISTUNGEN' in facility:
        facility = SPFacilityModel(**facility)

    else:
        raise HTTPException(status_code=400, detail="Invalid facility type")

    result = await users_collection.update_one(
        {"username": username},
        {"$set": {"favorite_facility": facility.dict()}}
    )

    if result.modified_count == 1:
        return await get_user(username)

    return None


async def get_favorite_facility(username: str) -> dict:
    user = await get_user(username)

    if user and "favorite_facility" in user:
        favorite_facility = user["favorite_facility"]
        # favorite_facility["id"] = str(favorite_facility["_id"])
        return favorite_facility

    return None


def convert_objectid_to_str(document):
    if '_id' in document:
        document['_id'] = str(document['_id'])
    return document


async def fetch_facility(facility_id: str):
    collections = [
        kindergarten,
        school,
        social_child_project,
        social_teenage_project
    ]
    facility = None
    for collection in collections:
        facility = await collection.find_one({"_id": ObjectId(facility_id)})
        if facility:
            break

    facility = convert_objectid_to_str(facility)

    # Infer the facility type based on the presence of specific fields
    if 'KITA' in facility or 'HORT' in facility:
        return KinderGartenFacilityModel(**facility)
    elif 'TYP' in facility or 'ART' in facility:
        return SchoolFacilityModel(**facility)
    elif 'LEISTUNGEN' in facility:
        return SPFacilityModel(**facility)
    else:
        raise HTTPException(status_code=400, detail="Invalid facility type")


async def delete_user_favorite(username: str) -> dict:
    result = await users_collection.update_one(
        {"username": username},
        {"$unset": {"favorite_facility": None}}
    )

    if result.modified_count == 1:
        return await get_user(username)

    raise HTTPException(status_code=404, detail="User not found or favorite facility already removed")
