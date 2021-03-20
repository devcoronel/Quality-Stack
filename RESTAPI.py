# Página de inicio: localhost:3000/home
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import requests, json
from variables import *

app = Flask(__name__)

#Conectar con la Base de Datos MySQL en Linux Ubuntu
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
mysql = MySQL(app)

# Key para permitir insertar texto en index.html
app.secret_key = 'mysecretkey'

@app.route('/home', methods=['GET'])
def home():
    #Orden de los switches
    orden_switch = []
    # Nombres de los switches
    nombre_switch = []
    # Tipo de switch
    tipo_switch = []
    # Versión del switches
    version_switch = []

    response = requests.get(url_switches_variable)

    if response.status_code == 200:
        var_a = response.content
        data = json.loads(var_a)
        
        #Averiguar si en la tabla ya existe registro de los switches
        for i in data:
            # Crear el orden del análisis de los switches
            orden_switch.append(i)

            #Obtener las características del switch de turno
            str_i = str(i)
            url_caracteristicas = url_caracteristicas_variable +str_i
            caracteristicas = requests.get(url_caracteristicas)

            #Obtener los flujos del switch de turno
            url_flujos = url_flujos_variable +str_i
            flujos = requests.get(url_flujos)

            #Formar nombre del switch y almacenarlo
            var_b = "sw_"+str_i
            nombre_switch.append(var_b)
            
            if caracteristicas.status_code == 200 and flujos.status_code == 200:
                #Obtener el tipo y version de switch y almacenarlo
                var_c = caracteristicas.content
                var_d = json.loads(var_c)
                var_e = var_d[str_i]
                var_f = var_e["hw_desc"]
                tipo_switch.append(var_f)
                var_g = var_e["sw_desc"]
                version_switch.append(var_g)

                #Obtener la version del switch y almacenarlo
                var_h = flujos.content
                var_i = json.loads(var_h)
            
            else:
                print("Ocurrió un error con la API ofctl.rest.py")
    
    # Número de switches
    n_switch = len(orden_switch)
    
    return render_template('index.html', numero = n_switch, orden = orden_switch , nombre = nombre_switch, tipo = tipo_switch, version = version_switch) , 200

@app.route('/home/add', methods=['POST'])
def addflows():
    return jsonify({"message": "add flows"})

if __name__ == '__main__':
    app.run(debug = True, port = port)