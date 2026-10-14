from flask import Flask, request, jsonify, render_template
from pdf_utils import extraer_texto
from llm import resumir
from firebase_db import guardar_resumen
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    archivo = request.files["file"]
    if not archivo.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Solo se permiten PDFs"}), 400

    texto = extraer_texto(archivo.read())
    if not texto:
        return jsonify({"error": "El PDF no tiene texto extraíble (¿está escaneado?)"}), 422

    try:
        resumen = resumir(texto)
    except Exception as e:
        return jsonify({"error": f"Error con Ollama: {e}"}), 500

    try:
        doc_id = guardar_resumen(archivo.filename, resumen)
    except Exception as e:
        return jsonify({"error": f"Error con Firebase: {e}"}), 500

    return jsonify({"id": doc_id})

if __name__ == "__main__":
    app.run(debug=True, port=5000)