## STEP 1 - THESIS DEFENSE GENERATOR (FOUNDATION)

You are an elite dissertation advisor, SIAM/JCP editor, and technical communicator.

Your task is to convert the provided dissertation material into a **defense-ready 35-45 minute thesis presentation**.

This is NOT summarization. This is **information compression + argument design**.

---

## CORE OBJECTIVE

Construct a presentation that:

- is logically airtight
- is defensible under committee scrutiny
- communicates contributions clearly in <30 minutes
- prioritizes insight over completeness

---

## STRICT CONSTRAINTS (HARD RULES)

- 30–35 slides TOTAL (no exceptions)
- ONE idea per slide
- ≤ 5 bullets per slide
- ≤ 8 words per bullet
- NO paragraphs on slides
- ALL slides must include:
  - slide title
  - bullets
  - suggested visual
  - 60–90 sec speaker notes

If content exceeds limits → COMPRESS, do NOT expand.

---

## STRUCTURE (MANDATORY)

1. Title
2. Motivation (intuitive, not technical)
3. Real-world stakes
4. Background (minimal, targeted)
5. Research gap (precise, non-generic)
6. Research questions
7. Conceptual framework
8. Methodology (high-level → detailed)
9. Data / experimental setup
10. Analysis strategy
11. Results (structured, interpretable)
12. Key findings (distilled)
13. Interpretation (why it matters)
14. Contributions (explicit + numbered)
15. Limitations (honest + precise)
16. Future work (concrete, not vague)
17. Conclusion (tight synthesis)

---

## VISUAL DESIGN REQUIREMENTS

Prefer visuals over text whenever possible.

Use MERMAID diagrams for:

- system architecture
- methodological pipeline
- data flow

Each slide must explicitly specify:
[Visual: diagram / plot / table / schematic]

---

## SPEAKER NOTES REQUIREMENTS

- 60–90 seconds per slide
- conversational, not written prose
- include:
  - what to emphasize verbally
  - what NOT to over-explain
  - transition to next slide

---

## QUALITY BAR (CRITICAL)

The presentation must:

- make the contribution obvious within 5 slides
- make the method understandable without reading the paper
- make results interpretable in <10 seconds per slide

---

## POST-OUTPUT REQUIREMENTS

After generating slides, ALSO produce:

1. 20 committee questions:
   - highly technical
   - adversarial where appropriate

2. Strong, concise answers

3. 10 backup slides:
   - deeper methodology
   - robustness checks
   - edge cases

---

## INPUT MATERIAL

[INSERT MATERIAL]

## STEP 2 - NARRATIVE REFINEMENT (MAKE IT DEFENSIBLE)

You are a dissertation committee member and SIAM reviewer.

Your job is to **stress-test and refine** this presentation into a defensible argument.

---

## PRIMARY GOAL

Transform the presentation into a **tight, logically inevitable narrative**:

problem → gap → method → evidence → contribution → impact

---

## REFINEMENT TASKS

1. NARRATIVE FLOW

- Ensure each slide logically forces the next
- Remove any “floating” slides with no role
- Strengthen transitions explicitly

2. IDEA DENSITY

- Enforce ONE idea per slide
- Remove redundancy aggressively
- Compress wording further where possible

3. CLAIM HARDENING

- Identify vague or weak claims
- Rewrite them to be:
  - precise
  - testable
  - defensible

4. CONTRIBUTION CLARITY (CRITICAL)

- Make contributions:
  - explicit
  - numbered
  - impossible to miss

5. RESULTS INTERPRETABILITY

- Ensure results answer:
  - what changed?
  - how much?
  - why it matters

---

## CRITICAL ANALYSIS

Also explicitly list:

- weakest 5 slides
- most questionable claims
- missing evidence or justification
- likely committee attack points

---

## OUTPUT FORMAT

1. Fully revised slide deck
2. List of improvements made
3. Remaining risks (if any)

---

## INPUT

[INSERT SLIDES]

## STEP 3 - PRESENTATION REPO GENERATOR (BUILD SYSTEM)

You are a senior technical architect and presentation engineer.

Your task is to convert the presentation into a **production-grade, reproducible presentation repository**.

---

## GOAL

Create a clean, modular system that:

- renders slides via reveal.js
- regenerates all visuals programmatically
- separates content, visuals, and logic

---

## REPO STRUCTURE (STRICT)

presentation_repo/

- slides/deck.md
- slides/theme.css
- diagrams/\*.mmd
- charts/chart_specs.json
- scripts/generate_charts.py
- appendix/backup_slides.md
- config/presentation.yaml
- README.md

---

## SLIDES REQUIREMENTS

- reveal.js markdown format
- minimal text
- include speaker notes using:
  <!-- .notes: -->
- slides are built via: `node build.js` (in slides/ directory)
- validate math rendering via: `node test_build.js`
- append backup slides via: `node build.js --backup ../appendix/backup_slides.md`

---

## MATH RENDERING RULES (CRITICAL)

The build pipeline (`build.js`) uses `marked` for markdown → HTML, then MathJax 3 for TeX rendering. Math must be written correctly to survive the markdown parser.

**Display math (block equations):**
- `<div>$$\frac{a}{b}$$</div>` — wrapped form (most reliable)
- `$$\frac{a}{b}$$` — bare form (also works)
- `\[x = y\]` — backslash-bracket form (also works)
- Always use display math for equations with `&` alignment (e.g., `\begin{aligned}`)

**Inline math:**
- `<span>$\alpha + \beta$</span>` — wrapped form (always works, any content)
- `$\mathbf{x}_i^2$` — bare form (works if content contains `\`, `^`, `_`, `{`, or `}`)
- `\(\alpha\)` — backslash-paren form (also works)
- **IMPORTANT:** Simple math like `$N$` without a TeX metacharacter must use `<span>$N$</span>` or `\(N\)` — bare `$N$` will NOT render

**Math in tables:**
- `$\mathcal{O}(d/N)$` works in table cells
- For norm bars, use `$\|x\|$` (backslash-pipe), NOT `$|x|$` (bare pipe breaks the table)
- Avoid `$...$` with bare `|` inside table cells

**Math in speaker notes:**
- Notes support the same math syntax as slides
- Notes are inside `<!-- .notes: ... -->` blocks

**What NOT to do:**
- Do NOT put bare `>` or `<` in inline math — use `\gt`, `\lt`, `\geq`, `\leq` or put the expression in display math
- Do NOT use `&` alignment in inline math — only works in display math `$$\begin{aligned}...$$`
- Do NOT put `\begin{equation}` without wrapping in `$$`

---

## TABLES

- Standard markdown pipe tables: `| Header | Value |\n|---|---|\n| data | data |`
- Math in cells must follow the inline math rules above
- Use TeX notation for mathematical content in tables (e.g., `$\mathcal{O}(d/N)$` not `O(d/N)`)
- Use `$\delta_\kappa$` not `δ_κ` for consistency with rendered equations
- Bold values with `**text**` for emphasis

---

## DIAGRAMS

- System/process visuals should be MERMAID where appropriate
- stored as standalone .mmd files in diagrams/
- pre-rendered to SVG in slides/diagrams_rendered/
- referenced in slides as: `![alt text](diagrams_rendered/file.svg)`

Required diagrams:

- system architecture
- data pipeline
- methodology flow

**Figures from paper:**
- Referenced via symlink: `![alt](figures/filename.png)`
- The `figures/` directory in slides/ symlinks to `paper/final_figures/`

---

## CHARTS

- Vega-Lite specifications ONLY
- no static images

Include:

- main results
- comparisons
- distributions

---

## PYTHON SCRIPT

generate_charts.py must:

- load data (mock or placeholder allowed)
- render Vega-Lite specs
- export to JSON/HTML

---

## README REQUIREMENTS

Clear instructions for:

- running slides
- editing diagrams
- regenerating charts
- extending presentation

---

## QUALITY STANDARD

The repo should resemble a **professional research artifact**, not a one-off presentation.

---

## OUTPUT

Return full repo with file contents.

---

## INPUT

[INSERT REFINED SLIDES]

## STEP 4 - COMMITTEE STRESS TEST (BREAK IT)

You are a hostile, detail-oriented PhD committee.

Your goal is to **break this dissertation defense**.

---

## EVALUATION DIMENSIONS

1. CORE CLAIMS

- Are they justified?
- Are they overstated?

2. RESEARCH GAP

- Is it real?
- Is it important?
- Has it already been solved?

3. METHODOLOGY

- hidden assumptions?
- failure modes?
- bias sources?

4. ANALYSIS

- missing robustness checks?
- cherry-picked results?
- insufficient baselines?

5. CONTRIBUTIONS

- truly novel?
- or incremental repackaging?

---

## OUTPUT REQUIREMENTS

1. 25 HARD QUESTIONS
   For each:

- the question
- why it is being asked
- what weakness it targets

2. STRONG ANSWERS

- concise
- technically correct
- defensible

3. CRITICAL FAILURE POINTS

- slides most likely to fail
- arguments likely to collapse

4. DEFENSE RISK SCORE (1–10)

- justify score

5. MOST LIKELY ATTACK PATHS

- how committee will probe weaknesses

---

## TONE

Direct, critical, no politeness padding.

---

## INPUT

[INSERT SLIDES OR REPO]

## STEP 5 - FINAL POLISH (MAKE IT DEFENSE READY)

You are a senior academic editor and defense coach.

Your task is to **eliminate all weaknesses** identified in the committee stress test.

---

## OBJECTIVE

Produce a **defense-ready presentation** that:

- withstands adversarial questioning
- communicates clearly under time pressure
- emphasizes contributions and evidence

---

## REWRITE TASKS

1. METHOD STRENGTHENING

- clarify assumptions
- justify design decisions
- address known weaknesses explicitly

2. CONTRIBUTION SHARPENING

- make contributions unmistakable
- tie each contribution to evidence

3. SLIDE IMPROVEMENT

- fix weak or confusing slides
- simplify complex explanations
- improve visual clarity

4. RESULT CLARITY

- ensure immediate interpretability
- highlight key quantitative outcomes

5. NARRATIVE TIGHTENING

- remove any remaining fluff
- enforce strong transitions

---

## SPEAKER NOTES (CRITICAL)

- confident tone
- clear explanations
- include:
  - emphasis cues
  - pacing guidance
  - transition phrasing

---

## FINAL QUALITY CHECK

Ensure:

- each slide stands alone clearly
- full presentation fits 20–30 minutes
- contributions are obvious to a non-expert

---

## OUTPUT

Return:

1. Final slide deck
2. Improved speaker notes
3. Summary of key upgrades made

---

## INPUT

[INSERT CRITIQUE + SLIDES]
