# Análisis de Ventas Interactivo con Streamlit

Aplicación web interactiva desarrollada para analizar datos de ventas de forma sencilla y visual. La herramienta permite a los usuarios cargar sus propios conjuntos de datos en formato CSV y obtener métricas y visualizaciones clave para entender el rendimiento de sus productos.

## 🚀 Características

*   **Carga de Datos Personalizada**: Sube tus propios datos de ventas a través de un archivo CSV directamente desde la interfaz. La aplicación está diseñada para ser flexible, requiriendo las siguientes columnas: `Sucursal, Producto, Año, Mes, Unidades_vendidas, Ingreso_total, Costo_total`.
*   **Filtrado por Sucursal**: Analiza el rendimiento de tus productos en una sucursal específica o de forma global seleccionando la opción en el menú desplegable.
*   **Métricas Clave por Producto**:
    *   💰 **Precio Promedio**: Calcula el precio de venta promedio de cada producto.
    *   📈 **Margen Promedio**: Obtén el margen de ganancia porcentual promedio.
    *   📦 **Unidades Vendidas**: Visualiza el total de unidades vendidas.
    *   📊 **Cambio Anual**: Cada métrica se acompaña de su cambio porcentual promedio anual para un análisis de tendencias rápido.
*   **Visualización de la Evolución de Ventas**: Para cada producto, se genera un gráfico que muestra la evolución de las unidades vendidas a lo largo del tiempo, junto con una línea de tendencia para identificar patrones a largo plazo.

## 🛠️ Cómo Utilizar la Aplicación

1.  **Instalar las dependencias**:
    Asegúrate de tener todas las librerías necesarias ejecutando:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ejecutar la aplicación**:
    Lanza la aplicación Streamlit con el siguiente comando en tu terminal:
    ```bash
    streamlit run ejercicio.py
    ```

3.  **Interactuar con la App**:
    *   La aplicación se abrirá automáticamente en tu navegador.
    *   En la barra lateral, encontrarás la opción para cargar tu archivo CSV.
    *   Una vez cargado el archivo, podrás seleccionar una sucursal para filtrar los datos.
    *   Explora las tarjetas de métricas y los gráficos generados para cada uno de tus productos.

## 🧪 Generación de Datos de Prueba

Para facilitar la demostración y prueba de la aplicación, he incluido el cuaderno de Jupyter `datos.ipynb`. Este notebook genera datos sintéticos de ventas para dos categorías de productos (gaseosas y vinos) y los guarda en los archivos `gaseosas.csv` y `vinos.csv`.

## 💻 Tecnologías Utilizadas

*   **Python**: El lenguaje de programación principal.
*   **Streamlit**: Para la creación de la aplicación web interactiva.
*   **Pandas**: Para la manipulación y análisis de los datos.
*   **Matplotlib**: Para la generación de los gráficos y visualizaciones.
*   **Jupyter Notebook**: Para la generación de los datos de prueba.
