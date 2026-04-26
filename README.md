# claude-code-skills-evidence

**Reproduction package for Anthropic Claude Code skill catalog overhead + acknowledged degradation period (2026-03-04 to 2026-04-20)**

Documents an empirical investigation of how Claude Code loads its skill catalog (~12,700 tokens per turn from 296 skills) with no working user-level filter mechanism, in the context of Anthropic's own engineering postmortem published 2026-04-23.

**Author:** Adolfo "Fito" Prunotto · Senior Product Designer · Buenos Aires, Argentina · [@Fito-panda](https://github.com/Fito-panda)
**Anthropic account:** Max plan since 2026-02-26
**Date of investigation:** 2026-04-24
**License:** MIT (full evidence is reproducible)

---

## TL;DR

1. **Anthropic publicly acknowledged 47 days of Claude Code degradation** (2026-03-04 to 2026-04-20) in their own [engineering postmortem published 2026-04-23](https://www.anthropic.com/engineering/april-23-postmortem). For me, that is **78% of my paid period**. Only compensation offered: usage limit reset (no monetary refund).

2. **In addition to the postmortem-acknowledged issues**, I documented on 2026-04-24 that the Claude Code skill catalog loads **296 skills per turn (~12,700 tokens of fixed cost) with no working user-level filter**. I tested 5 mechanisms — all failed empirically. This is bug [`#40789`](https://github.com/anthropics/claude-code/issues/40789), open and stale.

3. **Real usage** of those 296 loaded skills (from my `~/.claude.json` `skillUsage` field): **12 invocations across 5 distinct skills in 2 months. 4% ever-used.** The remaining 96% of the catalog is loaded but never invoked.

4. **Quantified damage:** $812 USD requested resarcimiento ($312 refund proportional to 78% degraded period + $500 documented time loss at $100/h Senior Product Designer Buenos Aires market rate).

5. **Filing channels** (parallel, 2026-04-24): GitHub issue tracker, `support@anthropic.com`, `privacy@anthropic.com`, plus COPREC (Argentina mediation) + California AG (informational complaint, since CCPA does not directly apply to non-CA residents).

---

## The 5 mechanisms tested (all failed)

| # | Mechanism | Documentation status | Result |
|---|---|---|---|
| 1 | `enabledPlugins` in `.claude/settings.json` | Officially documented | **Bug #40789, open, stale, no ETA** |
| 2 | `enabled: false` in `manifest.json` of internal `skills-plugin` | Implied by JSON schema | **Ignored by harness** |
| 3 | `hasTrustDialogAccepted: false` in `~/.claude.json` | Implied by trust model | **Ignored by harness** |
| 4 | Physical `mv` of plugin folders to `.disabled-2026-04-24` | Reasonable expectation (filesystem walk) | **Ignored** — folders confirmed absent from original paths, skills still load |
| 5 | Brand-new empty project (different `cwd`) | Implied by per-project filtering | **Identical 296-skill catalog** in completely empty directory |

Full step-by-step methodology + commands + results in [`tests/`](./tests/).

---

## What is in this repo

```
.
├── README.md                              # this file
├── script-evidencia.py                    # reproducible measurement script (reads ~/.claude.json)
├── tests/                                 # the 5 mechanisms tested, full method
│   ├── test-1-enabledPlugins.md
│   ├── test-2-manifest-enabled-false.md
│   ├── test-3-trust-revoke.md
│   ├── test-4-filesystem-mv.md
│   └── test-5-empty-project.md            # cleanest reproduction (30 seconds)
├── calculo-economico.md                   # damage quantification with verifiable formula
├── marco-legal-verificado.md              # legal framework Argentina + California analysis
└── screenshots/                           # captures (added by Fito before publication)
    └── (TBD)
```

---

## 30-second reproduction

```bash
# Step 1: Create completely empty project
mkdir test-claude-skills-bug
cd test-claude-skills-bug

# Step 2: Open Claude Code in this empty directory
# (close Claude Code completely first via menu Salir, then reopen)

# Step 3: Look at the <system-reminder> block at session start
# Count skills listed under "available-skills"
```

If you see ~290+ skills loaded in a brand-new empty directory with no `.claude/`, no `CLAUDE.md`, and no plugin configuration, you are observing the same behavior I am reporting.

---

## Real usage data (from my own `~/.claude.json`)

```
Skill                                                Invocations
---------------------------------------------------------------
update-config                                                  6
abogado-del-diablo                                             3
anthropic-skills:bitacorista-py                                1
bitacora:bitacorista-py                                        1
repair-help                                                    1
---------------------------------------------------------------
TOTAL skills distinct invoked:                                 5
TOTAL invocations accumulated:                                12

Skills loaded per turn:                                      296
Tokens of fixed cost per turn (lower bound):              12,700
Tokens of fixed cost per turn (upper bound):              16,000

Utilization ratio (ever-used):                            4.05%
Per-turn utilization ratio:                               <0.1%
```

Run `python script-evidencia.py` against your own `~/.claude.json` to get the same shape of result.

---

## Why this matters

### For Max plan users (flat $200/month)

Damage is not direct $. Damage is:
- **Context window consumed:** 12,700–16,000 tokens lost per turn before user input
- **Rate-limit caps reached faster:** Max plan 5h / 24h caps exhaust earlier
- **Model degradation:** documented `TOOL BLINDNESS` from oversaturated tool descriptions
- **Overlap with acknowledged degradation period:** 47 of 60 paid days were in degraded state per Anthropic's own postmortem

### For API users (billed per token)

Direct cost. Estimates at 50 turns/day:
- Conservative ($15/M tokens, sub-200k context): **$285/month wasted**
- Aggressive (1M tier $75/M): **up to $1,428/month wasted**

---

## Anthropic's own postmortem (2026-04-23) — central evidence

URL: **https://www.anthropic.com/engineering/april-23-postmortem**

Three causes acknowledged:

| Date introduced | Cause | Date reverted |
|---|---|---|
| 2026-03-04 | Reasoning effort reduced from "high" to "medium" | 2026-04-07 |
| 2026-03-26 | Cache bug clearing reasoning every turn instead of per inactive session | 2026-04-10 |
| 2026-04-16 | System prompt instruction reducing verbosity damaging coding quality | 2026-04-20 |

**Total acknowledged degradation: 47 days. Compensation offered: usage limit reset only (no monetary refund).**

External coverage:
- [VentureBeat](https://venturebeat.com/technology/mystery-solved-anthropic-reveals-changes-to-claudes-harnesses-and-operating-instructions-likely-caused-degradation)
- [Fortune](https://fortune.com/2026/04/24/anthropic-engineering-missteps-claude-code-performance-decline-user-backlash/)
- [Simon Willison](https://simonwillison.net/2026/Apr/24/recent-claude-code-quality-reports/)

---

## Looking for

1. **Anthropic engineering response** to bug `#40789` and to the comment I posted today.
2. **Other affected users:** if you have similar conditions, run `script-evidencia.py` and post your results in the GitHub issue or contact me. Especially interested in:
   - Different plugin sets (rule out my Aleph-Libre as cause)
   - Different OS (rule out Windows-specific)
   - Different plans (Pro vs Max vs API)
3. **Anyone who has found a working filter mechanism I missed:** I will gladly correct this repo + retract publicly if I am wrong.

---

## Filing status (updates as they happen)

| Channel | Status | Date | Response |
|---|---|---|---|
| GitHub comment on #40789 | TBD | 2026-04-25+ | — |
| GitHub new complementary issue | TBD | 2026-04-25+ | — |
| Email to support@anthropic.com | TBD | 2026-04-25+ | — |
| Email to privacy@anthropic.com | TBD | 2026-04-25+ | — |
| COPREC Argentina (mediation) | scheduled day 14 | 2026-05-08 if no response | — |
| California Attorney General (informational) | scheduled day 14 | 2026-05-08 if no response | — |
| FTC US (informational) | scheduled day 14 | 2026-05-08 if no response | — |

---

## Legal framework (Argentina + California)

Full analysis in [`marco-legal-verificado.md`](./marco-legal-verificado.md).

Key articles:
- **Ley 24.240 Defensa del Consumidor (Argentina) Art. 19** — obligation to deliver service per documented terms (primary basis)
- **Ley 24.240 Art. 37** — nullity of abusive clauses in adhesion contracts (annuls Anthropic ToS Sec. 11 $100 cap in Argentine jurisdiction)
- **Ley 25.326 Protección de Datos Personales Art. 4.1** — data minimization principle
- **CCPA §1798.140(i)** — limits "Consumer" to California residents, **NOT applicable** to non-CA residents

---

## License

MIT. Full evidence is reproducible.

## Contact

- Email: fito@arcanomedia.com
- GitHub: [@Fito-panda](https://github.com/Fito-panda)

---

**Last updated:** 2026-04-24

**Status:** Day 1 of formal claim. All filings prepared. Anthropic response window: 15 business days from email send date.
