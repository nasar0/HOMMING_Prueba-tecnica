# 📘 MANUAL DE CONFIGURACIÓN DE CLIENTE: Patrimoniales Alta Vista SL

---

## Sección 0 — Datos Rápidos de Control

* **Razón Social:** Patrimoniales Alta Vista SL
* **Modelo Operativo:** Propietario / Patrimonial Puro
* **Estructura Societaria:** Alta Vista Inversiones SL
* **Volumen Estimado:** 150 inmuebles propios
* **Tipología de Activos:** Viviendas residenciales y locales comerciales
* **Ecosistema de Contratos:** Habitual (LAU larga)
* **Legacy Software (Origen):** Excel / Tradicional
* **Nivel de Confianza de la Sección:** 🟢 ALTA (Datos explícitos mapeados desde el Excel)

---

## Sección 1 — Resumen Ejecutivo del Modelo de Negocio

El cliente Patrimoniales Alta Vista SL, con una estructura corporativa bajo Alta Vista Inversiones SL, gestiona una cartera de 150 inmuebles propios, operando principalmente con contratos de alquiler de larga duración (LAU). Al tratarse de un propietario patrimonial puro, no se aplican honorarios ni liquidaciones. Desde el punto de vista fiscal, se encuentra sujeto al régimen de Verifactu, con la aplicación de QR a partir de 2027, y utiliza el método de cobro mediante remesa SEPA.

* **Nivel de Confianza de la Sección:** 🟢 ALTA (Sintetizado a partir de datos reales del kickoff)

---

## Sección 2 — Matriz de Casos Operativa

|   # | Tipo propietario   | Tipo inmueble       | ¿Quién cobra?             | Factura / Documento                                         | IVA    | Honorario   | ¿Hay liquidación?   | Flujo Operativo / Alerta                                         | Confianza   |
|----:|:-------------------|:--------------------|:--------------------------|:------------------------------------------------------------|:-------|:------------|:--------------------|:-----------------------------------------------------------------|:------------|
|   1 | Propio             | Vivienda (Habitual) | Alta Vista Inversiones SL | Alta Vista Inversiones SL. IVA: vivienda exenta, local 21%. | Exento | N/A         | No                  | Conciliación directa en cuenta patrimonial. Sin IVA repercutido. | 🟢 ALTA      |
|   2 | Propio             | Local (Comercial)   | Alta Vista Inversiones SL | Alta Vista Inversiones SL. IVA: vivienda exenta, local 21%. | 21%    | N/A         | No                  | Emisión de factura al 21%. Requiere serie contable específica.   | 🟢 ALTA      |

* **Nivel de Confianza de la Sección:** 🟢 ALTA (Cartera Patrimonial Pura)
* **Análisis de Riesgo:**
Todas las combinaciones se resuelven de forma directa dentro de la cuenta patrimonial. No existen cuentas puente, comisiones de administración ni flujos de liquidación externos.

---

## Sección 3 — Reglas Globales y Políticas del Sistema

* Prorrateo de renta: Sí en todos los contratos al inicio del mes.
* Suministros: Gasto fijo mensual a cuenta asignado en contrato.
* Actualización de rentas (IPC/IRAV): 
  + Habitual: IPC Anual.
  + Temporal: ⚠️ Pendiente de validar con CS.
* Servicios adicionales repercutibles: Comunidad incluida en renta.
* Día de vencimiento de renta: Día 5 de cada mes.
* Conciliación bancaria: Sí, 1 cuenta centralizada en BBVA.

* **Nivel de Confianza de la Sección:** 🟢 ALTA
* **Análisis de Riesgo:** Las políticas de cobro, prorrateo e indexación se aplican de forma uniforme sobre la cartera propia. No se detectan dependencias de aprobación de terceros.
