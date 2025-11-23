import re
import os
from datetime import datetime
import json

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
separacion = lambda ancho = 64, ch = '-': print(ch * ancho)
titulo = lambda txt: (separacion(), print(" " * ((64 - len(txt)) // 2) + txt), separacion())

def validar_opcion():
    """ Pide una opcion valida del menu (1 al 6). Devuelve la opcion si es valida, o None si hay error. """
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

#FUNCIÓN RECURSIVA
def mostrar_itinerario_recursivo(ruta, indice=0):
    """
    Muestra el itinerario (origen -> escalas -> destino) de forma recursiva.
    """
    if indice == len(ruta):
        return

    lugar = ruta[indice]
    
    if indice == 0:
        prefijo = "Origen:"
    elif indice == len(ruta) - 1:
        prefijo = "Destino:"
    else:
        prefijo = f"Escala {indice}:"

    print(f"  {prefijo} {lugar}")

    # Llamada recursiva (paso inductivo)
    mostrar_itinerario_recursivo(ruta, indice + 1)


def guardarViajesArchivo():
    """Guarda todos los viajes en un archivo json. Convierte los diccionarios de viajes y pasajeros en texto legible y los guarda línea por línea.
      Se usa isinstance(datos, list) para confirmar que el contenido
        del JSON sea una lista"""
    try:
        #convertir los sets a listas antes de guardar, sino da error
        lista_para_guardar = []
        for v in viajes:
            temp_viaje = v.copy()
            temp_viaje["dnis"] = list(v["dnis"]) 
            temp_viaje["ocupados"] = list(v["ocupados"])
            lista_para_guardar.append(temp_viaje)

        with open("viajes.json", "w") as f:
            json.dump(lista_para_guardar, f, indent=4)
    except Exception:
        print("Error al guardar los viajes en el archivo.")


def cargarViajesArchivo():
    """Carga los viajes desde el archivo . Reconstruye los diccionarios con los datos almacenados previamente.
      Se usa isinstance(datos, list) para confirmar que el contenido
        del JSON sea una lista"""
    
    try:
        with open("viajes.json", "r") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                print("Error: el archivo JSON no contiene una lista.")
                return []

            viajes_validos = []
            for v in datos:
                if (
                    isinstance(v, dict)
                    and "origen" in v
                    and "destino" in v
                    and "fecha" in v
                    and "asientos" in v
                    and isinstance(v["asientos"], list)
                ):
                    if "pasajeros" not in v or not isinstance(v["pasajeros"], list):
                        v["pasajeros"] = []
                    
                    # Convertimos de nuevo a set para que funcione 
                    v["dnis"] = set(v.get("dnis", []))
                    v["ocupados"] = set(v.get("ocupados", []))
                    if "escalas" not in v:
                        v["escalas"] = []

                    viajes_validos.append(v)
                else:
                    print("Se detectó un viaje inválido y fue descartado.")

            return viajes_validos

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error: el archivo JSON está dañado.")
        return []
    except Exception:
        print("Error inesperado al leer viajes.json.")
        return []


def menu():
    """Función principal que muestra el menú del programa. Carga los viajes desde archivo al iniciar y los guarda al salir."""
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
    """Inicia un nuevo viaje. Pide origen, destino y fecha. Crea la lista de asientos del 1 al 20. Guarda los datos en un diccionario y lo agrega a la lista general de viajes. Luego permite reservar asientos. """
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

    escalas_str = input("\nIngrese las escalas (separadas por coma, o enter para ninguna): ")
    if escalas_str.strip() == "":
        escalas = []
    else:
        escalas = [e.strip() for e in escalas_str.split(",")]
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
        "escalas": escalas, 
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
    """Muestra los viajes cargados. Si no hay viajes cargados informa al usuario. Si hay, muestra cada viaje con su número, origen, destino, fecha, pasajeros y asientos disponibles. """
    clear()
    titulo("TUS VIAJES")

    if len(viajes) == 0:
        print("\nNo hay Viajes cargados actualmente.\n")
    else:
        indice = 1
        for viaje in viajes:
            print(indice, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            
            ruta_completa = [viaje["origen"]] + viaje["escalas"] + [viaje["destino"]]
            print("\n  --- Itinerario del Viaje ---")
            mostrar_itinerario_recursivo(ruta_completa, 0)
            print("  ----------------------------\n")
            mostrarPasajeros(viaje)
            print("\nAsientos:", viaje["asientos"])
            indice += 1
            separacion()
    
    input("Presione Enter para continuar...") 

def eliminarViaje():
    """Elimina un viaje de la lista. Muestra los viajes existentes, pide el número del viaje a eliminar y lo elimina si es válido. """
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
    """Filtra viajes por origen. Pide el origen a buscar y muestra los viajes que coinciden. Si no hay coincidencias, informa al usuario. """
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
                
                ruta_completa = [viaje["origen"]] + viaje.get("escalas", []) + [viaje["destino"]]
                mostrar_itinerario_recursivo(ruta_completa, 0)
                
                mostrarPasajeros(viaje)
                print("\nAsientos:", viaje["asientos"])
                separacion()
    input("Presione Enter para continuar...")

def cargarPasajerosEnViaje():
    """Carga pasajeros en un viaje ya existente. Muestra los viajes disponibles, pide el número del viaje y permite reservar asientos en el viaje seleccionado. """
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
    """Gestiona la reserva de asientos. Muestra los asientos disponibles, permite elegir uno y valida que el asiento sea correcto. También permite escribir 'salir' para terminar. """
    salir = False
    mientras = salir == False
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
    """Carga un nuevo pasajero en la lista. Pide nombre, DNI y email. Valida los datos con expresiones regulares y previene DNIs duplicados dentro del mismo viaje. """
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
    """Muestra la lista de pasajeros de un viaje. Si hay pasajeros, los lista con nombre, DNI y asiento. Si no hay, informa que no existen pasajeros cargados. """
    if viaje["pasajeros"]:
        print("   Pasajeros:")

        # recursividad
        def mostrar_rec(i):
            if i == len(viaje["pasajeros"]):
                return
            p = viaje["pasajeros"][i]
            print("    -", p["nombre"], "-", p["dni"], "- asiento", p["asiento"])
            mostrar_rec(i + 1)

        mostrar_rec(0)
    else:
        print("   Pasajeros: No hay pasajeros cargados.")

if __name__ == "__main__":
    menu()