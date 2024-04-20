import uuid

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    contact = Column(String(50), nullable=False)


class OfficeEntity(Base):
    __tablename__ = 'office'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)


class RouteEntity(Base):
    __tablename__ = 'route'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    directions_text = Column(String, nullable=False)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    office_id = Column(String, ForeignKey('office.id'), nullable=False)
    owner_id = Column(String, ForeignKey('user.id'), nullable=False)

    office = relationship('OfficeEntity', backref='routes')
    owner = relationship('UserEntity', backref='routes')


class DriverRouteEntity(Base):
    __tablename__ = 'driver_route'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    passenger_count = Column(Integer, default=0)
    route_id = Column(String, ForeignKey('route.id'))

    route = relationship('RouteEntity', backref='driver_routes')


class PassengerRouteEntity(Base):
    __tablename__ = 'passenger_route'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    max_distance = Column(Float)
    route_id = Column(String, ForeignKey('route.id'))

    route = relationship('RouteEntity', backref='passenger_routes')


class RouteMatchEntity(Base):
    __tablename__ = 'route_match'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    passenger_route_id = Column(String, ForeignKey('passenger_route.id'), nullable=False)
    driver_route_id = Column(String, ForeignKey('driver_route.id'), nullable=False)

    passenger_route = relationship('PassengerRouteEntity', backref='matches')
    driver_route = relationship('DriverRouteEntity', backref='matches')
