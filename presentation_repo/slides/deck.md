---
title: "A Data-Consistent approach to Ensemble Filtering"
subtitle: "A Unified Theoretical Framework"
author: "Rylan Spence"
date: "2026"
theme: custom
transition: slide
revealOptions:
  slideNumber: true
  hash: true
  center: true
  width: 1920
  height: 1080
  margin: 0.04
---

<!-- ============================================================ -->
<!-- SECTION 1: PROBLEM (Slides 1-7) -->
<!-- ============================================================ -->

---

<!-- .slide: data-background="#1a1a2e" -->

# Spectral Regularization and Probabilistic Calibration in Ensemble Filtering

### A Unified Theoretical Framework

**Rylan Spence**

<!-- Dissertation Defense — 2026 -->

CHG Presentation - 2026

<!-- .notes:
Welcome everyone, and thank you for being here. Today I'm presenting my presentation on Data-Consistent Inversion for ensemble data assimilation. The core question: can we build ensemble filters that give reliable uncertainty estimates — not just accurate point predictions — under severe computational constraints? I'll show that deterministic spectral projection achieves this, with both rigorous theory and comprehensive experiments.
-->

---

## The Promise of Ensemble Filtering

- Bayesian state estimation for high-dimensional systems
- Represent uncertainty with N state realizations
- Practical for operational weather, ocean, climate
- Avoid explicit covariance manipulation

**But: what happens when N is small?**

<!-- .element: class="fragment" -->

<!-- .notes:
Ensemble Kalman filtering is the backbone of operational data assimilation — used in weather prediction, ocean modeling, and climate science. The idea is elegant: represent posterior uncertainty through a small collection of state vectors, avoiding the need to store or manipulate full covariance matrices. But operational constraints force us to use very small ensembles — often 10 to 50 members for systems with millions of unknowns. What happens to uncertainty quantification in that regime is the central question of this work.
-->

---

## The Undersampling Crisis

| Parameter               | Value     |
| ----------------------- | --------- |
| State dimension n       | 40        |
| Observations per time m | 20        |
| Ensemble size N         | 10        |
| Covariance rank         | 9 or less |

- **n > m > N**: severely undersampled
- Covariance has 31 zero eigenvalues
- Sampling noise corrupts nonzero eigenvalues

<!-- .notes:
Here's the regime I study. In the Lorenz-96 system with 40 state variables, we observe 20 components but have only 10 ensemble members. The empirical covariance has rank at most 9 — it's missing information in 31 directions. And the eigenvalues it does estimate are biased downward. This is a mathematical certainty, not an implementation failure. The question is: what do we do about it?
-->

---

## Variance Collapse in Action

![Spread vs RMSE Temporal](figures/spread_vs_rmse_temporal.png)

- **Stochastic EnKF**: spread ≈ 0.3, RMSE ≈ 4.5
- Ensemble claims $\sigma = 0.3$, actual error = 4.5
- **15× overconfident** uncertainty estimates

<!-- .notes:
This figure tells the whole story of the problem. The solid lines are ensemble spread — what the filter thinks the error is. The dashed lines are RMSE — the actual error. For sequential EnKF, the spread flatlines near 0.3 while the true error fluctuates between 3 and 6. That means the filter is 15 times more confident than it should be. The 4D-EnKF is slightly better but still severely underdispersed. This isn't just an academic concern — overconfident uncertainty renders ensemble forecasts unreliable for decision-making.
-->

---

## Why This Matters

- Weather: ensemble spread drives warning thresholds
- Ocean: misspecified uncertainty → poor reanalysis
- Climate: bias in projection confidence bands

**Overconfident ensembles are worse than no uncertainty**

<!-- .notes:
Why should we care about calibration? Because downstream decisions depend on it. In weather forecasting, ensemble spread directly controls warning thresholds. If spread is 15 times too small, extreme events go unwarned. In ocean reanalysis, misspecified uncertainty corrupts initialization. Overconfident uncertainty isn't just imprecise — it's actively misleading. It's worse than admitting you don't know.
-->

---

## The Stochastic Perturbation Problem

Standard EnKF adds random noise to preserve variance:

<div>$$\mathbf{x}^{(j),a} = \mathbf{x}^{(j),f} + \mathbf{K}(\mathbf{z} + \boldsymbol{\epsilon}^{(j)} - \mathbf{H}\mathbf{x}^{(j),f})$$</div>

- <span>$\mathbf{x}^{(j),f}$</span>: forecast state for member <span>$j$</span> — <span>$\mathbf{x}^{(j),a}$</span>: analysis (updated) state
- <span>$\mathbf{K}$</span>: Kalman gain matrix — <span>$\mathbf{H}$</span>: observation operator
- <span>$\mathbf{z}$</span>: observation vector — <span>$\boldsymbol{\epsilon}^{(j)} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$</span>: stochastic perturbation

**Two costs of perturbations** (where <span>$d = mL$</span>, total observation dimension):

1. Irreducible variance: $\mathcal{O}(\|\mathbf{K}\|^2 d / N)$
2. Noise distributed across all dimensions — no adaptivity

<!-- .notes:
Let me explain why standard methods fail. The stochastic EnKF adds random perturbations epsilon-j to each observation to preserve ensemble variance. This is mathematically elegant — it ensures second-moment consistency in expectation. But it injects sampling noise that scales with the gain magnitude, the observation dimension d, and inversely with ensemble size N. Critically, this noise is distributed uniformly across all observation dimensions. It doesn't distinguish between directions where there's real signal and directions dominated by noise. For small N, this uniform injection overwhelms the update.
-->

---

## The Gap This Work Addresses

| Challenge            | Current State                    |
| -------------------- | -------------------------------- |
| Variance collapse    | Patched with inflation heuristic |
| Calibration          | Not connected to regularization  |
| Perturbation noise   | Accepted as cost of business     |
| Bias-variance theory | Missing for spectral methods     |

**The core question: can we build ensemble filters that give reliable uncertainty estimates — not just accurate point predictions — under severe computational constraints? I'll show that the answer is yes.**

<!-- .notes:
So here's the landscape before this work. Variance collapse is treated with inflation — an empirical hack that requires per-system tuning. Calibration is measured post-hoc but not theoretically connected to algorithmic design choices. Observation perturbation noise is accepted as the price of maintaining ensemble diversity. And there's no theory explaining why or how spectral regularization in observation space should yield calibrated uncertainty. This dissertation fills that gap with three contributions: a new deterministic algorithm, a rigorous bias-variance theory, and comprehensive empirical validation. Let me start with the algorithm.
-->

---

<!-- ============================================================ -->
<!-- SECTION 2: METHOD (Slides 8-14) -->
<!-- ============================================================ -->

## QPCA-EnDCF: Core Idea

**Replace stochastic perturbations with deterministic spectral projection**

Three-stage pipeline:

1. **Whiten** residuals by observation uncertainty
2. **Identify** dominant mismatch modes via PCA
3. **Correct** only along signal-dominated directions

<!-- .notes:
The method I propose — QPCA-EnDCF — takes a fundamentally different approach. Instead of injecting noise to preserve variance, we apply a deterministic correction that's spectrally regularized. The pipeline has three stages. First, whiten the forecast-observation residuals so noise has unit covariance. Second, do PCA on those whitened residuals to find the directions of dominant mismatch. Third, correct only along those dominant directions — leave everything else unchanged. No random perturbations. No inflation. Let me walk through each stage.
-->

---

## Stage 1: Whitening

Normalize residuals by observation uncertainty:

<div>$$\mathbf{E} = (\mathbf{R}^{(L)})^{-1/2}(\mathbf{Z}^{(w)} - \mathbf{z}^{(w)}\mathbf{1}^\top)$$</div>

- <span>$\mathbf{Z}^{(w)} \in \mathbb{R}^{d \times N}$</span>: forecast observations stacked over the window (<span>$N$</span> columns, one per member)
- <span>$\mathbf{z}^{(w)} \in \mathbb{R}^{d}$</span>: actual observations; <span>$\mathbf{1}^\top$</span> broadcasts subtraction across all members
- <span>$\mathbf{R}^{(L)}$</span>: block-diagonal observation error covariance over <span>$L$</span> times; <span>$(\mathbf{R}^{(L)})^{-1/2}$</span> whitens so noise has unit covariance
- Each column of <span>$\mathbf{E}$</span>: one member's normalized mismatch — signal structure now visible in eigenspectrum

**Key insight: normalizing by $\mathbf{R}^{(L)}$ makes noise isotropic — any remaining structure is genuine forecast-observation mismatch**

<!-- .notes:
Stage 1 is whitening. We take each ensemble member's forecast observations, subtract the actual observations to get residuals, and normalize by the observation error covariance. After whitening, the observation noise has identity covariance. This is crucial because it means any structure we see in the eigenspectrum of the residual covariance represents genuine forecast-observation mismatch, not observation noise artifacts. The whitening step is what makes the subsequent PCA meaningful.
-->

---

## Stage 2: Spectral Decomposition

Decompose centered whitened residual covariance:

<div>$$\mathbf{C}_E = \frac{1}{N-1}\mathbf{E}_c\mathbf{E}_c^\top = \hat{\mathbf{V}}\hat{\boldsymbol{\Lambda}}\hat{\mathbf{V}}^\top = \sum_{i=1}^{r} \hat{\lambda}_i \hat{\mathbf{v}}_i \hat{\mathbf{v}}_i^\top$$</div>

- Large $\lambda_i$ → coherent dynamical mismatch (signal)
- Small $\lambda_i$ → sampling noise
- Rank <span>$r$</span> = min(<span>$d$</span>, <span>$N$</span>−1)

**Key insight: eigenspectrum separates signal from noise**

<!-- .notes:
Stage 2 decomposes the whitened residual covariance spectrally. The eigenvalues tell us how much variance there is in each orthogonal direction of observation space. Large eigenvalues correspond to coherent, dynamically meaningful discrepancies between forecast and observations — these are the directions where the ensemble is systematically wrong. Small eigenvalues are sampling noise. In our experiments, the leading eigenvalue captures 60 to 80 percent of the total residual variance. This rapid spectral decay is what makes aggressive truncation viable.
-->

---

## Stage 3: Truncated Correction

Project onto leading κ modes and correct:

<div>$$\mathbf{Q}_{\mathrm{PCA}} = -\hat{\mathbf{V}}_\kappa \hat{\mathbf{V}}_\kappa^\top \mathbf{E}$$</div>

<div>$$\boldsymbol{\Delta}_{\mathrm{obs}} = (\mathbf{R}^{(L)})^{1/2} \mathbf{Q}_{\mathrm{PCA}}$$</div>

<div>$$\mathbf{X}_{k_w}^a = \mathbf{X}_{k_w}^f + \mathbf{K}^{\mathrm{DC}} \boldsymbol{\Delta}_{\mathrm{obs}}$$</div>

- $\kappa = 1$ in all experiments (leading mode only)
- No perturbations → no perturbation noise
- Orthogonal directions left **unchanged**

<!-- .notes:
Stage 3 applies the correction. We project the whitened residuals onto just the leading kappa eigenvectors — in all our experiments, kappa equals 1. That single dominant mode captures the systematic forecast-observation mismatch. We correct along that direction and leave everything else alone. The negative sign ensures we're pushing ensemble members toward the observations. Then we un-whiten and apply through the cross-covariance gain to get state-space increments. The critical point: directions orthogonal to the retained subspace are not touched. No noise is injected there. Ensemble diversity in those directions is preserved exactly.
-->

---

## Algorithm Overview

<div style="display: flex; gap: 2em; align-items: flex-start;">
<div style="flex: 1;">

**For each assimilation window** $\mathbf{w}$:

1. Propagate ensemble through <span>$L$</span> observation times
2. Stack forecast observations $\mathbf{Z}^{(w)}$
3. Whiten: $\mathbf{E} = \mathbf{R}^{-1/2}(\mathbf{Z}^{(w)} - \mathbf{z}^{(w)})$
4. Center: $\mathbf{E}_c = \mathbf{E} - \mathrm{mean}(\mathbf{E})$
5. Eigendecompose: $\mathbf{C}_E = \mathbf{E}_c\mathbf{E}_c^\top/(N-1)$
6. Truncate: keep leading $\kappa$ eigenvectors
7. Project: $\mathbf{Q}_{\mathrm{PCA}} = -\hat{\mathbf{V}}_\kappa\hat{\mathbf{V}}_\kappa^\top\mathbf{E}$
8. Unwhiten: $\boldsymbol{\Delta}_{\mathrm{obs}} = \mathbf{R}^{1/2}\mathbf{Q}_{\mathrm{PCA}}$
9. Apply gain: $\mathbf{X}^a = \mathbf{X}^f + \mathbf{K}^{\mathrm{DC}}\boldsymbol{\Delta}_{\mathrm{obs}}$

</div>
<div style="flex: 1;">

![QPCA-EnDCF Pipeline](diagrams_rendered/qpca_pipeline.svg)

</div>
</div>

<!-- .notes:
Here's the full algorithm. For each assimilation window, we propagate the ensemble, stack the forecast observations, whiten, center, eigendecompose, truncate to kappa modes, project the whitened residuals, unwhiten, and apply the gain. It's completely deterministic — same inputs always give same outputs. No random number generation beyond the initial ensemble. The computational overhead relative to a standard EnKF is one eigendecomposition of a d-by-d matrix per window, which is negligible relative to model propagation cost.
-->

---

## Geometric Interpretation

<div style="display:flex; gap:0; align-items:flex-start; margin-top:0;">

<svg viewBox="0 0 460 470" style="flex:1; max-height:78vh;">
  <defs>
    <marker id="mr" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#b53a2a"/></marker>
    <marker id="mg" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#999"/></marker>
  </defs>
  <text x="230" y="22" text-anchor="middle" fill="#b53a2a" font-size="14" font-weight="700">(a) Stochastic EnKF</text>
  <!-- TOP: forecast + perturbations -->
  <line x1="40" y1="150" x2="420" y2="150" stroke="#c8c0b4" stroke-width="0.5"/>
  <line x1="230" y1="42" x2="230" y2="258" stroke="#c8c0b4" stroke-width="0.5"/>
  <text x="426" y="154" fill="#a09888" font-size="10" font-style="italic">v̂₁</text>
  <text x="234" y="40" fill="#a09888" font-size="10" font-style="italic">v̂₂</text>
  <circle cx="230" cy="150" r="120" fill="none" stroke="#b53a2a" stroke-width="0.5" stroke-dasharray="2.5,3" opacity="0.2"/>
  <ellipse cx="230" cy="150" rx="100" ry="65" fill="#b53a2a" fill-opacity="0.04" stroke="#b53a2a" stroke-width="0.9" stroke-dasharray="4,3" stroke-opacity="0.4"/>
  <circle cx="178" cy="132" r="3.5" fill="#5a4e40"/>
  <line x1="178" y1="132" x2="145" y2="108" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="205" cy="112" r="3.5" fill="#5a4e40"/>
  <line x1="205" y1="112" x2="188" y2="78" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="242" cy="128" r="3.5" fill="#5a4e40"/>
  <line x1="242" y1="128" x2="278" y2="100" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="275" cy="140" r="3.5" fill="#5a4e40"/>
  <line x1="275" y1="140" x2="312" y2="145" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="262" cy="168" r="3.5" fill="#5a4e40"/>
  <line x1="262" y1="168" x2="292" y2="194" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="215" cy="178" r="3.5" fill="#5a4e40"/>
  <line x1="215" y1="178" x2="195" y2="208" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="188" cy="164" r="3.5" fill="#5a4e40"/>
  <line x1="188" y1="164" x2="152" y2="176" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="250" cy="160" r="3.5" fill="#5a4e40"/>
  <line x1="250" y1="160" x2="272" y2="186" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <text x="348" y="72" fill="#b53a2a" font-size="11" font-style="italic">ε⁽ʲ⁾ ~ 𝒩(0, R)</text>
  <text x="348" y="86" fill="#b53a2a" font-size="10" opacity="0.7">full d-space</text>
  <!-- Transition -->
  <line x1="230" y1="270" x2="230" y2="300" stroke="#999" stroke-width="1.2" marker-end="url(#mg)"/>
  <text x="248" y="290" fill="#999" font-size="10" font-style="italic">update + perturb</text>
  <!-- BOTTOM: collapsed -->
  <line x1="40" y1="380" x2="420" y2="380" stroke="#c8c0b4" stroke-width="0.5"/>
  <line x1="230" y1="315" x2="230" y2="445" stroke="#c8c0b4" stroke-width="0.5"/>
  <ellipse cx="230" cy="380" rx="100" ry="65" fill="none" stroke="#d0c8bc" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.3"/>
  <ellipse cx="230" cy="380" rx="24" ry="16" fill="#b53a2a" fill-opacity="0.06" stroke="#b53a2a" stroke-width="1.4" stroke-opacity="0.7"/>
  <circle cx="222" cy="375" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="232" cy="371" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="240" cy="378" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="226" cy="385" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="236" cy="388" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="218" cy="383" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="230" cy="380" r="3" fill="#b53a2a" opacity="0.7"/>
  <circle cx="228" cy="376" r="3" fill="#b53a2a" opacity="0.7"/>
  <text x="230" y="432" text-anchor="middle" fill="#b53a2a" font-size="12" font-weight="600">isotropic collapse</text>
  <text x="230" y="448" text-anchor="middle" fill="#999" font-size="10" font-style="italic">Var(ε) ~ 1/N  ≪  removed spread</text>
</svg>

<svg viewBox="0 0 460 470" style="flex:1; max-height:78vh;">
  <defs>
    <marker id="mt" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#1a7a6d"/></marker>
    <marker id="mg2" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#999"/></marker>
  </defs>
  <text x="230" y="22" text-anchor="middle" fill="#1a7a6d" font-size="14" font-weight="700">(b) QPCA-EnDCF</text>
  <!-- TOP: forecast + signal-only arrows -->
  <line x1="230" y1="42" x2="230" y2="258" stroke="#c8c0b4" stroke-width="0.5"/>
  <text x="234" y="40" fill="#a09888" font-size="10" font-style="italic">v⊥</text>
  <rect x="35" y="142" width="390" height="16" rx="1" fill="#1a7a6d" fill-opacity="0.05"/>
  <line x1="35" y1="150" x2="425" y2="150" stroke="#1a7a6d" stroke-width="1.2" opacity="0.35"/>
  <text x="430" y="154" fill="#1a7a6d" font-size="10" font-weight="600">v̂₁</text>
  <text x="430" y="166" fill="#1a7a6d" font-size="9" opacity="0.6">signal</text>
  <ellipse cx="230" cy="150" rx="100" ry="65" fill="#1a7a6d" fill-opacity="0.03" stroke="#1a7a6d" stroke-width="0.9" stroke-dasharray="4,3" stroke-opacity="0.4"/>
  <circle cx="178" cy="132" r="3.5" fill="#5a4e40"/>
  <line x1="178" y1="132" x2="202" y2="132" stroke="#1a7a6d" stroke-width="1.5" marker-end="url(#mt)"/>
  <circle cx="205" cy="112" r="3.5" fill="#5a4e40"/>
  <circle cx="242" cy="128" r="3.5" fill="#5a4e40"/>
  <circle cx="275" cy="140" r="3.5" fill="#5a4e40"/>
  <line x1="275" y1="140" x2="252" y2="140" stroke="#1a7a6d" stroke-width="1.5" marker-end="url(#mt)"/>
  <circle cx="262" cy="168" r="3.5" fill="#5a4e40"/>
  <line x1="262" y1="168" x2="242" y2="168" stroke="#1a7a6d" stroke-width="1.5" marker-end="url(#mt)"/>
  <circle cx="215" cy="178" r="3.5" fill="#5a4e40"/>
  <circle cx="188" cy="164" r="3.5" fill="#5a4e40"/>
  <line x1="188" y1="164" x2="208" y2="164" stroke="#1a7a6d" stroke-width="1.5" marker-end="url(#mt)"/>
  <circle cx="250" cy="160" r="3.5" fill="#5a4e40"/>
  <line x1="250" y1="160" x2="234" y2="160" stroke="#1a7a6d" stroke-width="1.5" marker-end="url(#mt)"/>
  <text x="200" y="100" fill="#bbb" font-size="9" text-anchor="middle">no update</text>
  <line x1="200" y1="103" x2="200" y2="109" stroke="#ccc" stroke-width="0.6"/>
  <text x="266" y="192" fill="#bbb" font-size="9" text-anchor="middle">no update</text>
  <line x1="266" y1="184" x2="266" y2="178" stroke="#ccc" stroke-width="0.6"/>
  <text x="355" y="82" fill="#1a7a6d" font-size="11" font-weight="600">project onto V̂κ</text>
  <text x="355" y="96" fill="#1a7a6d" font-size="10" opacity="0.7">(leading κ modes)</text>
  <!-- Transition -->
  <line x1="230" y1="270" x2="230" y2="300" stroke="#999" stroke-width="1.2" marker-end="url(#mg2)"/>
  <text x="248" y="290" fill="#999" font-size="10" font-style="italic">spectral projection</text>
  <!-- BOTTOM: anisotropic result -->
  <line x1="40" y1="380" x2="420" y2="380" stroke="#c8c0b4" stroke-width="0.5"/>
  <line x1="230" y1="315" x2="230" y2="445" stroke="#c8c0b4" stroke-width="0.5"/>
  <ellipse cx="230" cy="380" rx="100" ry="65" fill="none" stroke="#d0c8bc" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.3"/>
  <ellipse cx="230" cy="380" rx="28" ry="63" fill="#1a7a6d" fill-opacity="0.05" stroke="#1a7a6d" stroke-width="1.4" stroke-opacity="0.7"/>
  <circle cx="225" cy="338" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="233" cy="352" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="228" cy="368" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="235" cy="382" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="223" cy="396" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="232" cy="410" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="237" cy="375" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="226" cy="360" r="3.5" fill="#1a7a6d" opacity="0.7"/>
  <!-- Bracket for preserved noise spread -->
  <line x1="188" y1="318" x2="188" y2="442" stroke="#1a7a6d" stroke-width="0.8" opacity="0.3"/>
  <line x1="188" y1="318" x2="192" y2="318" stroke="#1a7a6d" stroke-width="0.8" opacity="0.3"/>
  <line x1="188" y1="442" x2="192" y2="442" stroke="#1a7a6d" stroke-width="0.8" opacity="0.3"/>
  <text x="182" y="384" text-anchor="middle" fill="#1a7a6d" font-size="9" font-weight="600" transform="rotate(-90 182 384)">v⊥ preserved</text>
  <text x="230" y="432" text-anchor="middle" fill="#1a7a6d" font-size="12" font-weight="600">anisotropic correction</text>
  <text x="230" y="448" text-anchor="middle" fill="#999" font-size="10" font-style="italic">noise-direction variance unchanged</text>
</svg>

</div>

<div style="margin-top:-0.2em; padding:0.2em 1em; text-align:center; font-family:Georgia,'Times New Roman',serif; font-size:0.68em; color:var(--text-secondary,#6b5d4e); line-height:1.3; font-style:italic;">Signal-subspace updates preserve orthogonal variance; isotropic perturbations do not.</div>

<!-- .notes:
This table captures the geometric difference. Stochastic EnKF corrects along signal directions but also injects perturbation noise there. Along noise directions, it injects noise uniformly. The net effect: variance is compressed everywhere because the observation perturbations add noise in all dimensions while the Kalman update removes variance along observed directions. QPCA-EnDCF corrects only along the kappa signal directions — deterministically, without added noise. Noise directions are untouched. This is why it preserves ensemble diversity: it operates surgically on the signal subspace and leaves everything else intact.
-->

---

## MUD ↔ QPCA-EnDCF: Algebraic Correspondence

**MUD** updates parameters <span>$\theta$</span> via inversion through a QPCA-learned QoI map:

<div>$$\theta_{\mathrm{MUD}} = \underbrace{\theta_{\mathrm{init}}}_{\text{prior}} + \underbrace{\Sigma_\theta A^\top \Sigma_{\mathrm{pred}}^{-1}}_{\text{covariance pullback}}\;\underbrace{(\mathbf{z}_{\mathrm{obs}} - A\,\theta_{\mathrm{init}})}_{\text{QoI innovation}}$$</div>

<div class="fragment">

**QPCA-EnDCF** updates state <span>$\mathbf{x}$</span> via spectral projection of whitened residuals:

<div>$$\mathbf{x}^{(j),a} = \underbrace{\mathbf{x}^{(j),f}}_{\text{prior}} + \underbrace{\mathbf{K}^{\mathrm{DC}}\,\mathbf{R}^{1/2}}_{\text{covariance pullback}}\;\underbrace{\hat{\mathbf{V}}_\kappa\hat{\mathbf{V}}_\kappa^\top\,\mathbf{R}^{-1/2}(\mathbf{z}^{(w)} - \mathbf{z}_f^{(j)})}_{\text{projected innovation}}$$</div>

</div>

<div class="fragment">

**Shared template:** prior + covariance-weighted pullback of subspace-restricted innovation

- **QPCA defines** the signal subspace (<span>$A$</span> in MUD, <span>$\hat{\mathbf{V}}_\kappa$</span> in EnDCF) via spectral decomposition
- **Both methods confine** updates to this subspace — orthogonal directions unchanged
- **Implication:** ensemble diversity preserved outside signal subspace → calibrated spread

</div>

<!-- .notes:
This slide establishes the formal algebraic correspondence between MUD parameter estimation and QPCA-EnDCF filtering. Both follow the same template: prior plus covariance-weighted pullback of a subspace-restricted innovation. In MUD, the QPCA-learned map A defines a low-rank subspace for parameter inversion; the gain pulls back through that subspace using population covariances. In QPCA-EnDCF, the leading eigenvectors of the whitened residual covariance define the signal subspace; the data-consistent gain pulls the projected correction back to state space. The critical shared insight: updates are confined to a learned signal subspace, and orthogonal directions receive no correction. This is precisely why ensemble diversity — and therefore calibration — is preserved. The method is grounded in established MUD inverse problem theory from Butler, Wildey, and Zhang, which opens the door to transferring theoretical results between parameter estimation and filtering.

Now that I've shown what the method does and where it comes from, the natural question is: why does spectral truncation produce calibrated ensembles? That's what the theory answers.
-->

---

<!-- ============================================================ -->
<!-- SECTION 3: THEORY (Slides 15-20) -->
<!-- ============================================================ -->

## Theoretical Framework: Overview

Three-stage analysis:

1. **Covariance concentration** → sample $\mathbf{C}_E$ approximates population $\boldsymbol{\Sigma}_E$
2. **Spectral perturbation** → empirical projector approximates population projector
3. **Bias-variance decomposition** → $\mathrm{MSE} = \mathrm{Bias}^2(\kappa) + \mathrm{Var}(N,\kappa)$

**Goal: explain WHY spectral regularization yields calibration**

<!-- .notes:
Now let me present the theoretical contribution. The analysis has three stages. First, we show the sample covariance of whitened residuals concentrates around its population counterpart at rate O(1/N). Second, we use Davis-Kahan perturbation theory to show the empirical spectral projector is close to the population projector — controlled by the cutoff gap. Third, we combine these to get a bias-variance decomposition that cleanly separates the effects of truncation, sampling, and approximation. This isn't just a convergence result — it explains mechanistically why spectral regularization produces calibrated ensembles.
-->

---

## Key Assumptions

- Forecast ensemble: i.i.d. samples with finite 4th moment
- Observation covariance $\mathbf{R}^{(L)}$ positive definite
- Spectral cutoff gap: <span>$\lambda_\kappa - \lambda_{\kappa+1} \geq \delta_\kappa > 0$</span>

**All assumptions are mild:**

- No Gaussianity required (used only for sharpening)
- i.i.d. is idealization; cycling experiments validate
- Gap condition ensures projector stability

<!-- .notes:
The assumptions are deliberately mild. We need i.i.d. ensemble members with finite fourth moments — strictly weaker than Gaussianity. The observation covariance must be positive definite, which is always true in practice. And we need a spectral gap at the truncation cutoff — this ensures the projector is well-defined and stable. The i.i.d. assumption is an idealization that doesn't hold in cycling; we verify empirically that the theoretical predictions hold nonetheless. Gaussianity is only invoked for sharper constants, not for the main results.
-->

---

## Main Theorem: Bias-Variance Decomposition

<div>$$\mathbb{E}\|\bar{\mathbf{x}}^a - \mathbf{x}^{\mathrm{true}}\|^2 = \mathrm{Bias}^2(\kappa) + \mathrm{Var}(N, \kappa)$$</div>

**Bias bound:**

<div>$$\mathrm{Bias}^2 \leq 2\,\mathrm{Bias}_{\mathrm{base}}^2 + 4\,\mathbb{E}[\|\mathbf{K}\|^2]\|\mathbf{R}\|\,\|(\mathbf{I} - \mathbf{P}_\kappa)\boldsymbol{\mu}_E\|^2 + \text{sampling, approx}$$</div>

**Variance bound:**

<div>$$\mathrm{Var} \leq \frac{2}{N}\mathbb{E}[\|\mathbf{x}^f - \boldsymbol{\mu}^f\|^2] + \frac{2\|\mathbf{R}\|}{N}\mathbb{E}[\|\mathbf{K}\|^2]\,\mathrm{tr}(\boldsymbol{\Sigma}_E) + \text{projector term}$$</div>

<!-- .notes:
Here's the main theorem. The MSE decomposes exactly into squared bias and variance. The bias has several contributions: a base term reflecting how well the untruncated correction would do, a truncation term depending on how much of the mean innovation is discarded — that's the I minus P-kappa mu-E norm — and sampling and approximation terms. The variance has two main pieces: forecast variance scaled by 1/N, and observation-space variance also scaled by 1/N with a gain-dependent prefactor. The projector estimation term involves kappa over delta-kappa-squared, connecting projector stability directly to variance.
-->

---

## The Critical Comparison

**Stochastic EnKF variance (lower bound):**

<div>$$\mathrm{Var}_{\mathrm{stoch}} \geq \frac{\|\mathbf{K}\|^2 \cdot \mathrm{tr}(\mathbf{R}^{(L)})}{N} = \mathcal{O}\!\left(\frac{d}{N}\right)$$</div>

**QPCA-EnDCF variance:**

<div>$$\mathrm{Var}_{\mathrm{QPCA}} = \mathcal{O}\!\left(\frac{1}{N}\right) \text{ with } \frac{\kappa}{\delta_\kappa^2} \text{ prefactor}$$</div>

- Stochastic: perturbation variance scales with <span>$d = mL$</span>
- QPCA-EnDCF: no perturbation term; projector term scales with $\kappa$
- At $\kappa=1$, <span>$d=100$</span>: up to two orders of magnitude in the perturbation component

<!-- .notes:
This is the theoretical punchline. The stochastic EnKF variance has an irreducible lower bound — Corollary 2 in the paper — from observation perturbations that scales with d over N. For windowed methods with d = mL = 100, that's a substantial floor. QPCA-EnDCF eliminates this specific variance component entirely. Its variance is still O(1/N), but the prefactor involves the effective rank kappa and the cutoff gap delta-kappa — not the observation dimension d. I want to be careful here: this comparison is between the perturbation-induced variance component in stochastic methods and its absence in QPCA-EnDCF. Both methods still have forecast sampling variance that scales with 1/N. The net advantage depends on how large the perturbation component is relative to the forecast component — and in our experiments, it's the dominant contributor to the variance gap.

Moving from theory to evidence, the bias-variance decomposition will show this plays out exactly as predicted.
-->

---

## Why the Favorable Bias-Variance Tradeoff?

Classical regularization: reduce variance → increase bias

**QPCA-EnDCF achieves a favorable tradeoff when spectra decay rapidly:**

- Leading eigenmode captures 60–80% of residual variance
- Mean innovation <span>$\boldsymbol{\mu}_E$</span> aligns with leading eigenvector
- <span>$\|(\mathbf{I} - \mathbf{P}_\kappa)\boldsymbol{\mu}_E\|^2$</span> is empirically small
- Discarded modes carry sampling noise, not signal

**Condition for this to hold: rapid spectral decay + mean-signal alignment**

<!-- .notes:
You might ask: doesn't truncation always introduce bias? In classical Tikhonov or ridge regularization, yes — there's a strict tradeoff. QPCA-EnDCF achieves a more favorable tradeoff, and the theory tells you exactly when and why. The truncation bias depends on the norm of (I minus P-kappa) times mu-E — how much of the mean innovation lies outside the retained subspace. When the mean mismatch aligns with the leading eigenvector, this term is small. Empirically, this alignment is strong in our setting because the dominant eigenmode captures the coherent dynamical forecast-observation discrepancy. The discarded modes are dominated by sampling noise, not signal. I want to be precise: this favorable regime requires rapid spectral decay and mean-signal alignment. The theorem identifies these as sufficient conditions, and the experiments verify they hold in the Lorenz-96 setting. In systems where the eigenspectrum is flat or the mean mismatch is diffuse, the advantage would be reduced — and the theory quantifies exactly how much through the truncation bias term.
-->

---

## Theoretical Summary

| Property            | Stochastic EnKF    | QPCA-EnDCF                     |
| ------------------- | ------------------ | ------------------------------ |
| Variance scaling    | $\mathcal{O}(d/N)$ | $\mathcal{O}(\kappa/N)$        |
| Perturbation noise  | Irreducible        | Eliminated                     |
| Regularization      | Uniform via R      | Adaptive spectral              |
| Bias-variance       | Classical tradeoff | Favorable under spectral decay |
| Projector stability | N/A                | Controlled by $\delta_\kappa$  |

<!-- .notes:
To summarize the theory: stochastic EnKF has variance scaling with observation dimension over N, irreducible perturbation noise, and uniform regularization. QPCA-EnDCF has variance scaling with effective rank over N, no perturbation noise, adaptive spectral regularization, and a favorable bias-variance tradeoff under spectral decay. The projector stability is controlled by the cutoff gap delta-kappa, which is intrinsic to the problem spectrum, not a tuning parameter.

That's the theory. Now let me show you the experiments that test these predictions. The question is: do the theoretical advantages materialize in practice, under realistic cycling conditions?
-->

---

<!-- ============================================================ -->
<!-- SECTION 4: EVIDENCE (Slides 21-32) -->
<!-- ============================================================ -->

## Experimental Setup

**Forward model — Lorenz-96** (chaotic, nonlinear dynamical system generating state evolution):

<div>$$\frac{dx_i}{dt} = (x_{i+1} - x_{i-2})\,x_{i-1} - x_i + F, \qquad i = 1, \dots, n$$</div>

with cyclic indexing: <span>$x_{-1} = x_{n-1}$</span>, <span>$x_0 = x_n$</span>, <span>$x_{n+1} = x_1$</span>

| Parameter               | Value                                              |
| ----------------------- | -------------------------------------------------- |
| State dimension <span>$n$</span>        | 40 (<span>$x_i$</span>: state variable at index <span>$i$</span>)           |
| Forcing <span>$F$</span>               | 8 (chaotic regime, 13 positive Lyapunov exponents) |
| Observations <span>$m$</span>          | 20 every-other component, <span>$\sigma_{\mathrm{obs}} = 1.5$</span>        |
| Ensemble size <span>$N$</span>         | 10 (severe undersampling)                          |
| Window length <span>$L$</span>         | 5 (spanning 0.83 Lyapunov times — time for errors to grow by factor <span>$e$</span>) |
| Methods                 | Seq-EnKF, 4D-EnKF, QPCA-EnDCF (<span>$\kappa=1$</span>)        |
| Trials                  | 5 independent Monte Carlo realizations             |

<!-- .notes:
All experiments use the Lorenz-96 system — the canonical testbed in the data assimilation literature, used by Evensen, Hunt, Anderson, Whitaker, and essentially every major ensemble filtering study. This is the forward model that generates the state dynamics: each variable is driven by nonlinear advection-like coupling to its neighbors, linear damping, and constant forcing F. At F equals 8, the system is fully chaotic with 13 positive Lyapunov exponents, making it a demanding test for ensemble filters. We observe 20 of 40 components with noise standard deviation 1.5, giving a signal-to-noise ratio of about 2.4 — an intermediate regime that demands effective regularization. Ensemble size is 10, which is severely undersampled: the covariance rank is at most 9 in a 40-dimensional space. Stochastic methods use multiplicative inflation of 1.05, which is near their optimum for this N. QPCA-EnDCF uses kappa equals 1 with no inflation — these are not tuned but follow from the spectral structure.
-->

---

## Result 1: Probabilistic Calibration

**Spread-skill ratio** — per-window ratio of ensemble spread to estimation error:

<div>$$\gamma_w := \frac{\sigma_w}{\mathrm{RMSE}_w}, \qquad \bar{\gamma} := \frac{1}{W}\sum_{w=1}^{W}\gamma_w, \qquad \sigma_w := \left[\tfrac{1}{n}\,\mathrm{tr}(\hat{\mathbf{P}}^a_{k_w})\right]^{1/2}$$</div>

Ideal calibration: <span>$\bar{\gamma} = 1$</span>. Temporal correlation <span>$\rho$</span> measures whether spread tracks RMSE across time.

![Combined Calibration Analysis](figures/combined_calibration_analysis.png)

- **(A)** QPCA-EnDCF: <span>$\bar{\gamma} \approx 0.81$</span> (near-ideal); stochastic methods: <span>$\bar{\gamma} \approx 0.1$</span> (15× overconfident)
- **(B)** QPCA-EnDCF clusters along the diagonal (<span>$\rho \approx 0.82$</span>); stochastic methods show no spread–error tracking (<span>$\rho \approx 0$</span>)
- **Simultaneous:** 20% lower RMSE with calibrated uncertainty — not a tradeoff

<!-- .element: class="fragment" -->

<!-- .notes:
This slide presents the central empirical finding. I first define the metric: the spread-skill ratio gamma-w is the per-window ratio of ensemble spread — the square root of the mean analysis variance — to RMSE. Ideal calibration means gamma-bar equals 1. The temporal correlation rho measures whether spread and RMSE co-vary across assimilation windows. Panel A shows gamma-w over time: QPCA-EnDCF fluctuates around the ideal line at 1.0 with a time-averaged ratio of 0.81 plus or minus 0.10, while stochastic methods flatline near 0.1 — their spread is 15 times too small. Panel B is the reliability diagram: spread versus RMSE for individual windows. QPCA-EnDCF clusters along the diagonal with rho of 0.82, meaning when it reports high uncertainty, the error is indeed high. Stochastic methods show vertical clustering at very low spread regardless of actual error, with effectively zero temporal correlation. Critically, this calibration improvement comes with a simultaneous 20 percent RMSE reduction — this is not a tradeoff between accuracy and reliability.
-->

---

## Result 2: Bias-Variance Decomposition

![Bias Variance Evolution](figures/bias_variance_evolution.png)

| Method         | MSE    | $\mathrm{Bias}^2$ | Variance | $\mathrm{Bias}^2/\mathrm{MSE}$ |
| -------------- | ------ | ----------------- | -------- | ------------------------------ |
| Seq-EnKF       | 22     | ~10               | ~12      | 45%                            |
| 4D-EnKF        | 21     | ~10               | ~11      | 47%                            |
| **QPCA-EnDCF** | **13** | **~11**           | **~2**   | **82%**                        |

<!-- .notes:
The bias-variance decomposition reveals the mechanism. All three methods have roughly equal squared bias — about 10 to 11. The difference is variance. Stochastic methods have variance around 11-12, making them variance-limited. QPCA-EnDCF has variance of only 2.3 — an 80 percent reduction. Its error is overwhelmingly bias-dominated. This validates the theory exactly: spectral truncation removes variance-dominated modes without increasing bias. The 5× variance reduction is consistent with eliminating the O(d/N) perturbation term.
-->

---

## Result 2: MSE Decomposition

![MSE Decomposition Bars](figures/mse_decomposition_bars.png)

**QPCA-EnDCF: 80% variance reduction, no bias increase**

Consistent with theoretical prediction: O(κ/N) vs O(d/N)

<!-- .notes:
The bar chart summarizes this cleanly. On the left, absolute MSE with bias and variance contributions. QPCA-EnDCF's total bar is substantially shorter, and the variance component is tiny. On the right, the percentage breakdown confirms: stochastic methods are roughly 50-50 bias and variance, while QPCA-EnDCF is 82% bias. This means further improvements for QPCA-EnDCF should target the forward model or observation operator — not ensemble size. Stochastic methods, by contrast, remain fundamentally limited by sampling variance at fixed N.
-->

---

## Result 3: Inflation-Free Operation

![Multiplicative Inflation](figures/inflation_multiplicative_20.png)

- QPCA-EnDCF optimal at $\lambda_{\mathrm{infl}} = 1.0$ (no inflation) for all <span>$N$</span>
- Stochastic methods need N-dependent tuning
- **Eliminates a major source of heuristic calibration**

<!-- .notes:
One of the most practically important results: QPCA-EnDCF needs no inflation. This figure shows RMSE versus multiplicative inflation factor for different ensemble sizes. QPCA-EnDCF achieves its best performance at lambda equals 1.0 — no inflation — for every ensemble size tested. Stochastic methods have ensemble-size-dependent optima that shift as N changes. This eliminates a major operational headache: inflation tuning is one of the most time-consuming aspects of deploying ensemble filters, and getting it wrong can cause either filter divergence or excessive variance. QPCA-EnDCF simply doesn't need it.
-->

---

## Result 4: Robustness — Non-Gaussian Errors

<div style="display: flex; gap: 1.5em; align-items: flex-start;">
<div style="flex: 1;">

![Noise Distributions](figures/noise_distributions.png)

</div>
<div style="flex: 1;">

![Mean RMSE Non-Gaussian](figures/mean_rmse_comparison_nongaussian.png)

</div>
</div>

- 9 distributions: Gaussian, Student-t, Laplace, Gamma, Log-normal
- QPCA-EnDCF RMSE: 3.51–3.69 (CV ≈ 1.4%)
- **18–25% improvement** over stochastic methods, every distribution

<!-- .notes:
Real observation errors are rarely Gaussian. We tested 9 distributions spanning symmetric heavy tails, right skewness, and the Gaussian reference — all standardized to the same variance. QPCA-EnDCF is essentially insensitive to distributional shape: RMSE stays in the narrow band 3.51 to 3.69, with a coefficient of variation of only 1.4 percent. The improvement over stochastic methods is 18 to 25 percent for every single distribution. This robustness comes from the fact that QPCA-EnDCF is driven by second-moment structure — the whitening and PCA depend only on covariances, not on higher-order distributional properties.
-->

---

## Result 4: Robustness — Correlated Errors

<div style="display: flex; gap: 1.5em; align-items: center;">
<div style="flex: 1;">
<img src="figures/correlation_structures.png" alt="Correlation Structures" style="max-height: 50vh; max-width: 100%;">
</div>
<div style="flex: 1;">
<img src="figures/reconstruction_errors.png" alt="Reconstruction Errors" style="max-height: 50vh; max-width: 100%;">
</div>
</div>

- Condition numbers spanning 5 orders of magnitude
- QPCA-EnDCF: within 7% of uncorrelated baseline
- Advantage **grows** with correlation: 25% → 32%

<!-- .notes:
We also tested correlated observation errors, spanning condition numbers from 1 to 370,000. QPCA-EnDCF degrades only modestly — within 7 percent of the uncorrelated baseline even under severe ill-conditioning. Crucially, the advantage over 4D-EnKF grows with correlation strength, from 25 percent improvement at the diagonal baseline to 32 percent under severe ill-conditioning. This happens because whitening effectively decorrelates the observations before spectral analysis, whereas stochastic perturbations sampled from the correlated structure become less efficient as correlations reduce effective information content.
-->

---

## Result 5: Ensemble Size Scaling

![Performance Degradation](figures/performance_degradation.png)

- QPCA-EnDCF viable down to N=5
- At N=10: matches stochastic methods at N=20–30
- **2–3× ensemble savings** for equivalent accuracy

<!-- .notes:
This figure shows how methods scale with ensemble size. QPCA-EnDCF degrades gracefully from N=100 down to N=5, with only 28 percent degradation — much less than stochastic methods. At N=10, QPCA-EnDCF matches the accuracy of stochastic methods at N=20 to 30. That's a 2 to 3 times savings in ensemble size, which translates directly to 50 to 67 percent reduction in forecast propagation cost. For operational centers where each ensemble member requires a full model integration, this is a substantial computational savings.
-->

---

## Result 5: Calibration Across Ensemble Sizes

![Ensemble Size Spread Skill](figures/fig_ensemble_size_spread_skill.png)

- QPCA-EnDCF at <span>$N=10$</span>: $\bar{\gamma} \approx 0.77$
- Stochastic at <span>$N=50$</span>: $\bar{\gamma} \approx 0.12$
- **QPCA-EnDCF at <span>$N=10$</span> > stochastic at <span>$N=50$</span>**
- → 5× calibration savings

<!-- .notes:
The calibration story is even more dramatic. QPCA-EnDCF at N=10 achieves a spread-skill ratio of 0.77 — substantially better than stochastic methods at N=50, which still only reach 0.12 to 0.14. That's a 5 times savings in ensemble size for equivalent — actually, far superior — calibration. By N=50, QPCA-EnDCF reaches gamma-bar of 0.95, essentially ideal calibration. Stochastic methods never get close, even at N=100. This is the most operationally impactful finding: you can get calibrated uncertainty at a fraction of the computational cost.
-->

---

## Result 6: Window Length Sensitivity

![Window RMSE Analysis](figures/combined_window_rmse_analysis.png)

- <span>$L=1$</span>: QPCA-EnDCF slightly worse (no temporal structure)
- <span>$L \geq 3$</span>: 16–21% improvement over 4D-EnKF
- Sweet spot: $L \in [5, 10]$

<!-- .notes:
Window length matters for QPCA-EnDCF. At L equals 1 — purely sequential — it's slightly worse than 4D-EnKF because there's insufficient temporal residual structure for meaningful spectral analysis. But as soon as L reaches 3, QPCA-EnDCF outperforms by 16 to 21 percent, and performance stabilizes for L between 5 and 10. The practical recommendation is simple: use windows of at least 3 observation times. The sweet spot balances accuracy against computational cost of the larger eigendecomposition.
-->

---

<!-- ============================================================ -->
<!-- SECTION 5: CONTRIBUTIONS & IMPACT (Slides 33-37) -->
<!-- ============================================================ -->

## Contributions Summary

### Theoretical

1. Bias-variance decomposition for spectral ensemble filters
2. $\mathcal{O}(\kappa/N)$ vs $\mathcal{O}(d/N)$ variance scaling distinction
3. Projector stability analysis via Davis-Kahan

### Empirical

4. Near-ideal calibration under severe undersampling
5. Inflation-free operation across ensemble sizes
6. Robustness under non-Gaussian and correlated errors

### Practical

7. 2–3× accuracy savings, 5× calibration savings
8. Operational guidelines: <span>$L \geq 3$</span>, $\kappa = 1$

<!-- .notes:
Let me summarize the contributions explicitly. On the theoretical side: the first bias-variance decomposition for spectral ensemble filters, the O(kappa/N) versus O(d/N) variance distinction, and projector stability analysis through Davis-Kahan. Empirically: near-ideal calibration, inflation-free operation, and broad robustness. Practically: 2-3 times ensemble savings for accuracy, 5 times for calibration, and concrete operational guidelines — use windows of at least 3 with kappa equals 1.
-->

---

## Limitations and Scope

- **Perfect model:** no structural model error (most important gap)
- **Moderate dimension:** <span>$n=40$</span>; spectral ops scale as $\mathcal{O}(dN^2)$, not $\mathcal{O}(n)$
- **Linear observations:** nonlinear H handled via ensemble H(x), untested
- **i.i.d. theory:** standard idealization; cycling experiments validate predictions
- **Single test system:** Lorenz-96 (standard DA benchmark, 13 positive LEs)

**Each limitation has a concrete mitigation path (next slide)**

<!-- .notes:
Let me be direct about what this work does and does not show. The most important limitation is the perfect-model assumption — real systems have model error that could spread signal across more eigenvalues, potentially requiring larger kappa. I label this as the most important gap explicitly. On dimension: the spectral operations are in observation space, not state space. The thin SVD costs O(d times N-squared), which is linear in d and independent of n. So the algorithm itself scales — the open question is whether the spectral separation mechanism persists in richer dynamics. The i.i.d. assumption is standard in the EnKF convergence literature — used by Le Gland, Mandel, Tong, and others. Our cycling experiments run 50 full windows and confirm the predicted scaling. Lorenz-96 is the canonical DA benchmark precisely because it captures essential challenges — sustained chaos, scale interactions, multiple positive Lyapunov exponents — at tractable cost. But validation on richer systems is needed, and I've designed the future work to address each gap systematically.
-->

---

## Future Work

1. **Model error:** systematic and stochastic perturbations
2. **Adaptive** $\kappa$: data-driven truncation rank selection
3. **Intermediate-complexity models:** quasi-geostrophic, shallow water
4. **Nonlinear observations:** satellite radiances, retrievals
5. **Operational scale:** $n \sim 10^6$ with localization

<!-- .notes:
Concretely, the next steps are: first, introducing controlled model error to test robustness beyond the perfect-model setting. Second, developing adaptive selection of the truncation rank — possibly using the eigenvalue gap itself as a criterion. Third, validating on intermediate-complexity models like quasi-geostrophic or shallow water equations. Fourth, testing with nonlinear observation operators. And fifth, the big challenge: scaling to operational dimensions with localization. I believe the spectral regularization principle will translate, but the interaction with localization needs careful study.
-->

---

## Conclusion

**QPCA-EnDCF: deterministic spectral regularization → calibrated UQ**

- Eliminates perturbation-induced variance (Corollary 2)
- Theory predicts: favorable bias-variance tradeoff under spectral decay
- Experiments confirm: $\bar{\gamma} = 0.81 \pm 0.10$ vs $0.10 \pm 0.11$, RMSE reduced 20%
- No inflation needed, robust across 9 noise distributions and 5 orders of $\mathrm{cond}(\mathbf{R})$

**In the regime of rapid spectral decay and severe undersampling, deterministic spectral regularization provides calibrated uncertainty quantification where stochastic methods cannot**

<!-- .notes:
To conclude: this dissertation makes three contributions. First, a new deterministic ensemble filter — QPCA-EnDCF — that replaces stochastic perturbations with spectral projection. Second, a rigorous theoretical framework — the bias-variance decomposition — that explains why this works: it eliminates the O(d/N) perturbation variance and replaces it with a rank-dependent term that is small under rapid spectral decay. Third, comprehensive experimental validation showing near-ideal calibration, inflation-free operation, and robustness across noise distributions and correlation structures.

The core insight is geometric: by confining corrections to the signal subspace and leaving noise subspaces untouched, ensemble diversity is preserved exactly where it matters. This is what produces calibrated uncertainty — spread that tracks actual error.

I want to end with what I think is the most important open question: does this mechanism persist under model error and at operational scale? The theory and experiments suggest yes, because the spectral separation is a property of the residual structure, not of the specific test system. But proving that requires the future work I've outlined. Thank you. I'm happy to take questions.
-->

---

<!-- .slide: data-background="#1a1a2e" -->

# Thank You

### Questions?

**Rylan Spence**

Code: github.com/[repo]

<!-- .notes:
Thank you for your attention. I'm happy to take any questions.
-->
