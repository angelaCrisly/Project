import duckdb
import polars as pl
import os

# Define la ruta donde se va a crear y guardar el archivo de la base de datos
route_db = os.path.join("database", "icfes.db")

# Crea la carpeta 'database' si no existe y abre la conexión para poder guardar o leer datos
def create_connection ()-> duckdb.DuckDBPyConnection:
    os.makedirs("database", exist_ok=True)
    return duckdb.connect(route_db)

# Borra la tabla si ya existía antes y guarda el nuevo DataFrame de Polars directamente en DuckDB
def save_dataframe (df: pl.DataFrame, nombre_tabla: str) -> None:
    con = create_connection()
    arrow_table = df.to_arrow() # Convierte los datos a un formato intermedio rápido que DuckDB entiende al tiro
    con.execute(f"DROP TABLE IF EXISTS {nombre_tabla}")
    con.execute(f"CREATE TABLE {nombre_tabla} AS SELECT * FROM arrow_table")
    con.close()

# Recibe una consulta en lenguaje SQL, busca la información en la base de datos y te la devuelve como un DataFrame de Polars listo para usar
def consult(query: str) -> pl.DataFrame:
    con = create_connection()
    results = con.execute(query).pl()
    con.close()
    return results