from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)

# Agrega la URL de tu servicio web y la API key
SERVICE_URL = 'https://ussouthcentral.services.azureml.net/workspaces/a2900c28e54549cbb59d4f55dc628091/services/e98ab0123be3476eb3e64f2fbdc15c5a/execute?api-version=2.0&details=true'
API_KEY = 'LTxhP9DSIRUqut+/qLaclRkC845amkFCfN2UpM7MZrcZ+L1srxBLhi0cyNq3kBya5BwcmLIZNLRb+AMCB9cjlQ=='


def get_prediction(data):
    body = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + API_KEY)}

    req = urllib.request.Request(SERVICE_URL, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        return result
    except urllib.error.HTTPError as error:
        return json.loads(error.read().decode('utf-8'))


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Obtén los datos del formulario
        modelo = request.form['modelo']
        generacion = request.form['generacion']
        serie = request.form['serie']
        cpu_nucleos = int(request.form['cpu_nucleos'])
        tipo_grafica = request.form['tipo_grafica']
        ram_gb = int(request.form['ram_gb'])
        tipo_almacenamiento = request.form['tipo_almacenamiento']
        capacidad_disco_gb = int(request.form['capacidad_disco_gb'])
        c_energetico = request.form['c_energetico']
        camara = request.form['camara']
        tamano_pantalla = int(request.form['tamano_pantalla'])
        pantalla_tactil = request.form['pantalla_tactil']

        # Crea un diccionario con los datos
        data = {
            "Inputs": {
                "input1": {
                    "ColumnNames": ["Modelo", "Generacion", "Serie", "CPU-Nucleos", "Tipo_grafica", "RAM (GB)", "Tipo_almacenamiento", "Capacidad_disco(GB)", "C_Energetico", "Camara", "Tamano_pantalla", "Pantalla_tactil", "Precio (S./)"],
                    "Values": [[modelo, generacion, serie, cpu_nucleos, tipo_grafica, ram_gb, tipo_almacenamiento, capacidad_disco_gb, c_energetico, camara, tamano_pantalla, pantalla_tactil, 0]]
                },
            },
            "GlobalParameters": {}
        }
        # Obten la predicción del servicio web
        result = get_prediction(data)
        return render_template('result.html', prediction=result)

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
