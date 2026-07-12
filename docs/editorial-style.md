# Final Prime editorial style rules

## Punctuation rule: no long dashes

Public-facing copy must not contain either of these Unicode punctuation characters:

- U+2013, EN DASH
- U+2014, EM DASH

Use one of these alternatives instead:

- a period for a clean break;
- a comma for a short continuation;
- a colon for an explanation or label;
- a semicolon when two complete clauses belong together;
- parentheses for a true aside;
- a normal hyphen only inside a compound term.

Do not imitate the rhythm commonly associated with generated copy by joining clauses with long dashes. Rewrite the sentence so the logic is explicit.

## Enforcement

`tools/check_editorial_style.py` scans public site source files and fails when either forbidden code point appears. The GitHub Actions workflow runs the check on every push to `main` and on every pull request.
