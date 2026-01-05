Proof of concept exposing serious Windows UX and recovery weaknesses.
This program demonstrates how a user-mode application can convincingly lock a Windows session without admin privileges. It switches the user to a separate desktop, displays a full-screen BSOD-style screen, and continuously terminates Task Manager to block the most common escape route.

No kernel exploits. No drivers. No elevation.
Just abusing design decisions.

Recovery is still possible by signing out, switching users, or powering off — but the fact that this works at all highlights how fragile Windows’ trust model is around desktops, UI authority, and recovery tooling.

This is a demonstration, not an attack. The goal is to raise awareness of how easily Windows can be made to look catastrophically broken while remaining entirely user-space.
