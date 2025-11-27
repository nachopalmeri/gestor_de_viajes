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
    Pide una opcion valida del menu (1 al 8).
    Devuelve la opcion si es valida, o None si hay error.
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
    """Inicia un nuevo viaje.
    Pide origen, destino y fecha. Crea la lista de asientos del 1 al 20.
    Guarda los datos en un diccionario y lo agrega a la lista general de viajes.
    Luego permite reservar asientos.
    """
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


def mostrarViajeExistente(pausar=True):
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
    if pausar:
        input("\nPresione Enter para volver al menú...")


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
        mostrarViajeExistente(pausar=False)  
        try:
            numeroAEliminar = int(input("\nQue numero de viaje desea eliminar?: "))  
            if 1 <= numeroAEliminar <= len(viajes):
                eliminar = viajes.pop(numeroAEliminar - 1) 
                print("\nSe eliminó el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "la fecha", eliminar["fecha"])
            else:
                print("\nEl viaje ingresado no es valido.\n")
        except ValueError:
            print("\nDebe ingresar un número válido.\n")

    input("\nPresione Enter para volver al menú...")

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
    """Carga pasajeros en un viaje ya existente.
    Muestra los viajes disponibles, pide el número del viaje
    y permite reservar asientos en el viaje seleccionado.
    """
    clear()
    titulo("CARGAR PASAJEROS")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
        input("\nPresione Enter para volver al menú...")

    else:
        print("\nSeleccione el número de viaje para cargar pasajeros:")
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
        reservar_asiento(viaje["asientos"], viaje["pasajeros"])  

def reservar_asiento(asientos_disponibles, lista_pasajeros):
    """Gestiona la reserva de asientos.
    Muestra los asientos disponibles, permite elegir uno y valida
    que el asiento sea correcto. También permite escribir 'salir' para terminar.
    """
    salir = False
    while salir == False:
        print("\nAsientos disponibles:\n")
        
        for i in range (0, len(asientos_disponibles), 2):
            if i + 1 < len(asientos_disponibles):
                print(f"|  {asientos_disponibles[i]:<3} {asientos_disponibles[i+1]:<3} |")
            else:
                print(f"|  {asientos_disponibles[i]:<3} |")
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
                cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento)  
                print("\nAsiento reservado correctamente.\n")


def elegir_asiento_para_edicion(asientos_disponibles, lista_pasajeros):
    """Permite elegir un asiento al editar un pasajero.
       Muestra los asientos disponibles y valida que no esté ocupado."""
    
    print("\nAsientos disponibles:\n")
    
    for i in range(0, len(asientos_disponibles), 2):
        if i + 1 < len(asientos_disponibles):
            print(f"{asientos_disponibles[i]:<3} {asientos_disponibles[i+1]:<3}")
        else:
            print(f"{asientos_disponibles[i]}")

    elegir = input("\nNuevo asiento ('salir' para cancelar): ").lower()

    if elegir == "salir":
        print("Cambio de asiento cancelado.")
        return None

    if not elegir.isdigit():
        print("Debe ingresar un número válido.")
        return None

    nuevo_asiento = int(elegir)

    if not (1 <= nuevo_asiento <= len(asientos_disponibles)):
        print("Ese asiento no existe.")
        return None

    if asientos_disponibles[nuevo_asiento - 1] == "X":
        print("Ese asiento está ocupado.")
        return None

    return nuevo_asiento



def cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento):
    """Carga un nuevo pasajero en la lista.
    Pide nombre, DNI y email. Valida los datos con expresiones regulares
    y previene DNIs duplicados dentro del mismo viaje.
    """
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

    """ Evitar duplicado de DNI en el mismo viaje """
    for p in lista_pasajeros:
        if p["dni"] == dni:
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
    print("\nPasajero agregado correctamente.\n")

    """ Marcar el asiento como ocupado """
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


def mostrar_asientos(matriz_asientos, pasajeros):
    print("\n----- ASIENTOS -----")

    ocupados = []
    for dni in pasajeros:
        ocupados.append(pasajeros[dni]["asiento"])

    for fila in matriz_asientos:
        linea = ""
        for asiento in fila:

            if asiento in ocupados:
                linea += "[XX] "
            else:
                linea += "[" + asiento + "] "

        print(linea)   

    print("\n(XX = ocupado)\n")



def elegir_asiento(matriz_asientos, pasajeros):
    mostrar_asientos(matriz_asientos, pasajeros)

    ocupados = []
    for dni in pasajeros:
        ocupados.append(pasajeros[dni]["asiento"])

    asiento = input("\nIngrese el asiento que quiere asignar: ").upper()

    existe = False
    for fila in matriz_asientos:
        for a in fila:
            if asiento == a:
                existe = True

    if not existe:
        print(" Ese asiento no existe.")
        return None

    if asiento in ocupados:
        print(" Ese asiento esta ocupado.")
        return None

    return asiento


def editarPasajeroEnViaje():
    clear()
    titulo("EDITAR PASAJERO")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente.\n")
        return
    
    print("\nSeleccione el numero de viaje donde desea editar un pasajero:")
    for i, viaje in enumerate(viajes):
        print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])

    try:
        num = int(input("Número de viaje: "))
        if 1 <= num <= len(viajes):
            viaje = viajes[num - 1]
            editar_pasajero(viaje)   
        else:
            print("Numero no valido")
    except ValueError:
        print("Debe ingresar un numero valido.")




def editar_pasajero(viaje):
    """
    Edita un pasajero dentro del viaje
    Recibe el diccionario del viaje y modifica el pasajero en esa lista.
    """
    if not viaje["pasajeros"]:
        print("\nNo hay pasajeros para editar en este viaje.\n")
        input("\nPresione ENTER para continuar...")
       
        return

    print("\nPasajeros en este viaje:")
    for p in viaje["pasajeros"]:
        print(f" - {p['nombre']} | DNI: {p['dni']} | Email: {p['email']} | Asiento: {p['asiento']}")

    dni = input("\nIngrese el DNI del pasajero a editar: ").strip()
    indice = None
    for i, p in enumerate(viaje["pasajeros"]):
        if p["dni"] == dni:
            indice = i
            break

    if indice is None:
        print("\nNo existe un pasajero con ese DNI en este viaje.\n")
        input("\nPresione ENTER para continuar...")

        return

    pasajero = viaje["pasajeros"][indice]
    print("\n--- Editando pasajero ---")
    print(f"Actual: Nombre: {pasajero['nombre']} | Email: {pasajero['email']} | Asiento: {pasajero['asiento']}")
    print("1. Editar nombre completo")
    print("2. Editar email")
    print("3. Cambiar asiento")
    print("4. Eliminar pasajero")
    print("5. Volver (cancelar)")

    opcion = input("Seleccione opción: ").strip()

    if opcion == "1":
        nuevo_nombre = input("Nuevo nombre y apellido: ").strip()
        while not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_nombre) or nuevo_nombre == "":
            print("Nombre inválido. Solo letras y espacios.")
            nuevo_nombre = input("Nuevo nombre y apellido: ").strip()
        pasajero["nombre"] = nuevo_nombre
        print("Nombre actualizado correctamente.")
        input("\nPresione ENTER para continuar...")


    elif opcion == "2":
        nuevo_email = input("Nuevo email: ").strip()
        while not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
            print("Email no valido. Ejemplo: ejemplo@mail.com")
            nuevo_email = input("Nuevo email: ").strip()
        pasajero["email"] = nuevo_email
        print("Email actualizado correctamente.")
        input("\nPresione ENTER para continuar...")


    elif opcion == "3":
        nuevo_asiento = elegir_asiento_para_edicion(viaje["asientos"], viaje["pasajeros"])
        if nuevo_asiento is None:
            return  

        try:
            antiguo = int(pasajero["asiento"])
            if 1 <= antiguo <= len(viaje["asientos"]):
                viaje["asientos"][antiguo - 1] = antiguo
        except Exception:
            pass

        viaje["asientos"][nuevo_asiento - 1] = "X"

        pasajero["asiento"] = nuevo_asiento
        print(f"Asiento cambiado correctamente a {nuevo_asiento}.")
        input("\nPresione ENTER para continuar...")

    elif opcion == "4":
        confirm = input(f"¿Confirma eliminar a {pasajero['nombre']} (DNI {pasajero['dni']})? (s/n): ").strip().lower()
        if confirm == "s":
            try:
                asiento_elim = int(pasajero["asiento"])
                if 1 <= asiento_elim <= len(viaje["asientos"]):
                    viaje["asientos"][asiento_elim - 1] = asiento_elim
            except Exception:
                pass
            viaje["pasajeros"].pop(indice)
            print("Pasajero eliminado correctamente.")
            input("\nPresione ENTER para continuar...")

        else:
            print("Eliminación cancelada.")
            input("\nPresione ENTER para continuar...")


    elif opcion == "5":
        print("Saliendo de la seccion de editar pasajeros.")
        input("\nPresione ENTER para continuar...")

        return

    else:
        print("Opcion no valida.")
        return




def editarViaje():
    """Permite seleccionar un viaje y editar su Origen, Destino o Fecha."""
    clear()
    titulo("EDITAR VIAJE")

    if len(viajes) == 0:
        print("\nNo hay viajes cargados actualmente para editar.\n")
        input("\nPresione ENTER para continuar...")
        return
    
    print("\nSeleccione el número de viaje para editar:")
    for i, viaje in enumerate(viajes):
        print(f"{i + 1}) Desde: {viaje['origen']} | Hasta: {viaje['destino']} | Fecha: {viaje['fecha']}")

    try:
        num = int(input("Número de viaje a editar: "))
        if 1 <= num <= len(viajes):
            viaje = viajes[num - 1]
            
            clear()
            titulo("EDITAR VIAJE SELECCIONADO")
            print(f"Viaje actual: {viaje['origen']} -> {viaje['destino']} ({viaje['fecha']})\n")
            
            print("1. Editar Origen")
            print("2. Editar Destino")
            print("3. Editar Fecha")
            print("4. Volver (cancelar)")
            
            opcion = input("Seleccione opción: ").strip()
            
            if opcion == "1":
                origenvalido = False
                while not origenvalido:
                    nuevo_origen = input("\nIngrese el nuevo origen: ")
                    if nuevo_origen.strip() == "":
                        print("El origen no puede estar vacío.")
                    elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_origen):
                        print("El origen solo debe contener letras y espacios.")
                    else:
                        viaje["origen"] = nuevo_origen
                        print("Origen actualizado correctamente.")
                        origenvalido = True
                        
            elif opcion == "2":
                # La lógica de validación de destino se toma de anotarNuevoViaje
                destinovalido = False
                while not destinovalido:
                    nuevo_destino = input("\nIngrese el nuevo destino: ")
                    if nuevo_destino.strip() == "":
                        print("El destino no puede estar vacio.")
                    elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nuevo_destino):
                        print("El destino solo debe contener letras y espacios.")
                    else:
                        viaje["destino"] = nuevo_destino
                        print("Destino actualizado correctamente.")
                        destinovalido = True
                        
            elif opcion == "3":
                fechaValida = False
                while fechaValida == False:
                    nueva_fecha = input("Ingrese la nueva fecha (dd/mm/aaaa): ")
                    try:
                        fechaConvertida = datetime.strptime(nueva_fecha, "%d/%m/%Y").date()
                        hoy = datetime.now().date()
                        if fechaConvertida < hoy:
                            print("\nLa fecha ingresada ya paso. Ingrese una fecha futura.\n")
                        else:
                            viaje["fecha"] = nueva_fecha
                            print("Fecha actualizada correctamente.")
                            fechaValida = True
                    except ValueError:
                        print("\nFormato no valido. Use el formato dd/mm/aaaa.\n")
                        
            elif opcion == "4":
                print("\nEdicion de viaje cancelada.")
            
            else:
                print("Opcion no valida.")

        else:
            print("Número de viaje no valido.")
            
    except ValueError:
        print("Debe ingresar un numero valido.")
        
    input("\nPresione ENTER para continuar...")


if __name__ == "__main__": #“Solo ejecutar menu() si este archivo se ejecuta directamente, no si se importa”.
    menu()
