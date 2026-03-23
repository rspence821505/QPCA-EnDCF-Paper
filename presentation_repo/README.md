# QPCA-EnDCF Thesis Defense Presentation

## Structure

```
presentation_repo/
├── slides/
│   ├── deck.md              # Main slide deck (37 slides, reveal.js markdown)
│   └── theme.css             # Custom dark theme
├── diagrams/
│   ├── qpca_pipeline.mmd     # QPCA-EnDCF algorithm flow
│   ├── method_comparison.mmd  # Stochastic vs QPCA-EnDCF comparison
│   ├── theory_structure.mmd   # Theoretical analysis dependency graph
│   └── experimental_overview.mmd  # Experimental evidence summary
├── charts/
│   └── chart_specs.json       # Vega-Lite specs for interactive charts
├── scripts/
│   └── generate_charts.py     # Chart generation script
├── appendix/
│   ├── backup_slides.md       # 10 backup slides
│   └── committee_qa.md        # 25 committee questions + answers
├── config/
│   └── presentation.yaml      # Presentation configuration
└── README.md                  # This file
```

## Running the Presentation

### Option 1: reveal.js (recommended)

```bash
# Install reveal.js
npm install reveal.js

# Or use reveal-md for quick serving
npm install -g reveal-md

# Serve the presentation
reveal-md slides/deck.md --theme slides/theme.css --port 8000
```

### Option 2: Manual reveal.js setup

1. Download reveal.js from https://revealjs.com
2. Place `slides/deck.md` as the content source
3. Include `slides/theme.css` as custom theme
4. Enable plugins: RevealMath, RevealNotes, RevealMermaid

### Viewing Mermaid Diagrams

```bash
# Install mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Render a diagram
mmdc -i diagrams/qpca_pipeline.mmd -o diagrams/qpca_pipeline.svg
```

### Generating Charts

```bash
pip install altair vl-convert-python
python scripts/generate_charts.py
```

## Figures

Publication figures are in `../paper/final_figures/`. The slide deck references them via relative paths.

## Speaker Notes

Speaker notes are embedded in each slide using `<!-- .notes: -->` blocks. Access them during presentation with the `S` key in reveal.js.

## Defense Preparation

- **Main deck:** 37 slides, targeting 35-40 minutes
- **Backup slides:** 10 slides covering proof details, full tables, implementation
- **Committee Q&A:** 25 hard questions with prepared answers in `appendix/committee_qa.md`
- **Pacing:** ~60-90 seconds per slide

## Key Keyboard Shortcuts (reveal.js)

- `S` — Open speaker notes
- `F` — Fullscreen
- `O` — Slide overview
- `B` — Black screen (pause)
- `→/←` — Navigate slides
- `Esc` — Exit overview/fullscreen
