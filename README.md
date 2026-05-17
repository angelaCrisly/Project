Análisis de Resultados ICFES Saber 11 (2020-2024)
Este proyecto consiste en un dashboard analítico interactivo diseñado para procesar y visualizar los resultados de las pruebas ICFES Saber 11 en Colombia para el periodo comprendido entre 2020 y 2024. El objetivo principal es identificar y comparar tendencias temporales, brechas socioeconómicas por estrato y capital cultural, diferencias entre la educación urbana y rural, y el desempeño general en el idioma inglés, además de un análisis detallado por departamentos.

Origen de los datos
Los datos utilizados en este análisis corresponden a los microdatos oficiales descargados de la página web del ICFES. Originalmente, la información se encontraba en archivos de texto plano (.txt) y fue convertida manualmente a archivos separados por comas (.csv) para facilitar su estructuración y lectura dentro del entorno de desarrollo.

Tecnologías utilizadas
El proyecto está desarrollado sobre el entorno de Python y utiliza las siguientes herramientas:

Visual Studio Code como entorno de desarrollo.

uv como gestor de paquetes de última generación para la creación del entorno virtual y la administración de dependencias.

Polars (utilizando LazyFrames) para la carga y limpieza eficiente de los archivos masivos de datos.

DuckDB como base de datos embebida para almacenar las tablas ya procesadas de forma rápida.

Flask como servidor web para administrar las rutas de la interfaz y los endpoints de la API.

Plotly.js para la renderización de los gráficos interactivos en el navegador.

Estructura del proyecto
El espacio de trabajo se organiza con la siguiente estructura de carpetas y archivos:

.venv/ - Entorno virtual administrado automáticamente por uv.

data_raw/ - Carpeta destinada a almacenar los archivos CSV que fueron convertidos manualmente desde los archivos de texto del ICFES.

database/ - Contiene el archivo icfes.db generado por DuckDB con los datos procesados.

static/ - Aloja el archivo styles.css con las reglas de diseño de la aplicación.

templates/ - Contiene el archivo dashboard.html que define la estructura de la página y el script de los gráficos.

app.py - Servidor principal de Flask que maneja la caché y la comunicación de datos.

db_storage.py - Módulo encargado de gestionar la conexión y el almacenamiento de datos en DuckDB.

main.py - Script principal que automatiza la lectura, limpieza y actualización de las tablas en la base de datos (actúa como el pipeline del proyecto).

process.py - El componente lógico que aplica los filtros de Polars y calcula los promedios y estadísticas.

pyproject.toml y uv.lock - Archivos de configuración y empaquetado generados por uv.

Instrucciones de configuración y ejecución
El proyecto se configuró desde cero utilizando las herramientas nativas de uv en PowerShell. Para replicar el entorno y ejecutar la aplicación, se deben seguir estos pasos:

1. Inicialización del entorno
Una vez instalado uv en el sistema, abre la carpeta del proyecto en Visual Studio Code y ejecuta en la terminal para inicializar la estructura:

Bash
uv init
2. Instalación de dependencias
Añade las librerías necesarias para el proyecto corriendo el siguiente comando, el cual creará el entorno virtual e instalará todo automáticamente:

Bash
uv add polars flask duckdb pyarrow
3. Procesamiento de los datos
Asegúrate de ubicar los archivos CSV convertidos manualmente dentro de la carpeta data_raw. Luego, ejecuta el script principal para procesar los datos crudos y transferirlos a DuckDB:

Bash
python main.py
4. Lanzamiento del Dashboard
Para encender el servidor de desarrollo de Flask utilizando el entorno gestionado por uv, ejecuta el siguiente comando en tu terminal:

Bash
uv run flask run --debug
Una vez que el servidor esté corriendo, abre tu navegador e ingresa a la dirección http://127.0.0.1:5000 (o la dirección local que te indique la consola) para interactuar con los paneles y las gráficas.