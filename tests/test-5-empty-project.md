# Test 5 — Proyecto nuevo vacío (control de cwd)

**Mecanismo bajo prueba:** abrir Claude Code en un directorio completamente vacío, sin `.claude/`, sin `CLAUDE.md`, sin archivos de proyecto. Si el catálogo se filtra por proyecto activo (cwd), un proyecto vacío debería cargar sólo skills built-in.

**Documentación:** ninguna oficial sobre per-project filtering. Mecanismo basado en la expectativa razonable de que diferentes proyectos pueden tener diferentes skills activas.

**Hipótesis:** un directorio vacío carga un catálogo mínimo (built-in del harness, sin plugins de proyecto).

---

## Método

### Pre-condiciones
- Conteo previo en `CLAUDE-CORE`: 296 skills

### Pasos

1. Crear directorio completamente vacío:
   ```bash
   mkdir C:\Users\adolp\Desktop\fito-sistem-3000
   cd C:\Users\adolp\Desktop\fito-sistem-3000
   ls -la
   # Output: total 32 / drwxr-xr-x . / drwxr-xr-x ..
   # Sin archivos, sin .claude/, nada.
   ```
2. Cerrar Claude Code completamente vía menú.
3. Abrir Claude Code nuevo apuntando a `C:\Users\adolp\Desktop\fito-sistem-3000`.
4. Contar skills en system reminder al inicio de sesión.

### Resultado esperado (si funciona el per-project filtering)
Catálogo mínimo (~10-30 built-in skills + nada más).

### Resultado obtenido (2026-04-24)
**296 skills cargadas, idénticas al conteo en `CLAUDE-CORE` u otros proyectos.**

| Namespace | CLAUDE-CORE | fito-sistem-3000 (vacío) | Δ |
|---|---|---|---|
| arcanomedia: | 78 | 78 | 0 |
| anthropic-skills: | 47 | 47 | 0 |
| engineering: | 10 | 10 | 0 |
| data: | 9 | 9 | 0 |
| operations: | 9 | 9 | 0 |
| legal: | 9 | 9 | 0 |
| sales: | 10 | 10 | 0 |
| product-management: | 7 | 7 | 0 |
| finance: | 7 | 7 | 0 |
| common-room: | 6 | 6 | 0 |
| slack-by-salesforce: | 7 | 7 | 0 |
| design: | 7 | 7 | 0 |
| bitacora: | 8 | 8 | 0 |
| cognitivo: | 7 | 7 | 0 |
| Otros (~16 namespaces) | ~58 | ~58 | 0 |
| Top-level | 14 | 14 | 0 |
| **Total** | **296** | **296** | **0** |

### Conclusión
**El catálogo de skills es global, no per-proyecto.** No hay filtering por cwd. Un directorio vacío carga exactamente las mismas 296 skills que un proyecto complejo con configuración propia.

Esto es la confirmación más limpia y reproducible de que el catálogo no depende del proyecto activo.

---

## Por qué este test es la "reproducción mínima reproducible"

Este test es ideal para reportes públicos (GitHub issue, blog, regulador) porque:
- No requiere acceso al sistema de Forja específico
- No expone datos sensibles (proyecto vacío)
- Cualquier usuario de Claude Code puede correrlo en 30 segundos
- El resultado es binario: o el catálogo cambia o no

---

## Reproducibilidad

```bash
mkdir test-claude-skills && cd test-claude-skills
# Cerrar Claude Code completamente (menú Salir)
# Abrir Claude Code en este directorio vacío
# Contar skills en <system-reminder>
# Comparar con conteo en otro proyecto
```

Si tu conteo en proyecto vacío es muy distinto del mío (296), reportá tu setup — me interesa entender la varianza.

---

## Referencias
- Sesión Claude paralela 2026-04-24 ejecutó este test independientemente y reportó **290 skills**, dentro del margen de error del conteo manual (±5-10 skills).
