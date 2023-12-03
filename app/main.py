from fastapi import FastAPI
from .api.endpoints import router as api_router
from .database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router)
