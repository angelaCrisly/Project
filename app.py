import json
import os
from flask import Flask, render_template, jsonify
import polars as pl
import process
import db_storage as db_module

app = Flask(__name__)

# Estas variables sirven para guardar los datos en la memoria del computador una vez cargados. 
# Así el servidor no tiene que volver a leer los archivos gigantes cada vez que alguien entra a la página.
_datos_cache = None
_lf_cache = None

DIRECTORY_DATA = "data_raw"

# Trae los archivos del ICFES, los limpia y los deja listos en memoria para cuando los necesitemos
def obtain_lazyframe() -> pl.LazyFrame:
    global _lf_cache
    if _lf_cache is None:
        lf = process.carry_file(DIRECTORY_DATA)
        lf = process.filter_colums(lf)
        lf = process.extract_anio(lf)
        _lf_cache = lf
    return _lf_cache

# Ejecuta todos los análisis del archivo 'process.py' de un solo golpe, arma la lista de departamentos 
# para el selector y calcula los números grandes (KPIs) del encabezado
def obtain_data() -> dict:
    global _datos_cache
    if _datos_cache is not None:
        return _datos_cache
    
    lf = obtain_lazyframe()
    trend = process.time_trend(lf)
    stratum = process.gap_socioeconomic(lf)
    urban_rural = process.gap_urbano_rural(lf)
    book = process.cultural_capital(lf)
    english = process.performance_english(lf)
    departments = process.top_departament(lf)
    stats_depto = process.statistics_group(lf, "cole_depto_ubicacion")

    # Lista de departamentos para el selector del radar
    list_deptos = sorted([d for d in stats_depto["cole_depto_ubicacion"].to_list() if d is not None])
    _datos_cache = {
        "trend": df_a_dict(trend),
        "stratum": df_a_dict(stratum),
        "urbano_rural": df_a_dict(urban_rural),
        "book": df_a_dict(book),
        "english": df_a_dict(english),
        "departments": df_a_dict(departments),
        "list_deptos": list_deptos,
    }
    
    # Calcular KPIs
    total_students = int(trend["n_estudiantes"].sum())
    general_average = round(float(trend["promedio_global"].mean()), 1)
    n_periods = len(trend)
    n_deptos = len(stats_depto)

    _datos_cache["kpis"] = [
        {"valor": f"{total_students:,}".replace(",", "."), "label": "Estudiantes Analizados"},
        {"valor": str(general_average), "label": "Puntaje Global Promedio"},
        {"valor": str(n_periods), "label": "Años de Datos"},
        {"valor": str(n_deptos), "label": "Departamentos"},
    ]
    return _datos_cache

# Convierte las tablas de Polars a diccionarios comunes de Python para que puedan ser leídos como JSON en el navegador sin que se rompan los números decimales o enteros
def df_a_dict(df: pl.DataFrame) -> dict:
    result = {}
    for col in df.columns:
        serie = df[col]
        if serie.dtype in (pl.Float64, pl.Float32):
            result[col] = [round(float(v), 2) if v is not None else 0 for v in serie.to_list()]
        elif serie.dtype in (pl.Int32, pl.Int64, pl.UInt32, pl.UInt64):
            result[col] = [int(v) if v is not None else 0 for v in serie.to_list()]
        else:
            result[col] = serie.to_list()
    return result

# Es la ruta principal de la aplicación. Cuando entras a la página, lee los datos guardados en caché y carga el diseño visual en 'dashboard.html'
@app.route("/")
def dashboard():
    data = obtain_data()
    return render_template(
        "dashboard.html",
        datos_json=json.dumps(_datos_cache),
        kpis=data["kpis"],
        departamentos=data["list_deptos"],
    )

# Es la ruta secreta que usa JavaScript para pedir los datos del gráfico de radar cada vez que el usuario cambia de departamento en el selector
@app.route("/api/radar/<departamento>")
def api_radar(departamento: str):
    lf = obtain_lazyframe()
    df_radar = process.radar_departamento(lf, departamento)
    
    respuesta = {
        "materia": df_radar["materia"].to_list(),
        "nacional": [round(float(v), 2) for v in df_radar["nacional"].to_list()],
        "departamento": [round(float(v), 2) for v in df_radar["departamento"].to_list()]
    }
    
    return jsonify(respuesta)

# Enciende el servidor local de desarrollo de Flask para poder ver la página web en tu computadora
if __name__ == "__main__":
    print("🚀 Iniciando dashboard en http://localhost:5000")
    app.run(debug=True, port=5000)