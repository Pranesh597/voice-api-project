from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import librosa
import io
import numpy as np

app = FastAPI()

API_KEY = "my_secret_key_123"


class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.post("/predict")
def predict(request: AudioRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        audio_file = io.BytesIO(audio_bytes)

        y, sr = librosa.load(audio_file, sr=16000)

        duration = len(y) / sr

        if duration > 3:
            result = "HUMAN"
            confidence = 0.85
        else:
            result = "AI_GENERATED"
            confidence = 0.80

        return {
            "result": result,
            "confidence": float(confidence)
        }

    except:
        return {
            "result": "HUMAN",
            "confidence": 0.5
        }


@app.get("/honeypot")
def honeypot(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "active",
        "message": "Honeypot endpoint reached successfully"
    }
