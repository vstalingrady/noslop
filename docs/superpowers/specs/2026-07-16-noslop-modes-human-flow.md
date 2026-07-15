# noslop modes — human flow over detector max

**Date:** 2026-07-16  
**Status:** design / goal handoff  

## Diagnosis

| Observation | Meaning |
|-------------|---------|
| Books mean StoryScope P(human) ~**0.13** (Gatsby ~0.27) | Real human prose lives in a **low–mid** band on that scorer |
| Noslop max packs hit ~**0.5–0.9** VOICE / StoryScope | We optimized **metric shape**, not reading flow |
| GPTZero / detectors still hate “crafted” samples | Chasing detectors makes **even, complete, checklist** prose |
| User experience | “Barely readable” despite “good” scores |

**Root cause:** One intensity (max craft / max VOICE / max StoryScope stack) collapses human flow into score-farming.

## Product principle

**Primary:** A careful human can read it without bouncing — flow, voice, uneven real detail.  
**Secondary:** Don’t reintroduce classic slop (glue phrases, abstract fog, sermon close).  
**Not primary:** Maximize StoryScope P(human), maximize VOICE to 9+, or beat any commercial detector.

StoryScope ~**0.15–0.30** with honest features is a **success neighborhood** for “human-like,” not failure. Sky-high scores with stiff prose are failure.

## Modes (required)

Same brief, three intensities (plus optional default for contrast):

| Mode | Intent | Craft knobs | Score expectation (guide, not law) |
|------|--------|-------------|--------------------------------------|
| **modest** | Closest to how people actually write | Light anchors, natural digression, incomplete thoughts OK, no forced arc toys, minimal “skill show” | VOICE mid; StoryScope often ~0.1–0.25 if labeled honestly |
| **balanced** | Default ship mode | Anchors + one mess + no sermon; skip checklist dump; readable first | VOICE pass band without maxing |
| **max** | Research / stress only | Full VOICE pressure and/or StoryScope constructions | High numbers; document readability cost |

Agent selects mode via PRE-WRITE `Mode: modest|balanced|max` (default **balanced**).

## Comparison deliverable

1. Fixed briefs (≥2 genres: e.g. fiction + email).  
2. For each brief: **default**, **modest**, **balanced**, **max** drafts.  
3. Score: VOICE CLI + optional honest StoryScope feature maps.  
4. **DOCX report** with: thesis, mode definitions, score tables, full quoted drafts side-by-side, readability notes, recommendation (default ship = balanced; max not default).  
5. Charts optional (bars only — **no text-in-matplotlib**).

## Skill changes (high level)

- Add `modes.md` (definitions + do/don’t per mode).  
- PRE-WRITE requires `Mode:`.  
- **balanced** ship bar: VOICE without requiring 9+; soft target VOICE ≥ ~5.5–7 and no hard fail, **or** human-read checklist PASS.  
- **max** explicitly labeled research; not README hero.  
- Demote “maximize score” language everywhere public.  
- Keep StoryScope diagnostic; if used, prefer matching **book band** over beating books.

## Non-goals this cycle

- Guaranteed commercial-detector pass as a product claim on README  
- Retrain XGBoost  
- Dropping VOICE entirely (still useful vs pure glue-slop)

## Success criteria

1. Modes documented in skill + PRE-WRITE.  
2. ≥2 briefs × 4 arms (default/modest/balanced/max) on disk.  
3. DOCX comparison delivered under `evals/results/` (or `docs/`).  
4. Written recommendation: ship **balanced**; **modest** for natural letters; **max** only when user asks.  
5. Public README: modes one short section; no “undetectable / GPTZero fail” theater.  
6. Push to GitHub when changes land.
