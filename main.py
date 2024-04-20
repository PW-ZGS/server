import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.office_route import offices
from routes.user_route import validate_user, user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(offices)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
