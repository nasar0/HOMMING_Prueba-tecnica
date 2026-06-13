# 📘 Pipeline Universal de Onboarding - Homming

Este programa es una herramienta automatizada en Python diseñada para procesar archivos de Kickoff (en formato Excel `.xlsx` o `.csv`) de nuevos clientes de **Homming**. A partir de estos datos, genera de forma automática y dinámica un **Manual de Configuración de Cliente** detallado en formato Markdown, optimizando el proceso de onboarding.

El sistema utiliza una arquitectura híbrida que combina un **motor de reglas deterministas** (para calcular la matriz de casos, IVA y flujos financieros) junto con **Inteligencia Artificial (Groq - Llama 3.3)** a través de Prompts adaptativos para redactar el resumen ejecutivo y estructurar las políticas globales del negocio del cliente.

---

## 🛠️ Características Principales

* **Lector Multiformato:** Carga y limpia automáticamente archivos Excel (`.xlsx`) y CSV (`.csv`), normalizando preguntas y respuestas.
* **Router de Prompts de IA:** Clasifica dinámicamente al cliente según su modelo operativo (Patrimonial Puro vs. Terceros/Mixto) para seleccionar el contexto y las instrucciones ideales para la IA (Groq).
* **Motor de Combinatoria:** Genera una matriz completa de casos operativos cruzando tipos de propietarios, tipos de activos (vivienda habitual, temporal, local, garaje) y contratos, asignando automáticamente reglas de IVA, honorarios y alertas financieras.
* **Evaluación de Confianza Dinámica:** Evalúa de forma automática el riesgo y el nivel de confianza de la información extraída, alertando sobre discrepancias financieras y fiscales comunes (como desfases entre quién cobra y quién factura).
* **Generación Automatizada:** Genera manuales listos para el equipo de Customer Success en la carpeta `manuals/`.

---

## 📂 Estructura del Proyecto

```text
homming/
│
├── data/                    # Archivos Excel/CSV de Kickoff de entrada
│   ├── kickoff_gestor_terceros.xlsx
│   ├── kickoff_propietario_puro.xlsx
│   └── kickoff_simplificado_marlovega.xlsx
│
├── src/                     # Código fuente de los módulos
│   ├── __init__.py
│   ├── conector_ia.py       # Conexión con Groq y plantillas/prompts de IA
│   ├── extractor_datos.py   # Carga, limpieza y parsing de los archivos Excel/CSV
│   └── generador_matriz.py  # Algoritmo de lógica y generación de matriz de casos
│
├── manuals/                 # Manuales generados en formato Markdown (.md)
│
├── docs/                    # Documentación de entrega del proyecto
│
├── .env.example             # Plantilla de variables de entorno
├── .env                     # Archivo con credenciales locales (creado al configurar)
├── main.py                  # Orquestador del pipeline principal
├── requirements.txt         # Dependencias del proyecto (Python)
├── package.json             # Metadatos del proyecto
└── README.md                # Esta guía de uso
```

---

## 🚀 Requisitos Previos e Instalación

### 1. Clonar o descargar el proyecto
Asegúrate de tener el código en tu máquina local.

### 2. Crear y activar un entorno virtual (Recomendado)
En tu terminal (dentro de la carpeta raíz del proyecto):

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
Instala las librerías necesarias con el siguiente comando:
```bash
pip install -r requirements.txt
```
*Las dependencias principales incluyen `pandas`, `openpyxl`, `groq`, `python-dotenv` y `tabulate` (para formatear tablas en Markdown).*

---

## ⚙️ Configuración del Entorno

El pipeline utiliza el modelo de lenguaje **Llama 3.3** a través de la API de **Groq** para generar los textos explicativos.

1. Duplica o renombra el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
2. Abre el archivo `.env` y coloca tu API Key de Groq:
   ```env
   # Configuración de API  
   GROQ_API_KEY=tu_api_key_de_groq_aqui
   ```
   *Puedes conseguir una clave gratuita o de pago registrándote en [Groq Console](https://console.groq.com/).*

---

## 📖 Instrucciones de Uso

### Paso 1: Preparar los datos
Coloca los archivos de kickoff (en formato `.xlsx` o `.csv`) dentro de la carpeta `data/`. El programa buscará automáticamente todos los archivos con extensión `.xlsx` dentro de esta carpeta para procesarlos.

> **Importante:** El archivo Excel/CSV debe contener al menos las columnas llamadas `Pregunta` y `Respuesta del cliente`.

### Paso 2: Ejecutar el Pipeline
Ejecuta el script principal desde la raíz del proyecto:
```bash
python main.py
```

El pipeline procesará cada archivo y mostrará en la terminal el progreso de ejecución:
```text
🚀 Ejecutando Pipeline Universal de Onboarding homming...

📂 Procesando: kickoff_gestor_terceros.xlsx
============================================================
🎉 Manual generado correctamente.
📄 Ruta de salida: manuals\kickoff_gestor_terceros.md
============================================================
```

### Paso 3: Ver los Resultados
Una vez finalizado, dirígete a la carpeta `manuals/`. Encontrarás un archivo `.md` (Markdown) con el nombre de cada archivo de kickoff procesado. Cada manual incluye:
1. **Datos Rápidos de Control:** Tabla resumen del cliente.
2. **Resumen Ejecutivo:** Un párrafo explicativo generado por la IA adaptado a su modelo operativo.
3. **Matriz de Casos Operativa:** Tabla detallada de cobros, facturación, IVA, retenciones, liquidaciones y alertas específicas.
4. **Reglas Globales:** Listado limpio y claro de las políticas de suministros, prorrateos, actualización de IPC, vencimiento de renta y conciliación bancaria.

---

## 🔍 Detalle de los Módulos de Código

* **[main.py](file:///c:/Users/Nasaro/OneDrive/Documentos/1barra/homming/main.py):** Orquestador central. Lee los archivos de entrada, invoca los módulos de extracción, cálculo de matriz y generación de textos, y ensambla el documento final en Markdown con las evaluaciones de confianza dinámica.
* **[src/extractor_datos.py](file:///c:/Users/Nasaro/OneDrive/Documentos/1barra/homming/src/extractor_datos.py):** Encargado de leer archivos Excel y CSV. Valida que el formato sea correcto, limpia filas vacías y mapea los datos en un diccionario de Python de forma flexible.
* **[src/generador_matriz.py](file:///c:/Users/Nasaro/OneDrive/Documentos/1barra/homming/src/generador_matriz.py):** Implementa la lógica de negocio para construir las casuísticas de arrendamiento. Calcula si aplica IVA (21%, 10% o Exento), si hay honorarios de gestión (utilizando expresiones regulares para leer porcentajes detallados en texto libre), si hay liquidación y genera alertas sobre posibles problemas operativos (por ejemplo, cuando el propietario factura directamente pero la gestora recauda).
* **[src/conector_ia.py](file:///c:/Users/Nasaro/OneDrive/Documentos/1barra/homming/src/conector_ia.py):** Gestiona la conexión con la API de Groq. Diseña los prompts dinámicos de sistema y de usuario según el tipo de cliente para estructurar el resumen ejecutivo y las reglas globales de negocio.
