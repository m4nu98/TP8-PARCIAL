import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

## ATENCION: Debe colocar la direccion en la que ha sido publicada la aplicacion en la siguiente linea\
# url = 'https://tp8-555555.streamlit.app/'

def mostrar_informacion_alumno():
    with st.container(border=True):
        st.markdown('**Legajo:** 55.555')
        st.markdown('**Nombre:** Juan Pérez')
        st.markdown('**Comisión:** C1')

mostrar_informacion_alumno()

def cargar_datos():
    try:
        # Cargar el archivo CSV
        df = pd.read_csv('gaseosas.csv')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def calcular_metricas(df, sucursal='Todas'):
    if sucursal != 'Todas':
        df = df[df['Sucursal'] == sucursal]
    
    metricas = df.groupby('Producto').agg({
        'Unidades_vendidas': 'sum',
        'Ingreso_total': 'sum',
        'Costo_total': 'sum'
    }).reset_index()
    
    metricas['Precio_promedio'] = metricas['Ingreso_total'] / metricas['Unidades_vendidas']
    metricas['Margen_promedio'] = (metricas['Ingreso_total'] - metricas['Costo_total']) / metricas['Ingreso_total']
    
    return metricas

def main():
    st.title('Análisis de Ventas')
    mostrar_informacion_alumno()
    
    # Cargar datos
    df = cargar_datos()
    if df is None:
        return
    
    # Selector de sucursal
    sucursales = ['Todas'] + list(df['Sucursal'].unique())
    sucursal_seleccionada = st.selectbox('Seleccione una sucursal:', sucursales)
    
    # Mostrar métricas
    metricas = calcular_metricas(df, sucursal_seleccionada)
    st.subheader('Métricas por Producto')
    st.dataframe(metricas)

if __name__ == '__main__':
    main()

def graficar_evolucion_ventas(df, sucursal='Todas'):
    if sucursal != 'Todas':
        df = df[df['Sucursal'] == sucursal]
    
    # Usar el código del notebook para el gráfico
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ventas_producto = df.groupby(['Año', 'Mes', 'Producto'])['Unidades_vendidas'].sum().reset_index()
    productos = df['Producto'].unique()

    for producto in productos:
        data = ventas_producto[ventas_producto['Producto'] == producto]
        ax.plot(data['Año'].astype(str) + '-' + data['Mes'].astype(str), 
                data['Unidades_vendidas'], 
                label=producto)

    ax.set_title('Ventas por Producto')
    ax.set_xlabel('Período (Año-Mes)')
    ax.set_ylabel('Unidades Vendidas')
    ax.legend()
    plt.xticks(rotation=90)
    
    return fig

def main():
    st.title('Análisis de Ventas')
    mostrar_informacion_alumno()
    
    # Cargar datos
    df = cargar_datos()
    if df is None:
        return
    
    # Selector de sucursal
    sucursales = ['Todas'] + list(df['Sucursal'].unique())
    sucursal_seleccionada = st.selectbox('Seleccione una sucursal:', sucursales)
    
    # Mostrar métricas
    metricas = calcular_metricas(df, sucursal_seleccionada)
    st.subheader('Métricas por Producto')
    st.dataframe(metricas)
    
    # Mostrar gráfico
    st.subheader('Evolución de Ventas')
    fig = graficar_evolucion_ventas(df, sucursal_seleccionada)
    st.pyplot(fig)