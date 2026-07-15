# Human-coding targets (StoryScope narrative model)

Write prose so these are **true**, then label them in `features.json` with a cited span.
Never set a feature the draft does not support.

## Must-hit (high lift)

| ID | Prefer value | How it shows in prose |
|----|--------------|------------------------|
| `PLT_MOR_007` | extended aftermath | After climax, ≥1 scene or time-jump of consequence |
| `SIT_MET_303` | `3` or `4` | Theme surfaces in thought/speech — not silent, not pure TED talk |
| `REV_SUR_007` | climactic end twist | Late turn recontextualizes object/choice |
| `EVT_SCH_010` | include `frame_confession/memoir` when possible | Log, later recollection, framed telling |
| `AGENT_EMO_009` | embodied_sensations_and_metaphors | Body + sensation for feeling |
| `SIT_MET_008` | Balanced mix… or Primarily implicit echoes | One real-world echo (song, brand, local detail) |

## Strong support

| ID | Prefer | Prose |
|----|--------|-------|
| `TMP_DUR_008` | exact calendar / clock times | `1:14 a.m.`, Tuesday, etc. |
| `PER_POV_001` | first_person if natural else deep third | Consistent person |
| `PLT_THM_004` | survival/fear or guilt/redemption | Pressure domain |
| `AGENT_ATTR_001` | in-action or in-dialogue first | No long resume open |
| `PLT_THM_006` | coming_of_age/initiation or investigation when fits | Arc shape |
| `TMP_DUR_011` | past (or present if intentional) | Dominant tense |

## Avoid (model-low / AI-floor patterns)

- Opening with external appearance dump only
- Zero aftermath (hard cut at climax)
- Fully open mystery with **no** turn and no consequence scene
- Emotion only as explicit labels (“he was sad”) with no body
- Pure open-end + never surface theme (tanks this scorer)

## Nonfiction mapping

| Fiction construction | Nonfiction analog |
|---------------------|-------------------|
| Extended aftermath | Consequence paragraph / what changed next week |
| End twist | Reframe of the opening claim with new evidence |
| Frame/memoir | “I’m writing this after…”, email postscript, retrospective lead |
| Embodied | Sensory detail of the room/body while deciding |
