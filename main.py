from flask import Flask, jsonify, request
import socket
import datetime
import json
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return f"Hola desde el contenedor! Hostname: {socket.gethostname()}"

@app.route("/salud")
def salud():
    return jsonify({"status": "ok", "timestamp": datetime.datetime.now().isoformat()})

@app.route("/suma")
def suma():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        resultado = a + b
        return jsonify({"a": a, "b": b, "resultado": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/info")
def info():
    return jsonify({
        "hostname": socket.gethostname(),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/env")
def env():
    """Devuelve variables de entorno seleccionadas."""
    keys = request.args.getlist("key")
    if not keys:
        # Si no se especifican, devuelve todas (limitado a 10 para no saturar)
        env_vars = dict(list(os.environ.items())[:10])
    else:
        env_vars = {k: os.environ.get(k, None) for k in keys}
    return jsonify(env_vars)

@app.route("/json_echo", methods=["POST"])
def json_echo():
    """Recibe un JSON y lo devuelve junto con su representación en string."""
    try:
        data = request.get_json(force=True)
        data_str = json.dumps(data, ensure_ascii=False)
        return jsonify({"original": data, "string": data_str})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/archivo_demo")
def archivo_demo():
    """Crea un archivo demo.json y lo lee usando json."""
    demo_data = {"mensaje": "Esto es un archivo demo", "fecha": datetime.datetime.now().isoformat()}
    filename = "demo.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(demo_data, f)
    with open(filename, "r", encoding="utf-8") as f:
        contenido = json.load(f)
    os.remove(filename)
    return jsonify(contenido)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
