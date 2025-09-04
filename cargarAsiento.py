def reservar_asiento():

    asientos_disponibles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                            31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                            41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                            51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                            61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                            71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                            81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                            91, 92, 93, 94, 95, 96, 97, 98, 99, 100
                                                                    ]
                           
    reserva = []
    salir = False

    while salir == False:
        print("Asientos disponibles:")
        print(asientos_disponibles)

        elegir_asiento = input("¿Qué asiento desea elegir? ('salir' para terminar): ")

        if elegir_asiento == "salir":
            salir = True
        
        else:
            asiento = int(elegir_asiento)

            if asiento not in asientos_disponibles:
                print("Ese asiento esta ocupado o no existe.")
            
            else:
                reserva.append(asiento)
                asientos_disponibles.remove(asiento)

               
    return reserva , asientos_disponibles

mis_reservas, asientos_libres = reservar_asiento()



print("Su reserva es:", mis_reservas)
print("Asientos disponibles:",asientos_libres)