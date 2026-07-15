Green local. Red CI. Same commit. 14:03 UTC.

Toast paints ~80ms on my laptop, 400–900ms under CI load. `toBeVisible()` already timed out if you raced the click. Or the toast unmounts before you assert text. Or two toasts in DOM and strict mode throws.

Open the CI trace. Count `[data-testid=toast]` right after the action. Prefer `getByRole('status', { name: /saved/i })`. Wait on text with `{ timeout: 15_000 }`, not `waitForTimeout(2000)`.

Half the “toast flakes” I see: preceding API 500s on slow CI DB. Toast never fires. Network panel first.

I left a 15s timeout in the PR. Pipeline green at 14:10. Coffee was cold.
