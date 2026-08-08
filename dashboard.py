#!/usr/bin/env python3
"""Minimal local dashboard for first SHCE receiver experiments.

Run: python dashboard.py
Open: http://127.0.0.1:8765
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

STATE = {
    "status": "WAITING",
    "packets": 0,
    "valid": 0,
    "crc_errors": 0,
    "last_message": "",
    "last_rx": None,
    "signal": None,
}

HTML = '''<!doctype html><html><head><meta charset="utf-8"><title>SHCE Lab</title>
<style>body{font-family:system-ui;background:#111;color:#eee;max-width:900px;margin:40px auto} .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#1c1c1c;padding:18px;border-radius:12px}.v{font-size:28px;font-weight:700}#msg{font-family:monospace;background:#050505;padding:18px;border-radius:10px;min-height:50px}</style></head>
<body><h1>SHCE Lab — Link Monitor</h1><div class="grid">
<div class="card">STATUS<div class="v" id="status">—</div></div><div class="card">PACKETS<div class="v" id="packets">0</div></div><div class="card">VALID<div class="v" id="valid">0</div></div><div class="card">CRC ERR<div class="v" id="crc">0</div></div></div>
<h2>Last received packet</h2><div id="msg">Waiting for receiver…</div><h2>Telemetry</h2><pre id="telemetry">—</pre>
<script>async function poll(){let r=await fetch('/api/state');let s=await r.json();for(let k of ['status','packets','valid'])document.getElementById(k).textContent=s[k];document.getElementById('crc').textContent=s.crc_errors;document.getElementById('msg').textContent=s.last_message||'—';document.getElementById('telemetry').textContent=JSON.stringify(s,null,2)}setInterval(poll,500);poll();</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/state':
            data=json.dumps(STATE).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data); return
        data=HTML.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self, *args): pass

if __name__ == '__main__':
    print('SHCE dashboard: http://127.0.0.1:8765')
    HTTPServer(('127.0.0.1',8765), Handler).serve_forever()
