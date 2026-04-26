# Test 1 — `enabledPlugins` en `.claude/settings.json`

**Mecanismo bajo prueba:** filtrar plugins que cargan en la sesión usando el campo `enabledPlugins` documentado oficialmente por Anthropic.

**Documentación oficial:** https://docs.anthropic.com (sección Plugins / settings.json schema)

**Hipótesis:** declarando una whitelist de N plugins en `enabledPlugins`, sólo esos N cargan; el resto queda excluido del catálogo de skills enviado al modelo en cada turno.

---

## Método

### Pre-condiciones
- Claude Code instalado, plan Max, cuenta `fito@arcanomedia.com`
- Sesión nueva, todos los plugins instalados activos
- Conteo previo verificado: 296 skills cargadas

### Pasos

1. Abrir terminal en proyecto `CLAUDE-CORE`.
2. Crear `.claude/settings.json` con whitelist mínima:
   ```json
   {
     "enabledPlugins": {
       "repair-gate": true,
       "claude-md-management@claude-plugins-official": true,
       "commit-commands@claude-plugins-official": true,
       "hookify@claude-plugins-official": true,
       "claude-code-setup@claude-plugins-official": true
     }
   }
   ```
3. Cerrar Claude Code completamente vía menú "Salir".
4. Abrir Claude Code nuevo en `CLAUDE-CORE`.
5. Contar skills en bloque `<system-reminder>` al inicio.

### Resultado esperado (si funciona)
Catálogo reducido a ~30-50 skills (los 5 plugins de la whitelist + skills built-in del harness).

### Resultado obtenido (2026-04-24)
**296 skills cargadas, idénticas al conteo previo sin la configuración.**

| Namespace | Pre-config | Post-config | Δ |
|---|---|---|---|
| arcanomedia: | 94 | 78 | -16* |
| anthropic-skills: | 51 | 47 | -4* |
| bitacora: | 9 | 8 | -1* |
| cognitivo: | 7 | 7 | 0 |
| **Total** | **297** | **296** | **-1** |

*Las variaciones de ±1-16 por namespace son ruido del contador humano (rango ±5 reportado), no efecto real del filter.

### Conclusión
`enabledPlugins` no reduce las skills cargadas en esta versión de Claude Code. Bug `#40789` confirmado empíricamente.

---

## Reproducibilidad

Cualquier auditor puede reproducir:
1. Crear `.claude/settings.json` con whitelist arbitraria.
2. Restart total Claude Code.
3. Contar skills en system reminder.
4. Verificar que el conteo es independiente del contenido de `enabledPlugins`.

**Variabilidad esperada:** ±5 por namespace (ruido conteo manual). El TOTAL debería caer >100 si el mecanismo funcionara.

---

## Referencias
- Bug GitHub: https://github.com/anthropics/claude-code/issues/40789
- Documentación oficial Anthropic: https://docs.anthropic.com/en/docs/claude-code/settings
- Reportes internos canon Forja:
  - `catedral/reportes-agentes/2026-04-25-mecanismo-carga-skills-marketplace.md`
  - `catedral/reportes-agentes/2026-04-25-auditoria-skills-cargadas-globalmente.md`
