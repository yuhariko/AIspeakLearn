import os
import uvicorn
import shutil

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse

from utils.utils import find_or_create_temp_dir
from pipeline.speak_pipeline import SpeakAI

app = FastAPI()

try:
    temp_dir = find_or_create_temp_dir()
    temp_voice_in = os.path.join(temp_dir, 'voice_in')
    if not os.path.exists(temp_voice_in):
        os.makedirs(temp_voice_in, exist_ok=True)
except OSError:
    pass

speak_pipeline = SpeakAI()

@app.get("/")
async def get():
    return {"message": "HUY SPEAK AI API}"}


@app.post("/speak")
async def speak_ai(id: str = Form(...), topic: str = Form(...), file: UploadFile = File(...)):
    file_location = f"{temp_voice_in}/{file.filename}"

    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = speak_pipeline.serve(id, file_location, topic)

    if os.path.exists(result['speak']):
        # Open the audio file for streaming
        def iterfile():
            with open(result['speak'], mode="rb") as file_like:
                yield from file_like

        audio_response = StreamingResponse(iterfile(), media_type="audio/mpeg")

        audio_response.headers["user_text"] = result["user_text"]
        audio_response.headers["llm_message"] = result["llm_message"]

        return audio_response
    return JSONResponse(content={"error": "File not found"}, status_code=404)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        proxy_headers=True
    )