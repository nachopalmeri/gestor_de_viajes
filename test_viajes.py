from main import guardarViajesArchivo

import json

# Datos base para pruebas
viaje_ejemplo = {
    "origen": "Buenos Aires",
    "destino": "Córdoba",
    "fecha": "15/12/2025",
    "asientos": [1, 2, 3],
    "pasajeros": []
}

def test_guardar_viajes_archivo():
    """Verifica que el archivo JSON se guarde correctamente."""
    from main import viajes
    viajes.clear()
    viajes.append(viaje_ejemplo)

    guardarViajesArchivo()

    with open("viajes.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    assert len(datos) == 1
    assert datos[0]["origen"] == "Buenos Aires"
    assert datos[0]["destino"] == "Córdoba"


def test_agregar_pasajero_y_asiento():
    """Simula agregar un pasajero manualmente."""
    pasajeros = []
    asientos = [1, 2, 3]

    pasajero = {
        "nombre": "Juan Perez",
        "dni": "12345678",
        "email": "juan@mail.com",
        "asiento": 2
    }

    pasajeros.append(pasajero)
    asientos[1] = "X"

    assert len(pasajeros) == 1
    assert pasajeros[0]["dni"] == "12345678"
    assert asientos[1] == "X"


def test_dni_repetido():
    """Verifica que se detecte un DNI duplicado en el mismo viaje."""
    pasajeros = [
        {"nombre": "Ignacio", "dni": "11111111", "email": "ignacio@mail.com", "asiento": 1}
    ]
    nuevo_pasajero = {
        "nombre": "Pedro",
        "dni": "11111111",
        "email": "pedro@mail.com",
        "asiento": 2
    }

    dni_duplicado = False
    for p in pasajeros:
        if p["dni"] == nuevo_pasajero["dni"]:
            dni_duplicado = True

    assert dni_duplicado == True


def test_viaje_sin_pasajeros():
    """Comprueba que un viaje vacío no tenga pasajeros."""
    viaje = {
        "origen": "Temperley",
        "destino": "Bariloche",
        "fecha": "10/01/2026",
        "asientos": [1, 2, 3],
        "pasajeros": []
    }

    assert len(viaje["pasajeros"]) == 0
