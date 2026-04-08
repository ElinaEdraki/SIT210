import json, urllib.request, urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

THING_ID      = "86fc4d36-cd83-4d8e-87ea-bb003cf5876d"
CLIENT_ID     = "Kr6PXpgcS32odxshp17X6lwwJGSP18jF"
CLIENT_SECRET = "hET81x4DMOXT9pZxuNjGH7hzGxVvwXAdp9GRL528Z9wOtG02LKKwpoSnJAt1mHBS"

def get_token():
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": "https://api2.arduino.cc/iot"
    }).encode()
    req = urllib.request.Request(
        "https://api2.arduino.cc/iot/v1/clients/token", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]

def get_prop_id(token, var_name):
    req = urllib.request.Request(
        f"https://api2.arduino.cc/iot/v2/things/{THING_ID}/properties",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as r:
        props = json.loads(r.read())
    for p in props:
        if p["name"] == var_name:
            return p["id"]
    raise Exception(f"Property '{var_name}' not found")

def publish(token, prop_id, value):
    data = json.dumps({"value": value}).encode()
    req = urllib.request.Request(
        f"https://api2.arduino.cc/iot/v2/things/{THING_ID}/properties/{prop_id}/publish",
        data=data, method="PUT",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.status

class Handler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/toggle":
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            try:
                token = get_token()
                prop_id = get_prop_id(token, body["var"])
                status = publish(token, prop_id, body["value"])
                self.respond(200, {"ok": True})
                print(f"  OK  {body['var']} -> {'ON' if body['value'] else 'OFF'}")
            except Exception as e:
                self.respond(500, {"ok": False, "error": str(e)})
                print(f"  ERR {e}")
        else:
            super().do_POST()

    def respond(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass

print("Server running -> open http://localhost:8080/linda_light_control.html")
HTTPServer(("", 8080), Handler).serve_forever()
