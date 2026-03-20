# ================================================
# CREACION Y LIMPIEZA DEL DATASET DE SALUD
# ================================================

import pandas as pd
import numpy as np
from datetime import datetime

print("="*60)
print("INICIANDO PROCESO DE CREACIÓN DEL DATASET")
print("="*60)

# --- 1. CARGAR DATOS ---
print("\n📁 Cargando archivo Excel...")
nombre_archivo = 'PILOTO_SEMIAUTOMATICO_28_FEBRERO_2025.xlsx'
try:
    df_bruto = pd.read_excel(nombre_archivo, sheet_name='Hoja1')
    print(f"✅ Archivo cargado exitosamente")
    print(f"   Filas: {df_bruto.shape[0]}, Columnas: {df_bruto.shape[1]}")
except Exception as e:
    print(f"❌ Error al cargar el archivo: {e}")
    print("   Verifica que el archivo esté en la carpeta correcta")
    exit()

# --- 2. EXPLORACIÓN INICIAL ---
print("\n📊 Información del dataset:")
print(df_bruto.info())
print(f"\nPrimeras filas:\n{df_bruto.head()}")

# --- 3. LIMPIEZA DE DATOS ---
print("\n🧹 Iniciando limpieza...")
df_limpio = df_bruto.copy()

# Eliminar duplicados
df_limpio = df_limpio.drop_duplicates()
print(f"✅ Duplicados eliminados")

# Eliminar columnas vacías
df_limpio = df_limpio.dropna(axis=1, how='all')
print(f"✅ Columnas vacías removidas")

print("\n✨ Proceso completado exitosamente")

vars = df_limpio.columns.tolist()
print("\n📋 Columnas en el dataset:")
for i, col in enumerate(vars, start=1):
    print(f"   {i}. {col}")

df_cleaned = df_limpio.copy()

# Manejo de valores faltantes para 'FECHA FACT'
# Imputar con la moda (fecha más frecuente)
if df_cleaned['FECHA FACT'].isnull().any():
    mode_fecha_fact = df_cleaned['FECHA FACT'].mode()[0]
    df_cleaned['FECHA FACT'].fillna(mode_fecha_fact, inplace=True)

# Descriptive statistics for categorical/object columns (value counts)
print("\nFrecuencia de Valores para Columnas Categóricas/Objeto:")
for column in df_cleaned.select_dtypes(include='object').columns:
    print(f"\nColumna: {column}")
    print(df_cleaned[column].value_counts(dropna=False).head(10))

# Visualizaciones para columnas categóricas 
import matplotlib.pyplot as plt
import seaborn as sns  
# Visualización de la distribución de 'TIPO DE SERVICIO'
plt.figure(figsize=(10, 6))
sns.countplot(data=df_cleaned, x='TIPO DE SERVICIO', order=df_cleaned['TIPO DE SERVICIO'].value_counts().index)
plt.title('Distribución de TIPO DE SERVICIO')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 'Factura' - Top 10
plt.figure(figsize=(12, 6))
top_10_facturas = df_cleaned['Factura'].value_counts().head(10)
sns.barplot(y=top_10_facturas.index, x=top_10_facturas.values, palette='viridis')
plt.title('Top 10 Facturas más Frecuentes')
plt.xlabel('Conteo')
plt.ylabel('Factura')
plt.show()

# 'AUTORIZACION' - Distribution
plt.figure(figsize=(10, 6))
sns.countplot(x=df_cleaned['AUTORIZACION'], palette='cubehelix')
plt.title('Distribución de AUTORIZACION')
plt.xlabel('AUTORIZACION')
plt.ylabel('Conteo')
plt.xticks(rotation=45)
plt.show()

# 'COD SERVICIO' - Top 10
plt.figure(figsize=(12, 6))
top_10_cod_servicio = df_cleaned['COD SERVICIO'].value_counts().head(10)
sns.barplot(y=top_10_cod_servicio.index.astype(str), x=top_10_cod_servicio.values, palette='rocket')
plt.title('Top 10 Códigos de Servicio más Frecuentes')
plt.xlabel('Conteo')
plt.ylabel('Código de Servicio')
plt.show()

# 'DIAGNOSTICO' - Top 10
plt.figure(figsize=(12, 6))
top_10_diagnostico = df_cleaned['DIAGNOSTICO'].value_counts().head(10)
sns.barplot(y=top_10_diagnostico.index, x=top_10_diagnostico.values, palette='mako')
plt.title('Top 10 Diagnósticos más Frecuentes')
plt.xlabel('Conteo')
plt.ylabel('Diagnóstico')
plt.show()

# Manejo de valores faltantes para 'Valor Radicado'
# Imputar con la mediana para evitar distorsionar con valores extremos

daily_valor_radicado = df_cleaned.groupby(df_cleaned['FECHA FACT'].dt.date)['Valor Radicado'].sum().reset_index()
daily_valor_radicado['FECHA FACT'] = pd.to_datetime(daily_valor_radicado['FECHA FACT'])

plt.figure(figsize=(15, 7))
sns.lineplot(x='FECHA FACT', y='Valor Radicado', data=daily_valor_radicado)
plt.title('Tendencia del Valor Radicado por Fecha')
plt.xlabel('Fecha')
plt.ylabel('Suma de Valor Radicado')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Identificar registros con problemas de fecha o valor radicado
problematic_records = df_cleaned[df_cleaned['FECHA FACT'].isnull() | df_cleaned['Valor Radicado'].isnull()]
print(f"\nRecords with problematic dates or values: {problematic_records.shape[0]}")
print("\nProblematic Records:")
print(problematic_records.head())


# Análisis de series de tiempo para 'FECHA FACT' si corresponde
# Agrupar por fecha y sumar 'Valor Radicado'
daily_valor_radicado = df_cleaned.groupby(df_cleaned['FECHA FACT'].dt.date)['Valor Radicado'].sum().reset_index()
daily_valor_radicado['FECHA FACT'] = pd.to_datetime(daily_valor_radicado['FECHA FACT'])
plt.figure(figsize=(15, 7))
sns.lineplot(x='FECHA FACT', y='Valor Radicado', data=daily_valor_radicado)
plt.title('Tendencia del Valor Radicado por Fecha')
plt.xlabel('Fecha')
plt.ylabel('Suma de Valor Radicado')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Eliminar columnas con porcentajes muy altos de valores faltantes o que se consideren poco informativas.
columns_to_drop = ['Unnamed: 18', 'DIAGNOSTICO.1', 'Unnamed: 18', 'CASO']
df_limpio = df_limpio.drop(columns=columns_to_drop, errors='ignore')
print(f"✅ Columnas poco informativas eliminadas")

print(f"Dropped columns: {columns_to_drop}")
print("\nDataFrame after dropping columns (first 5 rows):")
display(df_cleaned.head())

print("\nDataFrame Info after dropping columns:")
df_cleaned.info()

# Vuelva a comprobar los valores que faltan en las columnas restantes.
problemas_fecha_fact = df_limpio[df_limpio['FECHA FACT'].isnull()]
print(f"\nRecords with problematic dates: {problemas_fecha_fact.shape[0]}")
print("\nProblematic Records (FECHA FACT):")
print(problemas_fecha_fact.head())

# Descriptive statistics for categorical/object columns (value counts)
print("\nFrecuencia de Valores para Columnas Categóricas/Objeto:")
for column in df_cleaned.select_dtypes(include='object').columns:
    print(f"\nColumna: {column}")
    print(df_cleaned[column].value_counts(dropna=False).head(10))
    
#Entorno de Ejecución: Google Colaboratory (basado en Jupyter Notebooks).
#Versión de Python: La versión de Python que se está utilizando en este entorno de Colab es 3.10.12.
#Puedes verificar esto ejecutando el siguiente código en una celda: !python --version

#Librerías utilizadas:
#pandas: Para la manipulación y análisis de datos (lectura de Excel, DataFrames, manejo de valores nulos, estadísticas descriptivas).
#matplotlib: Para la creación de gráficos estáticos.
#seaborn: Para la creación de visualizaciones estadísticas atractivas, construido sobre matplotlib.
#tarfile: Para la extracción de archivos comprimidos .tar.xz.
#os: Módulo estándar de Python para interactuar con el sistema operativo (listado de archivos y directorios).
#datetime: Para el manejo de fechas y horas.

# evidencia de la limpieza de datos
print("\n📊 Estadísticas descriptivas para columnas numéricas:")
print(df_cleaned.describe())
print("\n📋 Columnas en el dataset después de la limpieza:")
print(df_cleaned.columns.tolist())

#problemas específicos antes de la limpieza
problemas_fecha_fact = df_cleaned[df_cleaned['FECHA FACT'].isnull()]
print(f"\nRegistros sin fecha de factura: {len(problemas_fecha_fact):,}")
print("\nEjemplo de registros sin fecha de factura:")
print(problemas_fecha_fact.head())

# Confusion matrix visualization (commented out - requires y_true and y_pred to be defined)
# from sklearn.metrics import confusion_matrix
# mc = confusion_matrix(y_true, y_pred)
# plt.figure(figsize=(8, 6))
# sns.heatmap(mc, annot=True, fmt='d', cmap='Blues')
# plt.title('Matriz de Confusión')
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.show()


# datos nuevos después de la limpieza
print("\n📊 Estadísticas descriptivas para columnas numéricas después de la limpieza:")
print(df_cleaned.describe())
print("\n📋 Columnas en el dataset después de la limpieza:")
print(df_cleaned.columns.tolist())

# Calcular la matriz de confusión
# from sklearn.metrics import confusion_matrix
# y_true = [...]  # Reemplaza con tus etiquetas verdaderas1
# y_pred = [...]  # Reemplaza con tus etiquetas predichas
# mc = confusion_matrix(y_true, y_pred)
# Visualizar la matriz de confusión
# plt.figure(figsize=(8, 6))
# sns.heatmap(mc, annot=True, fmt='d', cmap='Blues')
# plt.title('Matriz de Confusión')
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.show()
