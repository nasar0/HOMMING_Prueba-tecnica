import os
import pandas as pd
from src.extractor_datos import cargar_y_limpiar_kickoff
from src.generador_matriz import generar_matriz_casos
from src.conector_ia import generar_resumen_ejecutivo, estructurar_reglas_globales


# ---------------------------------------------------------------------------
# EVALUACIÓN DE CONFIANZA DINÁMICA
# ---------------------------------------------------------------------------

def _evaluar_confianza_secciones(tipo_cliente):
    """
    Devuelve los textos de confianza y análisis de riesgo para las secciones 2 y 3
    según el perfil del cliente. Lógica centralizada para no duplicarla.
    """
    tipo = tipo_cliente.lower()

    if "tercero" in tipo or "mixto" in tipo:
        confianza_matriz = "🟡 MEDIA-BAJA (Fricciones estructurales detectadas en la gestión de terceros)"
        analisis_riesgo_matriz = (
            "  * Los casos patrimoniales (propios) cuentan con confianza alta al ser directos.\n"
            "  * Los casos de **Terceros** presentan riesgo de desacople financiero-fiscal: "
            "el propietario puede facturar externamente mientras la gestora recauda. "
            "Se aconseja validar con el KAM la activación de un Mandato de Facturación en homming.\n"
            "  * Los honorarios marcados como '🟡 MEDIA-BAJA' deben confirmarse con el cliente antes de configurar homming."
        )
        confianza_reglas = "🟡 MEDIA"
        analisis_riesgo_reglas = (
            "La política de refacturación de suministros o servicios adicionales puede introducir "
            "complejidad en la administración de terceros. Requiere definir el proceso de carga "
            "de facturas de proveedores externos para evitar duplicidades contables."
        )
    else:
        confianza_matriz = "🟢 ALTA (Cartera Patrimonial Pura)"
        analisis_riesgo_matriz = (
            "Todas las combinaciones se resuelven de forma directa dentro de la cuenta patrimonial. "
            "No existen cuentas puente, comisiones de administración ni flujos de liquidación externos."
        )
        confianza_reglas = "🟢 ALTA"
        analisis_riesgo_reglas = (
            "Las políticas de cobro, prorrateo e indexación se aplican de forma uniforme sobre la cartera propia. "
            "No se detectan dependencias de aprobación de terceros."
        )

    return confianza_matriz, analisis_riesgo_matriz, confianza_reglas, analisis_riesgo_reglas


# ---------------------------------------------------------------------------
# ENSAMBLADOR DE MARKDOWN
# ---------------------------------------------------------------------------

def construir_manual_cliente_markdown(datos, resumen, matriz, reglas):
    """
    Ensambla el Manual de Cliente completo en Markdown a partir de los
    resultados de cada módulo del pipeline.
    """
    # Lectura dinámica del nombre — nunca hardcodeado
    cliente_nombre = datos.get("Cliente (razón social principal)", "Cliente sin identificar")
    tipo_cliente = datos.get("Tipo de cliente", "")

    # Tabla de la Sección 2
    df_matriz = pd.DataFrame(matriz)
    tabla_markdown = df_matriz.to_markdown(index=False)

    # Evaluación de confianza dinámica
    confianza_matriz, analisis_riesgo_matriz, confianza_reglas, analisis_riesgo_reglas = (
        _evaluar_confianza_secciones(tipo_cliente)
    )

    contenido_manual = f"""# 📘 MANUAL DE CONFIGURACIÓN DE CLIENTE: {cliente_nombre}

---

## Sección 0 — Datos Rápidos de Control

* **Razón Social:** {cliente_nombre}
* **Modelo Operativo:** {datos.get('Tipo de cliente', 'N/A')}
* **Estructura Societaria:** {datos.get('Sociedades emisoras de factura', 'N/A')}
* **Volumen Estimado:** {datos.get('Volumen total de inmuebles', 'N/A')}
* **Tipología de Activos:** {datos.get('Tipos de inmueble', 'N/A')}
* **Ecosistema de Contratos:** {datos.get('Tipos de contrato', 'N/A')}
* **Legacy Software (Origen):** {datos.get('Software previo', 'N/A')}
* **Nivel de Confianza de la Sección:** 🟢 ALTA (Datos explícitos mapeados desde el Excel)

---

## Sección 1 — Resumen Ejecutivo del Modelo de Negocio

{resumen}

* **Nivel de Confianza de la Sección:** 🟢 ALTA (Sintetizado a partir de datos reales del kickoff)

---

## Sección 2 — Matriz de Casos Operativa

{tabla_markdown}

* **Nivel de Confianza de la Sección:** {confianza_matriz}
* **Análisis de Riesgo:**
{analisis_riesgo_matriz}

---

## Sección 3 — Reglas Globales y Políticas del Sistema

{reglas}

* **Nivel de Confianza de la Sección:** {confianza_reglas}
* **Análisis de Riesgo:** {analisis_riesgo_reglas}
"""
    return contenido_manual


# ---------------------------------------------------------------------------
# PIPELINE PRINCIPAL
# ---------------------------------------------------------------------------

def ejecutar_pipeline_onboarding():
    """
    Punto de entrada del pipeline. Procesa todos los .xlsx en la carpeta /data
    y genera un Manual de Cliente en Markdown en /manuals por cada uno.
    """
    print("🚀 Ejecutando Pipeline Universal de Onboarding homming...")

    os.makedirs("manuals", exist_ok=True)

    archivos_excel = [f for f in os.listdir("data") if f.endswith(".xlsx")]

    if not archivos_excel:
        print("⚠️  No se encontraron archivos .xlsx en la carpeta /data. Abortando.")
        return

    for nombre_archivo in archivos_excel:
        ruta_entrada = os.path.join("data", nombre_archivo)
        ruta_salida = os.path.join("manuals", nombre_archivo.replace(".xlsx", ".md"))

        print(f"\n📂 Procesando: {nombre_archivo}")

        try:
            # 1. Extracción y limpieza del Excel
            datos_cliente = cargar_y_limpiar_kickoff(ruta_entrada)

            # 2. Generación de la Sección 2 (determinista)
            matriz_casos = generar_matriz_casos(datos_cliente)

            # 3. Generación de Sección 1 y Sección 3 (IA)
            resumen = generar_resumen_ejecutivo(datos_cliente)
            reglas = estructurar_reglas_globales(datos_cliente)

            # 4. Ensamblaje del documento final
            documento_final = construir_manual_cliente_markdown(
                datos_cliente, resumen, matriz_casos, reglas
            )

            # 5. Escritura del archivo de salida
            with open(ruta_salida, "w", encoding="utf-8") as archivo:
                archivo.write(documento_final)

            print("=" * 60)
            print("🎉 Manual generado correctamente.")
            print(f"📄 Ruta de salida: {ruta_salida}")
            print("=" * 60)

        except FileNotFoundError as e:
            print(f"❌ Archivo no encontrado: {e}")
        except ValueError as e:
            print(f"❌ Error estructural en el Excel: {e}")
        except EnvironmentError as e:
            print(f"❌ Error de configuración del entorno: {e}")
        except Exception as e:
            print(f"❌ ERROR INESPERADO en el pipeline [{nombre_archivo}]: {e}")


if __name__ == "__main__":
    ejecutar_pipeline_onboarding()