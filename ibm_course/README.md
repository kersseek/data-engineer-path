# IBM Curso

Este directorio está dedicado al contenido del curso **[IBM Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-engineer)** en Coursera, contiene prácticas y ejercicios realizados durante el curso.

## Secciones

### [Pruebas unitarias](unit_test/test_mymodule.py)

Esta sección contiene funciones simples (square, double, add) y sus respectivas pruebas unitarias usando el módulo unittest en Python. Las pruebas validan el comportamiento correcto de las funciones con diferentes tipos de entradas.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

### [Proceso ETL multiformato para unificar y convertir la data usando Pandas](etl_multiformat/main.py)

Esta sección contiene un script que implementa un proceso ETL. El código extrae datos desde archivos locales en formatos CSV, JSON y XML, los transforma aplicando conversiones de altura y peso a unidades métricas usando Pandas, y luego guarda los resultados unificados en un archivo CSV. Además, se genera un archivo de log que documenta cada fase del proceso.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4CAF50?style=flat&logo=files&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-292929?style=flat&logo=json&logoColor=white)
![XML](https://img.shields.io/badge/XML-0060ac?style=flat&logo=xml&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

### [Crear y gestionar una base de datos SQLite local con cursor usando Pandas](database_pandas/main.py)

Esta sección contiene un script que utiliza SQLite como base de datos local y Pandas para mostrar los resultados de forma tabular.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

### [Proceso ETL con web scraping uniendo data de URL y CSV para almacenamiento en CSV y SQLite local](etl_web_scraping/main.py)

Esta sección contiene un script que extrae datos de una página web usando Requests y BeautifulSoup, transforma esos datos con Pandas y con la data del CSV aplicando conversiones monetarias con Numpy y crea logs para cada proceso para posteriormente guardar los datos en un archivo CSV y en una base de datos SQLite local.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4CAF50?style=flat&logo=files&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FF9900?style=flat&logo=beautifulsoup&logoColor=white)

### [Líneas mágicas conexión SQLite local y consultas usando Pandas para almacenamiento en SQLite local](magic_commands/database_query_pandas/main.py)

Esta sección contiene un script que descarga y carga conjuntos de datos públicos de la ciudad de Chicago relacionados con censos, escuelas y crímenes. Utiliza pandas para leer los archivos CSV desde URLs, almacena estos datos en una base de datos SQLite local mediante líneas mágicas de SQL en un entorno interactivo y realiza consultas SQL.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4CAF50?style=flat&logo=files&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

### [Líneas mágicas conexión SQLite local y gráfico Seaborn usando Pandas para almacenamiento en SQLite local](magic_commands/database_graph_pandas/main.py)

Esta sección contiene un script que implementa una conexión a la base de datos SQLite con líneas mágicas de SQL, se extraen datos socioeconómicos de la ciudad de Chicago de un CSV, se almacenan en una base de datos SQLite local y se realizan consultas, por último, se utiliza Seaborn para visualizar gráficamente la relación entre ingresos per cápita e índice de dificultad social.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-4CAF50?style=flat&logo=files&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-6DB7C6?style=flat&logo=seaborn&logoColor=white)

---

[Regresar](../README.md)
