import requests, json
from variables import *


response = requests.get(url_switches_variable)
if response.status_code == 200:
    data = response.content
    switches = json.loads(data)
    switches = sorted(switches)

switches = switches
n_switch = len(switches)

def detalles_switch(): # USADO EN /HOME
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

def estadisticas_puertos(n): # USADO EN /HOME
    #n es el número del Switch
    n = str(n)
    url_estadisticas_puertos = url_estadisticas_puertos_variable + n
    response = requests.get(url_estadisticas_puertos)

    if response.status_code == 200:
        data = response.content
        data = json.loads(data)
        data = data[n] # Estadísticas de todos los puertos
        return data

def flowtables(n): # USADO EN /FLOWTABLES
    # Obtener las tablas del switch "n"
    url_tablas_flujo = url_tablas_flujo_variable + n
    tablas_flujo = requests.get(url_tablas_flujo)

    #Obtener los flujos del switch "n"
    url_flujos = url_flujos_variable + n
    flujos = requests.get(url_flujos)
    
    if tablas_flujo.status_code == 200 and flujos.status_code == 200:
        
        # Obtener las tablas en json
        tablas = tablas_flujo.content
        tablas = json.loads(tablas)
        tablas = tablas[n]
        n_tablas = len(tablas)
        
        #Obtener los flujos en json
        flujos = flujos.content
        flujos = json.loads(flujos)
        flujos = flujos[n]
        n_flujos = len(flujos)
        
        flow_table = []
        active_tables = []
        for i in range(n_tablas):

            if (tablas[i])["active_count"] != 0:
                table_id = (tablas[i])["table_id"]
                active_tables.append(str(table_id))

                for flujo in flujos:
                    if flujo["table_id"] == table_id:
                        formato = { str(table_id): flujo }
                        flow_table.append(formato)
        
        return (flow_table, active_tables)
