# Contributing

Thank you for helping. The most valuable contributions are corrections.

## Ways to help

1. **Report an error.** Wrong command, outdated behavior, unclear explanation. Use the "Error report" issue template.
2. **Suggest a topic.** Something missing from a subject, with a primary source if you have one.
3. **Fix a typo or a broken link** with a pull request directly.
4. **Share your own solution** by linking your repository in a discussion. Please do not open pull requests with full solutions to the subjects.

## What I do not merge

- Text written entirely by an AI and not verified on a real lab. Disclose AI help; unverified commands will be rejected.
- Real secrets, private keys, real hostnames or personal data.
- Material that targets systems you do not own.

## Pull request checklist

- [ ] I ran `pip install -r requirements.txt && python tools/curriculum.py refresh && mkdocs build --strict` and it passes.
- [ ] I tested any command I changed.
- [ ] I did not add secrets (the pre-commit hook and CI scan for them).

Enable the hook once per clone: `git config core.hooksPath .githooks`

By contributing you agree your contribution is licensed under the same terms as the repository (see `LICENSE` and `LICENSE-CONTENT.md`).
