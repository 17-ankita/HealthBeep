import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse

DB_FILE = 'medicines.db'

# Ensure database exists
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS Medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    time TEXT NOT NULL
)
''')
conn.commit()
conn.close()

class MedicineHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/get_medicines':
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT id, name, dosage, time FROM Medicines ORDER BY time")
            rows = c.fetchall()
            conn.close()
            medicines = [{"id": r[0], "name": r[1], "dosage": r[2], "time": r[3]} for r in rows]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(medicines).encode())
        else:
            # Serve static files (like index.html, CSS, JS)
            super().do_GET()

    def do_POST(self):
        if self.path == '/add_medicine':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            name = data.get('name')
            dosage = data.get('dosage')
            time_input = data.get('time')

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO Medicines (name, dosage, time) VALUES (?, ?, ?)",
                      (name, dosage, time_input))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Success')

# Run server
PORT = 8000
with HTTPServer(('', PORT), MedicineHandler) as server:
    print(f"Server running on port {PORT}")
    server.serve_forever()
