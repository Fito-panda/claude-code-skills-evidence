# Test 2 — `enabled: false` en `manifest.json` del plugin interno `skills-plugin`

**Mecanismo bajo prueba:** desactivar skills individuales del plugin embedded `skills-plugin` (ubicado en `AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/`) seteando `enabled: false` por skill en su `manifest.json`.

**Documentación:** ninguna oficial. Mecanismo inferido del schema del archivo `manifest.json` que tiene un campo booleano `enabled` por cada entrada de skill.

**Hipótesis:** si seteamos 44 de 51 skills a `enabled: false`, el harness debería respetar el flag y cargar sólo las 7 restantes.

---

## Método

### Pre-condiciones
- Plugin `skills-plugin` instalado en `AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/{userUuid}/{orgUuid}/`
- `manifest.json` contiene array de 51 skills, todas con `enabled: true`

### Pasos

1. Backup del manifest:
   ```bash
   cp manifest.json manifest.json.backup-2026-04-24-pre-disable-anthropic-skills
   ```
2. Editar `manifest.json` con script Python que mantiene 7 skills `KEEP-GLOBAL` (docx, pdf, pptx, xlsx, schedule, skill-creator, consolidate-memory) y setea las otras 44 a `enabled: false`.
3. Verificar JSON válido + 51 entries con flag correcto.
4. Cerrar Claude Code completamente.
5. Abrir sesión nueva.
6. Contar skills `anthropic-skills:*` en system reminder.

### Resultado esperado (si funciona)
`anthropic-skills:` cae de 51 a 7 skills.

### Resultado obtenido (2026-04-24)
**`anthropic-skills:` se mantiene en ~47-51 skills** (variación dentro del ruido del contador). El flag `enabled: false` es ignorado.

### Conclusión
El harness no respeta `enabled: false` per-skill en el `manifest.json` del plugin interno `skills-plugin`. Mecanismo no funcional.

### Restauración post-test
```bash
cp manifest.json.backup-2026-04-24-pre-disable-anthropic-skills manifest.json
```
Restaurado a estado original (51 enabled). Backup conservado para auditoría.

---

## Reproducibilidad

Cualquier auditor puede reproducir:
1. Localizar `manifest.json` del `skills-plugin` (path varía por UUID de cuenta).
2. Hacer backup.
3. Editar enabled flags.
4. Restart total Claude Code.
5. Verificar que el conteo de `anthropic-skills:` no cambia.

---

## Referencias
- Reporte interno: `catedral/reportes-agentes/2026-04-25-mecanismo-carga-skills-marketplace.md` §3.3
- El reporte interno había marcado este mecanismo como "primera palanca granular" basándose en la presencia del flag en el schema. Test empírico refuta esa hipótesis.
