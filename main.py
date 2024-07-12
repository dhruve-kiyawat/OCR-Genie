# Importing necessary modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing custom modules
from models.RestfulModel import *
from routers import ocr
from utils.ImageHelper import *


app = FastAPI(
    title="Paddle OCR API",
    description="API using Paddle OCR and FastAPI for OCR operations."
)


# CORS settings
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Including routers
app.include_router(ocr.router)
