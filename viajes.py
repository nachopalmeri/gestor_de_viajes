viajes= []

def matriz_asientos (filas, columnas):
    matriz = []
    for i in range (filas):
        fila = []
        for i in range (columnas):
            fila.append ("L") #Libre
        matriz.append (fila)
    return matriz

def mostrar_matriz (matriz):
    for fila in matriz:
        for asiento in fila:
            print (asiento, end= "")

def cargar_viaje ():
    destino = ("Ingrese su destino")
    fecha = ("Ingrese la fecha (dd/mm/aaaa)")
    asientos = matriz_asientos (4, 5)
    viaje = [destino, fecha, asientos]
    viajes.append (viaje)
    print("Su viaje fue cargado con exito.")

def listar_viajes ():
    if len(viajes) == 0:
        print("No hay viajes cargados.")
    else:
        print("Lista de viajes:")
        for i in range(len(viajes)):
            print(i+1, "Destino:", viajes [i][0], "Fecha:", viajes [i][1])
    input("Presione ENTER para volver al menú...")

def buscar_viajes ():
    criterio_busqueda = input("Buscar por destino o por fecha.")
    encontrados = []
    for viaje in viajes:
        if viaje [0] == criterio_busqueda or viaje [1] == criterio_busqueda:
            encontrados.append (viaje)
    
    if len(encontrados) == 0:
        print("No se encontraron viajes.")
    else:
        print("Viajes encontrados:")
        for i in encontrados:
            print("Destino:", i[0], "Fecha:",i[1])
            print("Asientos:")
            mostrar_matriz (i[2])
    input("Presione ENTER para volver al menú...")


opcion= ""
while opcion != "4":
    print("--- Gestor de viajes ---")
    print("1. Cargar viaje")
    print("2. Listar viajes")
    print("3. Buscar viaje(Destino/Fecha)")
    print("4. Salir")
    opcion = input("Elija alguna opcion:")

    if opcion == "1":
        cargar_viaje()
    elif opcion == "2":
        listar_viajes()
    elif opcion == "3":
        buscar_viajes
    elif opcion == "4":
        print("Saliendo.")
    else:
        print("Opcion invalida.")