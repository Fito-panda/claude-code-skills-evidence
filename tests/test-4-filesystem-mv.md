# Test 4 — `mv` físico de carpetas de plugins

**Mecanismo bajo prueba:** renombrar las carpetas de plugins en el filesystem para que no existan en su path original. Si el harness hace filesystem walk para descubrir plugins, debería no encontrarlos y no cargar sus skills.

**Documentación:** ninguna oficial. Mecanismo basado en la expectativa razonable de que un plugin discovery basado en filesystem walk no carga lo que no existe en disco.

**Hipótesis:** moviendo 3 paths críticos a `.disabled-2026-04-24`, las skills de esos plugins desaparecen del catálogo.

---

## Método

### Pre-condiciones
- 3 paths con plugins activos:
  - `C:/Users/adolp/Desktop/Aleph/Aleph-Libre/plugins/` (arcanomedia + bitacora + cognitivo)
  - `C:/Users/adolp/AppData/Roaming/Claude/local-agent-mode-sessions/{userUuid}/{orgUuid}/cowork_plugins/marketplaces/knowledge-work-plugins/` (~75 skills knowledge-work)
  - `.../cowork_plugins/cache/knowledge-work-plugins/` (clone hermano del anterior)
- Conteo pre-test: 296 skills

### Pasos

1. Backups implícitos: el `mv` es reversible con `mv` inverso. No se hace copia.
2. Mover los 3 paths:
   ```bash
   mv "C:/Users/adolp/Desktop/Aleph/Aleph-Libre/plugins" \
      "C:/Users/adolp/Desktop/Aleph/Aleph-Libre/plugins.disabled-2026-04-24"

   mv ".../cowork_plugins/marketplaces/knowledge-work-plugins" \
      ".../knowledge-work-plugins.disabled-2026-04-24"

   mv ".../cowork_plugins/cache/knowledge-work-plugins" \
      ".../knowledge-work-plugins.disabled-2026-04-24"
   ```
3. Verificar filesystem:
   ```bash
   ls "C:/Users/adolp/Desktop/Aleph/Aleph-Libre/"
   # Output: solo plugins.disabled-2026-04-24, no plugins/
   ```
4. Buscar OTRAS copias de los plugins en disco (descartar fuentes alternativas):
   ```bash
   find "C:/Users/adolp" -maxdepth 8 -type d -name "arcanomedia" 2>/dev/null | grep -v ".disabled"
   # Output: vacío. No hay otra copia de arcanomedia en disco.
   ```
5. Cerrar Claude Code completamente.
6. Abrir sesión nueva.
7. Contar skills.

### Resultado esperado (si funciona)
Catálogo cae de 296 a ~110-120 skills (296 - 110 Aleph - 75 Cowork ≈ 111).

### Resultado obtenido (2026-04-24)
**Catálogo: 296 skills.** Sin cambio significativo. Especificamente:
- `arcanomedia:` 78 skills (esperado 0)
- `bitacora:` 8 skills (esperado 0)
- `cognitivo:` 7 skills (esperado 0)
- Knowledge-work namespaces (legal, finance, sales, etc.): cantidades similares al pre-test

### Conclusión
**Las skills NO se cargan desde el filesystem que el usuario controla.** Aunque las carpetas físicas no existen en sus paths originales, las skills siguen apareciendo en el catálogo. La fuente real es:
- Cache binario en path no encontrado, o
- RAM persistente que sobrevive el "Salir" del menú, o
- Sincronización server-side desde `api.anthropic.com`

En cualquiera de los 3 casos, **el filesystem local no es la palanca**.

### Restauración post-test
```bash
mv "...plugins.disabled-2026-04-24" "...plugins"
mv "...knowledge-work-plugins.disabled-2026-04-24" "...knowledge-work-plugins"
# (los 3 paths)
```

---

## Reproducibilidad

Cualquier auditor puede reproducir:
1. Identificar paths de plugins en su sistema.
2. Renombrar a `.disabled` (reversible).
3. Verificar via `ls` o `find` que las carpetas no existen en path original.
4. Restart total Claude Code.
5. Verificar que las skills siguen apareciendo en el catálogo.

---

## Referencias
- Reporte interno: `catedral/reportes-agentes/2026-04-25-mecanismo-carga-skills-marketplace.md` §6 Opción B
- Anthropic documentación de plugin caching: https://docs.anthropic.com (mencionada en el reporte como `~/.claude/plugins/cache`)
