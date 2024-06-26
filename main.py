import multitimer
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from geoRouter.geoRouter import schedule
from routes.driver_routes import driver_route
from routes.matches_routes import match_routes
from routes.office_route import office_router
from routes.passenger_routes import passenger_route_router
from routes.user_route import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(office_router)
app.include_router(driver_route)
app.include_router(passenger_route_router)
app.include_router(match_routes)

app.mount("/html", StaticFiles(directory="html"), name="html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    # timer = multitimer.MultiTimer(interval=15, function=schedule, runonstart=False)
    # timer.start()
    uvicorn.run(app, host="localhost", port=8080)
