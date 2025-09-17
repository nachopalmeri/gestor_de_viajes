def reservar_asiento():

    asientos_disponibles = list(range(1,101))
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
                #if asiento in asientos_disponibles:

                reserva.append(asiento)
                for i in range(len(asientos_disponibles)):
                    if asientos_disponibles[i] == asiento:
                        asientos_disponibles[i] = 'X'
                

               
    return reserva , asientos_disponibles

mis_reservas, asientos_libres = reservar_asiento()



print("Su reserva es:", mis_reservas)
print("Asientos disponibles:",asientos_libres)