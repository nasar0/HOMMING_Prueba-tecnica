# 📘 MANUAL DE CONFIGURACIÓN DE CLIENTE: Inversiones Marlovega SL

---

## Sección 0 — Datos Rápidos de Control

* **Razón Social:** Inversiones Marlovega SL
* **Modelo Operativo:** Mixto: tiene inmuebles propios y gestiona inmuebles de terceros
* **Estructura Societaria:** Marlovega Patrimonio SL (inmuebles propios) y Marlovega Gestión SL (inmuebles de terceros). Holding Marlovega SL agrupa ambas.
* **Volumen Estimado:** 300 (aprox. 200 propios + 100 de terceros)
* **Tipología de Activos:** Viviendas residenciales y locales comerciales
* **Ecosistema de Contratos:** Habitual (LAU larga) en mayoría. Temporal en algunos casos.
* **Legacy Software (Origen):** Inmosoft (van a migrar a homming)
* **Nivel de Confianza de la Sección:** 🟢 ALTA (Datos explícitos mapeados desde el Excel)

---

## Sección 1 — Resumen Ejecutivo del Modelo de Negocio

Inversiones Marlovega SL opera bajo un modelo mixto, con una cartera propia gestionada a través de Marlovega Patrimonio SL y una cartera administrada de terceros a través de Marlovega Gestión SL, ambas bajo el holding Marlovega SL. La estructura de honorarios se basa en un porcentaje sobre la renta cobrada, con un 8% para viviendas y un 6% para locales. La gestión de la cartera implica una complejidad adicional debido a la recaudación centralizada, las liquidaciones a propietarios y el régimen fiscal, aunque en este caso no aplica debido a que están acogidos al SII, y el método de cobro se realiza mayoritariamente a través de remesa SEPA y en algunos casos mediante transferencia.

* **Nivel de Confianza de la Sección:** 🟢 ALTA (Sintetizado a partir de datos reales del kickoff)

---

## Sección 2 — Matriz de Casos Operativa

|   # | Tipo propietario   | Tipo inmueble       | ¿Quién cobra?                     | Factura / Documento                                                                             | IVA    | Honorario                   | ¿Hay liquidación?                                    | Flujo Operativo / Alerta                                                                                                                              | Confianza    |
|----:|:-------------------|:--------------------|:----------------------------------|:------------------------------------------------------------------------------------------------|:-------|:----------------------------|:-----------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------|
|   1 | Propio             | Vivienda (Habitual) | Marlovega Patrimonio (el cliente) | Marlovega Patrimonio. IVA: vivienda exenta, local 21%.                                          | Exento | N/A                         | No                                                   | Conciliación directa en cuenta patrimonial. Sin IVA repercutido.                                                                                      | 🟢 ALTA       |
|   2 | Propio             | Vivienda (Temporal) | Marlovega Patrimonio (el cliente) | Marlovega Patrimonio. IVA: vivienda exenta, local 21%.                                          | 10%    | N/A                         | No                                                   | Emisión de factura al 10%. Requiere serie contable específica.                                                                                        | 🟢 ALTA       |
|   3 | Propio             | Local (Comercial)   | Marlovega Patrimonio (el cliente) | Marlovega Patrimonio. IVA: vivienda exenta, local 21%.                                          | 21%    | N/A                         | No                                                   | Emisión de factura al 21%. Requiere serie contable específica.                                                                                        | 🟢 ALTA       |
|   4 | Tercero            | Vivienda (Habitual) | Marlovega Patrimonio (el cliente) | No se emite factura al inquilino (alquiler residencial exento). El cliente cobra como gestor.   | Exento | 8% sobre renta en viviendas | Sí (Liquidación mensual el día 10 del mes siguiente) | Liquidación mensual (Liquidación mensual el día 10 del mes siguiente). Validar si homming emite el justificante en nombre del tercero.                | 🟢 ALTA       |
|   5 | Tercero            | Vivienda (Temporal) | Marlovega Patrimonio (el cliente) | No se emite factura al inquilino (alquiler residencial exento). El cliente cobra como gestor.   | 10%    | 8% sobre renta en viviendas | Sí (Liquidación mensual el día 10 del mes siguiente) | Liquidación con retención del honorario (8% sobre renta en viviendas). Validar si la gestora emite factura delegada al 10% IVA en nombre del tercero. | 🟢 ALTA       |
|   6 | Tercero            | Local (Comercial)   | Marlovega Patrimonio (el cliente) | El propietario emite factura al inquilino (21% IVA). El cliente cobra como gestor en su nombre. | 21%    | 6% sobre renta en locales   | Sí (Liquidación mensual el día 10 del mes siguiente) | ⚠️ ALERTA CS: Desacople financiero-fiscal. El propietario factura externamente pero la gestora recauda. Validar Mandato de Facturación en homming.    | 🟡 MEDIA-BAJA |

* **Nivel de Confianza de la Sección:** 🟡 MEDIA-BAJA (Fricciones estructurales detectadas en la gestión de terceros)
* **Análisis de Riesgo:**
  * Los casos patrimoniales (propios) cuentan con confianza alta al ser directos.
  * Los casos de **Terceros** presentan riesgo de desacople financiero-fiscal: el propietario puede facturar externamente mientras la gestora recauda. Se aconseja validar con el KAM la activación de un Mandato de Facturación en homming.
  * Los honorarios marcados como '🟡 MEDIA-BAJA' deben confirmarse con el cliente antes de configurar homming.

---

## Sección 3 — Reglas Globales y Políticas del Sistema

* Prorrateo de renta:
  + Contratos habituales: Sí (inicio y fin)
  + Contratos temporales: No
* Suministros: Refacturación al inquilino del gasto real del propietario
* Actualización de rentas (IPC/IRAV):
  + Contratos habituales: IPC anual en LAU larga, último publicado
  + Contratos temporales: No se actualiza
* Servicios adicionales repercutibles: Tasas de basura e IBI repercutibles en algunos contratos (definidos a nivel contrato)
* Día de vencimiento de renta:
  + Mayoría de contratos: Día 1 del mes
  + Algunos contratos: Día 15
* Conciliación bancaria: Sí, 2 cuentas: una por sociedad (Santander e ING)

* **Nivel de Confianza de la Sección:** 🟡 MEDIA
* **Análisis de Riesgo:** La política de refacturación de suministros o servicios adicionales puede introducir complejidad en la administración de terceros. Requiere definir el proceso de carga de facturas de proveedores externos para evitar duplicidades contables.
