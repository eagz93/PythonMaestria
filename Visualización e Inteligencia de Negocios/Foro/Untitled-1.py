# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv(r'D:\Documents\PythonMaestria\Visualización e Inteligencia de Negocios\Foro\Netflix_Customer _Subscription.csv')



print(df.head)

print(df.dtypes)


# Convertir la columna 'Date' a tipo datetime
df['Time Period'] = pd.to_datetime(df['Time Period'], format='%d-%m-%Y', errors='coerce')
# agregar columnas de año mes y día
df['Año'] = df['Time Period'].dt.year
df['Mes'] = df['Time Period'].dt.month
df['Día'] = df['Time Period'].dt.day
df['Periodo'] = df['Time Period'].dt.to_period('M').astype(str).str.replace('-', '')
df['Nombre_Mes'] = df['Time Period'].dt.strftime('%B')

print(df.head())


df_mensual=df.groupby('Año')['Subscribers'].sum().reset_index()

print(df_mensual.head())

# Visualizar la evolución de suscriptores
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x='Periodo', y='Subscribers')
plt.title('Evolución de Suscriptores')
plt.xlabel('Periodo')
plt.ylabel('Número de Suscriptores')
plt.xticks(rotation=45)

plt.show()

# Crear columna Trimestre
df['Trimestre'] = pd.to_datetime(df['Time Period']).dt.to_period('Q')

# Agrupar por Trimestre y calcular la suma de Suscriptores
df_trimestral = df.groupby(df['Trimestre'].dt.quarter)['Subscribers'].sum().reset_index()
df_trimestral.rename(columns={'Trimestre': 'Numero_Trimestre'}, inplace=True)
df_trimestral['Numero_Trimestre'] = 'Trimestre ' + df_trimestral['Numero_Trimestre'].astype(str)


# Configurar el estilo del gráfico
sns.set(style='darkgrid')
# Crear el gráfico de barras con el argumento `hue=x`
plt.figure(figsize=(8, 5))
ax = sns.barplot(x='Numero_Trimestre', y='Subscribers', hue='Numero_Trimestre', data=df_trimestral, palette='viridis',
legend=False)

# Agregar el valor a cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height()):,}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 9), 
                textcoords='offset points')

# Configurar título y etiquetas
plt.title('Cantidad de Suscriptores por Trimestre', fontsize=14)
plt.xlabel('Trimestre', fontsize=12)
plt.ylabel('Subscribers', fontsize=12)

# Mostrar gráfico
plt.show()


df["Fecha"] = pd.to_datetime(df["Time Period"])
#  Calcular la tasa de crecimiento trimestral
df["Tasa_Crecimiento"] = df["Subscribers"].pct_change() * 100

# Identificar los períodos de mayor caída
caidas_significativas = df[df["Tasa_Crecimiento"] < 0]

# Calcular el promedio de crecimiento anual
df["Año"] = df["Fecha"].dt.year
promedio_anual = df.groupby("Año")["Tasa_Crecimiento"].mean()

# Gráfico de líneas de tasa de crecimiento
plt.figure(figsize=(12, 6))
plt.plot(df["Fecha"], df["Tasa_Crecimiento"], marker='o', linestyle='-', color='r', label="Tasa de Crecimiento (%)")
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel("Fecha")
plt.ylabel("Tasa de Crecimiento (%)")
plt.title("Tasa de Crecimiento Trimestral de Suscriptores")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()


# Mostrar el promedio anual de crecimiento
print("Promedio anual de crecimiento:")
print(promedio_anual)

# Gráfico de barras de tasa de crecimiento por trimestre
df["Trimestre"] = df["Fecha"].dt.to_period("Q")
crecimiento_trimestral = df.groupby("Trimestre")["Tasa_Crecimiento"].sum() # o .mean() si prefieres el promedio

plt.figure(figsize=(15, 7))
ax = crecimiento_trimestral.plot(kind='bar', color='skyblue') # Store the axes object
for bar in ax.patches:
    if bar.get_height() < 0:
        bar.set_color('salmon') # Or any other color you prefer

plt.xlabel("Trimestre")
plt.ylabel("Tasa de Crecimiento (%)")
plt.title("Tasa de Crecimiento por Trimestre de Suscriptores")
plt.xticks(rotation=45, ha='right')
plt.tight_layout() # Ajusta el layout para que no se corten las etiquetas
plt.grid(axis='y')
plt.show()



