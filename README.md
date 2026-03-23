# **Análisis de Resultados ICFES (2020 - 2024)**
## **Descripción del Proyecto**
Este proyecto de investigación busca identificar problemáticas socioeconómicas y académicas en Colombia mediante el análisis de microdatos del examen Saber 11. Utilizando técnicas de Ciencia de Datos, procesamos grandes volúmenes de información para visualizar brechas de aprendizaje y tendencias temporales.

## **Tecnologías y Herramientas**
* Entorno de Desarrollo: Visual Studio Code & Python.

* Gestión de Rendimiento: uv (Gestor de paquetes de alta velocidad).

* Motor de Datos: Polars (Lazy API) para procesamiento eficiente en memoria.

* Almacenamiento Analítico: DuckDB con consultas SQL.

* Visualización: Plotly Express para gráficos interactivos.

* Despliegue: Flask (Backend) con HTML y CSS (Frontend).

## **Estructura del Proyecto**
Plaintext
project-city/
├── data_raw/          # Microdatos CSV del ICFES (2020-2024)
├── database/          # Base de datos relacional .db (DuckDB)
├── static/            # Estilos CSS para la interfaz web
├── templates/         # Vistas HTML para la app Flask
├── main.py            # Orquestador del análisis
├── process.py         # Lógica de limpieza y transformación
└── .gitignore         # Archivos excluidos del control de versiones
## **Plan de Análisis y Visualización**
He definido cuatro ejes críticos para transformar los datos en información accionable:

1. Brecha Socioeconómica
[ ] Boxplot (Puntaje Global vs. Estrato): Para observar la distribución y dispersión de puntajes según el nivel económico.

[ ] Barras de Capital Cultural: Relación entre el número de libros en el hogar (fami_numlibros) y el éxito académico.

2. Comparativa Geográfica
[ ] Histograma Urbano vs. Rural: Comparar el cole_area_ubicacion para visualizar la brecha de oportunidades.

[ ] Heatmaps de Correlación: Matriz de áreas (Matemáticas, Lectura, etc.) para identificar fortalezas y debilidades regionales.

3. Evolución Temporal (2020 - 2024)
[ ] Líneas de Tendencia: Seguimiento anual del promedio del puntaje global.

[ ] Áreas Apiladas (Inglés): Evolución de los niveles de desempeño (desemp_ingles) a través de los años.

4. Rendimiento Específico
[ ] Gráfico de Radar (Araña): Comparativa de materias de un departamento frente al promedio nacional.

5. [ ] Scatter Plot: Relación entre Lectura Crítica y Matemáticas para identificar municipios con comportamientos atípicos.

## **Instalación y Ejecución**
Preparar el entorno con uv:

Bash
uv venv
uv pip install polars duckdb plotly flask
Ejecutar el proceso de datos:

Bash
uv run python main.py