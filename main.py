import re
import os
from datetime import datetime
import json

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
separacion = lambda ancho = 64, ch = '-': print(ch * ancho)
titulo = lambda txt: (separacion(), print(" " * ((64 - len(txt)) // 2) + txt), separacion())

def validar_opcion():
    try:
        opcion = input("Opción: ")
        if opcion in ["1", "2", "3", "4", "5", "6"]:
            return opcion
        else:
            print("Error: debe ingresar un número entre 1 y 6.")
            return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    

viajes = []

def guardarViajesArchivo():
    with open("viajes.json", "w") as f:
        json.dump(viajes, f, indent=4)

def cargarViajesArchivo():
    try:
        with open("viajes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [] 

def menu():
    global viajes
    viajes = cargarViajesArchivo()

    opcion = ""
    while opcion != "6":
        clear()
        titulo("GESTOR DE VIAJES")

        print("\n1) Iniciar nuevo viaje.")
        print("2) Consultar tus viajes.")
        print("3) Eliminar viaje.")
        print("4) Filtrar viaje por origen.")
        print("5) Cargar pasajeros en viaje existente.")
        print("6) Salir.\n")
        separacion()
        opcion = None
        while opcion is None:
            opcion = validar_opcion()
       
        if opcion == "1":
            anotarNuevoViaje()
        elif opcion == "2":
            mostrarViajeExistente()
        elif opcion == "3":
            eliminarViaje()
        elif opcion == "4":
            filtrarPorOrigen()
        elif opcion == "5":
            cargarPasajerosEnViaje()
        elif opcion == "6":
            guardarViajesArchivo()
            print("\nSaliendo del programa...\n")

def anotarNuevoViaje():
    clear()
    titulo("NUEVO VIAJE")
    origenvalido = False
    while not origenvalido:
        origen = input("\nIngrese el origen:")
        try:
            if origen.strip() != "":
                origenvalido = True
            else:
                print("El origen no puede estar vacio.")
        except ValueError:
            print("Error inesperado")

    destinovalido = False
    while not destinovalido:
        destino = input("\nIngrese el destino:")
        try:
            if destino.strip() != "":
                destinovalido = True
            else:
                print("El destino no puede estar vacio.")
        except ValueError:
            print("Error inesperado")

    fechaValida = False
    while fechaValida == False:
        fecha_ingresada = input("Ingrese la fecha (dd/mm/aaaa): ")
        try:
            fechaConvertida = datetime.strptime(fecha_ingresada, "%d/%m/%Y").date()
            hoy = datetime.now().date()
            if fechaConvertida < hoy:
                print("\nLa fecha ingresada ya pasó. Ingrese una fecha futura.\n")
            else:
                fechaValida = True
        except ValueError:
            print("\nFormato inválido. Use el formato dd/mm/aaaa.\n")

    asientos = list(range(1, 21))

    viaje = {
        "origen": origen,
        "destino": destino,
        "fecha": fecha_ingresada,
        "asientos": asientos,
        "pasajeros": [],
        "dnis": set(),
        "ocupados": set()
    }

    viajes.append(viaje)

    print("\nViaje creado correctamente.\n")
    print("Ahora puede reservar asientos para este viaje:")
    reservar_asiento(viaje["asientos"], viaje["pasajeros"], viaje)

def mostrarViajeExistente():
    clear()
    titulo("TUS VIAJES")

    if len(viajes) == 0:
        print("\nNo hay Viajes cargados actualmente.\n")
    else:
        indice = 1
        for viaje in viajes:
            print(indice, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            mostrarPasajeros(viaje)
            print("\nAsientos:", viaje["asientos"])
            indice += 1
            separacion()

def eliminarViaje():
    clear()
    titulo("ELIMINAR VIAJE")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
    else:
        mostrarViajeExistente()
        try:
            numeroAEliminar = int(input("\nQue numero de viaje desea eliminar?: "))
            if 1 <= numeroAEliminar <= len(viajes):
                eliminar = viajes.pop(numeroAEliminar - 1)
                print("\nSe eliminó el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "la fecha", eliminar["fecha"])
            else:
                print("\nEl viaje ingresado no es valido.\n")
        except ValueError:
            print("\nDebe ingresar un número válido.\n")

def filtrarPorOrigen():
    clear()
    titulo("FILTRAR VIAJES POR ORIGEN")

    if len(viajes) == 0:
        print("\nNo hay ningún viaje cargado.\n")
    else:
        origen_buscado = input("\nIngrese el origen a buscar: ")
        viajes_filtrados = list(filter(lambda viaje: viaje["origen"] == origen_buscado, viajes))
        if len(viajes_filtrados) == 0:
            print("\nNo hay viajes desde", origen_buscado, "\n")
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print("\ndesde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
                mostrarPasajeros(viaje)
                print("\nAsientos:", viaje["asientos"])
                separacion()

def cargarPasajerosEnViaje():
    clear()
    titulo("CARGAR PASAJEROS")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
    else:
        print("\nSeleccione el número de viaje para cargar pasajeros:")
        i = 0
        for viaje in viajes:
            print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            i += 1
        try:
            num = int(input("Numero de viaje: "))
            if 1 <= num <= len(viajes):
                viaje = viajes[num - 1]
                print("Cargando pasajeros en el viaje desde", viaje["origen"], "hasta", viaje["destino"])
                reservar_asiento(viaje["asientos"], viaje["pasajeros"], viaje)
            else:
                print("\nNumero no válido.\n")
        except ValueError:
            print("\nDebe ingresar un número válido.\n")

def reservar_asiento(asientos_disponibles, lista_pasajeros, viaje):
    salir = False
    while salir == False:
        print("\nAsientos disponibles:\n")
        print(asientos_disponibles)

        elegir_asiento = input("\n¿Que asiento desea elegir? ('salir' para terminar): ").lower()

        if elegir_asiento == "salir":
            salir = True
        else:
            if not elegir_asiento.isdigit():
                print("\nIngrese un numero de asiento valido.")
                continue

            asiento = int(elegir_asiento)

            if asiento in viaje["ocupados"]:
                print("\nEse asiento esta ocupado o no existe.\n")
            else:
                cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento, viaje)
                print("\nAsiento reservado correctamente.\n")

def cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento, viaje):
    nombre = input("\nNombre del pasajero: ")
    while not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        print("\nNombre inválido. Solo se permiten letras y espacios.")
        nombre = input("Nombre del pasajero: ")

    dni = input("DNI del pasajero: ")
    while not re.fullmatch(r"\d{7,8}", dni):
        print("\nDNI inválido. Debe contener solo 7 u 8 números.")
        dni = input("DNI del pasajero: ")

    if dni in viaje["dnis"]:
        print("\nEse DNI ya está registrado en este viaje.")
        return

    email = input("Email del pasajero: ")
    while not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        print("\nEmail inválido. Intente nuevamente (ej: ejemplo@mail.com).")
        email = input("Email del pasajero: ")

    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "email": email,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)

    viaje["dnis"].add(dni)
    viaje["ocupados"].add(asiento)

    for i in range(len(asientos_disponibles)):
        if asientos_disponibles[i] == asiento:
            asientos_disponibles[i] = "X"
            print("\nAsiento reservado:", asiento)

def mostrarPasajeros(viaje):
    if viaje["pasajeros"]:
        print("   Pasajeros:")
        for pasajero in viaje["pasajeros"]:
            print("    -", pasajero["nombre"], "-", pasajero["dni"], "- asiento", pasajero["asiento"])
    else:
        print("   Pasajeros: No hay pasajeros cargados.")

if __name__ == "__main__":
    menu()
