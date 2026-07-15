# High-signal StoryScope-ish IDs (host-agent fill)

When user wants XGBoost without full 304-dim extract, fill these real taxonomy IDs from the draft, write `features.json`, then:

`python -m noslop.cli score draft.md --features features.json`

| ID | What to judge |
|----|----------------|
| `SIT_MET_303` | Thematic explicitness / moralizing (scale 1–5) |
| `SIT_MET_501` | Narratorial thematic commentary (`yes`/`no`) |
| `SIT_MET_102` | Ending self-commentary on story (`yes`/`no`) |
| `PLT_MOR_001` | Moral/lesson explicitness (ordinal values from taxonomy) |
| `PLT_THM_008` | Thematic unity (scale 1–5) |
| `PLT_CON_007` | Agency in resolution |
| `PLT_THM_005` | Thematic resolution pattern |
| `PLT_STR_003` | Subplot density |
| `EVT_SCH_004` | Mode of resolution of main event chain |
| `EVT_CAU_001` | Explicitness of causal links |
| `TMP_ORD_001` | Global chronological structure |
| `TMP_DUR_008` | Precision of temporal anchoring |
| `REV_DIS_003` | Nonlinear framing for delayed disclosure |
| `REV_SUS_003` | Resolution of mysteries |
| `SET_ATM_005` | Sensory density |
| `PER_FOC_009` | Explicit evaluative/moral commentary |
| `SIT_GEN_010` | Moral/philosophical weighting |
| `SIT_MET_008` | Reference explicitness |
| `SIT_MET_002` | Fourth-wall breaking |

Values must match taxonomy options when possible (see `artifacts/taxonomy.json`).
