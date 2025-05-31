import os
import tempfile
import base64

import httpx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from config.setting import AI_BASE_URL
from fastapi.responses import StreamingResponse
import io
router = APIRouter()


@router.post("/separate-voice")
async def separate_voice(file: UploadFile = File(...)):
    """
    Receive an audio file, forward it to the AI server for voice separation,
    and return both the vocals and instrumental tracks as base64 encoded strings.
    """
    SEPARATE_VOICE_URL = f"{AI_BASE_URL}/ai/separate-voice"
    print(SEPARATE_VOICE_URL)
    # Đọc file nội dung
    file_bytes = await file.read()
    
    # Gửi file tới AI server
    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, file_bytes, file.content_type)}
        response = await client.post(SEPARATE_VOICE_URL, files=files, timeout=None)
    

    # Trả kết quả về FE dưới dạng StreamingResponse
    return StreamingResponse(
        io.BytesIO(response.content),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=separated_audio.zip"}
    )
