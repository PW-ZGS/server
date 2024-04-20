import json

from pydantic import BaseModel

from .models import Location
from typing import List
from fastapi import APIRouter
from common.models import OfficeEntity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.credentials import POSTGRE_CONNECTION
from fastapi.responses import JSONResponse

office_router = APIRouter(
    prefix="/offices",
    tags=["offices"]
)

class Office(BaseModel):
    officeId: str
    name: str
    location: Location

@office_router.post("/load_base")
def load_offices():
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    office1 = OfficeEntity(name="Main Office",latitude=52.196774,longitude=21.017593)
    office2 = OfficeEntity(name="Branch Office",latitude=51.107748,longitude=17.068012)
    try:
        session.add(office1)
        session.add(office2)
        session.commit()
        return JSONResponse(status_code=200, content="loaded")
    except Exception as e:
        return JSONResponse(status_code=404, content="not_loaded")






@office_router.get("/", response_model=List[Office])
def get_offices():
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        entities = session.query(OfficeEntity).all()
        offices = [{"officeId":str(entity.id), "name": entity.name,"location":{"latitude":float(entity.latitude),"longitude":float(entity.longitude)}} for entity in entities]
        return JSONResponse(status_code=200, content=json.dumps(offices))
    except Exception as e:
        return JSONResponse(status_code=404, content="User not found")
