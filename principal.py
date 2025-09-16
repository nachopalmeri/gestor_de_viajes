import re
viajes = []  # Aca guardamos todos los datos del viaje : ("origen":, "destino":, "fecha":, "asientos":, "pasajeros":)

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

def cargar_viaje():
    print("=== Nuevo Viaje ===")
    origen = input("Ingrese el origen: ")
    destino = input("Ingrese el destino: ")
    fecha = input("Ingrese la fecha (dd/mm/aaaa): ")
    asientos = matriz_asientos(4, 5) 
    viaje = {
        "origen": origen,
        "destino": destino,
        "fecha": fecha,
        "asientos": asientos,
        "pasajeros": []
    }
    viajes.append(viaje)
    print("Viaje cargado con exio.")

def listar_viajes():
    if len(viajes) == 0:
        print("No hay viajes cargados.")
    else:
        print("=== Lista de viajes ===")
        for i, viaje in enumerate(viajes):
            print(f"{i+1}. Origen: {viaje['origen']} | Destino: {viaje['destino']} | Fecha: {viaje['fecha']}")
        print()

def buscar_viajes():
    criterio = input("Ingrese destino o fecha a buscar: ")
    encontrados = []
    for i, viaje in enumerate(viajes):
        if viaje["destino"] == criterio or viaje["fecha"] == criterio:
            encontrados.append((i, viaje))
    if len(encontrados) == 0:
        print(" No se encontraron viajes.\n")
    else:
        print("=== Viajes encontrados ===")
        for idx, viaje in encontrados:
            print(f"{idx+1}. Origen: {viaje['origen']} | Destino: {viaje['destino']} | Fecha: {viaje['fecha']}")
            mostrar_matriz(viaje["asientos"])

def cargar_pasajero(lista_pasajeros): # cargamos el pasajero 

    nombre = input("Nombre del pasajero: ") # pedimos el nombre del pasajero
    dni = input("DNI del pasajero: ") # pedimos el dni del pasajero

    while not re.search("^[0-9]{7,8}$", dni): # aca verificamos que el dni que ingrese sea valido , es decir que sean solo numeros y mas de 7 digitos
        print("DNI no valido. Ingrese solo numeros.")
        dni = input("DNI del pasajero: ")

    asiento = input("Numero de asiento: ") # el numero de asiento del pasajero 

    for i in lista_pasajeros:  # en este for recorremos la lista de pasajeros y verificamos que no haya otra persona registtrada con el mismo dni 
        if i["dni"] == dni:
            print("Ese DNI ya esta registrado.")
            return

    pasajero = {
        "nombre": nombre,
        "dni": dni,
        "asiento": asiento
    }

    lista_pasajeros.append(pasajero)
    print("Pasajero agregado correctamente.")# agregamos el pasajero 

def lista_pasajeros(lista_pasajeros): # aca tenemos la lista de todos los pasajeros cargados
    if len(lista_pasajeros) == 0: 
        print("No hay pasajeros cargados.") # en caso que no haya pasasjeros cargados mostramos este mensaje
    else: 
        print("--- Lista de Pasajeros ---") 
        for i in range(len(lista_pasajeros)): 
            pasajero = lista_pasajeros[i] 
            print("Pasajero", i + 1) # nimero del pasajero 
            print("Nombre:", pasajero["nombre"]) # nombre de ese pasajero
            print("Dni:", pasajero["dni"]) # dni de ese pasajero 
            print("Asiento:", pasajero["asiento"]) # numero de asiento de ese pasajero
            print("----------------------")
