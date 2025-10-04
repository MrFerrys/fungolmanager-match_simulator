
import random

# ===================== EQUIPOS Y FORMACIONES =====================
equipos = {
    "Real Madrid": {"ataque": 85, "mediocampo": 82, "defensa": 80},
    "Barcelona": {"ataque": 86, "mediocampo": 84, "defensa": 79}
}

formaciones = {
    "4-3-3": {"defensas": 4, "medios": 3, "delanteros": 3},
    "4-4-2": {"defensas": 4, "medios": 4, "delanteros": 2}
}

# ===================== FUNCIONES =====================
def generar_jugadores(equipo, formacion):
    plantilla = []
    plantilla.append({"nombre": f"{equipo} - Portero", "pos": "GK", "tiros": 0, "goles": 0, "penaltis_atajados": 0})
    for i in range(formacion["defensas"]):
        plantilla.append({"nombre": f"{equipo} - DF{i+1}", "pos": "DF", "tiros": 0, "goles": 0, "penaltis_atajados": 0})
    for i in range(formacion["medios"]):
        plantilla.append({"nombre": f"{equipo} - MF{i+1}", "pos": "MF", "tiros": 0, "goles": 0, "penaltis_atajados": 0})
    for i in range(formacion["delanteros"]):
        plantilla.append({"nombre": f"{equipo} - FW{i+1}", "pos": "FW", "tiros": 0, "goles": 0, "penaltis_atajados": 0})
    return plantilla

def simular_goles(jugadores, tiros_equipo):
    goles = 0
    for _ in range(tiros_equipo):
        candidato = random.choices(jugadores, weights=[0.05 if j["pos"]=="GK" else 0.1 if j["pos"]=="DF" else 0.2 if j["pos"]=="MF" else 0.4 for j in jugadores])[0]
        candidato["tiros"] += 1
        prob = 0.3 if candidato["pos"] == "FW" else 0.15
        if random.random() < prob:
            candidato["goles"] += 1
            goles += 1
    return goles, jugadores

def simular_penaltis(jugadores_local, jugadores_visitante):
    lanzadores_local = [j for j in jugadores_local if j["pos"] in ["FW", "MF", "DF"]][:5]
    lanzadores_visitante = [j for j in jugadores_visitante if j["pos"] in ["FW", "MF", "DF"]][:5]
    portero_local = jugadores_local[0]
    portero_visitante = jugadores_visitante[0]

    goles_local = 0
    goles_visitante = 0

    for i in range(5):
        if random.random() < 0.75:
            goles_local += 1
        else:
            portero_visitante["penaltis_atajados"] += 1

        if random.random() < 0.75:
            goles_visitante += 1
        else:
            portero_local["penaltis_atajados"] += 1

    while goles_local == goles_visitante:
        if random.random() < 0.75:
            goles_local += 1
        else:
            portero_visitante["penaltis_atajados"] += 1

        if random.random() < 0.75:
            goles_visitante += 1
        else:
            portero_local["penaltis_atajados"] += 1

    return goles_local, goles_visitante

def format_stats(jugadores):
    return "\n".join([f"{j['nombre']} - Tiros: {j['tiros']} | Goles: {j['goles']} | Penaltis Atajados: {j['penaltis_atajados']}" for j in jugadores])

def simular_partido(local, visitante, form_local, form_visitante, es_eliminatoria=False):
    jugadores_local = generar_jugadores(local, formaciones[form_local])
    jugadores_visitante = generar_jugadores(visitante, formaciones[form_visitante])

    posesion_local = random.uniform(0.45, 0.55)
    posesion_visitante = 1 - posesion_local

    tiros_local = int(equipos[local]["ataque"] * posesion_local / 20)
    tiros_visitante = int(equipos[visitante]["ataque"] * posesion_visitante / 20)

    goles_local, jugadores_local = simular_goles(jugadores_local, tiros_local)
    goles_visitante, jugadores_visitante = simular_goles(jugadores_visitante, tiros_visitante)

    resultado = f"\n🆚 {local} {goles_local} - {goles_visitante} {visitante}\n"
    resultado += f"📊 Posesión: {int(posesion_local*100)}% - {int(posesion_visitante*100)}%\n"
    resultado += f"🎯 Tiros: {tiros_local} - {tiros_visitante}\n\n"

    if es_eliminatoria and goles_local == goles_visitante:
        res_pen_local, res_pen_vis = simular_penaltis(jugadores_local, jugadores_visitante)
        resultado += f"🏁 Tanda de Penaltis: {local} {res_pen_local} - {res_pen_vis} {visitante}\n"
        if res_pen_local > res_pen_vis:
            resultado += f"🎉 ¡{local} gana en penaltis!\n"
        else:
            resultado += f"🎉 ¡{visitante} gana en penaltis!\n"

    resultado += f"\n📈 {local} Stats:\n" + format_stats(jugadores_local)
    resultado += f"\n\n📈 {visitante} Stats:\n" + format_stats(jugadores_visitante)
    return resultado

# ===================== SIMULACIÓN =====================
if __name__ == "__main__":
    resultado = simular_partido("Real Madrid", "Barcelona", "4-3-3", "4-4-2", es_eliminatoria=True)
    print(resultado)
