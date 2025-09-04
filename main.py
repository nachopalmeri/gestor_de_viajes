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
    print ("Bienvenido a nuestro gestor de viajes")
    print ("1 Iniciar nuevo viaje")
    print ("2 Consulta tus viajes")
    print ("3 Elimar vviaje")
    print ("4 Salir del menu")
    opcion= input ("Opcion: ")
    
    if opcion == "1":
        anotarNuevoViaje()


def mostrarViajeExistente (): #unicamente imprime los viajes ya cargados, para poder visualizxar lo ya caragado