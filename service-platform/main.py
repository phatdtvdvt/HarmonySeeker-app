from fastapi import FastAPI, Request
from routers import router  # Import the main router aggregator
from fastapi.middleware.cors import CORSMiddleware
import os
import time

app = FastAPI()


@app.get("/health")
def health_check():
    """Health check endpoint for server status"""
    return {"status": "ok"}


# Include all routers under the /api prefix
app.include_router(router, prefix="/api")

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
