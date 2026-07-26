# Demo state reset

The demo console is fully client-side (localStorage). State resets:
1. automatically per visitor after 15 minutes (demo.js RESET_MS), and
2. on every deploy, because the JS ships a new deterministic seed if changed.

There is NO server-side demo state. No cron needed on the server.
