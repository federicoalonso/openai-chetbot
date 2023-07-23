from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from decouple import config
import openai

from functions.openai_requests import convert_audio_to_text
from functions.openai_requests import get_chat_response
from functions.database import store_message, reset_messages
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/health")
async def check_health():
    return {"message": "Status: OK"}

@app.get("/reset")
async def reset_messages():
    reset_messages()
    return {"message": "Messages reset"}

# Get bot response
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # audio_input = open("voice.mp3", "rb")
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")

    message_decoded = convert_audio_to_text(audio_input)

    # Guard: ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=500, detail="Message not decoded")
    
    # Get chat response
    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        return HTTPException(status_code=500, detail="Chat response not received")

    print(chat_response)

    # Store message
    store_message(message_decoded, chat_response)

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=500, detail="Audio not received")
    

    # Return audio
    def iterfile():
        yield audio_output
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream")