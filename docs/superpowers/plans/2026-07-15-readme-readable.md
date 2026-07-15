# README readability rewrite

> **For agentic workers:** Execute task-by-task; push when user asks for a change.

**Goal:** Make the GitHub README scannable for a stranger in 30 seconds — plain English first, no washed-out quotes, less jargon wall.

**Architecture:** Reorder sections (what → demo → how → numbers → install). Replace grey blockquotes with high-contrast fenced code blocks. Define terms once. Drop internal redesign noise from the hero.

**Tech Stack:** Markdown only (`README.md`); optional light chart regen later.

---

### Task 1: Hero + plain English

- [ ] One-line what it is without VOICE/StoryScope alphabet soup
- [ ] “What it is / isn’t” in short bullets a human can skim
- [ ] Define VOICE and StoryScope in one line each, later

### Task 2: Show don’t drown

- [ ] Excerpts as ` ```text ` fences (readable on dark GitHub), labeled default vs noslop
- [ ] Short score table after the demo, not before
- [ ] Charts after table; keep dark charts (data only)

### Task 3: How it works + pack + layout

- [ ] Simple loop in prose + one mermaid max (or keep two if small)
- [ ] Skill pack + repo layout brief

### Task 4: Install at bottom + license

- [ ] Install + quickstart last before license
- [ ] Push to origin/main

### Done when

- Stranger understands “agent skill for less AI-slop writing + local score tools”
- Excerpts are readable on GitHub dark mode
- Install is bottom
- Pushed
