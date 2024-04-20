from fastapi import FastAPI
from pydantic import BaseModel

from .models import Location
from typing import List
from fastapi import APIRouter
from common.models import OfficeEntity

office_router = APIRouter(
    tags=["offices"]
)

class Office(BaseModel):
    officeId: str
    name: str
    location: Location

@office_router.post("/load_base")
def load_offices():
    engine = create_engine(POSTGRE_CONNECTION)
    sesion_maker = sessionmaker(engine)
    session = sesion_maker()
    office1 = OfficeEntity(name="Main Office",lattitude=52.196774,longitude=21.017593)
    office2 = OfficeEntity(name="Branch Office",lattitude=51.107748,longitude=17.068012)
    try:
        session.add(office1)
        session.add(office2)
        session.commit()
        return JSONResponse(status_code=200, content="loaded")
    except Exception as e:
        return JSONResponse(status_code=404, content="loaded")






@office_router.get("/", response_model=List[Office])
def get_offices():
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        entity = session.query(OfficeEntity).all()
        content = {"name": entity.name,
                   "contact": entity.contact}
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        return JSONResponse(status_code=404, content="User not found")
