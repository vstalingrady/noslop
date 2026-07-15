# Feature IDs for local score

Fill from the **draft**, write `features.json`, then:

```powershell
$env:PYTHONPATH="src"
python -m noslop.cli score --features features.json --json
```

Template:

```powershell
python -m noslop.cli features-template --pack high-gain --out features_template.json
```

## Lean pack first (recommended)

Fill **must-hit + support** from `artifacts/human_coding_targets.json` first.
Bloated fills with middling values on dozens of IDs can **lower** P(human).
Prefer honest must-hit constructions over sparse guessing on all 265.

Optional: expand `high_gain_pack` only when each added ID has a cited span **and** a re-score does not drop P(human).

Must-hit values (when prose supports):

| ID | Prefer |
|----|--------|
| `PLT_MOR_007` | extended aftermath |
| `SIT_MET_303` | `3` or `4` |
| `REV_SUR_007` | climactic_end_twist |
| `EVT_SCH_010` | include frame_confession/memoir |
| `AGENT_EMO_009` | embodied_sensations_and_metaphors |
| `SIT_MET_008` | Balanced mix… or implicit echoes |
| `TMP_DUR_008` | exact times |
| `PER_POV_001` | first_person or third_person (match draft) |
| `PLT_THM_004` | survival/fear, guilt/redemption, etc. |
| `AGENT_ATTR_001` | in-action or in-dialogue first |

## Core pack (also fill)

| ID | What to judge |
|----|----------------|
| `SIT_MET_303` | Thematic explicitness 1–5 |
| `SIT_MET_501` | Narratorial thematic commentary yes/no |
| `SIT_MET_102` | Ending self-commentary on story yes/no |
| `PLT_MOR_001` | Moral/lesson explicitness ordinal |
| `PLT_THM_008` | Thematic unity 1–5 |
| `PLT_CON_007` | Agency in resolution |
| `PLT_THM_005` | Thematic resolution pattern |
| `PLT_STR_003` | Subplot density |
| `EVT_SCH_004` | Mode of resolution |
| `EVT_CAU_001` | Explicitness of causal links |
| `TMP_ORD_001` | Chronological structure |
| `TMP_DUR_008` | Temporal anchoring precision |
| `REV_DIS_003` | Nonlinear framing for disclosure |
| `REV_SUS_003` | Resolution of mysteries |
| `SET_ATM_005` | Sensory density |
| `PER_FOC_009` | Evaluative/moral commentary scale |
| `SIT_GEN_010` | Moral/philosophical weighting |
| `SIT_MET_008` | Reference explicitness |
| `SIT_MET_002` | Fourth-wall breaking |

Values must match taxonomy options (`artifacts/taxonomy.json`).

## Honesty rule

If the draft lacks support, leave the feature unset or pick the true weaker value — never invent climax aftermath that is not on the page.
