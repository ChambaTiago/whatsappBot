import requests

API_KEY = "AIzaSyBiK3VV4esdWaGJjsw09cf7SPHNN6PqT_E"

def preguntar_a_gemini(mensaje):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": mensaje
                    }
                ]
            }
        ]
    }
    response = requests.post(
        f"{url}?key={API_KEY}",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        respuesta = response.json()
        texto = respuesta["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini dice:\n", texto)
    else:
        print("Error:", response.text)

# PROBALO CON ESTO
preguntar_a_gemini("¿Qué opinás de la termodinámica?")
