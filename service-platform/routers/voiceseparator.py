import os
import tempfile

import httpx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from config.setting import AI_BASE_URL

router = APIRouter()


@router.post("/separate-voice")
async def separate_voice(file: UploadFile = File(...)):
    """
    Receive an audio file, forward it to the AI server for voice separation,
    and return both the vocals and instrumental tracks.
    """
    SEPARATE_VOICE_URL = f"{AI_BASE_URL}/ai/separate-voice"

    tmp_path = None
    vocals_path = None
    instrumental_path = None

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

        # Save the separated audio files temporarily
        vocals_path = tempfile.mktemp(suffix=".wav")
        instrumental_path = tempfile.mktemp(suffix=".wav")

        with open(vocals_path, "wb") as f:
            f.write(ai_response.json()["vocals"])
        with open(instrumental_path, "wb") as f:
            f.write(ai_response.json()["instrumental"])

        # Return both files in the response
        return JSONResponse(
            content={
                "vocals": FileResponse(
                    vocals_path, media_type="audio/wav", filename="vocals.wav"
                ),
                "instrumental": FileResponse(
                    instrumental_path,
                    media_type="audio/wav",
                    filename="instrumental.wav",
                ),
            }
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Clean up temporary files
        for path in [tmp_path, vocals_path, instrumental_path]:
            if path and os.path.exists(path):
                os.remove(path)
