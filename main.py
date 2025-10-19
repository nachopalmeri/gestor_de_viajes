import re   # la usamos para validar el dni

viajes = []  


def menu():
    """Función principal que muestra el menú del programa.
    Permite elegir entre iniciar un nuevo viaje, consultar, eliminar, filtrar,
    cargar pasajeros o salir. Repite el menú hasta que el usuario elija salir (opción 6).
    """
    opcion = ""
    while opcion != "6":  # se repite hasta que el usuario elija salir (opcion 6)
        print("Bienvenido a nuestro gestor de viajes.")
        print("1 Iniciar nuevo viaje.")
        print("2 Consultar tus viajes.")
        print("3 Eliminar viaje.")
        print("4 Filtrar viaje por origen.")
        print("5 Cargar pasajeros en viaje existente.")
        print("6 Salir.")
        opcion = input("Opción: ")

       
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
            print("Salir")  # sale del programa
        else:
            print("Error, opción inválida.") 


def anotarNuevoViaje():
    """Inicia un nuevo viaje.
    Pide origen, destino y fecha. Crea la lista de asientos del 1 al 20.
    Guarda los datos en un diccionario y lo agrega a la lista general de viajes.
    Luego permite reservar asientos.
    """
    print("Nuevo viaje? Ingreselo aca: ")
    origen = input("Ingrese el origen: ")   
    destino = input("Ingrese el destino: ") 
    fecha = input("Ingrese la fecha: ")     
    
    asientos = list(range(1, 21))  # crea lista de asientos del 1 al 20
    viaje = {"origen": origen, "destino": destino, "fecha": fecha, "asientos": asientos, "pasajeros": []}
    viajes.append(viaje) 

    print("Ahora puede reservar asientos para este viaje:")
    reservar_asiento(viaje["asientos"], viaje["pasajeros"])  
    print("Su viaje fue creado. Muchas gracias.")
    input("Presione Enter para volver al menú.")


def mostrarViajeExistente():
    """Muestra los viajes cargados.
    Si no hay viajes cargados informa al usuario. 
    Si hay, muestra cada viaje con su número, origen, destino, fecha,
    pasajeros y asientos disponibles.
    """
    if len(viajes) == 0:  
        print("No hay Viajes cargados actualmente.")
    else:
        indice = 1  
        for viaje in viajes:
            # muestra cada viaje con su número, origen, destino y fecha
            print(indice, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            mostrarPasajeros(viaje)  
            print("Asientos:", viaje["asientos"])  
            indice += 1
    input("Presione Enter para volver al menú.")


def eliminarViaje():
    """Elimina un viaje de la lista.
    Muestra los viajes existentes, pide el número del viaje a eliminar
    y lo elimina si es válido.
    """
    if len(viajes) == 0:
        print("No hay viajes cargados actualmente.")
    else:
        mostrarViajeExistente()  
        numeroAEliminar = int(input("Que numero de viaje desea eliminar?: "))  
        if 1 <= numeroAEliminar <= len(viajes):
            eliminar = viajes.pop(numeroAEliminar - 1) 
            print("Se eliminó el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "la fecha", eliminar["fecha"])
        else:
            print("El viaje ingresado no es valido.")
    input("Presione Enter para volver al menú.")


def filtrarPorOrigen():
    """Filtra viajes por origen.
    Pide el origen a buscar y muestra los viajes que coinciden.
    Si no hay coincidencias, informa al usuario.
    """
    if len(viajes) == 0:
        print("No hay ningún viaje cargado.")
    else:
        origen_buscado = input("Ingrese el origen a buscar: ")  # pide el origen que quiera buscar
        viajes_filtrados = list(filter(lambda viaje: viaje["origen"] == origen_buscado, viajes))  # filtra viajes
        if len(viajes_filtrados) == 0:
            print("No hay viajes desde", origen_buscado)
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print("desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
                mostrarPasajeros(viaje)
                print("Asientos:", viaje["asientos"])
    input("Presione Enter para volver al menu.")


def cargarPasajerosEnViaje():
    """Carga pasajeros en un viaje ya existente.
    Muestra los viajes disponibles, pide el número del viaje
    y permite reservar asientos en el viaje seleccionado.
    """
    if len(viajes) == 0:
        print("No hay viajes cargados actualmente.")
    else:
        print("Seleccione el número de viaje para cargar pasajeros:")
        i = 0
        for viaje in viajes:  
            print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"]) #muestra el numero del viaje  y los datos (origen,destino y fecha)
            i += 1
        num = int(input("Numero de viaje: "))
        if 1 <= num <= len(viajes):
            viaje = viajes[num - 1] 
            print("Cargando pasajeros en el viaje desde", viaje["origen"], "hasta", viaje["destino"])
            reservar_asiento(viaje["asientos"], viaje["pasajeros"])  
        else:
            print("Numero no válido.")
    input("Presione Enter para volver al menú.")


def reservar_asiento(asientos_disponibles, lista_pasajeros):
    """Gestiona la reserva de asientos.
    Muestra los asientos disponibles, permite elegir uno y valida
    que el asiento sea correcto. También permite escribir 'salir' para terminar.
    """
    salir = False
    while salir == False:
        print("Asientos disponibles:")
        print(asientos_disponibles)  # muestra asientos libres y los ocupados con ("X")

        elegir_asiento = input("¿Que asiento desea elegir? ('salir' para terminar): ").lower()

        if elegir_asiento == "salir": 
            salir = True
        else:
            if not elegir_asiento.isdigit(): 
                print("Ingrese un numero de asiento valido.")
                continue

            asiento = int(elegir_asiento)  

            if asiento not in asientos_disponibles: 
                print("Ese asiento esta ocupado o no existe.")
            else:
                cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento)  # carga pasajero


def cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento):
    """Carga un nuevo pasajero en la lista.
    Pide nombre y DNI, valida el formato del DNI, evita duplicados
    y marca el asiento elegido como ocupado.
    """
    nombre = input("Nombre del pasajero: ")  
    dni = input("DNI del pasajero: ")       

    # revisa que el dni tenga 7 o 8 digitos y que lo escriba bien
    while not re.search("^[0-9]{7,8}$", dni):
        print("DNI no valido. Ingrese solo numeros.")
        dni = input("DNI del pasajero: ")

    # revisa si el DNI ya esta registrado en la lista de pasajeros
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

    for i in range(len(asientos_disponibles)):
        if asientos_disponibles[i] == asiento:  
            asientos_disponibles[i] = "X"     
            print("Asiento reservado:", asiento)


def mostrarPasajeros(viaje):
    """Muestra la lista de pasajeros de un viaje.
    Si hay pasajeros, los lista con nombre, DNI y asiento.
    Si no hay, informa que no existen pasajeros cargados.
    """
    if viaje["pasajeros"]:  # si hay pasajeros
        print("   Pasajeros:")
        for pasajero in viaje["pasajeros"]:
            print("    -", pasajero["nombre"], "-", pasajero["dni"], "- asiento", pasajero["asiento"])
    else:
        print("   Pasajeros: No hay pasajeros cargados.")  # si no hay pasajeros


menu()  # se llama al menú principal para iniciar el programa
