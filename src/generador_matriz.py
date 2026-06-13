import pandas as pd
import re


# ---------------------------------------------------------------------------
# HELPERS DE EXTRACCIÓN — claves ajustadas al Excel real de Marlovega
# ---------------------------------------------------------------------------

def _extraer_quien_cobra(datos_kickoff, tipo_propietario):
    """
    Lee quién cobra al inquilino según el tipo de propietario (Propio / Tercero).
    Las claves del Excel son específicas por tipo.
    """
    if tipo_propietario == "Propio":
        claves = [
            "En inmuebles propios: ¿quién cobra al inquilino?",
            "¿Quién cobra al inquilino? (propios)",
            "Quién cobra (propios)",
        ]
    else:
        claves = [
            "En inmuebles de terceros: ¿quién cobra al inquilino?",
            "¿Quién cobra al inquilino? (terceros)",
            "Quién cobra (terceros)",
        ]

    # Búsqueda exacta primero
    for clave in claves:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            return valor

    # Búsqueda parcial como fallback
    for clave, valor in datos_kickoff.items():
        if "cobra" in clave.lower() and tipo_propietario.lower() in clave.lower() and valor.strip():
            return valor.strip()

    # Fallback genérico
    for clave, valor in datos_kickoff.items():
        if "cobra" in clave.lower() and valor.strip():
            return valor.strip()

    return "Por definir — revisar con CS"


def _extraer_honorarios(datos_kickoff, tipo_inmueble):
    """
    Extrae el porcentaje de honorario para el tipo de inmueble dado.
    En el Excel real, el valor está en 'Porcentajes específicos' como texto libre:
      "8% sobre renta en viviendas; 6% sobre renta en locales"
    Lo parseamos con regex. Devuelve (descripcion, confianza).
    """
    # 1. Intentar clave directa por tipo de inmueble
    claves_directas = [
        f"Honorario {tipo_inmueble.lower()}",
        f"% honorario {tipo_inmueble.lower()}",
        f"Comisión {tipo_inmueble.lower()}",
    ]
    for clave in claves_directas:
        valor = datos_kickoff.get(clave, "").strip()
        if valor and valor.lower() not in ("n/a", "no", ""):
            return valor, "🟢 ALTA"

    # 2. Intentar clave genérica del Excel real
    claves_genericas = [
        "Porcentajes específicos",
        "Honorario / comisión de gestión",
        "Modelo de honorario",
        "Honorario",
        "Comisión de gestión",
    ]
    texto_honorarios = ""
    for clave in claves_genericas:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            texto_honorarios = valor
            break

    if not texto_honorarios:
        return "Por definir — revisar con CS", "🟡 MEDIA-BAJA"

    # 3. Parseo regex del texto libre: "8% sobre renta en viviendas; 6% sobre renta en locales"
    tipo_lower = tipo_inmueble.lower()

    # Mapa de palabras clave por tipo de inmueble
    palabras_clave = {
        "vivienda": ["vivienda", "residencial", "piso", "apartamento", "habitacion"],
        "local": ["local", "comercial", "oficina", "nave"],
        "garaje": ["garaje", "garage", "trastero", "parking"],
    }

    keywords = palabras_clave.get(tipo_lower, [tipo_lower])

    # Dividir por separadores comunes
    segmentos = re.split(r"[;,\n]", texto_honorarios)
    for segmento in segmentos:
        segmento_lower = segmento.lower()
        if any(kw in segmento_lower for kw in keywords):
            # Extraer el porcentaje del segmento
            match = re.search(r"(\d+(?:[.,]\d+)?%[^;,\n]*)", segmento)
            if match:
                return match.group(1).strip(), "🟢 ALTA"

    # 4. Si no encontramos match específico, devolver el texto completo con confianza media
    modelo_base = datos_kickoff.get("Modelo de honorario", "")
    if modelo_base:
        return f"{texto_honorarios} (modelo: {modelo_base})", "🟡 MEDIA"

    return texto_honorarios, "🟡 MEDIA"


def _extraer_dia_liquidacion(datos_kickoff):
    """
    Extrae el día de liquidación al propietario.
    En el Excel real la clave es 'Modelo de pago al propietario'.
    """
    claves = [
        "Modelo de pago al propietario",
        "Día de liquidación al propietario",
        "¿Cuándo se liquida al propietario?",
        "Liquidación",
        "Día liquidación",
    ]
    for clave in claves:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            return valor
    return "Día no especificado — revisar con CS"


def _extraer_datos_fiscales(datos_kickoff):
    """
    Extrae régimen fiscal y método de cobro directamente del Excel.
    Claves ajustadas al Excel real de Marlovega.
    """
    # Régimen fiscal — clave real: "Verifactu"
    claves_fiscal = [
        "Verifactu",
        "Régimen fiscal",
        "¿Está sujeto a SII?",
        "SII / Verifactu",
        "Régimen de facturación",
    ]
    regimen = ""
    for clave in claves_fiscal:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            regimen = valor
            break
    if not regimen:
        regimen = "No especificado — revisar con CS"

    # Método de cobro — clave real: "Pasarela de pago del inquilino"
    claves_cobro = [
        "Pasarela de pago del inquilino",
        "Método de cobro",
        "Forma de cobro",
        "Cobro por remesa SEPA",
        "¿Opera por remesa SEPA?",
    ]
    metodo = ""
    for clave in claves_cobro:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            metodo = valor
            break
    if not metodo:
        metodo = "No especificado — revisar con CS"

    return {"regimen_fiscal": regimen, "metodo_cobro": metodo}


# ---------------------------------------------------------------------------
# GENERADOR PRINCIPAL DE MATRIZ
# ---------------------------------------------------------------------------

def generar_matriz_casos(datos_kickoff):
    """
    Genera la matriz combinatoria adaptativa para TODOS los tipos de cliente.
    Claves ajustadas al Excel real de kickoff.
    """
    tipo_cliente_raw = datos_kickoff.get("Tipo de cliente", "").lower()
    tipos_inmueble_raw = datos_kickoff.get("Tipos de inmueble", "").lower()
    tipos_contrato_raw = datos_kickoff.get("Tipos de contrato", "").lower()

    # -----------------------------------------------------------------------
    # 1. Ramas de propietario
    # -----------------------------------------------------------------------
    ramas = []
    if "propio" in tipo_cliente_raw or "mixto" in tipo_cliente_raw or "patrimonial" in tipo_cliente_raw:
        ramas.append("Propio")
    if "tercero" in tipo_cliente_raw or "mixto" in tipo_cliente_raw:
        ramas.append("Tercero")

    if not ramas:
        return [{
            "#": 1,
            "Tipo propietario": "Por definir",
            "Tipo inmueble": "Por definir",
            "¿Quién cobra?": "Por definir",
            "Factura / Documento": "Por definir",
            "IVA": "Por definir",
            "Honorario": "N/A",
            "¿Hay liquidación?": "No",
            "Flujo Operativo / Alerta": "⚠️ Tipo de cliente no reconocido. Revisión manual obligatoria.",
            "Confianza": "🔴 BAJA",
        }]

    # -----------------------------------------------------------------------
    # 2. Tipos de activo
    # -----------------------------------------------------------------------
    activos_posibles = []
    if "vivienda" in tipos_inmueble_raw or "residencial" in tipos_inmueble_raw:
        activos_posibles.append(("Vivienda", "Habitual"))
    if "temporal" in tipos_contrato_raw or "temporal" in tipos_inmueble_raw:
        activos_posibles.append(("Vivienda", "Temporal"))
    if "local" in tipos_inmueble_raw or "comercial" in tipos_inmueble_raw:
        activos_posibles.append(("Local", "Comercial"))
    if "garaje" in tipos_inmueble_raw or "trastero" in tipos_inmueble_raw:
        activos_posibles.append(("Garaje/Trastero", "Anexo"))

    if not activos_posibles:
        activos_posibles = [("Por definir", "Por definir")]

    # -----------------------------------------------------------------------
    # 3. Datos transversales
    # -----------------------------------------------------------------------
    dia_liquidacion = _extraer_dia_liquidacion(datos_kickoff)

    # -----------------------------------------------------------------------
    # 4. Construcción de la matriz
    # -----------------------------------------------------------------------
    matriz_resultado = []
    contador = 1

    for propietario in ramas:
        quien_cobra = _extraer_quien_cobra(datos_kickoff, propietario)

        for inmueble, contrato in activos_posibles:

            # IVA
            if inmueble == "Local":
                iva = "21%"
            elif inmueble == "Garaje/Trastero":
                iva = "21% (independiente) / Exento (junto a vivienda)"
            elif contrato == "Temporal":
                iva = "10%"
            else:
                iva = "Exento"

            caso = {
                "#": contador,
                "Tipo propietario": propietario,
                "Tipo inmueble": f"{inmueble} ({contrato})",
                "¿Quién cobra?": quien_cobra,
                "Factura / Documento": "Por definir",
                "IVA": iva,
                "Honorario": "N/A",
                "¿Hay liquidación?": "No",
                "Flujo Operativo / Alerta": "Estándar",
                "Confianza": "🟢 ALTA",
            }

            # --- RAMA: PROPIO ---
            if propietario == "Propio":
                caso["¿Hay liquidación?"] = "No"
                caso["Honorario"] = "N/A"

                # Factura según lo que dice el Excel para inmuebles propios
                clave_factura_propio = "En inmuebles propios: ¿quién emite factura al inquilino?"
                factura_info = datos_kickoff.get(clave_factura_propio, "").strip()

                if iva == "Exento":
                    caso["Factura / Documento"] = "No se emite factura (Recibo)" if not factura_info else factura_info
                    caso["Flujo Operativo / Alerta"] = "Conciliación directa en cuenta patrimonial. Sin IVA repercutido."
                else:
                    caso["Factura / Documento"] = "Factura Cliente" if not factura_info else factura_info
                    caso["Flujo Operativo / Alerta"] = f"Emisión de factura al {iva}. Requiere serie contable específica."

                if "por definir" in iva.lower():
                    caso["Confianza"] = "🟡 MEDIA"

            # --- RAMA: TERCERO ---
            elif propietario == "Tercero":
                caso["¿Hay liquidación?"] = f"Sí ({dia_liquidacion})"

                honorario_valor, confianza_honorario = _extraer_honorarios(datos_kickoff, inmueble)
                caso["Honorario"] = honorario_valor

                if inmueble == "Local":
                    # El Excel dice: "El propietario emite factura al inquilino (21% IVA)."
                    clave_factura_local = "En inmuebles de terceros (local): ¿quién emite factura al inquilino?"
                    factura_local = datos_kickoff.get(clave_factura_local, "Propietario (Emisión externa)").strip()
                    caso["Factura / Documento"] = factura_local if factura_local else "Propietario (Emisión externa)"
                    caso["Confianza"] = "🟡 MEDIA-BAJA"
                    caso["Flujo Operativo / Alerta"] = (
                        "⚠️ ALERTA CS: Desacople financiero-fiscal. El propietario factura externamente "
                        "pero la gestora recauda. Validar Mandato de Facturación en homming."
                    )
                else:
                    # El Excel dice: "No se emite factura al inquilino (alquiler residencial exento)."
                    clave_factura_viv = "En inmuebles de terceros (vivienda): ¿cómo se factura?"
                    factura_viv = datos_kickoff.get(clave_factura_viv, "No se emite factura (Recibo)").strip()
                    caso["Factura / Documento"] = factura_viv if factura_viv else "No se emite factura (Recibo)"
                    caso["Confianza"] = confianza_honorario

                    if contrato == "Temporal":
                        caso["Flujo Operativo / Alerta"] = (
                            f"Liquidación con retención del honorario ({honorario_valor}). "
                            "Validar si la gestora emite factura delegada al 10% IVA en nombre del tercero."
                        )
                    else:
                        caso["Flujo Operativo / Alerta"] = (
                            f"Liquidación mensual ({dia_liquidacion}). "
                            "Validar si homming emite el justificante en nombre del tercero."
                        )

                    if "Por definir" in honorario_valor:
                        caso["Confianza"] = "🟡 MEDIA-BAJA"

            matriz_resultado.append(caso)
            contador += 1

    return matriz_resultado