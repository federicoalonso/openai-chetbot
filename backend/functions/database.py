import json
import random
# get recent messages
def get_recent_messages():
    file_name = "stored_data.json"
    learn_instructions = {
        "role": "system",
        "content": "Eres un profesor de ingles, estas tratando con un usuario que te contrató para una clase de 5 minutos de conversación en ingles. El objetivo es que practique ingles fluido y que a su vez aprenda, por lo que si comete errores debes enseñarle. Primero habría que preguntar cuáles son sus intereses o de qué desea hablar y posteriormente tu función es también hacer que hable y llevar el control de la conversación para que el usuario practique y aprenda ingles, por lo que tus respuestas deben ser cortas y deben introducir una pregunta o tema al usuario, para que el usuario participe. Tu nombre es Bella"
    }

    # Initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)

    if x < 0.5:
        learn_instructions["content"] = learn_instructions["content"] + " Tu respuesta va a ser divertida, pero no te rías de él, solo hazlo para que se sienta cómodo y se ría contigo."
    else:
        learn_instructions["content"] = learn_instructions["content"] + " Tu respuesta va a incluir una pregunta para que el usuario participe y hable."

    # Add learn instructions
    messages.append(learn_instructions)

    # Get last messages
    try:
        with open(file_name, "r") as f:
            data = json.load(f)

            # Append last 5 items of data
            if data:
                if len(data) > 5:
                    for item in data[-5:]:
                        messages.append(item)
                else:
                    for item in data:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass

    return messages

# Store message
def store_message(request_message, response_message):
    file_name = "stored_data.json"

    # Get last messages
    messages = get_recent_messages()[1:]

    # Append new message
    user_message = {
        "role": "user",
        "content": request_message
    }
    assistant_message = {
        "role": "assistant",
        "content": response_message
    }
    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as f:
        json.dump(messages, f)

def reset_messages():
    file_name = "stored_data.json"

    # Initialize messages
    messages = []

    with open(file_name, "w") as f:
        json.dump(messages, f)