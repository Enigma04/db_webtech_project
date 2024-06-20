from fastapi import Body
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union


class KinderGartenFacilityModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    X: float
    Y: float
    OBJECTID: int
    ID: int
    TRAEGER: Optional[str] = None
    BEZEICHNUNG: Optional[str] = None
    KURZBEZEICHNUNG: Optional[str] = None
    STRASSE: str
    STRSCHL: Optional[int] = None
    HAUSBEZ: Optional[int] = None
    PLZ: int
    ORT: str
    HORT: Optional[int] = None
    KITA: Optional[int] = None
    TELEFON: Optional[str] = None
    EMAIL: Optional[str] = None
    BARRIEREFREI: Optional[int] = None
    INTEGRATIV: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "_id": {"$oid": "66588e8c5bee3b05edaf25c7"},
                "X": 12.9297116893286,
                "Y": 50.849579370555,
                "OBJECTID": 1,
                "ID": 1,
                "TRAEGER": "Privater Träger",
                "BEZEICHNUNG": "Josephinenplatz 8 \"Entdeckerland\", Kindertagespflege",
                "KURZBEZEICHNUNG": "Josephinenplatz 8 \"Entdeckerland\", Kindertagespflege",
                "STRASSE": "Josephinenplatz",
                "STRSCHL": 1340,
                "HAUSBEZ": 8,
                "PLZ": 9113,
                "ORT": "Chemnitz",
                "HORT": 0,
                "KITA": 1,
                "TELEFON": "0174 5909703",
                "EMAIL": "gudrun-entdeckerland@gmx.de",
                "BARRIEREFREI": 0,
                "INTEGRATIV": 0
            }
        }


class SchoolFacilityModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    X: float
    Y: float
    OBJECTID: int
    ID: int
    TYP: int
    ART: Optional[str] = None
    STANDORTTYP: Optional[int] = None
    BEZEICHNUNG: Optional[str] = None
    KURZBEZEICHNUNG: Optional[str] = None
    STRASSE: str
    PLZ: int
    ORT: str
    TELEFON: Optional[str] = None
    FAX: Optional[str] = None
    EMAIL: Optional[EmailStr] = None
    PROFILE: Optional[str] = None
    WWW: Optional[str] = None
    TRAEGER: Optional[str] = None
    TRAEGERTYP: Optional[int] = None
    BEZUGNR: Optional[int] = None
    GEBIETSARTNUMMER: Optional[int] = None
    SNUMMER: Optional[int] = None
    NUMMER: Optional[int] = None

    # GlobalID: Optional[UUID] = None

    class Config:
        schema_extra = {
            "example": {
                "_id": "66588e0a5bee3b05edaf2547",
                "X": 12.9412264741818,
                "Y": 50.8364972682956,
                "OBJECTID": 15,
                "ID": 30,
                "TYP": 10,
                "ART": "Grundschule",
                "STANDORTTYP": 1,
                "BEZEICHNUNG": "Grundschule Sonnenberg",
                "KURZBEZEICHNUNG": "GS Sonnenberg",
                "STRASSE": "Ludwig-Kirsch-Straße 27",
                "PLZ": 9130,
                "ORT": "Chemnitz",
                "TELEFON": "0371 36777220",
                "FAX": "0371 367772218",
                "EMAIL": "gs-sonnenberg@schulen-chemnitz.de",
                "PROFILE": "Hort",
                "WWW": "https://cms.sachsen.schule/gscsonnenberg/start.html",
                "TRAEGER": "Kommunal",
                "TRAEGERTYP": 10,
                "BEZUGNR": 30,
                "GEBIETSARTNUMMER": 40,
                "SNUMMER": 139,
                "NUMMER": 503,
                # "GlobalID": "0e6df524-c87d-4844-9c7f-11feabdc3d6b"
            }
        }


class SPFacilityModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    X: float
    Y: float
    OBJECTID: int
    ID: int
    TRAEGER: Optional[str] = None
    LEISTUNGEN: Optional[str] = None
    STRASSE: str
    PLZ: int
    ORT: str
    TELEFON: str
    FAX: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_id": {"$oid": "66588eaa5bee3b05edaf26bf"},
                "X": 12.8251258225996,
                "Y": 50.8115128110385,
                "OBJECTID": 6,
                "ID": 6,
                "TRAEGER": "Selbsthilfe Wohnprojekt Further Straße e. V.",
                "LEISTUNGEN": "Schulsozialarbeit",
                "STRASSE": "Lennéstraße 1",
                "PLZ": 9117,
                "ORT": "Chemnitz",
                "TELEFON": "0371 8157527\n0174 3522231",
                "FAX": "0371 3692321"
            }
        }


FacilityType = Union[SchoolFacilityModel, KinderGartenFacilityModel, SPFacilityModel]
favourite_facility_dt = Union[dict, str, int, bool, float, list]


class UserModel(BaseModel):
    username: str = Field(..., example="johndoe@mail.com")
    email: EmailStr = Field(..., example="johndoe@mail.com")
    full_name: Optional[str] = Field(None, example="John Doe")
    address: str = Field(..., example="Luscious Avenue 114")
    house_number: Optional[str] = Field(None, example="123")
    plz: str = Field(..., example="09123")


class UserFavoriteFacilityModel(BaseModel):
    user_id: str
    facility_id: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="John Doe")
    password: Optional[str] = Field(None, example="strong_password")
    favourite_facility: Optional[favourite_facility_dt] = Field(None, example="id: ...., X: ...., Y: .....")
    address: str = Field(..., example="Luscious Avenue 114")
    house_number: Optional[str] = Field(None, example="123")
    plz: str = Field(..., example="09123")


class UserLogin(BaseModel):
    username: str
    password: str


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    address: str
    house_number: Optional[str] = None
    plz: str


class UserInDB(UserModel):
    hashed_password: str


class FavoriteFacility(BaseModel):
    facility_id: str


class TokenResponse(BaseModel):
    message: str = Field(..., example="User registered and logged in successfully"),
    access_token: str = Field(...,
                              example="access_token"),
    token_type: str = Field(..., example="bearer"),


class LoginResponse(BaseModel):
    access_token: str = Field(...,
                              example="access_token"),
    token_type: str = Field(..., example="bearer"),
