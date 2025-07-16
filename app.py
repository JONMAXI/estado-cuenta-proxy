from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

MY_TOKEN = "1234567890abcdef"
TOKEN_API_ORIGINAL = "3oJVoAHtwWn7oBT4o340gFkvq9uWRRmpFo7p"
API_ORIGINAL_URL = "https://servicios.s2movil.net/s2maxikash/estadocuenta"

@app.route("/api/estado-cuenta", methods=["POST"])
def estado_cuenta():
    # 1. Validación del token personalizado
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"codigo_http": 401, "error": "Token de autorización no proporcionado"}), 401

    client_token = auth_header.split(" ")[1]
    if client_token != MY_TOKEN:
        return jsonify({"codigo_http": 403, "error": "Token inválido"}), 403

    datos = request.get_json()
    if not datos:
        return jsonify({"codigo_http": 400, "error": "Falta el body con datos JSON"}), 400

    # 2. Fecha automática
    if "fechaCorte" not in datos or not datos["fechaCorte"]:
        datos["fechaCorte"] = datetime.today().strftime("%Y-%m-%d")

    try:
        headers = {
            "Token": TOKEN_API_ORIGINAL,
            "Content-Type": "application/json"
        }

        response = requests.post(API_ORIGINAL_URL, headers=headers, json=datos)

        if response.status_code != 200:
            return jsonify({
                "codigo_http": response.status_code,
                "error": "Error al consultar la API original",
                "detalles": response.text
            }), response.status_code

        # 3. Limpiar el response
        original_data = response.json()

        estado_cuenta = original_data.get("estadoCuenta", {})
        datos_filtrados = {
            "cuota": estado_cuenta.get("cuota"),
            "datosCargos": [],
            "fechaInicio": estado_cuenta.get("fechaInicio"),
            "fechaLiquidacion": estado_cuenta.get("fechaLiquidacion"),
            "idCredito": estado_cuenta.get("idCredito"),
            "periodicidad": estado_cuenta.get("periodicidad"),
            "primerVencimiento": estado_cuenta.get("primerVencimiento"),
            "referenciaSTP": estado_cuenta.get("referenciaSTP"),
            "statusCredito": estado_cuenta.get("statusCredito"),
            "ultimoVencimiento": estado_cuenta.get("ultimoVencimiento"),
        }

        # Extraer y limpiar datosCargos
        for cargo in estado_cuenta.get("datosCargos", []):
            datos_filtrados["datosCargos"].append({
                "concepto": cargo.get("concepto"),
                "fechaMovimiento": cargo.get("fechaMovimiento"),
                "fechaVencimiento": cargo.get("fechaVencimiento"),
                "idCargo": cargo.get("idCargo"),
                "monto": cargo.get("monto")
            })

        return jsonify({
            "codigo_http": 200,
            "data": datos_filtrados
        }), 200

    except Exception as e:
        return jsonify({"codigo_http": 500, "error": "Error interno", "detalles": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
