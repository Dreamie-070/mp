from flask import Flask, render_template_string, request
import requests
import socket
import whois
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# --- FINDER-X CORE INTELLIGENCE ---
def finder_x_core(target):
    # Extracting username from email if provided
    username = target.split('@')[0] if "@" in target else target
    
    data = {
        "target": target,
        "insta_found": False,
        "insta_url": f"https://www.instagram.com/{username}/",
        "nodes": [{"data": {"id": 'target', "label": target}}],
        "edges": [],
        "social_links": [],
        "threat_score": 0,
        "network": {"ip": "N/A", "geo": "Unknown"},
        "hit_count": 0
    }

    # 1. SPECIAL INSTAGRAM TRACKER (Always Active)
    def trace_insta():
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(data["insta_url"], headers=headers, timeout=5)
            if res.status_code == 200:
                data["insta_found"] = True
                data["nodes"].append({"data": {"id": 'insta', "label": 'INSTAGRAM'}})
                data["edges"].append({"data": {"source": 'target', "target": 'insta'}})
                data["hit_count"] += 1
        except: pass

    # 2. GLOBAL IDENTITY MAPPING
    platforms = {
        "GitHub": "https://github.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Facebook": "https://facebook.com/{}",
        "Snapchat": "https://snapchat.com/add/{}",
        "Reddit": "https://reddit.com/user/{}"
    }

    def trace_social(name, url):
        try:
            r = requests.get(url.format(username), timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                link = url.format(username)
                data["social_links"].append({"name": name, "url": link})
                data["nodes"].append({"data": {"id": name, "label": name}})
                data["edges"].append({"data": {"source": 'target', "target": name}})
                data["hit_count"] += 1
        except: pass

    # 3. NETWORK INTELLIGENCE
    domain = target.split('@')[-1] if "@" in target else target
    try:
        ip = socket.gethostbyname(domain)
        data["network"]["ip"] = ip
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        data["network"]["geo"] = f"{geo.get('city')}, {geo.get('country')}"
        data["nodes"].append({"data": {"id": 'ip', "label": f"IP: {ip}"}})
        data["edges"].append({"data": {"source": 'target', "target": 'ip'}})
    except: pass

    # Parallel Execution for Speed
    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.submit(trace_insta)
        for n, u in platforms.items(): executor.submit(trace_social, n, u)

    # Risk Analysis
    data["threat_score"] = min(data["hit_count"] * 20, 100)
    return data

# --- FINDER-X FUTURISTIC UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>FINDER-X | RED-EYE RECON</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap');
        
        body { 
            background: #000; color: #f00; font-family: 'Orbitron', sans-serif;
            background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.95)), url('https://img.freepik.com/premium-vector/red-eye-with-glowing-eye-middle_45003749.jpg');
            background-size: cover; background-attachment: fixed; background-position: center;
        }

        .finder-box { 
            background: rgba(25, 0, 0, 0.7); border: 2px solid #f00; 
            box-shadow: 0 0 25px #f005; backdrop-filter: blur(10px); padding: 35px;
        }

        #cy { height: 450px; width: 100%; background: rgba(0,0,0,0.5); border: 1px solid #f002; }
        
        .insta-card { 
            background: linear-gradient(45deg, #400, #f00); color: #fff; 
            padding: 15px; border: 1px solid #fff3; text-align: center; margin-bottom: 20px;
        }

        .risk-meter { height: 12px; background: #200; border: 1px solid #f00; margin: 10px 0; }
        .risk-fill { height: 100%; background: #f00; box-shadow: 0 0 15px #f00; transition: 2s ease-out; }

        input { background: #000 !important; color: #f00 !important; border: 1px solid #f00 !important; border-radius: 0 !important; }
        .btn-trace { background: #f00; color: #000; font-weight: 900; border-radius: 0; letter-spacing: 4px; transition: 0.3s; }
        .btn-trace:hover { background: #fff; box-shadow: 0 0 30px #fff; }
        
        .glow-text { text-shadow: 0 0 15px #f00; }
    </style>
</head>
<body class="container py-5">
    <div class="text-center mb-5">
        <h1 class="display-2 fw-bold glow-text">FINDER-X</h1>
        <p class="text-uppercase" style="letter-spacing: 10px;">Neural Network Identity Tracker</p>
    </div>

    <form action="/scan" method="post" target="_blank" class="finder-box text-center mb-5">
        <input type="text" name="target" class="form-control mb-4 text-center py-3" placeholder="SIGNATURE: USERNAME / EMAIL / IP" required>
        <button type="submit" class="btn btn-trace w-100 py-3">INITIALIZE X-TRACE</button>
    </form>

    {% if data %}
    <div class="row g-4">
        <div class="col-md-4">
            <div class="finder-box text-center">
                <h5 class="glow-text mb-4">INSTAGRAM SENSOR</h5>
                {% if data.insta_found %}
                    <div class="insta-card">
                        <p class="mb-2 small">[ MATCH FOUND ]</p>
                        <a href="{{ data.insta_url }}" target="_blank" class="btn btn-sm btn-light fw-bold">VIEW PROFILE</a>
                    </div>
                {% else %}
                    <p class="text-muted small">[ NO DIRECT MATCH ]</p>
                {% endif %}
                
                <hr style="border-color: #f00;">
                <h6 class="small">THREAT EXPOSURE</h6>
                <div class="risk-meter"><div class="risk-fill" style="width: {{ data.threat_score }}%"></div></div>
                <h2 class="glow-text">{{ data.threat_score }}%</h2>
            </div>
        </div>

        <div class="col-md-8">
            <div class="finder-box">
                <h5 class="glow-text mb-3">🕸️ RELATIONSHIP MAPPING</h5>
                <div id="cy"></div>
            </div>
        </div>

        <div class="col-12">
            <div class="finder-box">
                <div class="row text-center">
                    <div class="col-md-4 border-end border-danger">
                        <p class="small text-muted mb-1">NETWORK LOCATION</p>
                        <p class="glow-text">{{ data.network.geo }}</p>
                    </div>
                    <div class="col-md-4 border-end border-danger">
                        <p class="small text-muted mb-1">IP SIGNATURE</p>
                        <p class="glow-text">{{ data.network.ip }}</p>
                    </div>
                    <div class="col-md-4">
                        <p class="small text-muted mb-1">PLATFORM HITS</p>
                        <p class="text-success fw-bold">
                            {% for s in data.social_links %}{{ s.name }} {% endfor %}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        var cy = cytoscape({
            container: document.getElementById('cy'),
            elements: {{ data.nodes | tojson }} + {{ data.edges | tojson }},
            style: [
                { selector: 'node', style: { 'background-color': '#f00', 'label': 'data(label)', 'color': '#f00', 'font-size': '10px', 'font-family': 'Orbitron', 'text-outline-width': 1, 'text-outline-color': '#000' }},
                { selector: 'edge', style: { 'width': 2, 'line-color': '#400', 'target-arrow-color': '#f00', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' }}
            ],
            layout: { name: 'cose', padding: 20 }
        });
    </script>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    results = finder_x_core(target)
    return render_template_string(HTML_TEMPLATE, data=results)

if __name__ == '__main__':
    app.run(debug=True)
