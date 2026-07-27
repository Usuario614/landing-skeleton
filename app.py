from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# --- Config por cliente ---
# Cambiá esta variable para apuntar al cliente que estés armando
CLIENTE_ACTUAL = "cliente_ejemplo"

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
    whatsapp = request.form.get("whatsapp")

    # Por ahora lo guardamos en un archivo de texto simple
    with open("leads.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre} | {email} | {whatsapp}\n")

    return redirect("/gracias")

@app.route("/gracias")
def gracias():
    config = cargar_config(CLIENTE_ACTUAL)
    return render_template("gracias.html", config=config)

if __name__ == "__main__":
    app.run(debug=True)