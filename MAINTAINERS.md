# Maintainer guide (for the author)

This file is for you, the owner. It is not published on the site.

## One-time setup

1. Replace the placeholders everywhere:
   `grep -rl YOUR_GITHUB_USERNAME . | xargs sed -i 's/YOUR_GITHUB_USERNAME/<your-username>/g'`
   and put your name in `LICENSE` (`YOUR_NAME`). Then write your own `docs/about.md`.
2. Create a **public** repository named `appsec-mastery`, then push.
3. Repository settings:
   - Pages → Source: **GitHub Actions**.
   - Security → enable **secret scanning** and **push protection**.
   - Enable **Discussions** (Q&A and "show your solution" categories).
   - About box: description, website URL, topics (`appsec`, `application-security`, `cybersecurity`, `web-security`,
     `penetration-testing`, `ctf`, `study-notes`, `learning-in-public`, `owasp`, `linux`, `mkdocs`).
   - Settings → Social preview: upload a 1280x640 image (`docs/assets/banner.svg` exported to PNG).
4. Enable the pre-commit hook in your clone: `git config core.hooksPath .githooks`
5. Install locally: `pip install -r requirements.txt`, then `mkdocs serve`.

## Writing workflow

1. Draft in `docs/<stage>/<NN-subject>/lessons/_my-draft.md` (underscore = not published).
2. Do the lab. Paste real output. Redact anything secret (write `REDACTED`).
3. Check against a primary source. Fill the "Verified on" box.
4. Rename to drop the underscore. Add the lesson to the chapter's lessons index.
5. `python tools/curriculum.py refresh && mkdocs build --strict`
6. Commit. CI publishes.

Set `status: complete` in a chapter's `index.md` front matter only when lessons, solutions and defense answers all exist.

## Quality checklist per lesson

- Explains a mechanism, not just commands.
- Names primary sources.
- Real output from your lab, with versions and date.
- Includes at least one mistake you made.
- Has check-yourself questions answered from memory.
- Notes any AI use at the top.

## Growth, honestly

- Nothing replaces consistent, correct work. Publish something real every week.
- Do not announce the repo until Stage 0 has a lab-setup page and at least a handful of solid lessons.
- Share each strong lesson where learners already are (relevant subreddits, Hacker News for standout pieces, Mastodon/X/LinkedIn,
  Discords for CTF and AppSec learners, 42/1337 communities). Read each community's self-promotion rules first.
- Network by being useful: answer questions, fix others' docs, link your sources, credit people who correct you.
- Cut a GitHub release when a stage chapter completes.
- No star-buying, no spam. Both are noticed and cost you credibility, which is the real asset.
