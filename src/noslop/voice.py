"""
VOICE heuristics — reader anti-slop gate (primary for noslop v2).

Does NOT replace StoryScope.
Scores text only: anchors, unevenness, moral-close, rhythm, ban/glue.
"""

from __future__ import annotations

import math
import re
from typing import Any

# Surface bans / glue (subset of style-and-bans.md)
BAN_WORDS = re.compile(
    r"\b("
    r"delve|delving|tapestry|testament|vibrant|pivotal|intricate|intricacies|"
    r"meticulous|meticulously|bolster|garner|underscore|multifaceted|nuanced|"
    r"foster|fostering|leverage|utilize|commence|facilitate|encompass|paramount|"
    r"groundbreaking|cutting[- ]edge|game[- ]changer|game[- ]changing|"
    r"transformative|revolutionize|seamless|seamlessly|robust|comprehensive|"
    r"endeavor|aforementioned|harnessing|spearheading|showcasing|highlighting|"
    r"emphasizing|enhancing|unprecedented|remarkable|stunning|synergy|"
    r"holistic|paradigm|unlock|unleash|empower|streamline|elevate|"
    r"moreover|furthermore|consequently|nevertheless"
    r")\b",
    re.I,
)

BAN_PHRASES = [
    r"in today's",
    r"it's worth noting",
    r"it's important to note",
    r"let's dive",
    r"at its core",
    r"in the realm of",
    r"when it comes to",
    r"at the end of the day",
    r"the bottom line is",
    r"here's the thing",
    r"here's the turn",
    r"without further ado",
    r"in a nutshell",
    r"in conclusion",
    r"i hope this finds you well",
    r"i hope this helps",
    r"based on the information provided",
    r"as an ai",
    r"navigate (the |your |complex )",
    r"pain points",
    r"move the needle",
    r"bridge the gap",
    r"take it to the next level",
]

MORAL_CLOSE = re.compile(
    r"("
    r"i used to think.{0,80}turns out|"
    r"what (really )?matters is|"
    r"at the end of the day|"
    r"the (real )?lesson|"
    r"caring first|"
    r"follow(ing)? (your|the) heart|"
    r"that's what (life|it)('s| is) about|"
    r"in the end,? (we|you|i|what)|"
    r"remember that|"
    r"never forget that"
    r")",
    re.I | re.S,
)

# Anchors: digits, clock-ish, proper-noun-ish tokens
DIGIT = re.compile(r"\d")
TIMEISH = re.compile(
    r"\b(\d{1,2}:\d{2}\s*(a\.?m\.?|p\.?m\.?)?|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"january|february|march|april|june|july|august|september|october|november|december)\b",
    re.I,
)
# Capitalized word not at sentence start only — simple: 2+ Capital words or mixed
PROPERISH = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+|[A-Z]{2,}|\b[A-Z][a-z]{3,}\b)")

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

DEFAULT_THRESHOLD = 6.5


def _sentences(text: str) -> list[str]:
    parts = [p.strip() for p in SENT_SPLIT.split(text.strip()) if p.strip()]
    return parts if parts else ([text.strip()] if text.strip() else [])


def _ban_hits(text: str) -> int:
    hits = len(BAN_WORDS.findall(text))
    low = text.lower()
    for pat in BAN_PHRASES:
        hits += len(re.findall(pat, low))
    return hits


def _anchor_signals(text: str) -> dict[str, int]:
    digits = len(DIGIT.findall(text))
    times = len(TIMEISH.findall(text))
    # Multi-word proper names/places only (avoid counting sentence starters)
    multi = len(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text))
    codes = len(re.findall(r"[#$]\w+|\b[A-Za-z]*\d+[A-Za-z0-9]*\b", text))
    total = digits + times * 2 + multi * 3 + min(codes, 6)
    return {
        "digits": digits,
        "times": times,
        "multi_proper": multi,
        "codes": codes,
        "total": total,
    }


def _sentence_lengths(sents: list[str]) -> list[int]:
    return [len(s.split()) for s in sents if s.split()]


def _stdev(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def _axis_anchors(text: str, words: int) -> tuple[int, dict[str, Any]]:
    sig = _anchor_signals(text)
    per_100 = (sig["total"] / max(words, 1)) * 100
    # 0–2 scale
    if per_100 >= 4 or sig["total"] >= 6:
        score = 2
    elif per_100 >= 1.5 or sig["total"] >= 3:
        score = 1
    else:
        score = 0
    return score, {"per_100": round(per_100, 2), **sig}


def _axis_moral(text: str) -> tuple[int, dict[str, Any]]:
    hits = MORAL_CLOSE.findall(text)
    # Also last 2 sentences thesis-y
    sents = _sentences(text)
    tail = " ".join(sents[-2:]) if sents else ""
    tail_bad = bool(
        re.search(
            r"\b(matters|lesson|realize[sd]?|caring|heart|wisdom|journey)\b",
            tail,
            re.I,
        )
        and re.search(r"\b(used to|turns out|in the end|always)\b", tail, re.I)
    )
    n = len(hits) + (1 if tail_bad else 0)
    if n == 0:
        return 2, {"hits": 0, "tail_bad": False}
    if n == 1:
        return 1, {"hits": n, "tail_bad": tail_bad}
    return 0, {"hits": n, "tail_bad": tail_bad}


def _axis_glue(text: str) -> tuple[int, int]:
    hits = _ban_hits(text)
    words = max(len(text.split()), 1)
    rate = hits / words * 100
    if hits == 0:
        return 2, hits
    if hits <= 2 and rate < 1.5:
        return 1, hits
    return 0, hits


def _axis_rhythm(sents: list[str]) -> tuple[int, dict[str, Any]]:
    lens = _sentence_lengths(sents)
    if len(lens) < 3:
        return 1, {"stdev": 0.0, "n": len(lens)}
    sd = _stdev([float(x) for x in lens])
    # short hits present
    shorts = sum(1 for x in lens if x <= 4)
    if sd >= 4.0 and shorts >= 1:
        sc = 2
    elif sd >= 2.0 or shorts >= 1:
        sc = 1
    else:
        sc = 0
    return sc, {"stdev": round(sd, 2), "n": len(lens), "shorts": shorts}


def _axis_uneven(text: str, sents: list[str]) -> tuple[int, dict[str, Any]]:
    """Reward incomplete beats / digression / wasted detail signals."""
    signals = 0
    low = text.lower()
    # fragments / one-word lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    short_lines = sum(1 for ln in lines if len(ln.split()) <= 3)
    if short_lines >= 1:
        signals += 1
    # ellipsis or dash cutoffs
    if "..." in text or "—" in text or " - " in text:
        signals += 1
    # unfinished / open markers
    if re.search(r"\b(didn't|did not|maybe|not sure|left it|still|yet)\b", low):
        signals += 1
    # paragraph length imbalance
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paras) >= 2:
        plens = [len(p.split()) for p in paras]
        if max(plens) >= 2 * max(min(plens), 1):
            signals += 1
    if signals >= 3:
        return 2, {"signals": signals}
    if signals >= 1:
        return 1, {"signals": signals}
    return 0, {"signals": 0}


def score_voice(
    text: str,
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict[str, Any]:
    """
    Score prose for reader anti-slop VOICE gate.

    Returns:
      score: 0–10 float
      gate: pass|fail
      hard_fail: bool
      axes: per-axis 0–2
      details: diagnostic counts
      threshold: float
    """
    text = text or ""
    words = len(text.split())
    sents = _sentences(text)

    a_anchors, d_anchors = _axis_anchors(text, words)
    a_moral, d_moral = _axis_moral(text)
    a_glue, ban_hits = _axis_glue(text)
    a_rhythm, d_rhythm = _axis_rhythm(sents)
    a_uneven, d_uneven = _axis_uneven(text, sents)

    axes = {
        "anchors": a_anchors,
        "uneven": a_uneven,
        "moral_close": a_moral,  # 2 = clean
        "rhythm": a_rhythm,
        "glue_bans": a_glue,
    }

    # Weighted mean of axes (0–2) → 0–10
    # moral_close and glue weighted slightly higher for anti-slop
    weights = {
        "anchors": 1.2,
        "uneven": 1.0,
        "moral_close": 1.3,
        "rhythm": 1.0,
        "glue_bans": 1.2,
    }
    wsum = sum(weights.values())
    mean01 = sum(axes[k] * weights[k] for k in axes) / (2.0 * wsum)
    score = round(mean01 * 10.0, 2)

    hard_reasons: list[str] = []
    # Hard fails
    if a_moral == 0:
        hard_reasons.append("moral_close_sermon")
    if ban_hits >= 5:
        hard_reasons.append("ban_spam")
    if words >= 80 and a_anchors == 0:
        hard_reasons.append("zero_anchors_long")
    if words >= 40 and a_glue == 0 and ban_hits >= 3:
        hard_reasons.append("glue_ban_heavy")

    hard_fail = len(hard_reasons) > 0
    gate = "pass" if (score >= threshold and not hard_fail) else "fail"

    return {
        "score": score,
        "gate": gate,
        "hard_fail": hard_fail,
        "hard_reasons": hard_reasons,
        "axes": axes,
        "details": {
            "words": words,
            "sentences": len(sents),
            "ban_hits": ban_hits,
            "anchors": d_anchors,
            "moral": d_moral,
            "rhythm": d_rhythm,
            "uneven": d_uneven,
        },
        "threshold": threshold,
    }
