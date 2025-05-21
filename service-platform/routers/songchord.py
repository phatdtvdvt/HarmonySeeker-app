import os
import tempfile

import httpx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import soundfile as sf

router = APIRouter()


@router.post("/predict-chord")
async def predict_chord(file: UploadFile = File(...)):
    """
    Receive an audio file, forward it to the AI server, then group the returned chord sequence
    into segments with the same consecutive chords, each with start_time and end_time.
    """
    AI_BASE_URL = os.getenv("AI_BASE_URL", "http://localhost:8000")
    PREDICT_CHORD_URL = f"{AI_BASE_URL}/ai/predict-chord"
    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 22050))
    HOP_LENGTH = int(os.getenv("HOP_LENGTH", 512))
    N_FRAMES = int(os.getenv("N_FRAMES", 1000))

    tmp_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Get duration of the uploaded audio file (in seconds)
        with sf.SoundFile(tmp_path) as audio_file:
            total_duration = len(audio_file) / audio_file.samplerate

        # Send file to AI server
        with open(tmp_path, "rb") as f:
            files = {"file": (file.filename, f, file.content_type)}
            async with httpx.AsyncClient(timeout=60.0) as client:
                ai_response = await client.post(PREDICT_CHORD_URL, files=files)

        # Handle AI server response
        if ai_response.status_code != 200:
            return JSONResponse(
                content={"error": "AI server error", "detail": ai_response.text},
                status_code=500,
            )

        ai_data = ai_response.json()
        chord_sequence = ai_data.get("chord_sequence", [])
        key = ai_data.get("key")
        main_chord = ai_data.get("main_chord")
        interval = total_duration / len(chord_sequence) if chord_sequence else 0

        # Group consecutive identical chords into segments with timing (simple version)
        result = []
        if chord_sequence and interval > 0:
            n = len(chord_sequence)
            i = 0
            while i < n:
                chord = chord_sequence[i]
                start_idx = i
                # Move j forward while the next chord is the same
                j = i + 1
                while j < n and chord_sequence[j] == chord:
                    j += 1
                # j is now the first index with a different chord or n
                result.append(
                    {
                        "chord": chord,
                        "start_time": round(start_idx * interval, 3),
                        "end_time": round(j * interval, 3),
                    }
                )
                i = j

        return JSONResponse(
            content={"key": key, "main_chord": main_chord, "chord_segments": result}
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
