import uuid

from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float = Field(description="Latitude coordinate")
    longitude: float = Field(description="Longitude coordinate")

class DriverRoute(BaseModel):
    routeId: str = Field(description="Unique identifier of the route", default= lambda: str(uuid.uuid4()))
    startPoint: Location = Field(description="Geographic location of the starting point")
    endPoint: Location = Field(description="Geographic location of the ending point")

class DateRange(BaseModel):
    startDate: int = Field(description="Start date as Unix timestamp (milliseconds since epoch)")
    endDate: int = Field(description="End date as Unix timestamp (milliseconds since epoch)")


class RouteInput(BaseModel):
    officeId: str = Field(description="Unique identifier of the starting point (office)")
    startPoint: Location = Field(description="Geographic location of the starting point")
    fromTime: str = Field(description="Scheduled departure time")
    availableSeats: int = Field(description="Number of available seats")
    userId: str = Field(description="Unique identifier of the user creating the route")


class PassengerRouteInput(BaseModel):
    officeId: str = Field(description="Unique identifier of the desired starting point (office)")
    startPoint: Location = Field(description="Geographic location of the desired starting point")
    timeRange: DateRange = Field(description="Desired time range for the route")
    maxDist: int = Field(gt=0, description="Maximum acceptable distance from the desired starting point")


class DriverRoute(BaseModel):
    routeId: str = Field(description="Unique identifier of the route", default= lambda: str(uuid.uuid4()))
    startPoint: Location = Field(description="Geographic location of the starting point")
    endPoint: Location = Field(description="Geographic location of the ending point")


class PassengerRoute(BaseModel):
    passengerRouteId: str = Field(description="Unique identifier of the passenger's route",
                                  default= lambda: str(uuid.uuid4()))
    startPoint: Location = Field(description="Geographic location of the passenger's starting point")
    endPoint: Location = Field(description="Geographic location of the passenger's ending point")
