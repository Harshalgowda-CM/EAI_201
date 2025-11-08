# flask_app.py
"""
Minimal Flask app that shows an instant "Quick Predict" result (top 4 teams).
Run:
    python flask_app.py
Open http://127.0.0.1:5000
"""
import os
import csv
from flask import Flask, render_template_string, url_for, send_from_directory, redirect, flash
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUT_DIR = os.path.join(BASE_DIR, "outputs")
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "quick_predict_secret"
app.static_folder = STATIC_DIR

# Hard-coded top-4 prediction (exact values you provided)
TOP4 = [
    {"team": "🇪🇸 Spain",      "score": 0.9243},
    {"team": "🇧🇷 Brazil",     "score": 0.9237},
    {"team": "🇦🇷 Argentina",  "score": 0.7898},
    {"team": "🇫🇷 France",     "score": 0.7893},
]

INDEX_HTML = """
<!doctype html>
<title>FIFA Quick Predictor — Top 4</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
<h1>FIFA Quick Predictor</h1>
<p>This is a one-click demo: press <strong>Quick Predict</strong> to show the top 4 predicted finalists (no uploads required).</p>

<form action="/predict" method="get">
  <button type="submit">Quick Predict</button>
</form>

{% if results %}
  <hr>
  <h2>Top 4 Predicted Finalists</h2>
  <table>
    <thead><tr><th>Rank</th><th>Team</th><th>Predicted Score</th></tr></thead>
    <tbody>
    {% for r in results %}
      <tr><td>{{loop.index}}</td><td style="font-size:1.2rem">{{r.team}}</td><td>{{"%.4f"|format(r.score)}}</td></tr>
    {% endfor %}
    </tbody>
  </table>

  <p>
    <a href="{{ url_for('download', filename='top4.csv') }}">Download CSV</a>
  </p>

  <img src="{{ url_for('static', filename='top4.png') }}" alt="Top 4 chart" style="max-width:700px;">
{% endif %}
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML, results=None)

@app.route("/predict", methods=["GET"])
def predict():
    # Create DataFrame from TOP4
    df = pd.DataFrame(TOP4)
    csv_path = os.path.join(OUT_DIR, "top4.csv")
    df.to_csv(csv_path, index=False)

    # Create horizontal bar chart
    names = df['team'].tolist()
    scores = df['score'].tolist()
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.barh(names[::-1], scores[::-1])  # reversed so top is rank 1
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Predicted Score")
    ax.set_title("Top 4 Predicted Finalists")
    for i, v in enumerate(scores[::-1]):
        ax.text(v + 0.005, i, f"{v:.4f}", va="center")
    plt.tight_layout()
    img_path = os.path.join(STATIC_DIR, "top4.png")
    fig.savefig(img_path)
    plt.close(fig)

    return render_template_string(INDEX_HTML, results=[type("R",(object,),r)() for r in TOP4])

@app.route("/download/<path:filename>")
def download(filename):
    # Only allow the CSV we generate
    if filename not in ("top4.csv",):
        return "Not allowed", 403
    return send_from_directory(OUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    print("Starting Quick Predict app at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
