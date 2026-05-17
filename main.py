import process
import db_storage as db_module

# Ruta de la carpeta que contiene los archivos originales del ICFES
DIRECTORY_DATA = "data_raw"

def workflow():
    # --- FASE 1: CARGA Y LIMPIEZA DE DATOS ---
    print("Cargando datos .csv")
    # Carga los archivos CSV de la carpeta usando procesamiento perezoso (LazyFrame)
    lf_raw = process.carry_file(DIRECTORY_DATA)

    print("Filtrado y limpieza de datos")
    # Selecciona solo las columnas necesarias para el dashboard
    lf_clear = process.filter_colums(lf_raw)

    # Crea o formatea la columna del año para los análisis temporales
    lf_clear = process.extract_anio(lf_clear)

    # --- FASE 2: PROCESAMIENTO Y ANÁLISIS ---
    print("Generando analisis...")
    # Diccionario para almacenar los DataFrames resultantes de cada análisis
    results = {}

    # 1. Tendencia temporal (Evolución de promedios globales y por materia)
    print("Tendencia temporal (2020-2024)")
    results["tendencia"] = process.time_trend(lf_clear)

    # 2. Brecha socioeconómica por estrato (Promedios según el estrato de la vivienda)
    print("Brecha socioeconómica")
    results["estrato"] = process.gap_socioeconomic(lf_clear)

    # 3. Brecha urbano vs rural (Comparativa de colegios según su ubicación geográfica)
    print("Comparativa urbano vs rural")
    results["urbano_rural"] = process.gap_urbano_rural(lf_clear)

    # 4. Capital cultural (Relación entre el puntaje y la cantidad de libros en el hogar)
    print("Capital cultural")
    results["libros"] = process.cultural_capital(lf_clear)

    # 5. Distribución de niveles de inglés (Porcentaje de estudiantes en niveles A-, A1, B+, etc.)
    print("Distribución de inglés por año")
    results["ingles"] = process.performance_english(lf_clear)

    # 6. Ranking departamentos (Identifica los mejores y peores promedios por región)
    print("Top/Bottom departamentos")
    results["departamentos"] = process.top_departament(lf_clear)

    # 7. Estadísticas por departamento (Datos detallados por materia para el gráfico de radar)
    print("Estadísticas por departamento")
    results["stats_depto"] = process.statistics_group(
        lf_clear, "cole_depto_ubicacion"
    )

    # --- FASE 3: ALMACENAMIENTO ---
    print("Guardando en DuckDB")
    # Recorre cada análisis generado y lo guarda como una tabla individual en la base de datos
    for name, df in results.items():
        db_module.save_dataframe(df, name)
        print(f"Tabla '{name}' guardada ({len(df)} filas)")

    print("✅ Pipeline completado.")
    return results

# Punto de entrada para ejecutar el script directamente desde la terminal
if __name__ == "__main__":
    workflow()