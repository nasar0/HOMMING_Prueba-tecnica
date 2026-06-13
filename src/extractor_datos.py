import pandas as pd
import os


def cargar_y_limpiar_kickoff(ruta_archivo):
    """
    Carga el archivo de kickoff detectando automáticamente si es un Excel (.xlsx)
    o un CSV (.csv). Gestiona encodings, limpia filas vacías y devuelve un diccionario.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Error Crítico: No se encuentra el archivo en la ruta: {ruta_archivo}")

    _, extension = os.path.splitext(ruta_archivo.lower())
    df = None

    if extension == '.xlsx':
        try:
            df = pd.read_excel(ruta_archivo)
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Excel (.xlsx): {e}")

    elif extension == '.csv':
        encodings = ['utf-8', 'latin-1', 'cp1252']
        separadores = [',', ';']

        for enc in encodings:
            for sep in separadores:
                try:
                    df = pd.read_csv(ruta_archivo, encoding=enc, sep=sep)
                    if 'Pregunta' in df.columns:
                        break
                except Exception:
                    continue
            if df is not None and 'Pregunta' in df.columns:
                break
    else:
        raise ValueError(f"Formato no soportado: solo se admiten .xlsx o .csv (Recibido: {extension})")

    if df is None or 'Pregunta' not in df.columns:
        raise ValueError("Error Estructural: El archivo no contiene la columna obligatoria 'Pregunta'.")

    df.columns = df.columns.str.strip()
    df_limpio = df.dropna(subset=['Respuesta del cliente'])
    df_limpio['Pregunta'] = df_limpio['Pregunta'].astype(str).str.strip()
    df_limpio['Respuesta del cliente'] = df_limpio['Respuesta del cliente'].astype(str).str.strip()

    diccionario_datos = dict(zip(df_limpio['Pregunta'], df_limpio['Respuesta del cliente']))

    return diccionario_datos