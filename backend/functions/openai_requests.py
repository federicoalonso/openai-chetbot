import openai
from decouple import config

from functions.database import get_recent_messages

# Retrieve API key from .env file
openai.api_key = config("OPENAI_API_KEY")
openai.organization = config("OPENAI_ORGANIZATION")

# Open AI - Whisper
# Convert Audio to Text
def convert_audio_to_text(audio):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return
    
# Open AI - ChatGPT
# Get bot response to user message
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {
        "role": "user",
        "content": message_input
    }
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(response)
        messages_text = response["choices"][0]["message"]["content"]
        return messages_text
    except Exception as e:
        print(e)
        return