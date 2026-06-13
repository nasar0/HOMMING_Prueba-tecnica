import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_ENV_KEY = "GROQ_API_KEY"


def obtener_cliente_groq():
    api_key = os.getenv(_ENV_KEY)
    if not api_key:
        raise EnvironmentError(
            f"No se encontró la clave API. Define '{_ENV_KEY}' en tu archivo .env"
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# HELPERS: lectura de datos desde el Excel real
# ---------------------------------------------------------------------------

def _leer_regimen_fiscal(datos_kickoff):
    """
    Lee el régimen fiscal. En el Excel real la clave es 'Verifactu'.
    """
    claves = [
        "Verifactu",
        "Régimen fiscal",
        "¿Está sujeto a SII?",
        "SII / Verifactu",
        "Régimen de facturación",
    ]
    for clave in claves:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            return valor
    return "No especificado en el Excel — revisar con CS"


def _leer_metodo_cobro(datos_kickoff):
    """
    Lee el método de cobro. En el Excel real la clave es 'Pasarela de pago del inquilino'.
    """
    claves = [
        "Pasarela de pago del inquilino",
        "Método de cobro",
        "Forma de cobro",
        "Cobro por remesa SEPA",
        "¿Opera por remesa SEPA?",
        "Gestión bancaria",
    ]
    for clave in claves:
        valor = datos_kickoff.get(clave, "").strip()
        if valor:
            return valor
    return "No especificado en el Excel — revisar con CS"


# ---------------------------------------------------------------------------
# SECCIÓN 1: RESUMEN EJECUTIVO
# ---------------------------------------------------------------------------

def generar_resumen_ejecutivo(datos_kickoff):
    """
    Sección 1: Resumen Ejecutivo con Router de Prompt.
    Todos los datos se leen del Excel — ningún valor hardcodeado.
    """
    client = obtener_cliente_groq()
    tipo_cliente = datos_kickoff.get("Tipo de cliente", "").lower()
    regimen_fiscal = _leer_regimen_fiscal(datos_kickoff)
    metodo_cobro = _leer_metodo_cobro(datos_kickoff)

    # Router de prompts
    if "tercero" not in tipo_cliente and ("propio" in tipo_cliente or "patrimonial" in tipo_cliente):
        prompt_sistema = (
            "Eres un AI Process Engineer senior en homming. El cliente es un PROPIETARIO PATRIMONIAL PURO.\n"
            "REGLAS:\n"
            "1. Síntesis analítica de 2-3 frases. Sin jerga comercial.\n"
            "2. El cliente gestiona solo su propia cartera: no aplican liquidaciones ni honorarios.\n"
            "3. Menciona su régimen fiscal, método de cobro y estructura societaria tal como aparecen en los datos.\n"
            "4. Devuelve ÚNICAMENTE el párrafo. Sin títulos ni viñetas."
        )
    else:
        prompt_sistema = (
            "Eres un AI Process Engineer senior en homming. El cliente tiene modelo MIXTO o de TERCEROS.\n"
            "REGLAS:\n"
            "1. Síntesis analítica de 2-3 frases. Sin adjetivos comerciales.\n"
            "2. Explicita la división entre cartera propia y administrada, con modelos de honorarios.\n"
            "3. Menciona la complejidad de recaudación centralizada, liquidaciones a propietarios y régimen fiscal.\n"
            "4. Devuelve ÚNICAMENTE el párrafo. Sin títulos ni viñetas."
        )

    prompt_usuario = (
        f"Genera el resumen basándote EXCLUSIVAMENTE en estos datos reales del kickoff:\n"
        f"- Cliente: {datos_kickoff.get('Cliente (razón social principal)', 'N/A')}\n"
        f"- Perfil Operativo: {datos_kickoff.get('Tipo de cliente', 'N/A')}\n"
        f"- Estructura Corporativa: {datos_kickoff.get('Sociedades emisoras de factura', 'N/A')}\n"
        f"- Volumen de activos: {datos_kickoff.get('Volumen total de inmuebles', 'N/A')}\n"
        f"- Tipos de contrato: {datos_kickoff.get('Tipos de contrato', 'N/A')}\n"
        f"- Modelo de honorario: {datos_kickoff.get('Modelo de honorario', 'N/A')}\n"
        f"- Porcentajes de honorario: {datos_kickoff.get('Porcentajes específicos', 'N/A')}\n"
        f"- Régimen fiscal: {regimen_fiscal}\n"
        f"- Método de cobro: {metodo_cobro}\n"
    )

    try:
        respuesta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_tokens=250,
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error en la generación del resumen ejecutivo: {e}"


# ---------------------------------------------------------------------------
# SECCIÓN 3: REGLAS GLOBALES
# ---------------------------------------------------------------------------

def estructurar_reglas_globales(datos_kickoff):
    """
    Sección 3: Transcriptor de políticas del cliente.
    """
    client = obtener_cliente_groq()

    prompt_sistema = (
        "Eres un AI Process Engineer para la Sección 3 (Reglas Globales) del Manual de Cliente de homming.\n"
        "Transforma las anotaciones del kickoff en una lista Markdown estructurada.\n"
        "Si una regla varía por tipo de contrato (Habitual vs Temporal), añade sub-viñetas explícitas.\n"
        "Si un dato aparece como 'No especificado', márcalo con '⚠️ Pendiente de validar con CS'.\n"
        "Tono técnico y directo. Devuelve solo las viñetas, sin cabecera."
    )

    prompt_usuario = (
        f"Formatea las siguientes reglas de negocio:\n"
        f"- Prorrateo de renta: {datos_kickoff.get('Prorrateo de renta', 'No especificado')}\n"
        f"- Suministros: {datos_kickoff.get('Suministros', 'No especificado')}\n"
        f"- Actualización de rentas (IPC/IRAV): {datos_kickoff.get('Actualización de rentas', 'No especificado')}\n"
        f"- Servicios adicionales repercutibles: {datos_kickoff.get('Servicios adicionales', 'No especificado')}\n"
        f"- Día de vencimiento de renta: {datos_kickoff.get('Día de vencimiento de la renta', 'No especificado')}\n"
        f"- Conciliación bancaria: {datos_kickoff.get('Conciliación bancaria', 'No especificado')}\n"
    )

    try:
        respuesta = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0,
            max_tokens=400,
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error en la ordenación de reglas globales: {e}"