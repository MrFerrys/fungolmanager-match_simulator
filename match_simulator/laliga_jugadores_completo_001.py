
import requests
import pandas as pd
import time
import json

# ========== CONFIGURACIÓN ==========
API_KEY = "TU_API_KEY"  # Sustituye por tu clave de API-Football
API_HOST = "v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

# ========== FUNCIONES PRINCIPALES ==========

def obtener_teams_laliga(season=2024, league=140):
    url = f"https://{API_HOST}/teams?league={league}&season={season}"
    res = requests.get(url, headers=HEADERS).json()
    return res["response"]

def obtener_stats_jugador(player_id, season=2024, league=140):
    url = f"https://{API_HOST}/players?id={player_id}&season={season}&league={league}"
    res = requests.get(url, headers=HEADERS).json()
    if res["response"]:
        return res["response"][0]
    return None

def estadisticas_a_atributos(stats):
    try:
        games = stats["games"]["appearences"] or 1
        minutos = stats["games"]["minutes"]
        goles = stats["goals"]["total"] / games
        dribbles = stats["dribbles"]["success"] / games
        duelos = stats["duels"]["won"] / games
        faltas = stats["fouls"]["committed"] / games
        velocidad_aprox = dribbles  # simplificación
        agresividad = faltas

        maximos = {
            "ataque": 1.0,
            "tecnica": 5.5,
            "defensa": 6.5,
            "resistencia": 3060,
            "velocidad": 5.5,
            "agresividad": 3.5
        }

        atributos = {
            "Ataque": round(min(goles / maximos["ataque"], 1.0) * 100, 1),
            "Defensa": round(min(duelos / maximos["defensa"], 1.0) * 100, 1),
            "Técnica": round(min(dribbles / maximos["tecnica"], 1.0) * 100, 1),
            "Velocidad": round(min(velocidad_aprox / maximos["velocidad"], 1.0) * 100, 1),
            "Resistencia": round(min(minutos / maximos["resistencia"], 1.0) * 100, 1),
            "Agresividad": round(min(agresividad / maximos["agresividad"], 1.0) * 100, 1)
        }

        return atributos
    except:
        return None

def generar_csv_y_json_completo(salida_csv="la_liga_2024_atributos.csv", salida_json="la_liga_2024_raw.json"):
    equipos = obtener_teams_laliga()
    filas = []
    datos_crudos = []

    for tm in equipos:
        team = tm["team"]
        team_id = team["id"]
        team_name = team["name"]
        print(f"Procesando equipo: {team_name}...")

        url = f"https://{API_HOST}/players?team={team_id}&season=2024&league=140"
        res = requests.get(url, headers=HEADERS).json()
        jugadores = res["response"]

        for j in jugadores:
            pl = j["player"]
            player_data = obtener_stats_jugador(pl["id"])
            if not player_data:
                continue

            stats = player_data["statistics"][0]
            atributos = estadisticas_a_atributos(stats)
            if not atributos:
                continue

            fila = {
                "ID Jugador": pl["id"],
                "Nombre": pl["name"],
                "Edad": pl.get("age", None),
                "Posición": stats["games"]["position"],
                "Equipo": team_name,
                "ID Equipo": team_id,
                **atributos
            }
            filas.append(fila)
            datos_crudos.append({
                "jugador": pl,
                "estadisticas": stats
            })
            time.sleep(0.6)
        time.sleep(0.8)

    df = pd.DataFrame(filas)
    df.to_csv(salida_csv, index=False)

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(datos_crudos, f, ensure_ascii=False, indent=2)

    print(f"✅ CSV generado: {salida_csv}")
    print(f"✅ JSON generado: {salida_json}")
