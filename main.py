viajes=[]
def anotarNuevoViaje (): #Esta funcion se usa cuando el usuario inicia un viaje por primera vez en el programa
    print("Nuevo viaje? Ingreselo aca: ")
    origen= input("Ingrese el origen: ")
    destino= input("Ingrese el destino: ")
    fecha=input( "Ingrese la fecha: ")
    viaje= [origen,destino, fecha, []]  # agrego lista de pasajeros vacia
    viajes.append(viaje)
    print("Su viaje fue creado")

def menu (): #es el menu principal, que nos terminara llevando a cada parte del programa
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

def eliminarViaje(): #funcion para poder eliminar un viaje cargado anteriormente
    if len (viajes)==0:
        print("No hay viajes cargados actualmente")
    else:
        mostrarViajeExistente()
        numeroAEliminar=int(input("Que numero de viaje desea eliminar?: "))
        if 1<=numeroAEliminar<=len (viajes):
            eliminar=viajes.pop (numeroAEliminar-1)
            print("Se elimino el viaje que iba desde", eliminar[0], "hasta", eliminar[1], "La fecha", eliminar[2])
        else:
            print("El viaje ingresado no es valido")

def mostrarViajeExistente (): #unicamente imprime los viajes ya cargados, para poder visualizxar lo ya caragado
    if len (viajes) == 0:
        print("No hay Viajes cargados actualmente")
    else:
        print("Tus viajes son: ")
        for i in range(len(viajes)):
            viaje = viajes[i]
            print(i + 1, "desde", viaje[0], "hasta", viaje[1], "fecha", viaje[2])
            if viaje[3]:  # mostrar pasajeros si hay
                print("   Pasajeros:")
                for pasajero in viaje[3]:
                    print("    -", pasajero)
            else:
                print("   Pasajeros: ninguno")

def filtrarPorOrigen(): #funcion para filtrar con lambda y filter en la lista de viajes existentes por origen
    if len(viajes) == 0:
        print("No hay ningun viaje cargado")
    else:
        origen_buscado = input("Ingrese el origen a buscar: ")
        viajes_filtrados = list(filter(lambda viaje: viaje[0] == origen_buscado, viajes))

        if len(viajes_filtrados) == 0:
            print("No hay viajes desde", origen_buscado)
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print("desde", viaje[0], "hasta", viaje[1], "fecha", viaje[2])
                if viaje[3]:
                    print("   Pasajeros:")
                    for pasajero in viaje[3]:
                        print("    -", pasajero)
                else:
                    print("   Pasajeros: ninguno")