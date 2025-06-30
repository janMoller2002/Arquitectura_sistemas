import requests
from flask import Flask, request, Response
import itertools

# Lista de servidores backend (puertos de ejemplo)
BACKENDS = [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]

# Round-robin iterator
backend_cycle = itertools.cycle(BACKENDS)

app = Flask(__name__)

def get_next_backend():
    return next(backend_cycle)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    backend = get_next_backend()
    url = f"{backend}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args
        )
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return Response(f"Error al contactar backend: {e}", status=502)

if __name__ == "__main__":
    print("Load balancer escuchando en http://localhost:8088")
    app.run(host="0.0.0.0", port=8088)
