def ingreso_pasajeros():
    pasajeros = []

    while True:
        print("1. Cargar pasajero")
        print("2. Lista de pasajeros")
        print("3. Salir")

        opcion = input("Elija una opcion: ")

        if opcion == "1":
            cargar_pasajero(pasajeros)
        elif opcion == "2":
            lista_pasajeros(pasajeros)
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida.")



ingreso_pasajeros()