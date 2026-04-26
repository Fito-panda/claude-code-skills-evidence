# Test 3 — `hasTrustDialogAccepted: false` en `~/.claude.json`

**Mecanismo bajo prueba:** revocar el "trust" del directorio `Desktop/Aleph` en `~/.claude.json`, esperando que las skills de plugins ubicados ahí (Aleph-Libre: `arcanomedia`, `bitacora`, `cognitivo`) dejen de cargar en sesiones que NO estén ubicadas físicamente en ese directorio.

**Documentación:** ninguna oficial. Mecanismo inferido del modelo de "trust" de directorios de Claude Code, donde un directorio confiado habilita la carga de plugins .claude-plugin allí.

**Hipótesis:** seteando `projects."C:/Users/adolp/Desktop/Aleph".hasTrustDialogAccepted` de `true` a `false`, las 110 skills de Aleph-Libre dejan de cargarse en otros proyectos.

---

## Método

### Pre-condiciones
- `~/.claude.json` existe con entrada `projects."C:/Users/adolp/Desktop/Aleph"` con `hasTrustDialogAccepted: true`
- Conteo previo: arcanomedia: 94, bitacora: 9, cognitivo: 7 = **110 skills de Aleph-Libre**
- Sesión activa en `CLAUDE-CORE`, no en `Aleph`

### Pasos

1. Backup del archivo crítico:
   ```bash
   cp ~/.claude.json ~/.claude.json.backup-2026-04-24-pre-revoke-aleph-trust
   ```
2. Editar via script Python: cambiar `hasTrustDialogAccepted` de `true` a `false`. Otras configs de la entrada Aleph (allowedTools, mcpServers, etc.) preservadas.
3. Verificar JSON válido + cambio aplicado.
4. Cerrar Claude Code completamente.
5. Abrir sesión nueva en `CLAUDE-CORE`.
6. Contar skills de Aleph-Libre en system reminder.

### Resultado esperado (si funciona)
`arcanomedia:` + `bitacora:` + `cognitivo:` = 0 skills cargadas (110 menos en total).

### Resultado obtenido (2026-04-24)
**arcanomedia: 94, bitacora: 9, cognitivo: 7 = 110 skills cargadas.** Sin cambio.

### Conclusión
`hasTrustDialogAccepted: false` no impide la carga de skills del directorio. El mecanismo de trust no controla el discovery de plugins en esta versión.

### Restauración post-test
```bash
cp ~/.claude.json.backup-2026-04-24-pre-revoke-aleph-trust ~/.claude.json
```
Restaurado a estado original (`hasTrustDialogAccepted: true`).

---

## Reproducibilidad

Cualquier auditor puede reproducir:
1. Identificar entrada en `projects` de `~/.claude.json` para un directorio que contenga plugins .claude-plugin.
2. Backup del archivo.
3. Setear `hasTrustDialogAccepted: false`.
4. Restart total Claude Code.
5. Verificar que las skills siguen cargando.

---

## Referencias
- Reporte interno: `catedral/reportes-agentes/2026-04-25-mecanismo-carga-skills-marketplace.md` §3.7
