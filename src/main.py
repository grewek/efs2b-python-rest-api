# Python 3 Webserver mit REST API
from flask import Flask, jsonify, request

# Erstelle eine neue Flask App.
app = Flask(__name__)

# Unsere Temperaturwerte, sie haben jeweils eine id und die eigentliche Temperatur. Sie werden zur Demonstration in
# einem Array gespeichert.
temperatures = [ {'id': 1, 'temperature': 25.5},
                 {'id': 2, 'temperature': 26.8},
                 {'id': 3, 'temperature': 33.2}
]

# Diese GET route gibt uns alle daten zurück die unser Array beinhaltet.
@app.route('/temperatures', methods=['GET'])
def get_temperatures():
    # Wir 'serialisieren' unsere Temperaturwerte in das JSON format!
    return jsonify(temperatures), 200

# Versucht die spezifizierte ID vom Server zu lesen.
@app.route("/temperatures/<id>", methods=['GET'])
def get_temperature(id):
    # Wir ziehen eins von id ab, da unser erstes Element im obigen Array bei 0 startet nicht bei 1!
    id_value = int(id) - 1

    # Absicherung gegen Over- u. Underflows des Arrays.
    if id_value < 0:
        return '', 404
    elif id_value >= len(temperatures):
        return '', 404

    # Wir serialisieren den angefragten Wert wieder zurück in das JSON format
    return jsonify(temperatures[id_value]), 200

# Die Patch Route kann benutzt werden um einen bereits vorhandenen Eintrag zu ändern! Anders als PUT muss man hierbei
# nicht den gesamten Eintrag neuschreiben sondern kann einzelne Werte ändern.
@app.route("/temperatures/<id>", methods=['PATCH'])
def patch_temperature(id):
    id_value = int(id) - 1

    if id_value >= len(temperatures):
        return '', 404
    # Underflow?
    elif id_value < 0:
        return '', 404
    else:
        # Sollte alles bis hierhin geklappt haben, können wir die vom Nutzer übergebenen Daten
        # deserialisieren.
        temperature = json.loads(request.data)
        new_temp = float(temperature['temperature'])
        # Hier setzten wir den gewünschten Eintrag auf die neue Temperatur.
        temperatures[id_value]['temperature'] = new_temp

        return '', 201, {'location': f'/temperatures/{id_value}'}

# Route die benutzt wird um neue Werte hinzuzufügen, Werte werden immer an das Ende des Arrays gepackt.
@app.route('/temperatures', methods=['POST'])
def post_temperature():
    temperature = json.loads(request.data)

    id = len(temperatures) + 1

    #Packe die berechnete ID in unser Temperatur Objekt.
    temperature['id'] = id
    #Dieses Objekt packen wir wiederum ans Ende unserer Liste.
    temperatures.append(temperature)

    #Wenn wir hier landen war die Operation erfolgreich. Wir geben den Erfolgswert 201 zurück und verweisen
    #auf das neu angelegte element hier {id_value}
    return '', 201, { 'location': f'/temperatures/{id_value}' }


if __name__ == '__main__':
    #Startet den Server so dass er auf Port 1337 auf eingehende Verbindungen wartet!
    app.run(host="0.0.0.0", port=1337)
