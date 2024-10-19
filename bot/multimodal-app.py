from fastapi import FastAPI, Request
import httpx
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


# Replace with your own WhatsApp Business credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0/{phone_number_id}/messages"
MEDIA_URL = "https://graph.facebook.com/v17.0/{media_id}"
ACCESS_TOKEN = "EAAPvbjrr0ZAYBOw9VaZBK0FXGCUj66DqHwp7nyfnpZBKwpfymajcQgXRZAddJyqV94VtZA53QMAkeCV9kOdKjniwZAcQikGjABQLdTpZBklmOZCs0U9B0HSXXLcCwiGXgZBM8HIxrpxIVXHQdx9aVMtiYKxbZA0U9zFh4IoL3BzJOFnZBSAQha9lUHXfOUhHTWsQtgpR5Bb4jCMBGquxfMEVmZAZCZAJGqxZC4ZD"
PHONE_NUMBER_ID = "447655318432169"

# Model for WhatsApp message
class WhatsAppMessage(BaseModel):
    object: str
    entry: list

# Webhook to receive incoming messages from WhatsApp
# @app.post("/webhook")
# async def receive_message(request: Request):
#     data = await request.json()
#     message_data = WhatsAppMessage(**data)

#     if message_data.entry and message_data.entry[0]["changes"]:
#         messages = message_data.entry[0]["changes"][0]["value"]["messages"]
#         if messages:
#             for message in messages:
#                 user_phone = message["from"]

#                 # Handling Text Message
#                 if message.get("text"):
#                     user_message = message["text"]["body"]

#                     # Respond based on the text input
#                     if user_message.lower() == "hi":
#                         await send_message(user_phone, "Hello! Send text, image, or audio for processing.")
#                     elif user_message == "1":
#                         await send_message(user_phone, "Here is the info you requested.")
#                     elif user_message == "2":
#                         await send_message(user_phone, "Our support team will reach out to you soon.")
#                     elif user_message == "3":
#                         await send_message(user_phone, "Please submit your text, image, or audio request.")
#                     else:
#                         await send_message(user_phone, "I did not understand that. Please choose from the options: 1, 2, or 3.")

#                 # Handling Image Message
#                 elif message.get("image"):
#                     media_id = message["image"]["id"]
#                     media_url = await fetch_media(media_id)
#                     await send_message(user_phone, f"Image received. Download URL: {media_url}")

#                 # Handling Audio Message
#                 elif message.get("audio"):
#                     media_id = message["audio"]["id"]
#                     media_url = await fetch_media(media_id)
#                     await send_message(user_phone, f"Audio received. Download URL: {media_url}")

#     return {"status": "success"}

# Function to send a message using WhatsApp API
async def send_message(to: str, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            WHATSAPP_API_URL.format(phone_number_id=PHONE_NUMBER_ID),
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": text}
            }
        )
    if response.status_code == 200:
        print(f"Message sent to {to}: {text}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Function to fetch media (image or audio) using the media ID
async def fetch_media(media_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            MEDIA_URL.format(media_id=media_id),
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
    if response.status_code == 200:
        media_data = response.json()
        media_url = media_data.get("url")
        return media_url
    else:
        print(f"Failed to fetch media. Status code: {response.status_code}")
        return None

# Endpoint to verify webhook with WhatsApp
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    print(mode)
    print(token)
    print(challenge)

    # if mode and token and mode == "subscribe" and token == "1234":
        # return {"hub_verfiy_mode":mode,"hub_verify_token":token, "hub_verify_challange":challenge }
    return challenge
    # return {"error": "Invalid verification token"}
