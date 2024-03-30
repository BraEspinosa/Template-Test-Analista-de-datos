

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
    control = controller.new_controller()
    return control


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

    pass

def print_loaded_data(data):

    data_list = [list(fila.values()) for fila in data.values()]
    # total_ofertas = len(data_list)
    total_ofertas = controller.model.data_size(data)
    data_first = data_list[:3]
    data_last = data_list[-3:]
    data_list_zip = data_first + data_last
    # print(data_list_zip)
    encabezados = list(data.values())[0].keys()
    tabla = tabulate(data_list_zip, headers=encabezados, tablefmt="grid")
    print("El valor total de ofertas disponibles es de =")
    print(total_ofertas)

    print(tabla)


def print_data(control, id):
    pass

def print_req_1(data,N_registros):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1

    data_list = [list(fila.values()) for fila in data.values()]
    N=int(N_registros)
    total_ofertas = controller.model.data_size(data)
    last_n_data = data_list[-N:]
    if len(last_n_data) > 10:
        data_first = last_n_data[:5]
        data_last = last_n_data[-5:]
        data_list_zip = data_first + data_last
    else:
        data_list_zip = last_n_data
    encabezados = list(data.values())[0].keys()
    tabla = tabulate(data_list_zip, headers=encabezados, tablefmt="grid")
    pais_count = controller.count(data,'country_code')

    print("El valor total de ofertas disponibles mediante este filtro es de =")
    print(total_ofertas)
    print("El valor total de ofertas disponibles en cada ciudad es de =")
    print(pais_count)

    print(tabla)



def print_req_2(data,N_registros):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    data_list = [list(fila.values()) for fila in data.values()]
    N=int(N_registros)
    total_ofertas = controller.model.data_size(data)
    last_n_data = data_list[-N:]
    if len(last_n_data) > 10:
        data_first = last_n_data[:5]
        data_last = last_n_data[-5:]
        data_list_zip = data_first + data_last
    else:
        data_list_zip = last_n_data
    encabezados = list(data.values())[0].keys()
    tabla = tabulate(data_list_zip, headers=encabezados, tablefmt="grid")
    pais_count = controller.count(data,'country_code')

    print("El valor total de ofertas disponibles mediante este filtro es de =")
    print(total_ofertas)
    print("El valor total de ofertas disponibles en cada ciudad es de =")
    print(pais_count)

    print(tabla)


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
    archivo_jobs = cf.data_dir + "small-jobs.csv"
    data_jobs = ''
    data_skills = ''
    archivo_skills = cf.data_dir + "small-skills.csv"
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            inicio_load = datetime.datetime.now()
            control['data_jobs'] = controller.load_data(control['data_jobs'],archivo_jobs)
            data_jobs = control['data_jobs']
            control['data_skills'] = controller.load_data(control['data_skills'],archivo_jobs)
            data_skills = control['data_skills']
            print_loaded_data(data_jobs)
            fin_load = datetime.datetime.now()
            duracion = fin_load - inicio_load
            print(f"La función load_data tardó {duracion.total_seconds()} segundos en ejecutarse.")


        elif int(inputs) == 2:
            if data_jobs !='':
                print("Listar N ofertas de trabajo segun pais y nivel de experticia")
                while working_rq1:
                    data_rq1={}
                    print("* = campos obligatorios")
                    
                    N_registros = input('*Valor de registros consultar (ej: 3, 5, 10 o 20):\n')
                    Cod_pais = input('Codigo del pais preferible a consultar(ej: PL, CO, ES, etc):\n')
                    Nivel_exp = input('*Nivel de experticia a consultar(junior, mid o senior):\n')
                    inicio_rq1 = datetime.datetime.now()
                    data_rq1=controller.req_1(Cod_pais,Nivel_exp,data_jobs)

                    print_req_1(data_rq1,N_registros)
                    fin_rq1 = datetime.datetime.now()
                    duracion = fin_rq1 - inicio_rq1
                    print(f"La función rq1 tardó {duracion.total_seconds()} segundos en ejecutarse.")

                    Next_consulta = input('*Desea realizar otra consulta? SI/NO:\n')
                    if Next_consulta == "SI":
                        pass
                    else:
                        break
            else:
                print("Data vacia, verifique y cargue la informacion")
                pass

        elif int(inputs) == 3:
            if data_jobs !='':

                print("Listar N ofertas de trabajo segun pais y nivel de experticia")
                while working_rq2:
                    data_rq2={}
                    print("* = campos obligatorios")
                    
                    N_paises = input('*Numero de paises a consultar (ej: 3, 5, 10 o 20):\n')
                    Año_consulta = input('*Número de año de consulta (entre 1900 a 2024):\n')
                    Mes_consulta = input('*Número del mes de consulta :\n')
                    inicio_rq2 = datetime.datetime.now()
                    data_rq2=controller.req_2(N_paises,Año_consulta,Mes_consulta,data_jobs,data_skills)

                    print_req_2(data_rq2,N_paises)
                    fin_rq2 = datetime.datetime.now()
                    duracion = fin_rq2 - inicio_rq2
                    print(f"La función rq1 tardó {duracion.total_seconds()} segundos en ejecutarse.")

                    Next_consulta = input('*Desea realizar otra consulta? SI/NO:\n')
                    if Next_consulta == "SI":
                        pass
                    else:
                        break
            else:
                print("Data vacia, verifique y cargue la informacion")
                pass
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
