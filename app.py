from flask import Flask, render_template, request, redirect
import json
import os
import requests

app = Flask(__name__)

# --- Config por cliente ---
# Cambiá esta variable para apuntar al cliente que estés armando
CLIENTE_ACTUAL = "cliente_ejemplo"

# URL del webhook de n8n (test por ahora)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/35a29b1f-8cbb-409f-b58f-df8428191699"

def cargar_config(nombre_cliente):
    ruta = os.path.join("config", f"{nombre_cliente}.json")
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    config = cargar_config(CLIENTE_ACTUAL)
    return render_template("index.html", config=config)

@app.route("/enviar-lead", methods=["POST"])
def enviar_lead():
    nombre = request.form.get("nombre")
    email = request.form.get("email")

    # Guardamos el lead localmente como respaldo
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre} | {email}\n")

    # Enviamos el lead a n8n para automatizar lo que sigue
    try:
        requests.post(N8N_WEBHOOK_URL, json={
            "nombre": nombre,
            "email": email
        }, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"No se pudo enviar el lead a n8n: {e}")

    return redirect("/gracias")

@app.route("/gracias")
def gracias():
    config = cargar_config(CLIENTE_ACTUAL)
    return render_template("gracias.html", config=config)

if __name__ == "__main__":
    app.run(debug=True)