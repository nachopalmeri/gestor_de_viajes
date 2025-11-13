import re   # la usamos para validar el dni
import os   # la usamos para limpiar la pantalla
from datetime import datetime #la usamos para que no se pueda sacar vuelos para fechas pasadas+
import json


# Funciones visuales

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
separacion = lambda ancho = 64, ch = '-': print(ch * ancho)
titulo = lambda txt: (separacion(), print(" " * ((64 - len(txt)) // 2) + txt), separacion())


viajes = []  
def guardarViajesArchivo():
    """Guarda todos los viajes en un archivo json.
    Convierte los diccionarios de viajes y pasajeros en texto legible y los guarda línea por línea."""
    with open("viajes.json", "w") as f:
        json.dump(viajes, f, indent=4)


def cargarViajesArchivo():
    """Carga los viajes desde el archivo .
    Reconstruye los diccionarios con los datos almacenados previamente."""
    try:
        with open("viajes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [] 

def menu():
    """Función principal que muestra el menú del programa.
    Carga los viajes desde archivo al iniciar y los guarda al salir."""
    cargarViajesArchivo()  

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
        opcion = input("\nOpción: ")

       
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
        else:
            print("\nError, opción inválida.\n")
            input("Enter para continuar...")


def anotarNuevoViaje():
    """Inicia un nuevo viaje.
    Pide origen, destino y fecha. Crea la lista de asientos del 1 al 20.
    Guarda los datos en un diccionario y lo agrega a la lista general de viajes.
    Luego permite reservar asientos.
    """
    clear()
    titulo("NUEVO VIAJE")
    
    origen = input("\nIngrese el origen: ")   
    destino = input("Ingrese el destino: ") 

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
        "pasajeros": []
    }
    viajes.append(viaje) 

    print("\nViaje creado correctamente.\n")
    print("Ahora puede reservar asientos para este viaje:")
    reservar_asiento(viaje["asientos"], viaje["pasajeros"])  
    input("\nPresione Enter para volver al menú...")


def mostrarViajeExistente():
    """Muestra los viajes cargados.
    Si no hay viajes cargados informa al usuario. 
    Si hay, muestra cada viaje con su número, origen, destino, fecha,
    pasajeros y asientos disponibles.
    """
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
    input("\nEnter para volver al menú...")


def eliminarViaje():
    """Elimina un viaje de la lista.
    Muestra los viajes existentes, pide el número del viaje a eliminar
    y lo elimina si es válido.
    """
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
    input("\nEnter para volver al menú...")


def filtrarPorOrigen():
    """Filtra viajes por origen.
    Pide el origen a buscar y muestra los viajes que coinciden.
    Si no hay coincidencias, informa al usuario.
    """
    clear()
    titulo("FILTRAR VIAJES POR ORIGEN")

    if len(viajes) == 0:
        print("\nNo hay ningún viaje cargado.\n")
    else:
        origen_buscado = input("\nIngrese el origen a buscar: ")  
        viajes_filtrados = list(filter(lambda viaje: viaje["origen"] == origen_buscado, viajes))  
        if len(viajes_filtrados) == 0:
            print("\nNo hay viajes desde", origen_buscado,"\n")
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print("\ndesde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
                mostrarPasajeros(viaje)
                print("\nAsientos:", viaje["asientos"])
                separacion()

    input("\nEnter para volver al menú...")


def cargarPasajerosEnViaje():
    """Carga pasajeros en un viaje ya existente.
    Muestra los viajes disponibles, pide el número del viaje
    y permite reservar asientos en el viaje seleccionado.
    """
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
                reservar_asiento(viaje["asientos"], viaje["pasajeros"])  
            else:
                print("\nNumero no válido.\n")
        except ValueError:
            print("\nDebe ingresar un número válido.\n")
    input("\nEnter para volver al menú...")


def reservar_asiento(asientos_disponibles, lista_pasajeros):
    """Gestiona la reserva de asientos.
    Muestra los asientos disponibles, permite elegir uno y valida
    que el asiento sea correcto. También permite escribir 'salir' para terminar.
    """
    salir = False
    while salir == False:
        print("\nAsientos disponibles:\n")
        print(asientos_disponibles)  # muestra asientos libres y los ocupados con ("X")

        elegir_asiento = input("\n¿Que asiento desea elegir? ('salir' para terminar): ").lower()

        if elegir_asiento == "salir": 
            salir = True
        else:
            if not elegir_asiento.isdigit(): 
                print("\nIngrese un numero de asiento valido.")
                continue

            asiento = int(elegir_asiento)  

            if asiento not in asientos_disponibles: 
                print("\nEse asiento esta ocupado o no existe.\n")
            else:
                cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento)  # carga pasajero
                print("\nAsiento reservado correctamente.\n")


def cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento):
    """Carga un nuevo pasajero en la lista.
    Pide nombre y DNI, valida el formato del DNI, evita duplicados
    y marca el asiento elegido como ocupado.
    """
    nombre = input("\nNombre del pasajero: ")  
    dni = input("DNI del pasajero: ")       

    while not re.search("^[0-9]{7,8}$", dni):
        print("\nDNI no valido. Ingrese solo numeros.")
        dni = input("DNI del pasajero: ")

    for i in lista_pasajeros:
        if i["dni"] == dni:
            print("\nEse DNI ya esta registrado.\n")
            return

    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)  
    print("\nPasajero agregado correctamente.\n")

    for i in range(len(asientos_disponibles)):
        if asientos_disponibles[i] == asiento:  
            asientos_disponibles[i] = "X"     
            print("\nAsiento reservado:", asiento)


def mostrarPasajeros(viaje):
    """Muestra la lista de pasajeros de un viaje.
    Si hay pasajeros, los lista con nombre, DNI y asiento.
    Si no hay, informa que no existen pasajeros cargados.
    """
    if viaje["pasajeros"]:
        print("   Pasajeros:")
        for pasajero in viaje["pasajeros"]:
            print("    -", pasajero["nombre"], "-", pasajero["dni"], "- asiento", pasajero["asiento"])
    else:
        print("   Pasajeros: No hay pasajeros cargados.")


menu()  # se llama al menú principal para iniciar el programa

