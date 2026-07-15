I’m writing this after a green local run and a red CI job at 14:03 UTC on the same commit — jaw clenched, coffee gone cold — classic toast flake.

**What usually bites**

1. Local paints the toast in ~80ms; CI under load paints it in 400–900ms, after `expect(locator).toBeVisible()` already timed out at 5s if the click raced ahead.
2. The toast unmounts. Assert text after it’s gone.
3. Strict mode: two toasts in DOM (old + new). Playwright throws; people call it flake.

**Debug path I use (in order)**

1. Open the CI trace (`npx playwright show-trace trace.zip`). Jump to the action before the toast. Note the timestamp gap.
2. Log `page.locator('[data-testid=toast]').count()` right after the trigger. If it’s 0 in CI and 1 local, it’s timing, not selector poetry.
3. Prefer role + name: `getByRole('status', { name: /saved/i })` over CSS soup.
4. Wait on the condition, not `waitForTimeout(2000)`:
   `await expect(page.getByRole('status')).toContainText('Saved', { timeout: 15_000 })`
5. If the app removes the toast fast, assert during visibility or assert a durable side effect (URL, table row).

**The turn (climax)**

Half the “CI-only toast flakes” I see aren’t the toast — they’re a preceding API that 500s under CI’s slower DB, so the toast never fires. Trace the network panel before inventing smarter waits. That reframe is what closed my ticket at 14:10 when I merged the role selector, the 15s timeout, *and* a stub for the flaky API in CI.

**Aftermath — more than one room after the merge**

Same day, 16:30: CI ran twice green. I threw out the cold coffee. Jaw unclenched enough to eat.

Next morning, 09:02: pipeline green again without me touching the branch. Shoulders dropped at the desk.

Two days later: a junior pinged “toast flake?” I sent this path, not a pep talk. Their PR picked up the network check first.

One week out, 14:03 UTC on a different commit: still green on the toast suite. I’m writing this so the next person doesn’t spend another night with a locked jaw staring at a red check that only fails in CI — leave the role selector, the 15s wait, and the API stub in the PR.
