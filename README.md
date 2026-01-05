Proof of concept highlighting critical weaknesses in Windows UI trust and recovery design.

This project demonstrates that a standard user-mode process — without admin rights, drivers, or kernel exploits — can convincingly lock a Windows session. It does so by switching the user to a separate desktop, presenting a full-screen system-impersonating crash screen, and suppressing Task Manager to block the primary recovery path users rely on.

While this PoC allows recovery via sign-out or power-off, the underlying design flaws it exposes are far more serious. The same mechanisms shown here can be combined with persistence, session re-entry, or startup execution to create situations where recovery becomes extremely difficult for non-technical users.

Nothing here relies on undefined behavior or exploits — only documented APIs and expected OS behavior.
That is the problem.

This repository exists to raise awareness that Windows currently allows user-space applications to:

Impersonate critical system failure states

Obstruct built-in recovery tools

Abuse desktop isolation in ways users cannot easily escape or distinguish from real system failure

These are architectural issues, not edge cases.
