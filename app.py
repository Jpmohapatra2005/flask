# app.py (Flask API)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def api():
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
