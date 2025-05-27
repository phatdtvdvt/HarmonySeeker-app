# HarmonySeeker Service Platform

Backend service for the HarmonySeeker application, providing APIs for:
- Song chord recognition
- Voice separation
- Audio processing

## Setup

```bash
# Install dependencies
poetry install

# Run development server
poetry run uvicorn main:app --reload

# Run tests
poetry run pytest
```

## API Endpoints

### Voice Separator
`POST /api/separate-voice`
- Separates vocals and instrumental tracks from an audio file
- Input: Audio file (mp3, wav, flac)
- Output: Base64 encoded vocals and instrumental tracks

### Song Chord Recognition
`POST /api/recognize-chord`
- Recognizes chords from an audio file
- Input: Audio file (mp3, wav, flac)
- Output: JSON with chord progression and timing 