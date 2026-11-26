# ntfifwyb

A minimalist portfolio shown on the user's GitHub profile page (https://github.com/ntfifwyb),
built as a GitHub profile README. It is not the user's actual portfolio: a separate portfolio
website is planned as a later, separate idea.

The spec is `docs/BRIEF.md`; decisions are in `docs/DECISIONS.md`.

The web and the README links table are drawn by `scripts/web.py` from the project list in it:
edit the list, run `python3 scripts/web.py`, commit the output (`.local-ci` checks they match).

The repo is public (since 2026-11-25): everything committed here is visible to anyone.

## Not doing

- The real portfolio website (a separate, future idea).
- Auto-generated widgets (stats cards, streaks, language charts, badges).
- Automated updates: the list is edited by hand.

## Constraints

- Development costs $0.
- Anthropic's rules (checked 2026-11-25, Usage Policy effective 2026-11-12): allowed, with
  limits: no Anthropic logos or implied endorsement; built from the user's own repos.
