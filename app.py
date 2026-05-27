from flask import Flask, render_template, request, jsonify, Response
import socket
import concurrent.futures
import csv
import io

app = Flask(__name__)

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 8080: "HTTP-alt", 8443: "HTTPS-alt"
}

def scan_port(host, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return {"port": port, "status": "open", "service": COMMON_SERVICES.get(port, "-")}
        return {"port": port, "status": "closed", "service": COMMON_SERVICES.get(port, "-")}
    except Exception:
        return {"port": port, "status": "error", "service": "-"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    host = data.get("host", "").strip()
    port_range = data.get("range", "1-1024")

    try:
        start, end = map(int, port_range.split("-"))
        end = min(end, 3524)
    except Exception:
        return jsonify({"error": "Plage de ports invalide"}), 400

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return jsonify({"error": "Hôte introuvable"}), 400

    ports = range(start, end + 1)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: x["port"])
    open_ports = [r for r in results if r["status"] == "open"]
    return jsonify({"results": open_ports, "total_scanned": len(results)})
    
@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    results = data.get("results", [])
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["port", "service", "status"], delimiter=";")
    writer.writeheader()
    writer.writerows(results)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=scan_results.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)