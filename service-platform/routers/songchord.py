from fastapi import APIRouter, Depends, File, UploadFile, Form, Query, Request
from datetime import date


router = APIRouter()

@router.get(
    "/",
)
def get_auction():
    return []