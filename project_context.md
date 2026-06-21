# Project Context

This file gives the test-case generator background about *your* project so the
test cases come out specific and accurate. Edit it to match your project, then
commit it. Everything below is injected into every generation. Delete a section
if you don't need it. If this whole file is blank, the app behaves exactly as
before (no project context).

## Product / domain overview
<!-- 2-4 sentences: what the product does, who uses it, key concepts. -->
e.g. "Acme Bank's customer portal. Users are retail banking customers who log
in to view accounts, transfer money, and pay bills."

## Domain glossary
<!-- Terms the model should use correctly. -->
- **Payee**: a saved recipient a user can transfer money to.
- **Standing instruction**: a scheduled recurring transfer.

## Epic background
<!-- The bigger initiative this story belongs to, so the model has context the
     story alone doesn't carry. -->
e.g. "Epic: Self-service password recovery. Goal is to reduce support tickets
by letting users reset credentials without calling the helpdesk."

## Testing standards & conventions
<!-- House rules for how test cases should look or what to always cover. -->
- Always include a test for accessibility (keyboard-only navigation).
- Cover both desktop and mobile web for any UI story.
- Negative tests must assert the exact validation message shown.

## Out of scope
<!-- Things NOT to write test cases for. -->
- Native mobile apps (web only).
- Performance/load testing (handled separately).
