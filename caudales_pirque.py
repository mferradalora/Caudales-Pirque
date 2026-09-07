import requests
import pandas as pd
import os

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
                except Exception:
                    pass

    if registros_totales:
        df_nuevo = pd.DataFrame(registros_totales)
        
        try:
            df_nuevo['Fecha'] = pd.to_datetime(df_nuevo['Timestamp'], unit='ms')
            df_nuevo = df_nuevo[['Estacion', 'Fecha', 'Caudal', 'Unidad', 'Timestamp']]
        except Exception:
            print("No se pudo convertir el timestamp automáticamente.")
            
        nombre_archivo = 'caudales_pirque.csv'
        
        # --- LÓGICA ANTI-DUPLICADOS ---
        if os.path.exists(nombre_archivo):
            df_existente = pd.read_csv(nombre_archivo)
            if 'Fecha' in df_existente.columns:
                df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'])
            
            # Combinar datos existentes con nuevos
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            # Eliminar duplicados basados en Estacion y Timestamp
            df_final = df_final.drop_duplicates(subset=['Estacion', 'Timestamp'], keep='last')
        else:
            df_final = df_nuevo

        # Ordenar por estación y fecha
        df_final = df_final.sort_values(by=['Estacion', 'Fecha']).reset_index(drop=True)
        
        # Guardar archivo completo limpio
        df_final.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"\n✅ Datos procesados y guardados en: {nombre_archivo}")
        print(f"Total de registros acumulados: {len(df_final)}")
    else:
        print("La petición fue exitosa, pero no se encontraron datos de caudal.")

else:
    print(f"Error {response.status_code} al consultar la API.")
