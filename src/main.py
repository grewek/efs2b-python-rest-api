# Python 3 Webserver mit REST API
from flask import Flask, jsonify, request

from http.server import HTTPServer, BaseHTTPRequestHandler
import json


app = Flask(__name__)
#Unsere Temperaturwerte, sie haben jeweils eine id und die eigentliche Temperatur
temperatures = [ {'id': 1, 'temperature': 25.5},
                 {'id': 2, 'temperature': 26.8},
                 {'id': 3, 'temperature': 33.2}
]

#Diese get route gibt uns alle daten zurück
@app.route('/temperatures', methods=['GET'])
def get_temperatures():
    # Wir 'serialisieren' unsere Temperaturwerte in das JSON format!
    return jsonify(temperatures)

@app.route("/temperatures/<id>", methods=['GET'])
def get_temperature(id):
    # Wir ziehen eins von id_value ab, da unser erste element im obigen Array bei 0 startet nicht bei 1!
    id_value = int(id) - 1
    # Der Wert könnte unter 0 sein wenn der Nutzer 0 als Wert spezifiziert hat somit müssen wir die Route gegen
    # werte absichern die einen Undeflow erzeugen könnten
    if id_value < 0:
        #Wir benachrichtigen den Nutzer, dass wir den gewünschten Wert nicht liefern können
        return '', 404
    # Dasselbe gilt auch, wenn der Nutzer versucht werte abzurufen die noch nicht existieren
    elif id_value >= len(temperatures):
        #Auch hier benachrichtigen wir den Nutzer über den fehlschlag der Operation
        return '', 404

    # Wir serialisieren den angefragten temperatur wert wieder
    return jsonify(temperatures[int(id) - 1])

@app.route("/temperatures/<id>", methods=['PATCH'])
def patch_temperature(id):
    id_value = int(id) - 1

    if id_value >= len(temperatures):
        return '', 404
    elif id_value - 1 < 0:
        return '', 404
    else:
        temperature = json.loads(request.data)
        new_temp = temperature['temperature']
        temperatures[int(id) - 1]['temperature'] = temperature['temperature']

        return '', 201, { 'location': f'/temperatures'}

@app.route('/temperatures', methods=['POST'])
def post_temperature():
    print("request: ", request.data)
    temperature = json.loads(request.data)
    
    id = len(temperatures) + 1
    temperature['id'] = id
    temperatures.append(temperature)

    return '', 201, { 'location': f'/temperatures' }


if __name__ == '__main__':
    app.run(port=5000)