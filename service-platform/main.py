from fastapi import FastAPI, Request
from routers import songchord
from fastapi.middleware.cors import CORSMiddleware
import os
import time
app = FastAPI()

songchord_app = FastAPI(debug=True)

songchord_app.include_router(songchord.router)

app.mount("/songchord", songchord_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("startup")



@app.on_event("shutdown")
async def shutdown():
    print("Closing...")

