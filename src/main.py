# Python 3 Webserver mit REST API
from flask import Flask, jsonify, request

from http.server import HTTPServer, BaseHTTPRequestHandler
from time import ctime, time
from urllib.parse import urlparse, parse_qs
import json
from pathlib import Path


app = Flask(__name__)

temperatures = [ {'id': 1, 'temperature': 25.5}, {'id': 2, 'temperature': 26.8}, {'id': 3, 'temperature': 33.2}]

@app.route('/temperatures', methods=['GET'])
def get_temperatures():
    return jsonify(temperatures)

@app.route('/temperatures', methods=['POST'])
def post_temperature():
    temperature = json.loads(request.data)
    
    id = len(temperatures) - 1
    temperature['id'] = id
    temperatures.append(temperature)

    return '', 201, { 'location': f'/temperatures/{temperature['id']}' }


if __name__ == '__main__':
    app.run(port=5000)


#hostName = "127.0.0.1"
#serverPort = 8080
#endpoint_temps = "/raumtemps"
#temps_fp = Path("./temps.json")
#tempset = {
#    "id": "",
#    "zeit": "",
#    "ort": "",
#    "temp": ""
#}
#templist = []
#error_msg = {
#    "problem": "",
#    "nachricht": "",
#    "zeit": ""
#}
#response = ""
#
#
#def get_data_from_file():
#    global templist
#    if temps_fp.is_file():
#        print("Opening file...")
#        with open(temps_fp, 'r') as read_file:
#            templist = json.load(read_file)
#
#
#def save_data_to_file():
#    # body of destructor, Datensätze sichern
#    global templist
#    temps_fp.touch(exist_ok=True)
#    print("Writing templist to file...")
#    with open(temps_fp, 'w') as write_file:
#        json.dump(templist, write_file)
#
#
#class MyServer(BaseHTTPRequestHandler):
#    # def __init__(self):
#
#    def do_GET(self):
#        global templist
#        global temp_set
#        global error_msg
#
#        print("Habe einen Request:")
#        endpoint = (urlparse(self.path)).path  # Endpunkt bestimmen
#        if endpoint[len(endpoint) - 1] == '/':
#            endpoint = endpoint[:-1]  # falls jemand am Ende einen / eingegeben hat, muss der weg
#        if endpoint.startswith(endpoint_temps):
#            # Endpunkt für Temperaturbearbeitung
#            # nun Endpunkt beim / trennen, um herauszufinden, ob alle Datensätze oder ein spezieller
#            # geliefert werden sollen (/raumtemps oder /raumtemps/7)
#            if (len(endpoint.split("/")) == 2):
#                # Nur Basispfad angegeben --> Alle Daten senden
#                response = json.dumps(templist)
#                self.send_response(200)
#            elif (len(endpoint.split("/")) > 2) and not (str.isdigit(endpoint.split("/")[2])):
#                # id ist nicht integer
#                error_msg["problem"] = "Datensatz nicht gefunden!"
#                error_msg["nachricht"] = "Die angegebene id " + (endpoint.split("/"))[2] + " ist keine Ganzzahl!"
#                error_msg["zeit"] = ctime(time())
#                response = json.dumps(error_msg)
#                self.send_response(400)  # 400 Bad Request
#
#            else:
#                # Bestimmten Datensatz suchen und senden
#                id_set = int((endpoint.split("/"))[2])
#                print("id_set: ", id_set)
#                temp_set = list(filter(lambda data: data['id'] == id_set, templist))
#                print("temp_set: ", temp_set)
#                # Suchen in einer List of Dictionaries siehe
#                # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search#comment18634157_8653568
#                if len(temp_set) > 0:
#                    # angefragten Datensatz gefunden, Ergebnis ist eine Liste
#                    response = json.dumps(temp_set[0])
#                    self.send_response(200)
#
#                else:
#                    # nicht gefunden
#
#                    error_msg["problem"] = "Datensatz nicht gefunden!"
#                    error_msg["nachricht"] = "Der Datensatz mit der id " + str(id_set) + " existiert nicht im System!"
#                    error_msg["zeit"] = ctime(time())
#                    response = json.dumps(error_msg)
#                    self.send_response(400)  # 400 Bad Request
#        else:
#            # Keinen gültigen Endpunkt gefunden
#            error_msg["problem"] = "Fehlerhafte URL"
#            error_msg["nachricht"] = "Der Endpunkt " + endpoint + " existiert nicht im System!"
#            error_msg["zeit"] = ctime(time())
#            response = json.dumps(error_msg)  # Datensatz von Dictionary in String wandeln (Serialize)
#            self.send_response(404)  # Nachricht über den Misserfolg, der eingegangenen Anfrage, 404 Not Found
#
#        self.send_header("Content-type",
#                         "application/json")  # Headerinformation über den Datentyp, der im Body zurückgesendet wird
#        self.end_headers()  # Header zu Ende
#        self.wfile.write(bytes(response, 'utf-8'))  # Die Rückmeldung an den Client über den body der Webseite
#
#    def do_POST(self):
#        # Übergabe der Daten über den Body mit "Content-type", "application/json"
#        post_body_dict = json.loads(self.rfile.read(int(self.headers.get('content-length', 0))))
#        # Bodylänge, Auslesen und Umwandeln des JSON-Strings aus dem Body in Dictionary (Deserialize) in einem Zug
#        t = str(post_body_dict["temp"])  # Der Wert, der im Body mit Parameter "temp" übergeben wurde,
#        o = str(post_body_dict["ort"])  # Der Wert, der im Body mit Parameter "ort" übergeben wurde
#        appended_data = self.append_data(o,
#                                         t)  # diese Methode speichert die Daten irgendwo hin (muss noch geschrieben werden)
#        self.send_response(
#            200)  # Nachricht über den Erfolg, der eingegangenen Anfrage, 200=OK, die Anfrage ist erfolgreich,
#        self.send_header("Content-type", "application/json")  # Datentyp im Body der zurückgelieferten Webseite,
#        self.end_headers()  # mit diesem Befehl wird der Header an den Client zurückgesendet
#        response = json.dumps(appended_data)  # Datensatz von Dictionary in String wandeln (Serialize)
#        self.wfile.write(bytes(response, 'utf-8'))  # Die Rückmeldung an den Client über den body der Webseite
#
#    def append_data(self, ort, temp):
#        global templist
#        global tempset
#        if len(templist) == 0:
#            tempset["id"] = 1  # vorher wurden noch keine Daten in der Liste gespeichert
#        else:
#            tempset["id"] = max(tdict['id'] for tdict in templist) + 1  # Größte id finden und inkrementieren
#        tempset["zeit"] = ctime(
#            time())  # ctime() https://docs.python.org/3/library/datetime.html?highlight=ctime#datetime.date.ctime
#        tempset["ort"] = ort
#        tempset["temp"] = temp
#        templist.append(dict(tempset))  # anfügen einer Kopie (dict()) des Datensatzes an die Liste
#        return dict(tempset)  # eine Kopie des Datensatzes mit Zusatzinfos Zeit und ID zurückgeben
#
#
#if __name__ == "__main__":
#    webServer = HTTPServer((hostName, serverPort), MyServer)
#    print("Server started http://%s:%s" % (hostName, serverPort))
#    get_data_from_file()  # Datenbank auslesen
#
#    try:
#        webServer.serve_forever()
#    except KeyboardInterrupt:
#        pass
#    save_data_to_file()  # Datenbank wieder speichern
#    webServer.server_close()
#    print("Server stopped.")