import os
import tempfile
import base64

import httpx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from config.setting import AI_BASE_URL

router = APIRouter()


@router.post("/separate-voice")
async def separate_voice(file: UploadFile = File(...)):
    """
    Receive an audio file, forward it to the AI server for voice separation,
    and return both the vocals and instrumental tracks as base64 encoded strings.
    """
    SEPARATE_VOICE_URL = f"{AI_BASE_URL}/ai/separate-voice"

    tmp_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Send file to AI server
        with open(tmp_path, "rb") as f:
            files = {"file": (file.filename, f, file.content_type)}
            async with httpx.AsyncClient(
                timeout=300.0
            ) as client:  # Longer timeout for processing
                ai_response = await client.post(SEPARATE_VOICE_URL, files=files)

        # Handle AI server response
        if ai_response.status_code != 200:
            return JSONResponse(
                content={"error": "AI server error", "detail": ai_response.text},
                status_code=500,
            )

        # Get the audio data from response
        response_data = ai_response.json()

        # Convert binary data to base64 if it's not already
        if isinstance(response_data["vocals"], bytes):
            vocals_base64 = base64.b64encode(response_data["vocals"]).decode()
            instrumental_base64 = base64.b64encode(
                response_data["instrumental"]
            ).decode()
        else:
            vocals_base64 = response_data["vocals"]
            instrumental_base64 = response_data["instrumental"]

        # Return both files as base64 strings
        return JSONResponse(
            content={"vocals": vocals_base64, "instrumental": instrumental_base64}
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
