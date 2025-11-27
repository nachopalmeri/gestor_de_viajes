import re   # la usamos para validar el dni
import os   # la usamos para limpiar la pantalla
from datetime import datetime #la usamos para que no se pueda sacar vuelos para fechas pasadas
import json

#Funciones visuales

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
separacion = lambda ancho = 64, ch = '-': print(ch * ancho)
titulo = lambda txt: (separacion(), print(" " * ((64 - len(txt)) // 2) + txt), separacion())

def validar_opcion():
    """
    Pide una opcion válida del menu (1 al 8).
    Devuelve la opcion si es válida, o None si hay error.
    """
    try:
        opcion = input("Opción: ")
        if opcion in ["1", "2", "3", "4", "5", "6","7","8"]:
            return opcion
        else:
            print("Error: debe ingresar un número entre 1 y 8.")
            return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    
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
    mostrar_itinerario_recursivo(ruta, indice + 1)

viajes = []  

def guardarViajesArchivo():
    """Guarda todos los viajes en un archivo json. Convierte los sets a listas."""
    try:
        lista_para_guardar = []
        for viaje in viajes:
            temp_viaje = viaje.copy()
            temp_viaje["dnis"] = list(viaje["dnis"]) 
            temp_viaje["ocupados"] = list(viaje["ocupados"])
            lista_para_guardar.append(temp_viaje)

        with open("viajes.json", "w") as f:
            json.dump(lista_para_guardar, f, indent=4)
        print("Cambios guardados correctamente en el archivo.")
    except Exception as e:
        print(f"Error al guardar los viajes en el archivo: {e}")


def cargarViajesArchivo():
    """Carga los viajes desde el archivo y reconstruye los Sets."""
    try:
        with open("viajes.json", "r") as f:
            datos = json.load(f)
            for viaje in datos:
                viaje["dnis"] = set(viaje["dnis"])
                viaje["ocupados"] = set(viaje["ocupados"])
                if "escalas" not in viaje:
                    viaje["escalas"] = []
            return datos
    except FileNotFoundError:
        return [] 
    except Exception:
        return []

def menu():
    """Función principal que muestra el menú del programa."""
    global viajes
    viajes = cargarViajesArchivo()  

    opcion = ""
    while opcion != "8":
        clear()
        titulo("GESTOR DE VIAJES")

        print("\n1) Iniciar nuevo viaje.")
        print("2) Consultar tus viajes.")
        print("3) Eliminar viaje.")
        print("4) Filtrar viaje por origen.")
        print("5) Cargar pasajeros en viaje existente.")
        print("6) Editar pasajeros de un viaje existente.")
        print("7) Editar un viaje existente.")
        print("8) Salir.\n")
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
            editarPasajeroEnViaje()
        elif opcion == "7":
            editarViaje()
        elif opcion == "8":
            guardarViajesArchivo()  
            print("\nSaliendo del programa...\n")
        

def anotarNuevoViaje():
    """Inicia un nuevo viaje e inicializa los Sets y las Escalas."""
    clear()
    titulo("NUEVO VIAJE")
    
    origenvalido = False
    while not origenvalido:
        origen = input("\nIngrese el origen: ").capitalize()
        
        if origen.strip() == "":
            print("El origen no puede estar vacío.")
        elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+",origen):
            print("El origen solo debe contener letras y espacios.")
        else:
            origenvalido = True
            
    destinovalido = False
    while not destinovalido:
        destino = input("\nIngrese el destino: ").capitalize()
        if destino.strip() == "":
            print("El destino no puede estar vacío.")
        elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+",destino):
            print("El destino solo debe contener letras y espacios.")
        else:
            destinovalido = True

    fechaValida = False
    while fechaValida == False:
        fecha_ingresada = input("\nIngrese la fecha (dd/mm/aaaa): ")
        try:
            fechaConvertida = datetime.strptime(fecha_ingresada, "%d/%m/%Y").date()
            hoy = datetime.now().date()
            if fechaConvertida < hoy:
                print("\nLa fecha ingresada ya pasó. Ingrese una fecha futura.\n")
            else:
                fechaValida = True
        except ValueError:
            print("\nFormato inválido. Use el formato dd/mm/aaaa.\n")
    escalas = []
    respuesta_valida = False
    cargar_escalas = False  
    while not respuesta_valida:
        agregar = input("\n¿Desea agregar escalas? (s/n): ").lower().strip()
        if agregar == "s":
            cargar_escalas = True
            respuesta_valida = True
        elif agregar == "n":
            cargar_escalas = False
            respuesta_valida = True
        else:
            print("Opción inválida. Por favor ingrese 's' o 'n'.")

    while cargar_escalas:
        nombre_valido = False
        while not nombre_valido:
            nueva_escala = input("Ingrese la ciudad de escala: ").capitalize().strip()
            
            if nueva_escala == "":
                print("La escala no puede estar vacía.")
            elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nueva_escala):
                print("La escala solo debe contener letras y espacios.")
            else:
                escalas.append(nueva_escala)
                print(f"Escala '{nueva_escala}' agregada.")
                nombre_valido = True  

        decision_valida = False
        while not decision_valida:
            otra = input("¿Desea agregar otra escala? (s/n): ").lower().strip()
            
            if otra == "s":
                cargar_escalas = True 
                decision_valida = True 
            elif otra == "n":
                cargar_escalas = False 
                decision_valida = True 
            else:
                print("Opción inválida. Por favor ingrese 's' o 'n'.")
        
    asientos = [str(i) for i in range(1, 21)]
    
    viaje = {
        "origen": origen,
        "destino": destino,
        "fecha": fecha_ingresada,
        "escalas": escalas,
        "asientos": asientos,
        "pasajeros": [],
        "dnis": set(),      
        "ocupados": set() 
    }
    viajes.append(viaje)

    print("\nViaje creado correctamente.\n")
    print("Ahora puede reservar asientos para este viaje:")
    reservar_asiento(viaje)


def mostrarViajeExistente(pausar=True):
    """Muestra los viajes y el itinerario recursivo real."""
    clear()
    titulo("TUS VIAJES")

    if len(viajes) == 0:  
        print("\nNo hay Viajes cargados actualmente.\n")
    else:
        indice = 1  
        for viaje in viajes:
            print(f"{indice}) Desde {viaje['origen']} hasta {viaje['destino']} ({viaje['fecha']})")
            ruta_completa = [viaje["origen"]] + viaje["escalas"] + [viaje["destino"]]
            
            print("   Itinerario:")
            mostrar_itinerario_recursivo(ruta_completa)
            print("")
            mostrarPasajeros(viaje)
            matriz_visual = [viaje["asientos"][i:i+4] for i in range(0, 20, 4)]
            mostrar_asientos(matriz_visual, viaje["pasajeros"])
            
            indice += 1
            separacion()
    if pausar:
        input("\nPresione Enter para volver al menú...")


def eliminarViaje():
    clear()
    titulo("ELIMINAR VIAJE")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
    else:
        mostrarViajeExistente(pausar=False)  
        try:
            numeroAEliminar = int(input("\nQue numero de viaje desea eliminar?: "))  
            if 1 <= numeroAEliminar <= len(viajes):
                eliminar = viajes.pop(numeroAEliminar - 1) 
                print("\nSe eliminó el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "la fecha", eliminar["fecha"])
            else:
                print("\nEl viaje ingresado no es válido.\n")
        except ValueError:
            print("\nDebe ingresar un número válido.\n")

    input("\nPresione Enter para volver al menú...")

def filtrarPorOrigen():
    clear()
    titulo("FILTRAR VIAJES POR ORIGEN")

    if len(viajes) == 0:
        print("\nNo hay ningún viaje cargado.\n")
    else:
        origen_buscado = input("\nIngrese el origen a buscar: ").capitalize()
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
    
    input("\nPresione Enter para volver al menú...")


def cargarPasajerosEnViaje():
    clear()
    titulo("CARGAR PASAJEROS")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
        input("\nPresione Enter para volver al menú...")

    else:
        print("\nSeleccione el número de viaje para cargar pasajeros: ")
        i = 0
        for viaje in viajes:  
            print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            i += 1
        
        valido = False

        while not valido:
            opcion = input("Número de viaje: ")

            if not opcion.isdigit():
                print("\nDebe ingresar un número válido (sólo números).\n")
                continue

            num = int(opcion)

            if 1 <= num <= len(viajes):
                valido = True
            else:
                print("\n El número de viaje no existe. Intente nuevamente.\n")

        viaje = viajes[num - 1] 
        print("Cargando pasajeros en el viaje desde", viaje["origen"], "hasta", viaje["destino"])
        reservar_asiento(viaje)  

def reservar_asiento(viaje):
    """
    Gestiona la reserva de asientos usando la visualización de matriz (avión).
    Recibe el objeto 'viaje' completo.
    """
    asientos_disponibles = viaje["asientos"]
    
    salir = False
    while not salir:
        matriz_visual = [asientos_disponibles[i:i+4] for i in range(0, 20, 4)]
        mostrar_asientos(matriz_visual, viaje["pasajeros"])
        
        elegir_asiento = input("\n¿Que asiento desea elegir? ('salir' para terminar): ").lower()

        if elegir_asiento == "salir": 
            salir = True
        else:
            if not elegir_asiento.isdigit(): 
                print("\nIngrese un número de asiento válido.")
                continue

            if elegir_asiento not in asientos_disponibles:
                 print("\nEse asiento no existe o ya fue borrado de la lista.")
            elif elegir_asiento in viaje["ocupados"]: 
                print("\nEse asiento esta ocupado.\n")
            else:
                cargar_pasajero(viaje, asientos_disponibles, elegir_asiento) 


def elegir_asiento_para_edicion(asientos_disponibles, lista_pasajeros):
    """Permite elegir un asiento al editar un pasajero."""
    
    matriz_visual = [asientos_disponibles[i:i+4] for i in range(0, 20, 4)]
    mostrar_asientos(matriz_visual, {})
    elegir = input("\nNuevo asiento ('salir' para cancelar): ").lower()
    if elegir == "salir":
        print("Cambio de asiento cancelado.")
        return None
    if not elegir.isdigit():
        print("Debe ingresar un número válido.")
        return None

    nuevo_asiento = int(elegir)
    nuevo_asiento_str = str(nuevo_asiento)
    if not (1 <= nuevo_asiento <= 20):
         print("Ese asiento no existe.")
         return None
    if asientos_disponibles[nuevo_asiento - 1] == "X":
        print("Ese asiento está ocupado.")
        return None

    return nuevo_asiento


def cargar_pasajero(viaje, asientos_disponibles, asiento):
    """Carga un nuevo pasajero, valida con Sets y actualiza el viaje."""
    
    lista_pasajeros = viaje["pasajeros"]

    """ Validar nombre """
    nombre = input("\nNombre del pasajero: ")
    while not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        print("\nNombre inválido. Solo se permiten letras y espacios.")
        nombre = input("Nombre del pasajero: ")

    """ Validar DNI  """
    dni = input("DNI del pasajero: ")
    while not re.fullmatch(r"\d{7,8}", dni):
        print("\nDNI inválido. Debe contener solo 7 u 8 números.")
        dni = input("DNI del pasajero: ")

    """ Evitar duplicado usando el SET """
    if dni in viaje["dnis"]:
        print("\nEse DNI ya está registrado en este viaje.")
        return

    """ Validar email """
    email = input("Email del pasajero: ")
    while not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        print("\nEmail inválido. Intente nuevamente (ej: ejemplo@mail.com).")
        email = input("Email del pasajero: ")

    """ Crear pasajero """
    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "email": email, 
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)
    viaje["dnis"].add(dni)
    viaje["ocupados"].add(asiento)

    print("\nPasajero agregado correctamente.\n")

    """ Marcar el asiento como ocupado (Visualmente en la lista) """
    idx = int(asiento) - 1
    if 0 <= idx < len(asientos_disponibles):
        asientos_disponibles[idx] = "X"
        print("\nAsiento reservado:", asiento)


def mostrarPasajeros(viaje):
    """Muestra la lista de pasajeros de un viaje."""
    if viaje["pasajeros"]:
        print("Pasajeros:")
        def mostrar_rec(i):
            if i == len(viaje["pasajeros"]):
                return
            p = viaje["pasajeros"][i]
            print("    -", p["nombre"], "-", p["dni"], "- asiento", p["asiento"])
            mostrar_rec(i + 1) 
        mostrar_rec(0)
    else:
        print("Pasajeros: No hay pasajeros cargados.")


def mostrar_asientos(matriz_asientos, pasajeros):
    """Muestra la matriz de asientos en formato [XX] [01]."""
    titulo("ASIENTOS")
    ocupados = []
    if isinstance(pasajeros, list):
        for p in pasajeros:
            ocupados.append(str(p["asiento"]))
    for fila in matriz_asientos:
        linea = ""
        for asiento in fila:
            if asiento == "X" or asiento in ocupados:
                linea += "[XX] "
            else:
                if len(asiento) == 1:
                    linea += f"[0{asiento}] "
                else:
                    linea += f"[{asiento}] "
        print(linea)

    print("\n(XX = ocupado)\n")



def elegir_asiento(matriz_asientos, pasajeros):
    """Solicita un número de asiento y devuelve el valor ingresado por el usuario."""
    mostrar_asientos(matriz_asientos, pasajeros)
    return input("\nIngrese el asiento que quiere asignar: ")


def editarPasajeroEnViaje():
    clear()
    titulo("EDITAR PASAJERO")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
        input("\nPresione Enter para continuar...")
        return
    

    while True:
        print("\nSeleccione el número de viaje donde desea editar un pasajero: ")
        for i, viaje in enumerate(viajes):
            print(f"{i + 1}) Desde: {viaje['origen']} | Hasta: {viaje['destino']} | Fecha: {viaje['fecha']}")
        
        print(f"\nIngrese '0' para volver (cancelar).") 

        opcion_ingresada = input("Número de viaje: ").strip()

        if opcion_ingresada == "0":
            print("\nEdición de pasajero cancelada.")
            input("\nPresione Enter para continuar...")
            return 
            
        try:
            num = int(opcion_ingresada)
            if 1 <= num <= len(viajes):
                viaje = viajes[num - 1]
                editar_pasajero(viaje) 
                break 
            else:
                print("Número no válido. Por favor, intente de nuevo.")
                input("\nPresione Enter para continuar...")
        except ValueError:
            print("Debe ingresar un número válido.")
            input("\nPresione Enter para continuar...")


def editar_pasajero(viaje):
    
    if not viaje["pasajeros"]:
        print("\nNo hay pasajeros para editar en este viaje.\n")
        input("\nPresione Enter para continuar...")
        return
        

    while True:
        print("\nPasajeros en este viaje:")
        for persona in viaje["pasajeros"]:
            print(f" - {persona['nombre']} | DNI: {persona['dni']} | Email: {persona['email']} | Asiento: {persona['asiento']}")

        dni = input("\nIngrese el DNI del pasajero a editar (o '0' para volver): ").strip()

        if dni == "0":
            print("Selección de pasajero cancelada.")
            input("\nPresione Enter para continuar...")
            return

        indice = None
        for i, p in enumerate(viaje["pasajeros"]):
            if p["dni"] == dni:
                indice = i
                break 
        
        if indice is None:
            print("\nNo existe un pasajero con ese DNI en este viaje. Intente de nuevo.")
            input("\nPresione Enter para continuar...")
            continue 

        pasajero = viaje["pasajeros"][indice]
        
        while True:
            clear()
            titulo("EDITAR PASAJERO SELECCIONADO")
            print(f"Pasajero: {pasajero['nombre']} | DNI: {pasajero['dni']}\n")
            print(f"Actual: Nombre: {pasajero['nombre']} | Email: {pasajero['email']} | Asiento: {pasajero['asiento']}")
            print("\n1) Editar nombre completo")
            print("2) Editar email")
            print("3) Cambiar asiento")
            print("4) Eliminar pasajero")
            print("5) Volver (seleccionar otro pasajero o salir)\n")

            opcion = input("Seleccione opción: ").strip()

            if opcion == "1":
                nuevo_nombre = input("Nuevo nombre y apellido: ").strip()
                while not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_nombre) or nuevo_nombre == "":
                    print("Nombre no válido. Solo letras y espacios.")
                    nuevo_nombre = input("Nuevo nombre y apellido: ").strip()
                pasajero["nombre"] = nuevo_nombre
                print("Nombre actualizado correctamente.")
                input("\nPresione Enter para continuar...")

            elif opcion == "2":
                nuevo_email = input("Nuevo email: ").strip()
                while not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
                    print("Email no valido. Ejemplo: ejemplo@mail.com")
                    nuevo_email = input("Nuevo email: ").strip()
                pasajero["email"] = nuevo_email
                print("Email actualizado correctamente.")
                input("\nPresione Enter para continuar...")


            elif opcion == "3":
                nuevo_asiento = elegir_asiento_para_edicion(viaje["asientos"], viaje["pasajeros"])
                if nuevo_asiento is not None: 
                    asiento_viejo_str = str(pasajero["asiento"])
                    nuevo_asiento_str = str(nuevo_asiento)
                    
                    if asiento_viejo_str in viaje["ocupados"]:
                        viaje["ocupados"].remove(asiento_viejo_str)
                    
                    if 1 <= int(pasajero["asiento"]) <= 20:
                        viaje["asientos"][int(pasajero["asiento"])-1] = str(pasajero["asiento"])
                        
                    viaje["ocupados"].add(nuevo_asiento_str)
                    viaje["asientos"][nuevo_asiento-1] = "X"
                    pasajero["asiento"] = nuevo_asiento_str
                    print(f"Asiento cambiado correctamente a {nuevo_asiento_str}.")
                
                input("\nPresione Enter para continuar...")

            elif opcion == "4":
                confirm = input(f"¿Confirma eliminar a {pasajero['nombre']} (DNI {pasajero['dni']})? (s/n): ").strip().lower()
                if confirm == "s":
                    asiento_str = str(pasajero["asiento"])
                    if asiento_str in viaje["ocupados"]:
                        viaje["ocupados"].remove(asiento_str)
                    if pasajero["dni"] in viaje["dnis"]:
                        viaje["dnis"].remove(pasajero["dni"])
                    if 1 <= int(pasajero["asiento"]) <= 20:
                        viaje["asientos"][int(pasajero["asiento"])-1] = str(pasajero["asiento"])
                    viaje["pasajeros"].pop(indice)
                    print("Pasajero eliminado correctamente.")
                    input("\nPresione Enter para continuar...")
                    return 
                else:
                    print("Eliminación cancelada.")
                    input("\nPresione Enter para continuar...")
            
            elif opcion == "5":
                break 

            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")
        



def editarViaje():
    """Permite seleccionar un viaje y editar su Origen, Destino o Fecha."""
    clear()
    titulo("EDITAR VIAJE")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente para editar.\n")
        input("\nPresione Enter para continuar...")
        return
    
    while True:
        print("\nSeleccione el número de viaje para editar: ")
        for i, viaje in enumerate(viajes):
            print(f"{i + 1}) Desde: {viaje['origen']} | Hasta: {viaje['destino']} | Fecha: {viaje['fecha']}")

        print(f"\nIngrese '0' para volver (cancelar).")
        
        opcion_ingresada = input("Número de viaje a editar: ").strip()

        if opcion_ingresada == "0":
            print("\nEdición de viaje cancelada.")
            input("\nPresione Enter para continuar...")
            return
        
        try:
            num = int(opcion_ingresada)
            if 1 <= num <= len(viajes):
                viaje = viajes[num - 1]
                
                while True: 
                    clear()
                    titulo("EDITAR VIAJE SELECCIONADO")
                    print(f"Viaje actual: {viaje['origen']} -> {viaje['destino']} ({viaje['fecha']})\n")
                    
                    print("\n1) Editar Origen")
                    print("2) Editar Destino")
                    print("3) Editar Fecha")
                    print("4) Volver (viaje seleccionado)")
                    
                    opcion = input("\nSeleccione opcion: ").strip()
                    
                    if opcion == "1":
                        origenvalido = False
                        while not origenvalido:
                            nuevo_origen = input("\nIngrese el nuevo origen: ").capitalize()
                            if nuevo_origen.strip() == "":
                                print("El origen no puede estar vacío.")
                            elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_origen):
                                print("El origen solo debe contener letras y espacios.")
                            else:
                                viaje["origen"] = nuevo_origen
                                print("Origen actualizado correctamente.")
                                origenvalido = True
                                input("\nPresione Enter para continuar...") 
                        
                    elif opcion == "2":
                        destinovalido = False
                        while not destinovalido:
                            nuevo_destino = input("\nIngrese el nuevo destino: ").capitalize()
                            if nuevo_destino.strip() == "":
                                print("El destino no puede estar vacio.")
                            elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_destino):
                                print("El destino solo debe contener letras y espacios.")
                            else:
                                viaje["destino"] = nuevo_destino
                                print("Destino actualizado correctamente.")
                                destinovalido = True
                                input("\nPresione Enter para continuar...") 
                                
                    elif opcion == "3":
                        fechaValida = False
                        while fechaValida == False:
                            nueva_fecha = input("Ingrese la nueva fecha (dd/mm/aaaa): ")
                            try:
                                fechaConvertida = datetime.strptime(nueva_fecha, "%d/%m/%Y").date()
                                hoy = datetime.now().date()
                                if fechaConvertida < hoy:
                                    print("\nLa fecha ingresada ya pasó. Ingrese una fecha futura.\n")
                                else:
                                    viaje["fecha"] = nueva_fecha
                                    print("Fecha actualizada correctamente.")
                                    fechaValida = True
                                    input("\nPresione Enter para continuar...") 
                            except ValueError:
                                print("\nFormato no válido. Use el formato dd/mm/aaaa.\n")
                                
                    elif opcion == "4":
                        break 
                    
                    else:
                        print("Opción no válida.")
                        input("\nPresione Enter para continuar...")

            else:
                print("Número de viaje no válido.")
                input("\nPresione Enter para continuar...")
                
        except ValueError:
            print("Debe ingresar un número válido.")
            input("\nPresione Enter para continuar...")



if __name__ == "__main__":
    menu()