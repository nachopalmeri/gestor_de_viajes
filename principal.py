import re   #la usamos para validar el dni

viajes = []  # lista que gurda todos los viajes


def menu(): # funcion principal que nos lleva a cada parte del proograma.
    opcion = ""
    while opcion != "6":  # se repite hasta que el usuario elija salir (opcion 6)
        print("Bienvenido a nuestro gestor de viajes")
        print("1 Iniciar nuevo viaje")
        print("2 Consultar tus viajes")
        print("3 Eliminar viaje")
        print("4 Filtrar viaje por origen")
        print("5 Cargar pasajeros en viaje existente")
        print("6 Salir")
        opcion = input("Opción: ")

        # segun la opcion elegida llama a la funcion correspondiente
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
            print("Error, opción inválida")  # si no eligio una opcion valida muestra este mensaje


def anotarNuevoViaje(): # cuando queremos iniciar un nuevo viaje llamamos a esta funcion.
    print("Nuevo viaje? Ingreselo aca : ")
    origen = input("Ingrese el origen : ")   # pide origen
    destino = input("Ingrese el destino : ") # pide destino
    fecha = input("Ingrese la fecha : ")     # pide fecha

    asientos = list(range(1, 21))  # crea lista de asientos del 1 al 20
    # se guarda todo en un diccionario con los datos del viaje
    viaje = {"origen": origen, "destino": destino, "fecha": fecha, "asientos": asientos, "pasajeros": []}
    viajes.append(viaje)  # agrega el viaje a la lista general

    print("Ahora puede reservar asientos para este viaje:")
    reservar_asiento(viaje["asientos"], viaje["pasajeros"])  
    print("Su viaje fue creado , Muchas gracias.")
    input("Presione Enter para volver al menu.")


def mostrarViajeExistente(): # te muestra los viajes cargados y en caso que no haya te dice que no hay viajes cargados.
    if len(viajes) == 0:  
        print("No hay Viajes cargados actualmente")
    else:
        indice = 1  
        for viaje in viajes:
            # muestra cada viaje con su numero, origen, destino y fecha
            print(indice, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            mostrarPasajeros(viaje)   # muestra los pasajeros del viaje
            print("Asientos:", viaje["asientos"])  # muestra el estado de los asientos
            indice += 1
    input("Presione Enter para volver al menu.")


def eliminarViaje():  # elimina un viaje de la lista
    if len(viajes) == 0:
        print("No hay viajes cargados actualmente")
    else:
        mostrarViajeExistente()  # primero muestra los viajes existentes
        numeroAEliminar = int(input("Que numero de viaje desea eliminar?: "))  # pide el numero de viaje que quiera eliminar 
        if 1 <= numeroAEliminar <= len(viajes):
            eliminar = viajes.pop(numeroAEliminar - 1)  # elimina el viaje de la lista
            print("Se eliminó el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "la fecha", eliminar["fecha"])
        else:
            print("El viaje ingresado no es valido")
    input("Presione Enter para volver al menu.")


def filtrarPorOrigen():  # busca viajes por origen
    if len(viajes) == 0:
        print("No hay ningún viaje cargado")
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


def cargarPasajerosEnViaje():  # permite cargar pasajeros a un viaje ya creado
    if len(viajes) == 0:
        print("No hay viajes cargados actualmente")
    else:
        print("Seleccione el numero de viaje para cargar pasajeros:")
        for i, viaje in enumerate(viajes):  # muestra lista de viajes con numeros
            print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
        num = int(input("Numero de viaje: "))
        if 1 <= num <= len(viajes):
            viaje = viajes[num - 1]  # selecciona el viaje elegido
            print("Cargando pasajeros en el viaje desde", viaje["origen"], "hasta", viaje["destino"])
            reservar_asiento(viaje["asientos"], viaje["pasajeros"])  # llama a la función de reservar asiento
        else:
            print("Numero no valido.")
    input("Presione Enter para volver al menu.")


def reservar_asiento(asientos_disponibles, lista_pasajeros):  # proceso de reservar un asiento
    salir = False
    while salir == False:
        print("Asientos disponibles:")
        print(asientos_disponibles)  # muestra asientos libres y los ocupados con ("X")

        elegir_asiento = input("¿Que asiento desea elegir? ('salir' para terminar): ").lower()

        if elegir_asiento == "salir":  # si el usuario escribe salir, corta el bucle
            salir = True
        else:
            if not elegir_asiento.isdigit():  # valida que sea un número
                print("Ingrese un numero de asiento valido.")
                continue

            asiento = int(elegir_asiento)  # convierte a número

            if asiento not in asientos_disponibles:  # si no está disponible
                print("Ese asiento esta ocupado o no existe.")
            else:
                cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento)  # carga pasajero


def cargar_pasajero(lista_pasajeros, asientos_disponibles, asiento):  # agrega un pasajero nuevo
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

    # crea el diccionario del pasajero
    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)  # agrego pasajero a la lista
    print("Pasajero agregado correctamente.")

    # marcar asiento como ocupado
    for i in range(len(asientos_disponibles)):
        if asientos_disponibles[i] == asiento:  # busca el asiento elegido
            asientos_disponibles[i] = "X"      # lo marca como ocupado
            print("Asiento reservado:", asiento)


def mostrarPasajeros(viaje):  # muestra la lista de pasajeros de un viaje
    if viaje["pasajeros"]:  # si hay pasajeros
        print("   Pasajeros:")
        for pasajero in viaje["pasajeros"]:
            print("    -", pasajero["nombre"], "-", pasajero["dni"], "- asiento", pasajero["asiento"])
    else:
        print("   Pasajeros: No hay pasajeros cargados.")  # si no hay pasajeros


menu()  # se llama al menú principal para iniciar el programa