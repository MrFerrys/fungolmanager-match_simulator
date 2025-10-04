import tkinter as tk

# ==== MODELO DE JUGADOR Y SIMULACION ====

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

# Plantilla inicial
jugadores_local = [
    Jugador("POR1", "POR", 10, 60, 30, 90),
    Jugador("DEF1", "DEF", 30, 70, 40, 90),
    Jugador("DEF2", "DEF", 35, 65, 45, 90),
    Jugador("DEF3", "DEF", 33, 67, 43, 90),
    Jugador("MED1", "MED", 60, 50, 70, 85),
    Jugador("MED2", "MED", 65, 45, 75, 85),
    Jugador("MED3", "MED", 62, 48, 72, 85),
    Jugador("DEL1", "DEL", 80, 30, 60, 80),
    Jugador("DEL2", "DEL", 75, 35, 65, 80)
]

# Banquillo
jugadores_banquillo = [
    Jugador("DEL_SUP", "DEL", 78, 32, 62, 85),
    Jugador("MED_SUP", "MED", 63, 48, 72, 88)
]

# Tácticas aplicadas por línea
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

aplicar_tacticas(jugadores_local, tacticas)

# Cambios programados
cambios_programados = {
    60: [("DEL", jugadores_banquillo[0])],
    75: [("MED", jugadores_banquillo[1])]
}

evento_cambios = []

# Simular partido
for minuto in range(1, 91):
    for j in jugadores_local:
        j.simular_minuto()
    if minuto in cambios_programados:
        for pos, nuevo_jugador in cambios_programados[minuto]:
            for i, j in enumerate(jugadores_local):
                if j.posicion == pos:
                    evento_cambios.append(f"Min {minuto}: Sale {j.nombre}, Entra {nuevo_jugador.nombre}")
                    jugadores_local[i] = nuevo_jugador
                    break

# ==== INTERFAZ GRAFICA PARA MOSTRAR FORMACION ====

ventana = tk.Tk()
ventana.title("Simulación y Formación táctica")
ventana.geometry("500x700")

canvas = tk.Canvas(ventana, width=480, height=680, bg="green")
canvas.pack(pady=10)

def dibujar_campo():
    canvas.create_rectangle(40, 40, 440, 640, outline="white", width=2)
    canvas.create_line(240, 40, 240, 640, fill="white", width=1)
    canvas.create_oval(190, 290, 290, 390, outline="white", width=2)
    canvas.create_rectangle(140, 40, 340, 140, outline="white", width=2)
    canvas.create_rectangle(140, 540, 340, 640, outline="white", width=2)

formacion_coords = {
    "POR": [(240, 620)],
    "DEF": [(140, 500), (240, 500), (340, 500)],
    "MED": [(140, 350), (240, 350), (340, 350)],
    "DEL": [(180, 200), (300, 200)]
}

def dibujar_formacion(jugadores):
    dibujar_campo()
    ocupadas = {"POR": 0, "DEF": 0, "MED": 0, "DEL": 0}
    for j in jugadores:
        if j.posicion in formacion_coords:
            pos = formacion_coords[j.posicion][ocupadas[j.posicion]]
            x, y = pos
            canvas.create_oval(x-20, y-20, x+20, y+20, fill="white", outline="black")
            canvas.create_text(x, y, text=j.nombre, font=("Arial", 8))
            ocupadas[j.posicion] += 1

dibujar_formacion(jugadores_local)

# Mostrar eventos de cambios en consola
print("\nEventos de cambio:")
for e in evento_cambios:
    print(e)

# Mostrar estadísticas al final
print("\nEstadísticas Finales:")
for j in jugadores_local:
    mod = j.atributos_modificados()
    print(f"{j.nombre} - Pos: {j.posicion} - Min: {j.minutos_jugados} - Rend: {round(j.rendimiento,2)} - ATA:{round(mod['ataque'],1)} DEF:{round(mod['defensa'],1)} PAS:{round(mod['pase'],1)}")

ventana.mainloop()
