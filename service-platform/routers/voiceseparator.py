import os
import tempfile
import base64

from dotenv import load_dotenv
import httpx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

# Load environment variables
load_dotenv(override=True)

AI_BASE_URL = os.getenv("AI_BASE_URL")

print("AI_BASE_URL", AI_BASE_URL)


@router.post("/separate-voice")
async def separate_voice(file: UploadFile = File(...)):
    """
    Receive an audio file, forward it to the AI server for voice separation,
    and return the S3 URLs for both the vocals and instrumental tracks.
    """
    SEPARATE_VOICE_URL = f"{AI_BASE_URL}/ai/separate-voice"
    file_bytes = await file.read()

    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, file_bytes, file.content_type)}
        response = await client.post(SEPARATE_VOICE_URL, files=files, timeout=None)

        # Parse the response JSON
        response_data = response.json()

        # Return the S3 URLs in the same format
        return JSONResponse(
            {
                "vocals_url": response_data["vocals_url"],
                "music_url": response_data["music_url"],
                "expiration": response_data["expiration"],
            }
        )
