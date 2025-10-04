# ===================== SIMULADOR DE PARTIDOS DE FÚTBOL =====================
import random

equipos = {
    "Real Madrid": {"ataque": 85, "mediocampo": 82, "defensa": 80},
    "Valencia": {"ataque": 75, "mediocampo": 77, "defensa": 78},
    "Barcelona": {"ataque": 86, "mediocampo": 84, "defensa": 79},
    "Atletico": {"ataque": 79, "mediocampo": 78, "defensa": 85}
}

formaciones = {
    "4-4-2": {"defensas": 4, "medios": 4, "delanteros": 2},
    "4-3-3": {"defensas": 4, "medios": 3, "delanteros": 3},
    "5-3-2": {"defensas": 5, "medios": 3, "delanteros": 2},
    "3-5-2": {"defensas": 3, "medios": 5, "delanteros": 2},
}

def generar_jugadores(equipo, formacion):
    plantilla = []
    plantilla.append(crear_jugador(equipo, "GK", 1))
    for i in range(formacion["defensas"]):
        plantilla.append(crear_jugador(equipo, "DF", i+1))
    for i in range(formacion["medios"]):
        plantilla.append(crear_jugador(equipo, "MF", i+1))
    for i in range(formacion["delanteros"]):
        plantilla.append(crear_jugador(equipo, "FW", i+1))
    plantilla += [crear_jugador(equipo, pos, i+1, True) for pos in ["DF", "MF", "FW"] for i in range(2)]
    return plantilla

def crear_jugador(equipo, pos, num, suplente=False):
    return {
        "nombre": f"{equipo} - {pos}{'_SUP' if suplente else ''}{num}",
        "pos": pos,
        "suplente": suplente,
        "goles": 0,
        "tiros": 0,
        "pases": 0,
        "cansancio": 0,
        "amarillas": 0,
        "expulsado": False
    }

def simular_partido_completo(local, visitante, form_local, form_visitante):
    fl = formaciones[form_local]
    fv = formaciones[form_visitante]
    jl = generar_jugadores(local, fl)
    jv = generar_jugadores(visitante, fv)
    cambios = {local: 5, visitante: 5}
    eventos = []
    goles_l = goles_v = 0

    for min in range(1, 91):
        for equipo, jugadores in [(local, jl), (visitante, jv)]:
            for j in jugadores:
                if j["suplente"] or j.get("expulsado"): continue
                j["pases"] += random.randint(0, 3)
                j["cansancio"] += 1 + (0.2 if j["pos"] == "MF" else 0.1)
                if j["pos"] == "FW" and random.random() < 0.04:
                    j["tiros"] += 1
                    if random.random() < (0.25 - j["cansancio"] * 0.005):
                        j["goles"] += 1
                        if equipo == local: goles_l += 1
                        else: goles_v += 1
                        eventos.append({"minuto": min, "jugador": j["nombre"], "accion": "⚽️ Gol", "equipo": equipo})
        generar_eventos_extra(jl, local, min, eventos, cambios)
        generar_eventos_extra(jv, visitante, min, eventos, cambios)

    mostrar_resultado(local, visitante, goles_l, goles_v, jl, jv, eventos)

def generar_eventos_extra(jugadores, equipo, minuto, eventos, cambios_restantes):
    for j in list(jugadores):
        if j["suplente"] or j.get("expulsado"): continue
        if random.random() < 0.01 + j["cansancio"] * 0.003:
            eventos.append({"minuto": minuto, "jugador": j["nombre"], "accion": "🤕 Lesionado y retirado", "equipo": equipo})
            reemplazar_lesionado(jugadores, j, equipo, eventos, minuto, cambios_restantes)
            continue
        if random.random() < 0.02:
            j["amarillas"] += 1
            eventos.append({"minuto": minuto, "jugador": j["nombre"], "accion": "🟨 Amarilla", "equipo": equipo})
        if j["amarillas"] >= 2:
            j["expulsado"] = True
            eventos.append({"minuto": minuto, "jugador": j["nombre"], "accion": "🟥 Segunda amarilla - Expulsado", "equipo": equipo})
            reemplazar_lesionado(jugadores, j, equipo, eventos, minuto, cambios_restantes)

def reemplazar_lesionado(jugadores, j_lesionado, equipo, eventos, minuto, cambios_restantes):
    if cambios_restantes[equipo] <= 0:
        eventos.append({"minuto": minuto, "jugador": j_lesionado["nombre"], "accion": "⚠️ No quedan cambios disponibles - Jugador retirado y no reemplazado", "equipo": equipo})
        jugadores.remove(j_lesionado)
        return False
    pos = j_lesionado["pos"]
    for s in jugadores:
        if s["suplente"] and s["pos"] == pos:
            s["suplente"] = False
            jugadores.remove(j_lesionado)
            jugadores.append(s)
            eventos.append({"minuto": minuto, "jugador": s["nombre"], "accion": f"🔁 Sustitución automática por {j_lesionado['nombre']}", "equipo": equipo})
            cambios_restantes[equipo] -= 1
            return True
    eventos.append({"minuto": minuto, "jugador": j_lesionado["nombre"], "accion": "⚠️ No hay suplente disponible para esa posición - Jugador retirado", "equipo": equipo})
    jugadores.remove(j_lesionado)
    return False

def mostrar_resultado(local, visitante, gl, gv, jl, jv, eventos):
    print(f"\n📊 Resultado Final: {local} {gl} - {gv} {visitante}")
    print("\n📋 Eventos del partido:")
    for e in sorted(eventos, key=lambda x: x["minuto"]):
        print(f" - {e['minuto']}' {e['equipo']} - {e['jugador']}: {e['accion']}")

    print("\n🔍 Estadísticas individuales:")
    for equipo, jugadores in [(local, jl), (visitante, jv)]:
        print(f"\n{equipo}:")
        for j in jugadores:
            if not j["suplente"]:
                linea = f"{j['nombre']} | Goles: {j['goles']}, Tiros: {j['tiros']}, Pases: {j['pases']}, Amarillas: {j['amarillas']}, Cansancio: {round(j['cansancio'],1)}"
                if j.get("expulsado"): linea += " 🟥"
                print(" -", linea)

# ===================== EJECUCIÓN =====================
simular_partido_completo("Barcelona", "Real Madrid", "4-4-2", "3-5-2")
