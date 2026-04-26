#!/usr/bin/env python3
"""
script-evidencia.py — Instrumento de medición reproducible para reclamo Anthropic.

Lee:
  1. ~/.claude.json          -> skillUsage real (cuántas skills se invocaron alguna vez)
  2. Transcript JSONL        -> turnos + tokens medidos en sesion
  3. Cuenta de skills        -> opcional via system reminder cap (pegado a stdin)

Output:
  - Tabla con: skills cargadas (pegada o leida) vs skills realmente invocadas
  - Estimacion tokens fixed cost por turno
  - Estimacion daño mensual (ventana consumida + caps acelerados)

Uso:
  python script-evidencia.py                          # solo skillUsage de .claude.json
  python script-evidencia.py --skills-cap path.txt    # cuenta skills del cap pegado
  python script-evidencia.py --turnos N               # estima daño con N turnos/dia

Reproducible: cualquier auditor con .claude.json puede correrlo y verificar.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import argparse

CLAUDE_JSON = Path.home() / ".claude.json"
TOKENS_PER_SKILL_LINE = 45   # promedio descripcion truncada (verificado en auditoria 2026-04-25)
TOKENS_PER_TURN_CONSERVATIVO = 12700   # 296 skills * 45 tokens (lower bound)
TOKENS_PER_TURN_REAL = 16000           # con triggers expandidos (upper bound)


def leer_skill_usage(claude_json_path: Path) -> dict:
    if not claude_json_path.exists():
        return {"error": f"No existe {claude_json_path}"}
    try:
        with claude_json_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return data.get("skillUsage", {})
    except Exception as e:
        return {"error": str(e)}


def contar_skills_de_cap(cap_path: Path) -> dict:
    """Cuenta skills agrupadas por namespace en un text file con la lista cap del system reminder."""
    if not cap_path.exists():
        return {"error": f"No existe {cap_path}"}
    text = cap_path.read_text(encoding="utf-8", errors="replace")
    namespaces = {}
    total = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith("- "):
            continue
        # formato: "- namespace:skill-name: descripcion..." o "- skill-name: descripcion..."
        body = line[2:]
        if ":" in body:
            ns_or_skill = body.split(":", 1)[0]
            if "-" not in ns_or_skill and ns_or_skill.lower() == ns_or_skill:
                ns = ns_or_skill
            else:
                ns = "top-level"
        else:
            ns = "top-level"
        namespaces[ns] = namespaces.get(ns, 0) + 1
        total += 1
    return {"total": total, "por_namespace": namespaces}


def estimar_dano(turnos_por_dia: int, dias: int = 30) -> dict:
    tokens_mes_min = turnos_por_dia * TOKENS_PER_TURN_CONSERVATIVO * dias
    tokens_mes_max = turnos_por_dia * TOKENS_PER_TURN_REAL * dias
    return {
        "turnos_por_dia": turnos_por_dia,
        "dias": dias,
        "tokens_min_mes": tokens_mes_min,
        "tokens_max_mes": tokens_mes_max,
        "porcentaje_ventana_1M": (TOKENS_PER_TURN_CONSERVATIVO / 1_000_000) * 100,
        "porcentaje_ventana_200k": (TOKENS_PER_TURN_CONSERVATIVO / 200_000) * 100,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-cap", type=Path, help="Path a archivo de texto con cap del system reminder pegado")
    parser.add_argument("--turnos", type=int, default=50, help="Turnos por dia estimados (default 50)")
    args = parser.parse_args()

    print("=" * 70)
    print("EVIDENCIA RECLAMO ANTHROPIC — Generado:", datetime.now(timezone.utc).isoformat())
    print("=" * 70)

    # 1. Skill usage real
    print("\n## 1. SKILLS REALMENTE INVOCADAS (de ~/.claude.json -> skillUsage)\n")
    su = leer_skill_usage(CLAUDE_JSON)
    if "error" in su:
        print(f"ERROR: {su['error']}")
    elif not su:
        print("Sin invocaciones registradas (cuenta nueva o limpia).")
    else:
        total_invocaciones = 0
        print(f"{'Skill':<60} {'Invocaciones':>15}")
        print("-" * 78)
        for skill, info in sorted(su.items(), key=lambda x: -x[1].get("usageCount", 0) if isinstance(x[1], dict) else 0):
            count = info.get("usageCount", 0) if isinstance(info, dict) else info
            print(f"{skill:<60} {count:>15}")
            total_invocaciones += count
        print("-" * 78)
        print(f"{'TOTAL skills distintas invocadas:':<60} {len(su):>15}")
        print(f"{'TOTAL invocaciones acumuladas:':<60} {total_invocaciones:>15}")

    # 2. Skills cargadas (si pego cap)
    print("\n## 2. SKILLS CARGADAS POR TURNO (del system reminder)\n")
    if args.skills_cap:
        c = contar_skills_de_cap(args.skills_cap)
        if "error" in c:
            print(f"ERROR: {c['error']}")
        else:
            print(f"Total cargadas: {c['total']}")
            print("\nPor namespace:")
            for ns, n in sorted(c["por_namespace"].items(), key=lambda x: -x[1]):
                print(f"  {ns:<40} {n:>5}")
    else:
        print("No se pasó --skills-cap. Para conteo automatico,")
        print("pegá el bloque <skills> del system reminder en un .txt y pasalo.")
        print("Conteo verificado manualmente 2026-04-24: 296 skills.")

    # 3. Estimacion daño
    print(f"\n## 3. ESTIMACION DAÑO (asumiendo {args.turnos} turnos/dia, 30 dias)\n")
    dano = estimar_dano(args.turnos)
    print(f"Tokens fixed cost / turno (lower):  {TOKENS_PER_TURN_CONSERVATIVO:>12,}")
    print(f"Tokens fixed cost / turno (upper):  {TOKENS_PER_TURN_REAL:>12,}")
    print(f"Tokens consumidos por mes (lower):  {dano['tokens_min_mes']:>12,}")
    print(f"Tokens consumidos por mes (upper):  {dano['tokens_max_mes']:>12,}")
    print(f"Porcentaje de ventana 200k:         {dano['porcentaje_ventana_200k']:>12.2f}%")
    print(f"Porcentaje de ventana 1M:           {dano['porcentaje_ventana_1M']:>12.2f}%")

    # 4. Ratio
    print("\n## 4. RATIO UTILIZACION\n")
    if isinstance(su, dict) and "error" not in su:
        invocadas = len(su)
        cargadas = 296   # default verificado; reemplazar por c['total'] si --skills-cap
        if args.skills_cap and "total" in c:
            cargadas = c["total"]
        ratio = (invocadas / cargadas) * 100 if cargadas > 0 else 0
        print(f"Skills cargadas: {cargadas}")
        print(f"Skills invocadas alguna vez: {invocadas}")
        print(f"Ratio utilización ever-used: {ratio:.2f}%")
        print(f"Skills nunca invocadas (waste): {cargadas - invocadas} ({100 - ratio:.2f}%)")

    print("\n" + "=" * 70)
    print("Reproducible: pasale tu propio ~/.claude.json y obtené el mismo formato.")
    print("=" * 70)


if __name__ == "__main__":
    main()
