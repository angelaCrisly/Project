import polars as pl
analysis_colums = [
    'periodo',
    'cole_depto_ubicacion',
    'cole_mcpio_ubicacion',
    'cole_area_ubicacion',
    'desemp_ingles',
    'fami_estratovivienda',
    'fami_numlibros',
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
# La función filtra las columnas que quiero
def filter_colums (lf: pl.LazyFrame):
    return (
    lf.select(analysis_colums)
    .with_columns(
            pl.col("cole_depto_ubicacion").str.strip_chars().str.to_uppercase()
        )
    .filter(
        (pl.col("punt_global") > 0) & (pl.col("punt_global").is_not_null())
    )
)
#La función agrupa
def group_colums (lf: pl.LazyFrame, column_filter: str ):
    return(
        lf.group_by(column_filter)
        .agg(pl.col("punt_global").mean().alias("promedio"))
    )
