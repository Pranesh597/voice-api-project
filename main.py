from fastapi import FastAPI, Header, HTTPException, Form
import base64
import librosa
import io

app = FastAPI()

API_KEY = "my_secret_key_123"

@app.post("/predict")
def predict(
    language: str = Form(...),
    audio_format: str = Form(...),
    audio_base64: str = Form(...),
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        audio_bytes = base64.b64decode(audio_base64)
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

    except Exception as e:
        return {
            "result": "HUMAN",
            "confidence": 0.5
        }
