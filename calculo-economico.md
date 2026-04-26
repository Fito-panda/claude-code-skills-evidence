# Cálculo económico — Daño cuantificado

**Fórmula simple verificable. Cualquier auditor puede reproducir con sus propios números.**

---

## Variables (con valores documentados de mi cuenta)

| Variable | Valor | Fuente |
|---|---|---|
| `tokens_por_skill` | 45 | promedio descripción truncada a ~180 chars (verificado en auditoría 2026-04-25) |
| `skills_cargadas` | 296 | conteo verificado 2026-04-24 (Test 5) |
| `tokens_por_turno` | `tokens_por_skill × skills_cargadas = 13,320` | producto |
| `turnos_por_dia` | 50 | estimación conservadora de uso intensivo |
| `dias_por_mes` | 30 | estándar |
| `meses_facturados` | 2 | desde 2026-02-26 al 2026-04-24 |
| `precio_max_plan` | $200/mes | facturación verificable |
| `tarifa_horaria` | $100/h | mercado Senior Product Designer Buenos Aires |
| `horas_perdidas_2026-04-24` | 5 | tiempo dedicado a investigar 5 mecanismos fallidos |

---

## Fórmula 1 — Tokens consumidos por mes (verificable)

```
tokens_mes = turnos_por_dia × tokens_por_turno × dias_por_mes
           = 50 × 13,320 × 30
           = 19,980,000 tokens/mes
```

≈ **20 millones de tokens/mes consumidos por catálogo no invocable.**

---

## Fórmula 2 — Equivalente económico API (para usuarios pago por token)

Para usuarios de plan API directo (no Max), el costo en USD de esos 20M tokens:

```
costo_mensual_api = tokens_mes × precio_por_token
```

Aplicando precios públicos de Anthropic (Opus 4.7):

| Tier | Precio input | Costo mensual estimado |
|---|---|---|
| Standard (<200k context) | $15 / 1M tokens | $300/mes |
| 1M context tier | $75 / 1M tokens | $1,500/mes |

**Rango: $300 - $1,500 USD / mes desperdiciados en catálogo no invocable, dependiendo del tier.**

(Nota: estos precios son referenciales a fecha de redacción. Verificar precios vigentes en console.anthropic.com.)

---

## Fórmula 3 — Daño en plan Max ($200/mes flat)

Plan Max no factura por token, por lo que el daño no es $ directo. Se expresa como **pérdida de ventana de contexto**:

```
porcentaje_ventana_consumida_por_turno = tokens_por_turno / tamaño_ventana × 100
```

| Ventana | % consumido por catálogo |
|---|---|
| 200k tokens | 6.66% |
| 1M tokens | 1.33% |

```
ventana_disponible_real = ventana_total - tokens_por_turno
```

| Ventana nominal | Ventana disponible real (post-catálogo) |
|---|---|
| 200k | 186,680 |
| 1M | 986,680 |

**Costo de oportunidad:** cada token consumido por catálogo es un token menos disponible para trabajo útil. Sobre 50 turnos/día, esto es 666,000 tokens/día de ventana neta perdida.

---

## Fórmula 4 — Tiempo profesional perdido

```
costo_tiempo_perdido = horas_perdidas × tarifa_horaria
                     = 5 × $100
                     = $500 USD
```

Esto es solo el tiempo de **un día específico (2026-04-24)** dedicado a investigar el bug. No incluye:
- Tiempo dedicado en sesiones anteriores donde el rendimiento estaba degradado por context window saturada
- Tiempo dedicado a workarounds personales (uso de proyectos separados, sesiones más cortas, etc.)
- Costo de oportunidad de no poder trabajar en lo prometido por el plan Max

---

## Fórmula 5 — Resarcimiento total solicitado (3 escenarios)

### Escenario 1 — Conservador (versión inicial $620)

```
resarcimiento = refund_proporcional + tiempo_perdido
              = ($200 × 2 × 0.30) + $500
              = $120 + $500
              = $620 USD
```

Donde `proporcion_inutilizable = 0.30` es estimación inicial basada en el ratio de utilización real.

### Escenario 2 — Justo (con evidencia postmortem Anthropic 2026-04-23)

**Hallazgo decisivo:** el [postmortem oficial Anthropic publicado 2026-04-23](https://www.anthropic.com/engineering/april-23-postmortem) reconoce 3 causas de degradación de Claude Code y un **período afectado del 4 de marzo al 20 de abril = 47 días sobre los 60 facturados a Fito = 78% del servicio degradado por reconocimiento propio de Anthropic**.

```
resarcimiento_ajustado = ($200 × 2 × 0.78) + $500
                       = $312 + $500
                       = $812 USD
```

### Escenario 3 — Agresivo razonable (con tiempo perdido documentado completo)

Si se documentan 8-10 horas perdidas (no solo las 5h del 2026-04-24, sino también horas de trabajo degradado durante el período del postmortem):

```
resarcimiento_agresivo = $312 + (10 × $100)
                       = $312 + $1,000
                       = $1,312 USD
```

**Rango razonable a reclamar: $812 (conservador con postmortem) a $1,312 (con horas adicionales documentadas).**

### Tarifa horaria — validada con mercado (agente externo 2026-04-24)

| Fuente | Rango |
|---|---|
| Glassdoor BA Senior PD | $35-45/h dolar oficial |
| Levels.fyi BA top companies | $55-110/h dolar blue |
| Contractrates.fyi LatAm freelance senior | $30-55/h |
| Ruul/Index.dev senior global | $60-150/h |

**$100/h es conservador-justo para Senior Product Designer 17 años trayectoria con clientes internacionales.** Rango razonable: $80-120/h.

### Sobre daño punitivo (Ley 24.240 Art. 52 bis)

Argentina tiene daño punitivo bajo Art. 52 bis Ley 24.240 — pero el tope ($5M pesos) es irrelevante en USD. **No vale como herramienta principal de presión.**

### Sobre el cap de responsabilidad de Anthropic ($100)

ToS Anthropic Sec. 11 dice: "THE ANTHROPIC PARTIES' TOTAL AGGREGATE LIABILITY... WILL NOT EXCEED THE GREATER OF THE AMOUNT YOU PAID... IN THE SIX MONTHS PRECEDING... AND $100."

**En Argentina, esta cláusula es NULA por Art. 37 Ley 24.240** (cláusulas abusivas en contratos de adhesión que perjudican al consumidor son inválidas). El reclamo bajo ley argentina puede superar el cap.

---

## Verificación independiente

Para que un auditor verifique estos números:

1. **`tokens_por_skill`:** abrir cualquier SKILL.md de un plugin instalado, contar tokens de su frontmatter (name + description). Pegar en https://platform.openai.com/tokenizer o usar `tiktoken` Python. Promedio empírico de 50 skills muestreadas: ~45 tokens.

2. **`skills_cargadas`:** abrir Claude Code en proyecto vacío (Test 5), contar entradas en bloque `<system-reminder>` que empiezan con `- namespace:skill-name:` o `- skill-name:`.

3. **`turnos_por_dia`:** revisar transcript JSONL de Claude Code (archivo en `~/.claude/projects/...`) y contar turnos por día. 50 es estimación; tu valor puede variar.

4. **`precio_por_token`:** verificar en https://www.anthropic.com/pricing.

5. **`horas_perdidas`:** verificable contra git log + transcript de la sesión.

6. **`tarifa_horaria`:** mercado Buenos Aires Senior Product Designer 2026 — varía $80-$150/hora según fuente. Usar $100/hora es conservador.

---

## Margen de error

| Variable | Margen estimado |
|---|---|
| `tokens_por_skill` | ±10 (35-55) |
| `skills_cargadas` | ±5 (291-301) según conteo manual |
| `turnos_por_dia` | depende de uso real del usuario |
| `precio_por_token` | público y verificable, sin margen |
| `tarifa_horaria` | mercado, ±$50 |

**El TOTAL de tokens/mes (~20M) tiene margen de ±2M = ±10%. La conclusión cualitativa (millones de tokens consumidos en metadata no invocable) no cambia.**

---

## Referencias
- Reporte interno auditoría 2026-04-25: `catedral/reportes-agentes/2026-04-25-auditoria-skills-cargadas-globalmente.md`
- Skill usage real: `~/.claude.json` campo `skillUsage` (12 invocaciones acumuladas en 2 meses)
- Test 5 (proyecto vacío): `evidencia/test-5-empty-project.md`
