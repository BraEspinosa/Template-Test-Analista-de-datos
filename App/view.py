

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import csv
import model
import datetime


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    pass


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("0- Salir")

# Variable global para almacenar los datos
datos = None

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    archivo = cf.data_dir + "large-jobs.csv"

    global datos_modificados
    datos_modificados = {}
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for indice, fila in enumerate(lector_csv):
            fila_modificada = {}
            for clave, valor in fila.items():
                if valor.strip() == '':
                    # Si el valor está en blanco, reemplazar por "DESCONOCIDO"
                    fila_modificada[clave] = 'DESCONOCIDO'
                else:
                    fila_modificada[clave] = valor
            datos_modificados[indice] = fila_modificada
    return datos_modificados

def print_loaded_data(data):

    lista_de_filas = [list(fila.values()) for fila in data.values()]
    total_ofertas = len(lista_de_filas)
    primeros_tres_datos = lista_de_filas[:3]
    ultimos_tres_datos = lista_de_filas[-3:]
    lista_de_filas = primeros_tres_datos + ultimos_tres_datos
    print(lista_de_filas)
    encabezados = list(data.values())[0].keys()
    tabla = tabulate(lista_de_filas, headers=encabezados, tablefmt="grid")
    print("El valor total de ofertas disponibles es de =")
    print(total_ofertas)

    print(tabla)

def contar_filas_por_valor_de_clave(data,clave):
    conteo = {}
    for fila in data.values():
        valor = fila.get(clave)
        if valor in conteo:
            conteo[valor] += 1
        else:
            conteo[valor] = 1
    return conteo

def print_data(control, id):
    pass

def print_req_1(data,N_registros):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1

    lista_de_filas = [list(fila.values()) for fila in data.values()]
    N=int(N_registros)
    total_ofertas = len(lista_de_filas)
    ultimos_datos = lista_de_filas[-N:]
    lista_de_filas = ultimos_datos
    encabezados = list(data.values())[0].keys()
    tabla = tabulate(lista_de_filas, headers=encabezados, tablefmt="grid")
    conteo_por_ciudad = contar_filas_por_valor_de_clave(data,'country_code')

    print("El valor total de ofertas disponibles mediante este filtro es de =")
    print(total_ofertas)
    print("El valor total de ofertas disponibles en cada ciudad es de =")
    print(conteo_por_ciudad)

    print(tabla)



def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    working_rq1 = True
    working_rq2 = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            inicio_load = datetime.datetime.now()
            data = load_data(control)
            print_loaded_data(data)
            fin_load = datetime.datetime.now()
            duracion = fin_load - inicio_load
            print(f"La función load_data tardó {duracion.total_seconds()} segundos en ejecutarse.")


        elif int(inputs) == 2:
            print("Listar N ofertas de trabajo segun pais y nivel de experticia")
            while working_rq1:
                data_rq1={}
                print("* = campos obligatorios")
                
                N_registros = input('*Valor de registros consultar (Valores admitidos 3, 5, 10 o 20):\n')
                Cod_pais = input('Codigo del pais preferible a consultar(ej: PL, CO, ES, etc):\n')
                Nivel_exp = input('*Nivel de experticia a consultar(junior, mid o senior):\n')
                inicio_rq1 = datetime.datetime.now()

                if N_registros == 3 or N_registros == 5 or N_registros == 10 or N_registros == 20:
                    if Nivel_exp =='' :
                        print('ingrese valor de Número de registros valido')
                        pass
                else:
                    data_rq1=model.req_1(Cod_pais,Nivel_exp,data)

                print_req_1(data_rq1,N_registros)
                fin_rq1 = datetime.datetime.now()
                duracion = fin_rq1 - inicio_rq1
                print(f"La función rq1 tardó {duracion.total_seconds()} segundos en ejecutarse.")

                Next_consulta = input('*Desea realizar otra consulta? SI/NO:\n')
                if Next_consulta == "SI":
                    pass
                else:
                    break


        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
