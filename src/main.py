# Python 3 Webserver mit REST API
from flask import Flask, jsonify, request
import json


app = Flask(__name__)
# Unsere Temperaturwerte, sie haben jeweils eine id und die eigentliche Temperatur
temperatures = [ {'id': 1, 'temperature': 25.5},
                 {'id': 2, 'temperature': 26.8},
                 {'id': 3, 'temperature': 33.2}
]

# Diese GET route gibt uns alle daten zurück die unser Array beinhaltet
@app.route('/temperatures', methods=['GET'])
def get_temperatures():
    # Wir 'serialisieren' unsere Temperaturwerte in das JSON format!
    return jsonify(temperatures)

# Versucht, den spezifizierten Wert vom Nutzer aus dem Array zu holen und sie zurückzugeben
@app.route("/temperatures/<id>", methods=['GET'])
def get_temperature(id):
    # Wir ziehen eins von id_value ab, da unser erste element im obigen Array bei 0 startet nicht bei 1!
    id_value = int(id) - 1
    # Der obige Wert könnte unter 0 sein wenn der Nutzer 0 als Wert spezifiziert hat
    # somit müssen wir die Route gegen werte absichern die einen Undeflow erzeugen könnten
    if id_value < 0:
        # Wir benachrichtigen den Nutzer, dass wir den gewünschten Wert nicht liefern können
        return '', 404
    # Dasselbe gilt auch, wenn der Nutzer versucht werte abzurufen, die noch nicht existieren (Overflow)
    elif id_value >= len(temperatures):
        # Auch hier benachrichtigen wir den Nutzer über den fehlschlag der Operation
        return '', 404

    # Wir serialisieren den angefragten temperatur wert wieder
    return jsonify(temperatures[int(id) - 1])

# Die Patchroute kann benutzt werden um einen bereits vorhandenen Eintrag zu ändern! Anders als PUT muss man hierbei
# nicht den gesamten Eintrag neuschreiben, sondern kann einzelne Werte ändern
@app.route("/temperatures/<id>", methods=['PATCH'])
def patch_temperature(id):
    # Wir nehmen die ID die uns der Nutzer gesendet hat und verwandeln sie in eine Ganzzahl, dann ziehen wir
    # eins ab da unser Array null basiert ist.
    id_value = int(id) - 1

    # Wie in der GET Route testen wir ob es zu einem Over- o. Underflow kommen könnte
    if id_value >= len(temperatures):
        # Auch hier antworten wir mit einem 404 Fehler wenn der Wert nicht exisistiert
        return '', 404
    # Underflow?
    elif id_value < 0:
        return '', 404
    else:
        # Sollte alles bis hierhin geklappt haben, können wir die vom Nutzer übergebenen Daten
        # deserialisieren (JSON -> Python)
        temperature = json.loads(request.data)
        # new_temp beinhaltet jetzt den neuen Temperatur wert. Zur sicherheit wandeln wir den wert nochmals in einen
        # floating point typen um!
        new_temp = float(temperature['temperature'])
        # Hier setzten wir den gewünschten Eintrag auf die neue Temperatur
        temperatures[id_value]['temperature'] = new_temp
        # Wir melden den Erfolg der Operation mit Code 201 und leiten den Nutzer auf /temperatures weiter
        return '', 201, { 'location': f'/temperatures'}

# Route die benutzt wird um neue Werte hinzuzufügen, Werte werden immer an das Ende des Arrays gepackt.
@app.route('/temperatures', methods=['POST'])
def post_temperature():
    #Serialisierung des Wertes in etwas das wir nutzen können
    temperature = json.loads(request.data)

    #Berechne die Id des elements
    id = len(temperatures) + 1
    #Packe die berechnete ID in unser temperatur Objekt.
    temperature['id'] = id
    #Dieses objekt packen wir wiederum ans Ende unserer Liste.
    temperatures.append(temperature)

    #Wenn wir hier landen war die Operation erfolgreich. Wir geben den Erfolgswert 201 zurück und leiten den Nutzer
    #auf /temperatures um
    return '', 201, { 'location': f'/temperatures' }


#Startet man die Datei wird zuerst der Code unter diesem Kommentar ausgeführt, der sogenannte Einstiegspunkt
if __name__ == '__main__':
    #Startet den Server so dass er auf Port 5000 auf eingehende Verbindungen wartet!
    app.run(host="0.0.0.0", port=5000)