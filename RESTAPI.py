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

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html')

@app.route('/', methods=['GET'])
def main():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT username FROM users ''')
        usernames = cursor.fetchall()
        
        for i in usernames:
            if usuario == i[0]:
                cursor.execute(''' SELECT pass FROM users WHERE username = %s ''', [usuario])
                password = cursor.fetchall()
                print(type((password[0])[0]))

        return "ok"


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

            #Formar nombre del switch y almacenarlo
            var_b = "sw_"+str_i
            nombre_switch.append(var_b)
            
            if caracteristicas.status_code == 200:
                #Obtener el tipo y version de switch y almacenarlo
                var_c = caracteristicas.content
                var_d = json.loads(var_c)
                var_e = var_d[str_i]
                var_f = var_e["hw_desc"]
                tipo_switch.append(var_f)
                var_g = var_e["sw_desc"]
                version_switch.append(var_g)
            
            else:
                print("Ocurrió un error con la API ofctl.rest.py")
    
    # Número de switches
    n_switch = len(orden_switch)
    
    return render_template('index.html', numero = n_switch, orden = orden_switch , nombre = nombre_switch, tipo = tipo_switch, version = version_switch) , 200

# Mostrar las tablas de flujos de cada switch
@app.route('/home/showflows/<string:n>', methods=['GET'])
def showflows(n):
    # Primero obtener las tablas de flujo del switch
    url_tablas_flujo = url_tablas_flujo_variable + n
    print(url_tablas_flujo)
    tablas_flujo = requests.get(url_tablas_flujo)

    #Obtener los flujos del switch de turno
    url_flujos = url_flujos_variable + n
    flujos = requests.get(url_flujos)

    flujos_por_tablas = []

    if tablas_flujo.status_code == 200 and flujos.status_code == 200:
        # Obtener las tablas en json
        contenido = tablas_flujo.content
        data = json.loads(contenido)
        tablas = data[n]
        n_tablas = len(tablas)

        #Obtener los flujos en json
        var_a = flujos.content
        var_b = json.loads(var_a)
        var_c = var_b[n]
        var_d = len(var_c)
        
        tablas_activas = []
        for i in range(n_tablas):
            if (tablas[i])["active_count"] != 0:
                str_i = str(i)
                tablas_activas.append(str_i)
                for j in var_c:
                    if j["table_id"] == i:
                        formato = {
                            str_i: j
                        }

                        flujos_por_tablas.append(formato)
    print(flujos_por_tablas)
    return render_template('showflows.html', numero = n, total = flujos_por_tablas, nflujos = var_d, tablas_activas = tablas_activas), 200

@app.route('/home/addflow/<string:n>', methods = ['GET'])
def addflow(n):
    return render_template('addflow.html', numero = n)

@app.route('/home/addflow/<string:n>', methods = ['POST'])
def add(n):
    if request.method == 'POST':
        id_tabla = request.form['id_tabla']
        print(type(id_tabla))

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True, port = port)