"""VOICE heuristics: reader anti-slop gate (not StoryScope)."""

from __future__ import annotations

from noslop.voice import score_voice


MORAL_CLOSE = """
The guard found the shoe and called the police. The boy was fine.
I used to think the job was about procedure. Turns out it was about caring first.
At the end of the day, what matters is following your heart.
"""

BAN_HEAVY = """
In today's rapidly evolving landscape, we leverage cutting-edge solutions to
unlock seamless workflows and empower stakeholders. It's important to note that
our robust, comprehensive platform will revolutionize how you navigate pain points.
Moreover, we foster holistic synergy to elevate operational excellence.
"""

GOOD_VOICE = """
Tuesday 6:12 p.m. — thrift bin under romance paperbacks. Dad's watch, strap
cracked white. Engraving half gone: For M.

I paid four dollars. Bus stop plastic. Rain.

Coffee cart woman said Albany like a place that keeps boxes. I kept the watch.

The bulb in the kitchen still dead. Second hand ticks in the dark.
Receipt in the drawer. Didn't buy a bulb yet.
"""

ZERO_ANCHORS = """
Someone found something important and had to decide what to do about it.
The situation was complicated and meaningful in many ways.
Feelings were involved. Eventually a choice was made.
"""


def test_moral_close_hard_fails_or_low():
    r = score_voice(MORAL_CLOSE)
    assert r["hard_fail"] is True or r["score"] < 6.5
    assert r["axes"]["moral_close"] <= 1
    assert r["gate"] == "fail"


def test_ban_heavy_low_glue_axis():
    r = score_voice(BAN_HEAVY)
    assert r["axes"]["glue_bans"] <= 1
    assert r["details"]["ban_hits"] >= 3
    assert r["gate"] == "fail" or r["score"] < 6.5


def test_good_voice_passes_threshold():
    r = score_voice(GOOD_VOICE)
    assert r["score"] >= 6.5
    assert r["gate"] == "pass"
    assert r["hard_fail"] is False
    assert r["axes"]["anchors"] >= 1


def test_zero_anchors_hard_fail_on_long_text():
    r = score_voice(ZERO_ANCHORS * 8)  # longer abstract fog
    assert r["hard_fail"] is True or r["axes"]["anchors"] == 0
    assert r["gate"] == "fail"


def test_score_has_required_keys():
    r = score_voice(GOOD_VOICE)
    for k in ("score", "gate", "hard_fail", "axes", "details", "threshold"):
        assert k in r
    for ax in ("anchors", "uneven", "moral_close", "rhythm", "glue_bans"):
        assert ax in r["axes"]


def test_sentence_variance_affects_rhythm():
    flat = "The cat sat. The dog ran. The bird flew. The fish swam. The fox hid. The owl saw."
    varied = (
        "The cat sat on the mat near the door. Rain. "
        "Somewhere under the sink a pipe ticked like a cheap watch and I left it alone."
    )
    r_flat = score_voice(flat)
    r_var = score_voice(varied + " " + "Kuala Lumpur 3:14 a.m. receipt #4421.")
    assert r_var["axes"]["rhythm"] >= r_flat["axes"]["rhythm"]
