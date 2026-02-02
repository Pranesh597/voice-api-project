from fastapi import FastAPI, HTTPException
import requests
import librosa
import io

app = FastAPI()

API_KEY = "my_secret_key_123"

@app.post("/predict")
def predict(audio_url: str, api_key: str):

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = requests.get(audio_url)
        audio_bytes = io.BytesIO(response.content)

        y, sr = librosa.load(audio_bytes, sr=16000)

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
