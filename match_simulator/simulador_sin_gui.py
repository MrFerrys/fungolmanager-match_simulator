
class Jugador:
    def __init__(self, nombre, posicion, ataque, defensa, pase, resistencia):
        self.nombre = nombre
        self.posicion = posicion  # "POR", "DEF", "MED", "DEL"
        self.ataque = ataque
        self.defensa = defensa
        self.pase = pase
        self.resistencia = resistencia
        self.rendimiento = 1.0
        self.minutos_jugados = 0

    def simular_minuto(self, intensidad=1.0):
        desgaste = 0.005 * intensidad
        self.rendimiento -= desgaste
        self.rendimiento = max(0.6, self.rendimiento)
        self.minutos_jugados += 1

    def atributos_modificados(self):
        return {
            "ataque": self.ataque * self.rendimiento,
            "defensa": self.defensa * self.rendimiento,
            "pase": self.pase * self.rendimiento
        }


# === Plantilla inicial
jugadores = [
    Jugador("POR1", "POR", 10, 60, 30, 90),
    Jugador("DEF1", "DEF", 30, 70, 40, 90),
    Jugador("DEF2", "DEF", 35, 65, 45, 90),
    Jugador("DEF3", "DEF", 33, 67, 43, 90),
    Jugador("MED1", "MED", 60, 50, 70, 85),
    Jugador("MED2", "MED", 65, 45, 75, 85),
    Jugador("MED3", "MED", 62, 48, 72, 85),
    Jugador("DEL1", "DEL", 80, 30, 60, 80),
    Jugador("DEL2", "DEL", 75, 35, 65, 80),
]

# === Suplentes
jugadores_banquillo = [
    Jugador("DEL_SUP", "DEL", 78, 32, 62, 85),
    Jugador("MED_SUP", "MED", 63, 48, 72, 88),
]

# === Tácticas aplicadas por línea
tacticas = {
    "DEF": "Suben al ataque",
    "MED": "Crear juego",
    "DEL": "Punta de lanza"
}

def aplicar_tacticas(jugadores, tacticas):
    for j in jugadores:
        if j.posicion == "DEF" and tacticas["DEF"] == "Suben al ataque":
            j.ataque *= 1.05
            j.defensa *= 0.95
        elif j.posicion == "MED" and tacticas["MED"] == "Crear juego":
            j.pase *= 1.1
            j.defensa *= 0.95
        elif j.posicion == "DEL" and tacticas["DEL"] == "Punta de lanza":
            j.ataque *= 1.1

aplicar_tacticas(jugadores, tacticas)

# === Cambios programados
cambios_programados = {
    60: [("DEL", jugadores_banquillo[0])],
    75: [("MED", jugadores_banquillo[1])]
}

eventos = []

# === Simulación del partido
for minuto in range(1, 91):
    for j in jugadores:
        j.simular_minuto()
    if minuto in cambios_programados:
        for pos, nuevo_jugador in cambios_programados[minuto]:
            for i, j in enumerate(jugadores):
                if j.posicion == pos:
                    eventos.append(f"Min {minuto}: Sale {j.nombre}, Entra {nuevo_jugador.nombre}")
                    jugadores[i] = nuevo_jugador
                    break

# === Mostrar formación en consola
def imprimir_formacion(jugadores):
    print("\n📋 Formación:")
    posiciones = {"POR": [], "DEF": [], "MED": [], "DEL": []}
    for j in jugadores:
        posiciones[j.posicion].append(j.nombre)
    for linea in ["POR", "DEF", "MED", "DEL"]:
        print(f"{linea}: {', '.join(posiciones[linea])}")

# === Mostrar eventos y estadísticas
print("\n⚽ Eventos del partido:")
for e in eventos:
    print(f"  - {e}")

imprimir_formacion(jugadores)

print("\n📊 Estadísticas Finales:")
for j in jugadores:
    stats = j.atributos_modificados()
    print(f"{j.nombre} ({j.posicion}) | Min: {j.minutos_jugados} | Rend: {round(j.rendimiento,2)} | "
          f"ATA:{round(stats['ataque'],1)} DEF:{round(stats['defensa'],1)} PAS:{round(stats['pase'],1)}")
