
import config as cf
import model
import time
import csv
import tracemalloc
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    data_jobs = model.new_data_structs()
    data_skills = model.new_data_structs()

    return {'data_jobs': data_jobs, 'data_skills': data_skills}


# Funciones para la carga de datos

def load_data(data_structs, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = {}

    with open(filename, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for indice, fila in enumerate(lector_csv):
            fila_modificada = {}
            for clave, valor in fila.items():
                if valor.strip() == '':
                    # Si el valor está en blanco, reemplazar por "DESCONOCIDO"
                    fila_modificada[clave] = 'DESCONOCIDO'
                else:
                    fila_modificada[clave] = valor
            data_structs[indice] = fila_modificada
    return data_structs


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass

def data_filter(datos, clave, valor):
    # datos_filtrados = {}
    # if clave=='published_at':
    #     for indice, fila in datos.items():
    #         fecha_fila = datetime.fromisoformat(fila[clave][:7])  # Obtiene año y mes de la fila
    #         if fecha_fila == valor:
    #             datos_filtrados[indice] = fila
    # else:
    #     for indice, fila in datos.items():
    #         if fila.get(clave) == valor:
    #             datos_filtrados[indice] = fila
    # return datos_filtrados
    datos_filtrados = {}
    if clave=='published_at':
        for indice, fila in datos.items():
            año_mes = fila[clave][:7]
            año, mes = map(int, año_mes.split('-'))
            fecha_fila = datetime.datetime(year=año, month=mes, day=1)
            if fecha_fila == valor:
                datos_filtrados[indice] = fila
    else:
        for indice, fila in datos.items():
            fila_clave = fila.get(clave)
            if fila_clave in valor:
                datos_filtrados[indice] = fila
    return datos_filtrados

def count(data,clave):
    conteo = {}
    for fila in data.values():
        valor = fila.get(clave)
        if valor in conteo:
            conteo[valor] += 1
        else:
            conteo[valor] = 1
    return conteo

def count_city(data,clave1,clave2,valor):
    clave1 = 'country_code'
    clave2 = 'city'
    count_city_pais = []
    for country in valor:
        conteo = {}
        datos_filtrados={}
        for indice, fila in data.items():
            fila_clave = fila.get(clave1)
            if fila_clave == country:
                datos_filtrados[indice] = fila
        for fila in datos_filtrados.values():
            valor2 = fila.get(clave2)
            if valor2 in conteo:
                conteo[valor2] += 1
            else:
                conteo[valor2] = 1
        count_city_pais.append({country: len(conteo)})
    return count_city_pais


def req_1(Cod_pais,Nivel_exp,data):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    Nivel_exp_m = [Nivel_exp]
    Cod_pais_m = [Cod_pais]
    if Nivel_exp =='' :
        print('ingrese valor de Nivel de experticia valido')
        pass
    else:
        if Cod_pais=='':
            data_rq1 = data_filter(data, 'experience_level', Nivel_exp_m)
        else:
            data_rq1 = data_filter(data, 'country_code', Cod_pais_m)
            data_rq1 = data_filter(data_rq1, 'experience_level', Nivel_exp_m)

    return data_rq1


def req_2(N_paises,Año_consulta,Mes_consulta,data_jobs,data_skills):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    try:
        Año = int(Año_consulta)
        Mes = int(Mes_consulta)
        N_paises = int(N_paises)
    except ValueError:
        print("¡Error! el año/mes no representa un número válido.")
    if 1900<Año<2024:
        if Mes<12:
            fecha_consulta = datetime.datetime(year=Año, month=Mes, day=1)
            data_rq2_date_filter = data_filter(data_jobs, 'published_at', fecha_consulta)
            
            count_pais = count(data_rq2_date_filter,'country_code')
            ord_pais = sorted(count_pais.items(), key=lambda x: x[1], reverse=True)
            n_pais = ord_pais[:N_paises]    #top paises y su numero de ofertas
            # 2.3
            top_1_pais = ord_pais[:1]

            code_n_pais = [pais for pais, _ in n_pais] #top paises 
            
            data_rq2 = data_filter(data_rq2_date_filter, 'country_code', code_n_pais)
            # 2.1
            total_ofertas = model.data_size(data_rq2)
            # 2.2
            conteo_ciudades = count_city(data_rq2,'country_code','city',code_n_pais)     #numero de ciudades con ofertas por pais       
            
            count_ciudad = count(data_rq2,'city')
            ord_ciudad = sorted(count_ciudad.items(), key=lambda x: x[1], reverse=True)
            # 2.4
            n_ciudad = ord_ciudad[:1]    #top 1 ciudad y su numero de ofertas
            
            return data_rq2,
        else:
            print("¡Error! el año/mes no representa un número válido.")
            pass            
    else:
        print("¡Error! el año/mes no representa un número válido.")    
        pass




# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
