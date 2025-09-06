viajes=[]
def anotarNuevoViaje (): #Esta funcion se usa cuando el usuario inicia un viaje por primera vez en el programa
    print("Nuevo viaje? Ingreselo aca: ")
    origen= input("Ingrese el origen: ")
    destino= input("Ingrese el destino: ")
    fecha=input( "Ingrese la fecha: ")
    viaje= [origen,destino, fecha]
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
            print("Falta esta funcioon")
        elif opcion == "4":
            filtrarPorOrigen()
        elif opcion == "5":
            print("Salir")
        else:
            print("Error, opcion invalida")



def mostrarViajeExistente (): #unicamente imprime los viajes ya cargados, para poder visualizxar lo ya caragado
    if len (viajes) == 0:
        print("No hay iajes cargados actualmente")
    else:
        print("Tus viajes son: ")
        for i in range(len(viajes)):
            viaje = viajes[i]
            print(i + 1, "desde", viaje[0], "hasta", viaje[1], "fecha", viaje[2])

def filtrarPorOrigen():  #esta funcion la usamos si el usuario desea filtrar los viajes existentes y encontrar por origen
    if len(viajes) == 0:
        print("No hay ningún viaje cargado")
    else:
        origen_buscado = input("Ingrese el origen a buscar: ")
        viajes_filtrados = list(filter(lambda viaje: viaje.origen == origen_buscado, viajes))

        if len(viajes_filtrados) == 0:
            print("No hay viajes desde", origen_buscado)
        else:
            print("Viajes encontrados:")
            for viaje in viajes_filtrados:
                print(viaje)
