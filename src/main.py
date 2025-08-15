from fastapi import FastAPI
from sqlmodel import Session
from src.database import SessionLocal, get_db, engine, Base
from src.api import api_router
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from src.EmployeeTasks.service import start_scheduler 
from src.Attendance.service import start_sign_out_scheduler
from src.ProductStages.service import start_scheduler1


#def init_db():
SQLModel.metadata.create_all(engine)

#Base.metadata.create_all(bind=engine)
db = SessionLocal()
app = FastAPI()



@app.on_event("startup")
def startup_event():
    
    start_scheduler()
    start_sign_out_scheduler()
    start_scheduler1()
    

@app.on_event("shutdown")
def shutdown_event():
    
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.shutdown()







logger = logging.getLogger()
logger.setLevel(logging.INFO)

origins = [
    "https://surfhealthprogram.com",
    "http://surfhealthprogram.com",
    "*",
#     "http://192.168.29.197:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# we add all API routes to the Web API framework
app.include_router(api_router, prefix="/v1")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.mount("/admin", StaticFiles(directory="admin"), name="admin")

app.mount("/superadmin", StaticFiles(directory="superadmin"), name="superadmin")


@app.get("/")
async def root():
    return {"message": "Production Code"}
