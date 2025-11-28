# IBM COURSE

La sección `ibm_course` está dedicada al contenido del curso **[IBM Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-engineer)** en Coursera. Esta sección contiene algunas prácticas y ejercicios realizados durante el curso para reforzar los conocimientos adquiridos en ingeniería de datos.

---

## PRACTICAS Y EJERCICIOS

### [PRUEBAS UNITARIAS](unit_test/test_mymodule.py)

Esta sección contiene funciones simples (square, double, add) y sus respectivas pruebas unitarias usando el módulo unittest en Python. Las pruebas validan el comportamiento correcto de las funciones con diferentes tipos de entradas.

### [LÍNEAS MÁGICAS CONEXIÓN SQLITE LOCAL Y CONSULTAS USANDO PANDAS PARA ALMACENAMIENTO EN SQLITE LOCAL](magic_commands\database_query_pandas\main.py)

Esta sección contiene un script que descarga y carga conjuntos de datos públicos de la ciudad de Chicago relacionados con censos, escuelas y crímenes. Utiliza pandas para leer los archivos CSV desde URLs, almacena estos datos en una base de datos SQLite local mediante líneas mágicas de SQL en un entorno interactivo y realiza consultas SQL.

### [LÍNEAS MÁGICAS CONEXIÓN SQLITE LOCAL Y GRÁFICO SEABORN USANDO PANDAS PARA ALMACENAMIENTO EN SQLITE LOCAL](magic_commands\database_graph_pandas\main.py)

Esta sección contiene un script que implementa una conexión a la base de datos SQLite con líneas mágicas de SQL, se extraen datos socioeconómicos de la ciudad de Chicago de un CSV, se almacenan en una base de datos SQLite local y se realizan consultas, por último, se utiliza Seaborn para visualizar gráficamente la relación entre ingresos per cápita e índice de dificultad social.

### [PROCESO ETL CON WEB SCRAPING UNIENDO DATA DE URL Y CSV PARA ALMACENAMIENTO EN CSV Y SQLITE LOCAL](etl_web_scraping\main.py)

Esta sección contiene un script que extrae datos de una página web usando Requests y BeautifulSoup, transforma esos datos con Pandas y con la data del CSV aplicando conversiones monetarias con Numpy y crea logs para cada proceso para posteriormente guardar los datos en un archivo CSV y en una base de datos SQLite local.

### [PROCESO ETL MULTIFORMATO PARA UNIFICAR Y CONVERTIR LA DATA USANDO PANDAS](etl_multiformat\main.py)

Esta sección contiene un script que implementa un proceso ETL. El código extrae datos desde archivos locales en formatos CSV, JSON y XML, los transforma aplicando conversiones de altura y peso a unidades métricas usando Pandas, y luego guarda los resultados unificados en un archivo CSV. Además, se genera un archivo de log que documenta cada fase del proceso.

### [CREAR Y GESTIONAR UNA BASE DE DATOS SQLITE LOCAL CON CURSOR USANDO PANDAS](database_pandas\main.py)

Esta sección contiene un script en Python que utiliza SQLite como base de datos local y Pandas para mostrar los resultados de forma tabular.
