import re

def ingreso_pasajeros(): 
    pasajeros = []

    while True:
        print("--- Menu ---")
        print("1. Cargar pasajero")
        print("2. Lista de pasajeros")
        print("3. Salir")

        opcion = input("Elija una opcion: ")

        if opcion == "1":
            cargar_pasajero(pasajeros)
        elif opcion == "2":
            lista_pasajeros(pasajeros)
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida.")


def cargar_pasajero(lista_pasajeros):

    nombre = input("Nombre del pasajero: ")
    dni = input("DNI del pasajero: ")

    while not re.search("^[0-9]{7,8}$", dni):
        print("DNI no valido. Ingrese solo numeros.")
        dni = input("DNI del pasajero: ")

    asiento = input("Numero de asiento: ")

    for i in lista_pasajeros:
        if i["dni"] == dni:
            print("Ese DNI ya esta registrado.")
            return

    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)
    print("Pasajero agregado correctamente.")


def lista_pasajeros(lista_pasajeros):
    if len(lista_pasajeros) == 0: 
        print("No hay pasajeros cargados.") 
    else: 
        print("--- Lista de Pasajeros ---") 
        for i in range(len(lista_pasajeros)): 
            pasajero = lista_pasajeros[i] 
            print("Pasajero", i + 1) 
            print("Nombre:", pasajero["nombre"]) 
            print("Dni:", pasajero["dni"]) 
            print("Asiento:", pasajero["asiento"]) 
            print("----------------------")


ingreso_pasajeros()
