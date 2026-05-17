import polars as pl
import os

# Esta es la lista de datos del ICFES que nos interesa revisar
analysis_colums = [
     'periodo',
    'cole_depto_ubicacion',
    'cole_mcpio_ubicacion',
    'cole_area_ubicacion',
    'desemp_ingles',
    'fami_estratovivienda',
    'fami_numlibros',
    'fami_educacionmadre',
    'fami_educacionpadre',
    'estu_genero',
    'cole_naturaleza',
    'percentil_lectura_critica',
    'percentil_matematicas',
    'percentil_c_naturales',
    'percentil_sociales_ciudadanas',
    'percentil_ingles',
    'percentil_global',
    'punt_lectura_critica',
    'punt_matematicas',
    'punt_c_naturales',
    'punt_sociales_ciudadanas',
    'punt_ingles',
    'punt_global'
]

# Sirve para buscar todos los archivos .csv de las pruebas Saber 11 y juntarlos en un solo bloque
def carry_file (directory: str) -> pl.LazyFrame:
    files = sorted([
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith('.csv')
    ])
    cleaning_date = []
    for file in files:
        lf = pl.scan_csv(file,separator=";", encoding="utf8-lossy")
        cleaning_date.append(lf)
    return pl.concat(cleaning_date, how="diagonal_relaxed")


# Esta función limpia la base de datos: quita filas dañadas con puntajes en cero y arregla los textos vacíos poniéndoles "SIN DATO"
def filter_colums (lf: pl.LazyFrame) -> pl.LazyFrame:
    cols_letters = [
        "cole_naturaleza"
    ]
    
    sin_date = [
        "cole_area_ubicacion",
        "cole_depto_ubicacion",
        "cole_mcpio_ubicacion",
        "fami_estratovivienda",
        "fami_numlibros",
        "estu_genero"
    ]
    
    cols_clear = [
        "desemp_ingles"
    ]

    return (
        lf.select(analysis_colums)
        .with_columns(
            pl.col(sin_date).fill_null("SIN DATO").replace("", "SIN DATO"),
            pl.col(cols_clear).str.strip_chars()
        )
        .with_columns(
            pl.col(sin_date).str.strip_chars().str.to_uppercase(),
            pl.col(cols_letters).str.strip_chars().str.to_uppercase()
        )
        .filter(
            (pl.col("punt_global") > 0) & (pl.col("punt_global").is_not_null())
        )
    )

# Corta el texto del periodo para dejarnos solo el año (por ejemplo, convierte 20232 en 2023)
def extract_anio (lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.with_columns(
        (pl.col("periodo")//10).cast(pl.Int32).alias("anio")
    )

# Es la función "maestra". Agrupa los estudiantes por la categoría que le pidamos y calcula promedios de matemáticas, inglés, global, etc.
def statistics_group(lf: pl.LazyFrame, columns_group: str) -> pl.DataFrame:
    p_global = pl.col("punt_global")

    subjects = {
        "punt_global": "promedio_global",
        "punt_lectura_critica": "promedio_lectura",
        "punt_matematicas": "promedio_matematicas",
        "punt_c_naturales": "promedio_ciencias",
        "punt_sociales_ciudadanas": "promedio_sociales",
        "punt_ingles": "promedio_ingles"
    }
    return(
        lf.group_by(columns_group)
        .agg(
           [
            p_global.median().alias("mediana_global"),
            p_global.std().alias("desviacion_global"),
            p_global.min().alias("min_global"),
            p_global.max().alias("max_global"),
            p_global.count().alias("n_estudiantes"),
            
            *[pl.col(col).mean().alias(nombre) for col, nombre in subjects.items()]
        ])
        .sort(columns_group)
        .collect()
    )

# Saca los promedios de los exámenes ordenados año por año (2020 a 2024)
def time_trend(lf: pl.LazyFrame) -> pl.DataFrame:
    return statistics_group(lf, "anio")

# Saca los promedios de los estudiantes según su estrato social (Estrato 1, 2, etc.)
def gap_socioeconomic (lf: pl.LazyFrame) -> pl.DataFrame:
    return statistics_group(lf, "fami_estratovivienda")

# Compara los promedios de los estudiantes de colegios urbanos contra los rurales
def gap_urbano_rural(lf: pl.LazyFrame) -> pl.DataFrame:
    return statistics_group(lf, "cole_area_ubicacion")

# Muestra cuántos estudiantes sacaron A-, A1, B1, etc., en inglés cada año y calcula su porcentaje
def performance_english (lf: pl.LazyFrame) -> pl.DataFrame:
    counter = (
        lf.group_by(
            ["anio", "desemp_ingles"]
            )
        .agg(
            pl.col("punt_global").count().alias("conteo")
            )
        .collect()
    )
    totales = counter.group_by("anio").agg(pl.col("conteo").sum().alias("total"))
    results = counter.join(totales, on="anio").with_columns(
        (pl.col("conteo") / pl.col("total") * 100).round(2).alias("porcentaje")
    )
    return results.sort(["anio", "desemp_ingles"])

# Compara los promedios según la cantidad de libros que los muchachos tienen en sus casas
def cultural_capital(lf: pl.LazyFrame) -> pl.DataFrame:
    return statistics_group(lf, "fami_numlibros")

# Hace una lista con los 10 departamentos con mejores notas (Top) y los 10 con puntajes más bajos (Bottom)
def top_departament(lf: pl.LazyFrame, n: int = 10) -> pl.DataFrame:
    stats = statistics_group(lf, "cole_depto_ubicacion")
    top = stats.sort("promedio_global", descending=True).head(n)
    bottom = stats.sort("promedio_global").head(n)
    return pl.concat([
        top.with_columns(pl.lit("Top").alias("categoria")),
        bottom.with_columns(pl.lit("Bottom").alias("categoria")),
    ])

# Organiza los datos de un departamento específico contra el promedio de todo el país para poder pintar el gráfico de radar
def radar_departamento(lf: pl.LazyFrame, departamento: str) -> pl.DataFrame:
    subjects = ["punt_lectura_critica", "punt_matematicas", "punt_c_naturales",
                "punt_sociales_ciudadanas", "punt_ingles"]

    national = lf.select([pl.col(m).mean().alias(m) for m in subjects]).collect()

    depart = (
        lf.filter(pl.col("cole_depto_ubicacion") == departamento.upper())
        .select([pl.col(m).mean().alias(m) for m in subjects])
        .collect()
    )

    name = ["Lectura Crítica", "Matemáticas", "C. Naturales", "Sociales", "Inglés"]
    return pl.DataFrame({
        "materia": name,
        "nacional": [float(national[m][0]) for m in subjects],
        "departamento": [float(depart[m][0]) for m in subjects] if len(depart) > 0 else [0.0] * 5,
    })