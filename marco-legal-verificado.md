# Marco legal verificado — Reclamo consumidor argentino vs Anthropic PBC

**Validado por agente externo 2026-04-24 con citas textuales de fuentes oficiales.**

---

## Postmortem Anthropic (evidencia central)

**URL exacta:** https://www.anthropic.com/engineering/april-23-postmortem
**Título:** "An update on recent Claude Code quality reports"
**Publicado:** 2026-04-23

**3 causas reconocidas por Anthropic:**

| Fecha | Causa | Revertido |
|---|---|---|
| 2026-03-04 | Reducción de reasoning effort de "high" a "medium" para bajar latencia | 2026-04-07 |
| 2026-03-26 | Bug en cache que limpiaba el razonamiento de Claude cada turno (debía limpiar solo en sesión inactiva) | 2026-04-10 |
| 2026-04-16 | Instrucción en system prompt para reducir verbosidad que dañó calidad de coding | 2026-04-20 |

**Período total degradado reconocido: 2026-03-04 a 2026-04-20 = 47 días.**

**Compensación ofrecida por Anthropic:** reset de límites de uso para todos los suscriptores al 2026-04-23. **Sin refund monetario.**

**Coberturas externas:**
- VentureBeat: https://venturebeat.com/technology/mystery-solved-anthropic-reveals-changes-to-claudes-harnesses-and-operating-instructions-likely-caused-degradation
- Fortune: https://fortune.com/2026/04/24/anthropic-engineering-missteps-claude-code-performance-decline-user-backlash/
- Simon Willison: https://simonwillison.net/2026/Apr/24/recent-claude-code-quality-reports/

**Aplicabilidad al caso de Fito:**
- Fito contrató plan Max desde 2026-02-26.
- Postmortem afectó del 2026-03-04 al 2026-04-20 = 47 días.
- Sobre 60 días facturados (al 2026-04-24): **78% del servicio fue degradado por reconocimiento propio de Anthropic.**
- Evidencia central para reclamo de refund proporcional: $400 × 0.78 = $312.

---

## Argentina — Ley 24.240 Defensa del Consumidor

**Fuente oficial:** https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/638/texact.htm

### Art. 4 — Información

> *"El proveedor está obligado a suministrar al consumidor en forma cierta, clara y detallada todo lo relacionado con las características esenciales de los bienes y servicios que provee, y las condiciones de su comercialización."*

**Aplicación:** Anthropic documentó `enabledPlugins` como mecanismo funcional. El comportamiento real (catálogo de 296 skills sin filter funcional) contradice la obligación de información "cierta y detallada".

### Art. 19 — Cumplimiento de lo ofrecido (PINZA MÁS FUERTE)

> *"Quienes presten servicios de cualquier naturaleza están obligados a respetar los términos, plazos, condiciones, modalidades, reservas y demás circunstancias conforme a las cuales hayan sido ofrecidos, publicitados o convenidos."*

**Aplicación:** servicio ofrecido/publicitado con `enabledPlugins` funcionando. Bug stale en GitHub `#40789` evidencia que el mecanismo no opera según lo convenido. **Es el artículo más fuerte del caso.**

### Art. 37 — Cláusulas abusivas (anula el cap $100 de Anthropic)

> Cláusulas abusivas en contratos de adhesión que perjudiquen al consumidor son **NULAS**.

**Aplicación:** ToS Anthropic Sec. 11 limita responsabilidad al "GREATER OF THE AMOUNT YOU PAID IN THE SIX MONTHS PRECEDING AND $100". Esta cláusula es nula en Argentina.

### Art. 52 bis — Daño punitivo

Permite multa civil al proveedor que no cumple sus obligaciones legales, a favor del consumidor. **Tope $5M pesos = irrelevante en USD pero útil como presión.**

### Art. 8 bis — Trato digno + no diferenciación a extranjeros

> *"No podrán ejercer sobre los consumidores extranjeros diferenciación alguna sobre precios, calidades técnicas o comerciales..."*

**Aplicación:** si Anthropic ofrece configurabilidad documentada que no funciona, y el consumidor argentino tiene canales de reclamo asimétricos vs el usuario estadounidense, hay diferenciación en calidad técnica efectiva.

### Competencia jurisdiccional

- Aplica cuando el consumidor está en Argentina, independiente de sede del proveedor.
- Autoridad de aplicación: Secretaría de Comercio Interior.
- **COPREC** (Conciliación Previa en Relaciones de Consumo) — mediación previa **obligatoria, gratuita, online, sin abogado**.

---

## Argentina — Ley 25.326 Protección de Datos Personales

**Fuente oficial:** https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm

### Art. 4.1 — Calidad de datos

> *"Los datos personales que se recojan a los efectos de su tratamiento deben ser ciertos, adecuados, pertinentes y no excesivos en relación al ámbito y finalidad para los que se hubieren obtenido."*

**Aplicación secundaria:** procesamiento de 296 skills (cuando 12 fueron invocadas en 2 meses) no cumple principio de "no excesivos". Sin mecanismo de opt-out funcional, hay tratamiento de datos no consentido por falla del sistema.

---

## California — CCPA (NO APLICA a Fito)

**Fuente oficial:** https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.110

### §1798.140(i) — Definición de Consumer

> *"Consumer means a natural person who is a California resident, as defined in Section 17014 of Title 18 of the California Code of Regulations."*

**Conclusión:** CCPA NO se aplica a Adolfo Prunotto como residente de Buenos Aires. **Esta vía queda cerrada como base directa de reclamo.** California Attorney General puede recibir queja informativa pero NO con base CCPA.

---

## ToS Anthropic — análisis cláusula por cláusula

**Fuente:** https://www.anthropic.com/legal/consumer-terms

| Cláusula | Texto | Clasificación |
|---|---|---|
| **Sec. 11 — As-Is** | *"THE SERVICES, OUTPUTS, AND ACTIONS ARE PROVIDED ON AN 'AS IS' AND 'AS AVAILABLE' BASIS... WITHOUT WARRANTIES OF ANY KIND..."* | **AMBIGUA** — Anthropic la usará como escudo, pero NO puede eliminar obligaciones legales irrenunciables del país donde opera. **Art. 19 Ley 24.240 prevalece.** |
| **Sec. 11 — Cap $100** | *"TOTAL AGGREGATE LIABILITY... WILL NOT EXCEED THE GREATER OF THE AMOUNT YOU PAID IN THE SIX MONTHS PRECEDING AND $100."* | **AMBIGUA** — limita reclamo monetario. **NULA en Argentina por Art. 37 Ley 24.240.** |
| **Sec. 6 — No reembolso** | *"Except as expressly provided in these Terms or **where required by law**, all payments are non-refundable."* | **PROTEGE A FITO** — la excepción "where required by law" habilita el refund bajo Ley 24.240. |
| **Sec. 4 — Opt-out de entrenamiento** | *"We may use Materials to provide, maintain, and improve the Services... unless you opt out of training **through your account settings**."* | **CONTRADICE** — el mismo mecanismo de "account settings" prometido (incluido `enabledPlugins`) no funciona. Si settings no opera, el consentimiento granular es ilusorio. |
| **Privacy Sec. 4 — Right to know** | *"Right to know: the right to know what personal data Anthropic processes about you... Deletion: the right to request..."* | **PROTEGE A FITO** — base para solicitar log de tokens procesados por sesión y auditoría costo real vs documentado. |

---

## Recomendación de foco (orden de aplicación)

### Pinza primaria
**Art. 19 Ley 24.240 + Sec. 6 ToS ("where required by law")**

Es la pinza más fuerte. Art. 19 obliga a cumplir lo publicitado (mecanismo `enabledPlugins`); la excepción legal en el no-reembolso de Anthropic abre la puerta al refund sin necesitar probar dolo.

### Pinza secundaria
**Art. 4 Ley 24.240 + contradicción Sec. 4 ToS**

La documentación de `enabledPlugins` como funcional es "información cierta" prometida que no se cumple. El bug stale en GitHub es evidencia de incumplimiento sostenido y conocido.

### Pinza neutralizadora
**Art. 37 Ley 24.240 anula el cap de $100 de Anthropic**

Cualquier intento de Anthropic de invocar el cap de responsabilidad puede neutralizarse citando esta nulidad.

### Pinza adicional
**Postmortem oficial Anthropic 2026-04-23**

Es admisión propia de la empresa de que el servicio estuvo degradado 47 días. **Evidencia central que cualquier mediador o regulador puede leer en 2 minutos.**

---

## Ruta procesal recomendada (validada por agente externo)

| Orden | Canal | Costo | Tiempo | Probabilidad |
|---|---|---|---|---|
| **1** | Email directo a `support@anthropic.com` citando postmortem + reclamando refund proporcional ajustado ($312 + $500 = $812) | $0 | 1-15 días | Media-alta. Anthropic ya reconoce el bug, hay chance real de credit. |
| **2** | COPREC (coprec.gob.ar) — mediación previa obligatoria | $0 | 3-8 meses | Alta de respuesta formal. Anthropic obligado a responder bajo Ley 24.240. |
| **3** | FTC US (reportfraud.ftc.gov) + California AG (oag.ca.gov) — quejas paralelas informativas | $0 | 2-6 meses | Sin compensación directa pero queda registro en jurisdicción Anthropic. |
| **4** | Justicia civil AR | Alto (abogado + costas) | 3-7 años | Baja — sentencia inejecutable contra empresa sin domicilio AR. **No vale para reclamos <$5k.** |

**Veredicto del agente externo:** la ruta 1+2+3 cubre el 90% del valor sin abogado. Solo escalar a 4 si el daño documentado supera $5,000 USD.

---

**Firma:** Marco verificado por agente externo 2026-04-24 con citas oficiales. Para uso del cliente y de su abogado. Actualizable si nuevos hallazgos lo contradicen.
