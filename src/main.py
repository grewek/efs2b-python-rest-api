# Python 3 Webserver mit REST API
from flask import Flask, jsonify, request

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path


app = Flask(__name__)

temperatures = [ {'id': 1, 'temperature': 25.5}, {'id': 2, 'temperature': 26.8}, {'id': 3, 'temperature': 33.2}]

@app.route('/temperatures', methods=['GET'])
def get_temperatures():
    return jsonify(temperatures)

@app.route("/temperatures/<id>", methods=['GET'])
def get_temperature(id):
    id_value = int(id) - 1
    if id_value < 0:
        return '', 404
    elif id_value >= len(temperatures):
        return '', 404
    
    return jsonify(temperatures[int(id) - 1])

@app.route('/temperatures', methods=['POST'])
def post_temperature():
    temperature = json.loads(request.data)
    
    id = len(temperatures) + 1
    temperature['id'] = id
    temperatures.append(temperature)

    return '', 201, { 'location': f'/temperatures/{temperature['id']}' }


if __name__ == '__main__':
    app.run(port=5000)