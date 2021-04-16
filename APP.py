# Falta agregar cabecera X-CSRF-TOKEN para las solicitudes POST
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import requests, json
from variables import *
from cripto import *
from validaciones import *
from API_request import *

app = Flask(__name__)

#Conectar con la Base de Datos MySQL en Linux Ubuntu
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
mysql = MySQL(app)

# Hacer que los JWT funcionen con cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# Por el momento debe estar en false ya que no estamos usando HTTPS
# pero son buenas prácticas usar HTTPS y activar a True
app.config["JWT_COOKIE_SECURE"] = False

# Configurar una llave para el JWT
app.config['JWT_SECRET_KEY'] = key_para_jwt()

# Curiosidad
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Dar un tiempo de expiración al JWT
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

# Activar JWT con todos los parámetros configurados
jwt = JWTManager(app)

# Key para permitir insertar texto
app.secret_key = 'mysecretkey'

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html')

# Refrescar JWT
@app.after_request
def refresh_expiring_jwts(response):
    try:
        if response.status_code == 401: # Si no estamos autorizados (JWT vencido o no logueado) se borrarán esas cookies  
            response = redirect('/login')
            unset_jwt_cookies(response)
            return response
            
        exp_timestamp = get_jwt()["exp"] # Obtener la fecha de expiración del JWT actual
        now = datetime.now(timezone.utc) # Obtener la hora local
        target_timestamp = datetime.timestamp(now + timedelta(hours=20)) # A la hora actual aumentar 15min
        
        if target_timestamp > exp_timestamp:
            additional_claims = {"roleuser": get_jwt()["roleuser"]} # Obtenemos el rol del JWT anterior para conservarlo
            access_token = create_access_token(identity=get_jwt_identity(), additional_claims=additional_claims) # crear el nuevo JWT con su misma identidad y rol
            set_access_cookies(response, access_token) # Configuramos el JWT y retornamos el request que se estaba pidiendo

        return response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@app.route('/login', methods=['GET'])
@jwt_required(optional=True)
def main():
    current_identity = get_jwt_identity()
    if current_identity:
        return redirect('/home')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT id FROM users WHERE username = %s);", [usuario])
        resultado = cursor.fetchall()
        resultado = (resultado[0])[0]

        if resultado == 1:
            clave = SHA256(clave)
            cursor.execute("SELECT IF(passbytes = %s, True, False), roleuser FROM users WHERE username = %s;", [clave, usuario])
            verif_clave = cursor.fetchall()
            clave = (verif_clave[0])[0]
            roleuser = (verif_clave[0])[1]
            print(clave, roleuser)

            if clave == 1:
                response = redirect('/home')
                additional_claims = {"roleuser": roleuser}
                access_token = create_access_token(identity= usuario, additional_claims=additional_claims)
                set_access_cookies(response, access_token)
                return response
            
            else:
                flash('Usuario y/o contraseña incorrectos')
                return render_template('login.html')

        else:
                flash('Usuario y/o contraseña incorrectos')
                return render_template('login.html')

@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = redirect('/login')
    unset_jwt_cookies(response)
    return response

@app.route(r'/home', methods=['GET'])
@app.route(r'/home/<string:n>', methods=['GET'])
@jwt_required()
def home(n=None):
    carac_all_sw = detalles_switch()

    if n:
        est_port = estadisticas_puertos(n)
        return render_template('home.html', carac_all_sw = carac_all_sw, n_sw = n_switch, switches = switches, n = n, est_port = est_port)
        
    else:
        return render_template('home.html', carac_all_sw = carac_all_sw, n_sw = n_switch, switches = switches)

@app.route(r'/flowtables', methods=['GET'])
@app.route(r'/flowtables/<string:n>', methods=['GET'])
@jwt_required()
def showflows(n=None):
    if n:
        flow_table = (flowtables(n))[0]
        active_tables = (flowtables(n))[1]

        return render_template('flowtables.html', n = n, switches = switches, flow_table = flow_table, active_tables = active_tables)

    else:
        return render_template('flowtables.html', switches = switches)

@app.route('/addflow', methods=['GET'])
@jwt_required()
def addflow():
    comprobar_role = get_jwt()['roleuser']
    if comprobar_role == "admin" or comprobar_role == 'operator':
        return render_template('addflow.html', switches = switches)

    else:
        return render_template('AccessDenied.html')

# FALTA HACER: UNA VEZ TERMINADO SE DEBE AGREGAR A LA RUTA DE ARRIBA CON UN IF PARA POST
@app.route('/addflow/<string:n>', methods = ['POST'])
@jwt_required()
def add(n):
    if request.method == 'POST':
        id_tabla = request.form['id_tabla']
        print(type(id_tabla))

        return redirect(url_for('home'))

# AUN NO PUEDO UNIR ADDUSER GET CON ADDUSER POST PORQUE NECESITO
# PONER EL JWT_REQUIRED() Y ESO AÚN NO PUEDO HACERLO PORQUE EN EL
# POST NO SÉ PONER LA CABECERA X-CSRF-TOKEN
@app.route('/adduser', methods=['GET'])
@jwt_required()
def adduser():
    comprobar_role = get_jwt()['roleuser']
    if comprobar_role == "admin":
        return render_template('adduser.html')
    else:
        return render_template('AccessDenied.html')

@app.route('/adduser', methods=['POST'])
#@jwt_required() #ARREGLAR: PONER CABECERA X-CSRF-TOKEN
def adduser_post():
    if request.method == 'POST':
        username = request.form["addusername"]
        password1 = request.form["addpassword1"]
        password2 = request.form["addpassword2"]
        rol = request.form["rol"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT id FROM users WHERE username = %s);", [username])
        resultado = cursor.fetchall()
        existe = (resultado[0])[0]

        validacion = validar(username, password1, password2, existe, rol)
        if validacion[0] == True:
            msg = validacion[1]
            flash(msg)
            enc_pass = SHA256(password1)
            opciones_rol = ['none','admin', 'operator', 'viewer']
            roleuser = opciones_rol[int(rol)]
            
            cursor.execute("INSERT INTO users(username, roleuser, passbytes) VALUES (%s, %s, %s)", [username, roleuser, enc_pass])
            mysql.connection.commit()

        else:
            msg = validacion[1]
            flash(msg)
        
        return render_template('adduser.html', usuario = username)

# @app.route('/desencriptar')
# def desencriptar():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT passbytes FROM users WHERE username = 'Brenda';")
#     resultado = cursor.fetchall()
#     resultado = (resultado[0])[0]

#     b = DEC_AES256CBC(a, key, iv)
#     return b

if __name__ == '__main__':
    app.run(debug = True, port = port)