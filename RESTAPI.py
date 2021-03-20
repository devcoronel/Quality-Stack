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
    response = requests.get(url_switches_variable)

    if response.status_code == 200:
        var_a = response.content
        data = json.loads(var_a)
        
        #Averiguar si en la tabla ya existe registro de los switches
        for i in data:

            #Obtener las características del switch de turno
            str_i = str(i)
            url_caracteristicas = url_caracteristicas_variable +str_i
            caracteristicas = requests.get(url_caracteristicas)

            #Obtener los flujos del switch de turno
            url_flujos = url_flujos_variable +str_i
            flujos = requests.get(url_flujos)

            #Formar nombre del switch
            var_b = "sw_"+str_i
            
            #Seleccionar (a modo de pregunta) el nombre del switch en MySQL
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT Nombre FROM Switches;')
            result = cursor.fetchall()

            #Encontrar coindidencias con los nombres guardados
            det_a = False
            
            for j in result:
                if j[0] == var_b:
                    det_a = True
            
            if det_a == False and caracteristicas.status_code == 200 and flujos.status_code == 200:
                #Obtener el contenido de las caracteristicas y transformar a JSON
                var_c = caracteristicas.content
                var_d = []
                var_d.append(var_c)

                #Obtener el contenido de los flujos y transformar a JSON
                var_e = flujos.content
                var_f = []
                var_f.append(var_e)
                
                cursor.execute('INSERT INTO Switches (Nombre, Caracteristicas, Flujos) VALUES (%s, %s, %s);', [var_b, var_d, var_f])
                mysql.connection.commit()
                print("El switch", var_b, "ahora es elemento de la tabla Switches")
            
            else:
                print(var_b, "ya pertenece a la tabla Switches")
            #Consultar las tablas que exiten en la BD SDN-flows
            #cursor.execute('SHOW TABLES;')
            #tablas = cursor.fetchall()
            
            #Ver si existe la tabla del switch de turno
            #det_b = False
            #for k in tablas:
            #    for m in k:
            #        if m == var_c:
            #            print("Tabla", var_c, "ya ha sido creada")
            #        else:
            #            cursor.execute('CREATE TABLE %s(Caracteristicas JSON NOT NULL, Flujos JSON NOT NULL);', [var_c])
            #            mysql.connection.commit()
            #            print("Tabla", var_c, "creada exitosamente")
        
    # Pedimos datos de la base de datos MySQL para mostrarlas en index.html
    # Solicitar nombres
    cur = mysql.connection.cursor()
    cur.execute('SELECT Nombre FROM Switches')
    nombres_mysql = cur.fetchall()
    #print(nombres_mysql)

    #Solicitar version
    cur.execute('SELECT Caracteristicas FROM Switches')
    version_mysql = cur.fetchall()
    
    return render_template('index.html', nombre = nombres_mysql, version = version_mysql) , 200

@app.route('/home/add', methods=['POST'])
def addflows():
    return jsonify({"message": "add flows"})

if __name__ == '__main__':
    app.run(debug = True, port = port)