import re
viajes=[]

def matriz_asientos(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append("L")  
        matriz.append(fila)
    return matriz

def mostrar_matriz(matriz):
    print("Mapa de asientos (L = libre, X = ocupado):")
    for i, fila in enumerate(matriz):
        fila_str = ""
        for j, asiento in enumerate(fila):
            fila_str += f"{i}{j}:{asiento}  "
        print(fila_str)
    print()

def anotarNuevoViaje (): #Esta funcion se usa cuando el usuario inicia un viaje por primera vez en el programa
    print("Nuevo viaje? Ingreselo aca: ")
    origen= input("Ingrese el origen: ")
    destino= input("Ingrese el destino: ")
    fecha=input( "Ingrese la fecha: ")
    asientos = matriz_asientos(4, 5)  # agrego la matriz de asientos
    viaje= {"origen": origen, "destino": destino, "fecha": fecha, "asientos": asientos, "pasajeros": []}  
    viajes.append(viaje)
    print("Su viaje fue creado")
    input("Presione Enter para volver al menu...")

def mostrarPasajeros(viaje):
    if viaje["pasajeros"]:
        print("   Pasajeros:")
        for pasajero in viaje["pasajeros"]:
            print("    -", pasajero["nombre"], "-", pasajero["dni"], "- asiento", pasajero["asiento"])
    else:
        print("   Pasajeros: ninguno")

def mostrarViajeExistente ():
    if len(viajes) == 0:
        print("No hay Viajes cargados actualmente")
    else:
        print("Tus viajes son: ")
        for i, viaje in enumerate(viajes):
            print(i + 1, "desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
            mostrarPasajeros(viaje)
            mostrar_matriz(viaje["asientos"])
    input("Presione Enter para volver al menu...")

def eliminarViaje():
    if len (viajes)==0:
        print("No hay viajes cargados actualmente")
    else:
        mostrarViajeExistente()
        numeroAEliminar=int(input("Que numero de viaje desea eliminar?: "))
        if 1<=numeroAEliminar<=len (viajes):
            eliminar=viajes.pop (numeroAEliminar-1)
            print("Se elimino el viaje que iba desde", eliminar["origen"], "hasta", eliminar["destino"], "La fecha", eliminar["fecha"])
        else:
            print("El viaje ingresado no es valido")
    input("Presione Enter para volver al menu...")

def filtrarPorOrigen():
    if len(viajes) == 0:
        print("No hay ningun viaje cargado")
    else:
        origen_buscado = input("Ingrese el origen a buscar: ")
        viajes_filtrados = list(filter(lambda viaje: viaje["origen"] == origen_buscado, viajes))
        if len(viajes_filtrados) == 0:
            print("No hay viajes desde", origen_buscado)
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print("desde", viaje["origen"], "hasta", viaje["destino"], "fecha", viaje["fecha"])
                mostrarPasajeros(viaje)
                mostrar_matriz(viaje["asientos"])
    input("Presione Enter para volver al menu...")

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

    pasajero = {"nombre": nombre, "dni": dni, "asiento": asiento}
    lista_pasajeros.append(pasajero)
    print("Pasajero agregado correctamente.")

def lista_pasajeros(lista_pasajeros):
    if len(lista_pasajeros) == 0:
        print("No hay pasajeros cargados.")
    else:
        print("--- Lista de Pasajeros ---")
        for i, pasajero in enumerate(lista_pasajeros):
            print("Pasajero", i + 1)
            print("Nombre:", pasajero["nombre"])
            print("Dni:", pasajero["dni"])
            print("Asiento:", pasajero["asiento"])
            print("----------------------")

def menu ():
    opcion= ""
    while opcion != "5":
        print ("Bienvenido a nuestro gestor de viajes")
        print ("1 Iniciar nuevo viaje")
        print ("2 Consulta tus viajes")
        print ("3 Elimar viaje")
        print ("4 Filtrar viaje por origen")
        print ("5 Salir del menu")
        opcion= input ("Opcion: ")

        if opcion == "1":
            anotarNuevoViaje()
        elif opcion=="2":
            mostrarViajeExistente()
        elif opcion== "3":
            eliminarViaje()
        elif opcion == "4":
            filtrarPorOrigen()
        elif opcion == "5":
            print("Salir")
        else:
            print("Error, opcion invalida")

menu()

def reservar_asiento():

    asientos_disponibles = list(range(1,101)) #lista con los asientos disponibles (100 es un ejemplo)
    reserva = []
    salir = False

    while salir == False:
        print("Asientos disponibles:")
        print(asientos_disponibles) # se muestra la lista

        elegir_asiento = input("¿Qué asiento desea elegir? ('salir' para terminar): ") #El pasajero elige el asiento

        if elegir_asiento == "salir": #si escribe 'salir' sale
            salir = True
        
        else:
            asiento = int(elegir_asiento)

            if asiento not in asientos_disponibles:
                print("Ese asiento esta ocupado o no existe.")
            
            else:
                reserva.append(asiento) #Agrega el asiento que elegiste en tu reserva
                for i in range(len(asientos_disponibles)):
                    if asientos_disponibles[i] == asiento: #Aca recorre la lista e intercambia el asiento elegido por una X
                        asientos_disponibles[i] = 'X'
                
    return reserva , asientos_disponibles

mis_reservas, asientos_libres = reservar_asiento()

print("Su reserva es:", mis_reservas)
print("Asientos disponibles:",asientos_libres)