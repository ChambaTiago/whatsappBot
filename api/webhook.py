import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

AI_KEY = os.getenv("AI_STUDIO_KEY")
WA_PHONE_ID = os.getenv("WA_PHONE_NUMBER_ID")
WA_TOKEN = os.getenv("WA_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")

AI_URL = "https://api.studio.google.com/v1/models/gemini-2.5-pro-preview:generateMessage"

@app.route("/api/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Unauthorized", 403

    data = request.get_json()
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_ = msg["from"]
        text = msg["text"]["body"]

        headers = {"Authorization": f"Bearer {AI_KEY}"}
        payload = {
            "prompt": {"text": text},
            "temperature": 0.7,
            "candidateCount": 1
        }
        res = requests.post(AI_URL, headers=headers, json=payload)
        reply = res.json()["candidates"][0]["content"]

        wa_url = f"https://graph.facebook.com/v17.0/{WA_PHONE_ID}/messages"
        wa_payload = {
            "messaging_product": "whatsapp",
            "to": from_,
            "text": {"body": reply}
        }
        wa_headers = {
            "Authorization": f"Bearer {WA_TOKEN}",
            "Content-Type": "application/json"
        }
        requests.post(wa_url, headers=wa_headers, json=wa_payload)
        return "ok", 200
    except Exception as e:
        print("Error:", e)
        return "error", 500
