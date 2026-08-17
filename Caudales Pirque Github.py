#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import os # <-- Necesario para verificar si el archivo ya existe

url = "https://amaruserver.captahydro.com/graphql"

graphql_query = """
query GetPublicOrganization($input: PublicOrganizationInput!, $pagination: PaginationInput) {
  publicOrganization(input: $input) {
    id
    name
    devices(pagination: $pagination) {
      nodes {
        name
        id
        telemetry {
          flow {
            data
            decimals
            unit
            __typename
          }
          level {
            data
            decimals
            unit
            __typename
          }
          __typename
        }
        __typename
      }
      pageInfo {
        count
        limit
        offset
        pageNumber
        totalCount
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

variables = {
    "input": {
        "name": "Asociación de Canalistas de Pirque"
    },
    "pagination": {
        "limit": 50,
        "offset": 0
    }
}

payload = {
    "operationName": "GetPublicOrganization",
    "query": graphql_query,
    "variables": variables
}

headers = {
    "Content-Type": "application/json"
}

print("Realizando petición al servidor...")
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    json_data = response.json()
    
    try:
        nodos = json_data['data']['publicOrganization']['devices']['nodes']
    except KeyError:
        print("La estructura del JSON no es la esperada.")
        nodos = []
        
    registros_totales = []
    
    for nodo in nodos:
        nombre_estacion = nodo.get('name', 'Desconocida')
        telemetry = nodo.get('telemetry')
        
        if not telemetry:
            continue
            
        flow = telemetry.get('flow')
        
        if flow and flow.get('data'):
            datos_serie = flow.get('data')
            unidad = flow.get('unit', 'L/s')
            
            for punto in datos_serie:
                try:
                    if isinstance(punto, list) and len(punto) >= 2:
                        timestamp = punto[0]
                        caudal = punto[1]
                        
                        registros_totales.append({
                            'Estacion': nombre_estacion,
                            'Timestamp': timestamp,
                            'Caudal': caudal,
                            'Unidad': unidad
                        })
                    elif isinstance(punto, dict):
                        registros_totales.append({
                            'Estacion': nombre_estacion,
                            'Timestamp': punto.get('x'),
                            'Caudal': punto.get('y'),
                            'Unidad': unidad
                        })
                except Exception as e:
                    pass

    if registros_totales:
        df = pd.DataFrame(registros_totales)
        
        try:
            df['Fecha'] = pd.to_datetime(df['Timestamp'], unit='ms')
            df = df[['Estacion', 'Fecha', 'Caudal', 'Unidad', 'Timestamp']]
        except Exception:
            print("No se pudo convertir el timestamp automáticamente.")
            
        print("\n¡Datos extraídos con éxito! Muestra de las primeras filas:")
        print(df.head())
        
        # --- NUEVA LÓGICA PARA ACUMULAR EN CSV ---
        nombre_archivo = 'caudales_pirque.csv'
        
        # Verificamos si el archivo ya existe
        archivo_existe = os.path.isfile(nombre_archivo)
        
        # mode='a' significa "Añadir" (Append) en lugar de sobreescribir
        # header=not archivo_existe asegura que las cabeceras solo se escriban la primera vez
        df.to_csv(nombre_archivo, mode='a', index=False, header=not archivo_existe, encoding='utf-8')
        
        print(f"\n✅ Datos agregados exitosamente a: {nombre_archivo}")
        
    else:
        print("La petición fue exitosa, pero no se encontraron datos de caudal.")

else:
    print(f"Error {response.status_code} al consultar la API.")

