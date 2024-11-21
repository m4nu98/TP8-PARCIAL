import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
## ATENCION: Debe colocar la direccion en la que ha sido publicada la aplicacion en la siguiente linea\
# url = 'https://tp8-555555.streamlit.app/'

def mostrar_informacion_alumno():
    with st.container(border=True):
        st.markdown('**Legajo:** 59043')
        st.markdown('**Nombre:** Medina Elias Manuel')
        st.markdown('**Comisión:** C7')


## CARGA EL ARCHIVO CSV
def cargar_datos():
    try:
        st.markdown("""
            <style>
            .upload-container {e
                border: 2px dashed #cccccc;
                border-radius: 5px;
                padding: 20px;
                background-color: #f8f9fa;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                border-radius: 4px;
                border: none;
            }
            </style>
        """, unsafe_allow_html=True)
        
         # Contenedor personalizado
        with st.container():
            
            # Título y descripción
            st.markdown("### 📊 Carga de Datos de Ventas")
            st.markdown("Por favor, sube tu archivo CSV con los datos de ventas")
            
        
        # Crear uploader para archivos CSV
        uploaded_file = st.file_uploader(
            "📂 Cargar archivo CSV de ventas",
            type=['csv'],
            help="El archivo debe contener las columnas: Sucursal, Producto, Año, Mes, Unidades_vendidas, Ingreso_total, Costo_total"
        )
        
        
            
        
        if uploaded_file is not None:
                with st.spinner('Procesando archivo...'):
                    df = pd.read_csv(uploaded_file)
                    st.success('✅ Archivo cargado exitosamente')
                    return df
        return None
            
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return None
        













def calcular_metricas(df, sucursal='Todas'):
    if sucursal != 'Todas':
        df = df[df['Sucursal'] == sucursal]
    
    # Calculamos precio por venta
    df['Precio_por_venta'] = df['Ingreso_total'] / df['Unidades_vendidas']
    
    metricas = df.groupby('Producto').agg({
        'Unidades_vendidas': 'sum',
        'Ingreso_total': 'sum',
        'Costo_total': 'sum',
        'Precio_por_venta': 'mean'  # Promedio real de precios
    }).reset_index()
    
    # Renombramos la columna
    metricas = metricas.rename(columns={'Precio_por_venta': 'Precio_promedio'})
    
    # Calculamos margen promedio
    metricas['Margen_promedio'] = (metricas['Ingreso_total'] - metricas['Costo_total']) / metricas['Ingreso_total'] *100
    metricas['Margen_promedio'] = metricas['Margen_promedio'].round(0)

    # Formatear margen promedio a dos decimales
    metricas['Margen_promedio'] = metricas['Margen_promedio'].map('{:.0f}%'.format)
    print(metricas)

    return metricas




def graficar_evolucion_ventas(df, sucursal='Todas'):
    if sucursal != 'Todas':
        df = df[df['Sucursal'] == sucursal]
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Preparar datos
    ventas_producto = df.groupby(['Año', 'Mes'])['Unidades_vendidas'].sum().reset_index()
    ventas_producto['Fecha'] = pd.to_datetime(ventas_producto['Año'].astype(str) + '-' + ventas_producto['Mes'].astype(str))
    ventas_producto = ventas_producto.sort_values('Fecha')
    
    # Graficar evolución de ventas
    ax.plot(ventas_producto['Fecha'], ventas_producto['Unidades_vendidas'], linestyle='-', label='Ventas')
    
    # Calcular y graficar línea de tendencia
    x = np.arange(len(ventas_producto))
    y = ventas_producto['Unidades_vendidas']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(ventas_producto['Fecha'], p(x), "r--", label='Tendencia')
    
    # Configurar gráfico
    ax.set_title('Evolución de Ventas')
    ax.set_xlabel('Período')
    ax.set_ylabel('Unidades Vendidas')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    return fig

def calcular_incremento(df, producto, metrica):
    """Calcula el incremento porcentual respecto al período anterior para una métrica específica."""
    df_producto = df[df['Producto'] == producto].copy()
    
    # Crear columna de fecha para ordenar
    df_producto['Fecha'] = pd.to_datetime(df_producto['Año'].astype(str) + '-' + df_producto['Mes'].astype(str) + '-01')
    
    # Ordenar por fecha
    df_producto = df_producto.sort_values('Fecha')
    
    # Calcular la métrica según el tipo
    if metrica == 'Margen_promedio':
        df_producto['Margen_promedio'] = ((df_producto['Ingreso_total'] - df_producto['Costo_total']) / 
                                           df_producto['Ingreso_total']) * 100
        df_mensual = df_producto.groupby(['Fecha']).agg({
            'Margen_promedio': 'mean'
        }).reset_index()
        df_mensual['Valor'] = df_mensual['Margen_promedio']
    elif metrica == 'Precio_promedio':
        df_producto['Precio_promedio'] = df_producto['Ingreso_total'] / df_producto['Unidades_vendidas']
        df_mensual = df_producto.groupby(['Fecha']).agg({
            'Precio_promedio': 'mean'
        }).reset_index()
        df_mensual['Valor'] = df_mensual['Precio_promedio']
    elif metrica == 'Unidades_vendidas':
        df_mensual = df_producto.groupby(['Fecha']).agg({
            'Unidades_vendidas': 'sum'
        }).reset_index()
        df_mensual['Valor'] = df_mensual['Unidades_vendidas']
    else:
        raise ValueError(f"Métrica no reconocida: {metrica}")
    
    # Ordenar por fecha
    df_mensual = df_mensual.sort_values('Fecha')
    
    # Verificar que hay al menos dos períodos para comparar
    if len(df_mensual) < 2:
        return 0.0  # No hay suficiente información para calcular el incremento
    
    # Obtener el valor actual y el valor del período anterior
    valor_actual = df_mensual['Valor'].iloc[-1]
    valor_anterior = df_mensual['Valor'].iloc[-2]
    
    # Calcular el incremento porcentual
    if valor_anterior == 0:
        return 0.0  # Evitar división por cero
    
    incremento = ((valor_actual - valor_anterior) / valor_anterior) * 100
    return round(incremento, 2)
def main():
    st.title('Análisis de Ventas')
    
    with st.sidebar:
        mostrar_informacion_alumno()
        df = cargar_datos()
        if df is None:
            return
        
        sucursales = ['Todas'] + list(df['Sucursal'].unique())
        sucursal_seleccionada = st.selectbox('Seleccione una sucursal:', sucursales)
    
    if df is not None:
        productos = df['Producto'].unique()
        
        for producto in productos:
            with st.container(border=True):
                st.subheader(f'Análisis de {producto}')
                
                col_metricas, col_grafico = st.columns([1, 2])
                
                with col_metricas:
                    df_producto = df[df['Producto'] == producto]
                    metricas = calcular_metricas(df_producto, sucursal_seleccionada)
                    
                    for idx, row in metricas.iterrows():
                        # Unidades vendidas
                        inc_unidades = calcular_incremento(df, producto, 'Unidades_vendidas')
                        st.metric(
                            "Unidades Vendidas", 
                            f"{int(row['Unidades_vendidas']):,}",
                            delta=f"{inc_unidades:.1f}%"
                        )
                        
                        # Precio promedio
                        inc_precio = calcular_incremento(df, producto, 'Precio_promedio')
                        st.metric(
                            "Precio Promedio",
                            f"${row['Precio_promedio']:,.2f}",
                            delta=f"{inc_precio:.1f}%"
                        )
                        
                        # Margen promedio
                        inc_margen = calcular_incremento(df, producto, 'Margen_promedio')
                        st.metric(
                            "Margen Promedio",
                            row['Margen_promedio'],
                            delta=f"{inc_margen:.1f}%"
                        )
                
                with col_grafico:
                    fig = graficar_evolucion_ventas(df_producto, sucursal_seleccionada)
                    st.pyplot(fig)
if __name__ == '__main__':
    main()