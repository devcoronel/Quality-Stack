import requests, json
from variables import *

response = requests.get(url_switches_variable)
if response.status_code == 200:
    data = response.content
    switches = json.loads(data)

n_switch = len(switches)

def detalles_switch():
    carac_all_sw = []
    for i in switches:
        #Obtener las características del switch de turno
        str_i = str(i)
        url_caracteristicas = url_caracteristicas_variable +str_i
        caracteristicas = requests.get(url_caracteristicas)
        if caracteristicas.status_code == 200:
            #Obtener las caracteristicas de un switch
            carac_sw = caracteristicas.content
            carac_sw = json.loads(carac_sw)
            carac_all_sw.append(carac_sw[str_i])
    return carac_all_sw

def estadisticas_puertos(n):
    #n es el número del Switch
    n = str(n)
    url_estadisticas_puertos = url_estadisticas_puertos_variable + n
    response = requests.get(url_estadisticas_puertos)

    if response.status_code == 200:
        data = response.content
        data = json.loads(data)
        data = data[n] # Estadísticas de todos los puertos
        return data

print(estadisticas_puertos(1))