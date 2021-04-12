
def validar(username, password1, password2, existe, rol):
    # Constantes de longitud de contraseña
    lenmin = 8
    lenmax = 20
    validar_len = False

    # Constantes de numero de mayusculas, minusculas, numeros y signos
    n_mayus = 1
    n_minus = 1
    n_num_sig = 1
    n_contador = {'minuscula': 0, 'mayuscula': 0, 'numeros_y_signos':0}
    validar_n = False

    # Constante de si la contraseña contiene el usuario dentro
    same_user = True

    # Comprobar si el usuario ya existe en la base de datos
    exist_user = True

    # Validacion total
    val = False

    # password en blanco
    blank_pass = True

    # usuario en blanco
    blank_user = True

    # Comprobar si las contraseñas coinciden
    same_pass = False

    # Comprobar si se eligió un rol
    rol_elegido = False

    # Mensaje
    msg = ""

    # SE EMPIEZA EL ANÁLISIS
    len_pass = len(password1)

    for i in password1:
        if i.isupper():
            n_contador['mayuscula'] += 1
        elif i.islower():
            n_contador['minuscula'] += 1
        else:
            n_contador['numeros_y_signos'] += 1
    
    # VALIDACIONES
    if username == "":
        msg = "Debe introducir un nombre de usuario"

    elif password1 == "" or password2 == "":
        msg = "Debe introducir una contraseña"

    elif existe == True:
        msg = "Este nombre de usuario ya existe"
    
    elif password1 != password2:
        msg = "Las contraseñas deben coincidir"

    elif len_pass < lenmin or len_pass >= lenmax:
        msg = "La contraseña debe tener entre {} y {} caracteres".format(lenmin, lenmax)
        
    elif n_contador['mayuscula'] < n_mayus:
        msg = "La contraseña debe tener al menos {} letras mayúsculas".format(n_mayus)
    
    elif n_contador['minuscula'] < n_minus:
        msg = "La contraseña debe tener al menos {} letras minúsculas".format(n_minus)
    
    elif n_contador['numeros_y_signos'] < n_num_sig:
        msg = "La contraseña debe tener al menos {} números o signos".format(n_num_sig)
    
    elif username.lower() in password1.lower():
        msg = "La contraseña no se puede parecer a el usuario"
    
    elif rol == '0':
        msg = "Elija un rol para el usuario"

    else:
        same_user = False
        validar_len = True
        validar_n = True
        exist_user = False
        blank_pass = False
        blank_user = False
        same_pass = True
        rol_elegido = True
    
    # DAR EL RESULTADO FINAL
    if same_user == False and validar_n == True and validar_len == True and exist_user == False and blank_user == False and blank_pass == False and same_pass == True and rol_elegido == True:
        val = True
        msg = "Usuario añadido correctamente"
        validacion = [val, msg]
    else:
        validacion = [val, msg]

    return validacion
