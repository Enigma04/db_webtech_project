from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, HttpUrl


class KinderGartenFacilityModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    X: float
    Y: float
    OBJECTID: int
    ID: int
    TRAEGER: str
    BEZEICHNUNG: str
    KURZBEZEICHNUNG: str
    STRASSE: str
    STRSCHL: int
    HAUSBEZ: int
    PLZ: int
    ORT: str
    HORT: int
    KITA: int
    TELEFON: Optional[str] = None
    EMAIL: Optional[str] = None
    BARRIEREFREI: int
    INTEGRATIV: int

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
    ART: str
    # STANDORTTYP: int
    BEZEICHNUNG: str
    KURZBEZEICHNUNG: str
    STRASSE: str
    PLZ: int
    ORT: str
    TELEFON: Optional[str] = None
    FAX: Optional[str] = None
    EMAIL: Optional[EmailStr] = None
    PROFILE: Optional[str] = None
    WWW: Optional[HttpUrl] = None
    TRAEGER: str
    TRAEGERTYP: int
    # BEZUGNR: Optional[int] = None
    GEBIETSARTNUMMER: int
    SNUMMER: int
    NUMMER: int
    GlobalID: Optional[UUID] = None

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
                # "STANDORTTYP": 1,
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
                # "BEZUGNR": 30,
                "GEBIETSARTNUMMER": 40,
                "SNUMMER": 139,
                "NUMMER": 503,
                "GlobalID": "0e6df524-c87d-4844-9c7f-11feabdc3d6b"
            }
        }


class SPFacilityModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    X: float
    Y: float
    OBJECTID: int
    ID: int
    TRAEGER: str
    LEISTUNGEN: str
    STRASSE: str
    PLZ: int
    ORT: str

    # TELEFON: Optional[str] = None

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
                # "TELEFON": "0371 8157527\n0174 3522231"
            }
        }


class UserModel(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str


class UserInDB(UserModel):
    hashed_password: str