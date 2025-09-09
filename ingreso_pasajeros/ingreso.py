def ingreso_pasajeros():
    pasajeros = []

    while True:
        print("1. Cargar pasajero")
        print("2. Lista de pasajeros")
        print("3. Salir")

        opcion = input("Elija una opcion: ")

        if opcion == "1":
            cargar_pasajero(pasajeros)
        elif opcion == "2":
            lista_pasajeros(pasajeros)
        elif opcion == "3":
            print("Saliendo.")
            break
        else:
            print("Opcion no valida.")
    
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

def cargar_pasajero(lista_pasajeros):
    nombre = input("nombre del pasajero: ")
    dni = input("dni del pasajero: ")
    asiento = input("numero de asiento: ")
    
    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)
    print("Pasajero agregado correctamente.")            
ingreso_pasajeros()