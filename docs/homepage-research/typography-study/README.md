# Final Prime motto typography study

Status: research-only. Nothing in this directory is loaded by the production homepage.

The study isolates the typography of the locked motto:

> Knowing the next move is survival.
>
> Understanding the game is control.

The investigation is split into three controlled stages:

1. **Font-family sweep:** the same refined four-line composition is rendered in Inter, Source Sans 3, IBM Plex Sans, Manrope and Segoe UI Variable, beside the current Aptos Display control.
2. **Composition sweep:** Inter is held constant while line count, hierarchy, color distribution, alignment and grouping change.
3. **Finalists:** the strongest combinations are rendered in the real hero proportions at desktop and mobile widths, then assessed against clarity, brand fit, visual balance, restraint and responsive stability.

## Reproducible preview sources

The three `*-source.txt` files are deliberately non-route source snapshots. Copy them to `.html` files in a temporary Playwright output directory when regenerating the boards; this keeps research scaffolding out of the public route contract.

Available variants: `C0`, `F1`-`F5`, `L1`-`L11`, and finalists `P1`-`P6`.

The browser preview loads research fonts from the official Inter distribution and Google Fonts. The rendered PNG artifacts are the durable comparison record. Production font delivery is a separate decision and must be self-hosted if Inter is selected.

## Results

- [Research report](research-report.md)
- [Evidence ledger](evidence-ledger.csv)
- [Decision matrix](decision-matrix.csv)
- [Font-family collage](screenshots/fonts-collage.png)
- [Composition collage](screenshots/layouts-collage.png)
- [Desktop + mobile finalists P1-P3](screenshots/finalists-part-1.png)
- [Desktop + mobile finalists P4-P6](screenshots/finalists-part-2.png)
