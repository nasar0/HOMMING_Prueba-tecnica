# 📘 MANUAL DE CONFIGURACIÓN DE CLIENTE: Rentals Gestión Gandía SL

---

## Sección 0 — Datos Rápidos de Control

* **Razón Social:** Rentals Gestión Gandía SL
* **Modelo Operativo:** Gestor de Terceros (Property Manager)
* **Estructura Societaria:** Rentals Gestión Gandía SL (solo para el cobro de comisiones a propietarios)
* **Volumen Estimado:** 450 inmuebles pertenecientes a 120 propietarios externos
* **Tipología de Activos:** Viviendas residenciales y alquileres temporales vacacionales
* **Ecosistema de Contratos:** Habitual (LAU larga) y contratos Temporales (estudiantes de septiembre a junio)
* **Legacy Software (Origen):** Rentger
* **Nivel de Confianza de la Sección:** 🟢 ALTA (Datos explícitos mapeados desde el Excel)

---

## Sección 1 — Resumen Ejecutivo del Modelo de Negocio

La gestión de Rentals Gestión Gandía SL se divide en cartera propia y administrada, con un modelo de honorarios que establece un porcentaje fijo sobre la renta efectivamente pagada por el inquilino, siendo del 10% para contratos habituales y del 12% para alquileres temporales. La complejidad de la recaudación centralizada y las liquidaciones a propietarios se ve influenciada por el régimen fiscal, que no aplica de forma directa a la gestora para los alquileres, pero sí requiere la emisión de facturas de honorarios bajo normativa general. La gestión de 450 inmuebles pertenecientes a 120 propietarios externos a través de contratos habituales y temporales, con un método de cobro mediante remesas masivas SEPA, agrega una capa adicional de complejidad a la operación.

* **Nivel de Confianza de la Sección:** 🟢 ALTA (Sintetizado a partir de datos reales del kickoff)

---

## Sección 2 — Matriz de Casos Operativa

|   # | Tipo propietario   | Tipo inmueble       | ¿Quién cobra?                    | Factura / Documento                                                                                                                                    | IVA    | Honorario                                                                                                                                                    | ¿Hay liquidación?                                                                                | Flujo Operativo / Alerta                                                                                                                                                                                                                                                               | Confianza   |
|----:|:-------------------|:--------------------|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|:-------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|
|   1 | Tercero            | Vivienda (Habitual) | N/A (No tiene inmuebles propios) | Alquiler residencial habitual exento de IVA. No se emite factura al inquilino; se emite recibo de cobro desde la plataforma en nombre del propietario. | Exento | 10% sobre renta cobrada en contratos habituales; 12% en alquileres temporales (modelo: Porcentaje fijo sobre la renta efectivamente pagada por el inquilino) | Sí (Liquidaciones agrupadas los días 5 y 20 de cada mes (según el ciclo de cobro del inquilino)) | Liquidación mensual (Liquidaciones agrupadas los días 5 y 20 de cada mes (según el ciclo de cobro del inquilino)). Validar si homming emite el justificante en nombre del tercero.                                                                                                     | 🟡 MEDIA     |
|   2 | Tercero            | Vivienda (Temporal) | N/A (No tiene inmuebles propios) | Alquiler residencial habitual exento de IVA. No se emite factura al inquilino; se emite recibo de cobro desde la plataforma en nombre del propietario. | 10%    | 10% sobre renta cobrada en contratos habituales; 12% en alquileres temporales (modelo: Porcentaje fijo sobre la renta efectivamente pagada por el inquilino) | Sí (Liquidaciones agrupadas los días 5 y 20 de cada mes (según el ciclo de cobro del inquilino)) | Liquidación con retención del honorario (10% sobre renta cobrada en contratos habituales; 12% en alquileres temporales (modelo: Porcentaje fijo sobre la renta efectivamente pagada por el inquilino)). Validar si la gestora emite factura delegada al 10% IVA en nombre del tercero. | 🟡 MEDIA     |

* **Nivel de Confianza de la Sección:** 🟡 MEDIA-BAJA (Fricciones estructurales detectadas en la gestión de terceros)
* **Análisis de Riesgo:**
  * Los casos patrimoniales (propios) cuentan con confianza alta al ser directos.
  * Los casos de **Terceros** presentan riesgo de desacople financiero-fiscal: el propietario puede facturar externamente mientras la gestora recauda. Se aconseja validar con el KAM la activación de un Mandato de Facturación en homming.
  * Los honorarios marcados como '🟡 MEDIA-BAJA' deben confirmarse con el cliente antes de configurar homming.

---

## Sección 3 — Reglas Globales y Políticas del Sistema

* Prorrateo de renta: 
  + Habitual: Sí, al inicio del alquiler
  + Temporal: No especificado ⚠️ Pendiente de validar con CS
* Suministros: 
  + Los recibos llegan a nombre del propietario
  + La gestora los paga mediante cuenta puente y los repercute como un concepto adicional en el recibo del mes siguiente al inquilino
* Actualización de rentas (IPC/IRAV): 
  + Habitual: Indexado al IGC (Índice de Garantía de Competitividad) anual
  + Temporal: No hay actualización
* Servicios adicionales repercutibles: 
  + Habitual: No especificado ⚠️ Pendiente de validar con CS
  + Temporal: Cobro extra de limpieza final fija contratada
* Día de vencimiento de renta: Plazo estricto del día 1 al 5 de cada mes
* Conciliación bancaria: Sí, 1 cuenta operativa puente en CaixaBank para recaudación y liquidación

* **Nivel de Confianza de la Sección:** 🟡 MEDIA
* **Análisis de Riesgo:** La política de refacturación de suministros o servicios adicionales puede introducir complejidad en la administración de terceros. Requiere definir el proceso de carga de facturas de proveedores externos para evitar duplicidades contables.
