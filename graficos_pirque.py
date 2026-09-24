import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# 1. Cargar el archivo CSV
df = pd.read_csv('caudales_pirque.csv')

# 2. Convertir la columna Fecha a objeto datetime
# Como el formato en el CSV es YYYY-MM-DD HH:MM:SS, pandas lo reconoce automáticamente
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# Limpiar valores nulos y eliminar registros duplicados
df = df.dropna(subset=['Fecha', 'Caudal'])
df = df.drop_duplicates(subset=['Estacion', 'Fecha']).sort_values('Fecha')

# 3. Directorio para guardar las imágenes
output_dir = 'graficos'
os.makedirs(output_dir, exist_ok=True)

# 4. Generar encabezado del README.md
readme_content = "# 📊 Monitoreo de Caudales Canal Pirque\n\n"
readme_content += "Visualización de caudales reportados en las estaciones del Canal Pirque.\n\n"
readme_content += ![Diagrama Unifilar Pirque](./unifilar_pirque.jpg)
readme_content += "> *Los gráficos se actualizan diariamente.*\n\n---\n\n"

# 5. Generar un gráfico por cada Estacion
estaciones = sorted(df['Estacion'].unique())

for estacion in estaciones:
    df_estacion = df[df['Estacion'] == estacion]

    plt.figure(figsize=(10, 4.5))
    plt.plot(
        df_estacion['Fecha'],
        df_estacion['Caudal'],
        marker='o',
        markersize=4,
        linestyle='-',
        color='#0366d6',
        linewidth=1.8,
    )

    # Configuración de título y ejes
    plt.title(f'{estacion}', fontsize=14, fontweight='bold', pad=12) 
    plt.ylabel('Caudal (l/s)', fontsize=10) 
    plt.xlabel('Fecha Reportada', fontsize=10)
    
    # Formato del eje X (una etiqueta por día, en formato dd-mm-yyyy)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator()) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) 
    plt.xticks(rotation=45, ha='right', fontsize=9) 

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # Normalizar el nombre del archivo
    filename = "".join(c if c.isalnum() else "_" for c in estacion).strip("_") + ".png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=120)
    plt.close()

    # Enlazar la imagen generada dentro del README.md
    readme_content += f"## {estacion}\n\n"
    readme_content += f"![{estacion}]({filepath})\n\n---\n\n"

# 6. Escribir o sobrescribir el README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("Gráficos y README.md actualizados correctamente.")
