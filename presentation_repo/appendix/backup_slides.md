---
title: "Backup Slides"
---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 1: Full Theorem Proof Sketch -->
<!-- ============================================================ -->

---

## Backup 1: Theorem Proof Sketch

**Step 1:** Bias-variance identity (Lemma 1)
$$\mathbb{E}\|\bar{\mathbf{x}}^a - \mathbf{x}^{\mathrm{true}}\|^2 = \|\mathbb{E}[\bar{\mathbf{x}}^a] - \mathbf{x}^{\mathrm{true}}\|^2 + \mathbb{E}\|\bar{\mathbf{x}}^a - \mathbb{E}[\bar{\mathbf{x}}^a]\|^2$$

**Step 2:** Express analysis mean via projector
$$\bar{\mathbf{x}}^a = \bar{\mathbf{x}}^f - \mathbf{K}^{\mathrm{DC}}(\mathbf{R}^{(L)})^{1/2}\hat{\mathbf{P}}_\kappa \bar{\mathbf{e}}$$

**Step 3:** Insert/subtract population projector, decompose $\bar{\mathbf{e}} = \boldsymbol{\mu}_E + (\bar{\mathbf{e}} - \boldsymbol{\mu}_E)$

**Step 4:** Apply submultiplicativity, Jensen, Cauchy-Schwarz to each term

<!-- .notes:
The proof proceeds in four steps. First, the standard bias-variance identity. Second, express the analysis mean through the empirical projector. Third, insert and subtract the population projector and decompose the sample mean into its expectation plus fluctuation. Fourth, bound each resulting term using submultiplicativity, Jensen's inequality, and Cauchy-Schwarz. The key technical ingredient is that the projector error and sample mean are dependent — both computed from the same ensemble — so we use Cauchy-Schwarz on fourth moments rather than independence.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 2: Davis-Kahan Details -->
<!-- ============================================================ -->

## Backup 2: Davis-Kahan Projector Stability

**Weyl's inequality:** $|\hat{\lambda}_i - \lambda_i| \leq \|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_2$

**Davis-Kahan sin Θ theorem:**
$$\sin\angle(\hat{\mathbf{v}}_i, \mathbf{v}_i) \leq \frac{\|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_2}{\delta_i}$$

**Projector form (rank-**$\kappa$**):**
$$\|\hat{\mathbf{P}}_\kappa - \mathbf{P}_\kappa\|_F \leq \frac{\sqrt{2\kappa}}{\delta_\kappa}\|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_F$$

- Gap $\delta_\kappa$ controls stability
- When $\kappa=1$ and gap is large → stable projector
- Empirically: leading eigenvalue is well-separated

<!-- .notes:
Davis-Kahan is the workhorse of the spectral perturbation analysis. Weyl's inequality gives pointwise eigenvalue stability. The sin-theta theorem controls eigenvector perturbation, inversely proportional to the spectral gap. For rank-kappa projectors, we get Frobenius control with a square-root-kappa prefactor divided by the cutoff gap. When kappa is 1 and the gap is large — as empirically observed — the projector is very stable under sampling perturbations.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 3: Covariance Concentration Details -->
<!-- ============================================================ -->

## Backup 3: Covariance Concentration

**Unbiasedness:** $\mathbb{E}[\mathbf{C}_E] = \boldsymbol{\Sigma}_E$ (Bessel correction)

**Mean-square Frobenius deviation:**
$$\mathbb{E}\|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_F^2 \leq \frac{C_{\mathrm{cov}}}{N-1}\mathrm{tr}(\boldsymbol{\Sigma}_E^2)$$

**Gaussian sharpening (Wishart):**
$$\mathbb{E}\|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_F^2 = \frac{(\mathrm{tr}(\boldsymbol{\Sigma}_E))^2 + \mathrm{tr}(\boldsymbol{\Sigma}_E^2)}{N-1}$$

**Fourth-moment bound (needed for variance):**
$$\mathbb{E}\|\mathbf{C}_E - \boldsymbol{\Sigma}_E\|_F^4 \leq \frac{C_W}{(N-1)^2}(\mathrm{tr}(\boldsymbol{\Sigma}_E^2))^2$$

<!-- .notes:
Three concentration results underpin the theory. The sample covariance is unbiased by the Bessel correction — this is standard but important. The mean-square Frobenius deviation is O(1/(N-1)) with a trace-of-sigma-squared prefactor — this is the backbone. Under Gaussianity, we get the exact Wishart expression with sharper constants. The fourth-moment bound is needed for the variance analysis because the projector and sample mean are dependent, requiring Cauchy-Schwarz on fourth moments.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 4: Rank Histogram Analysis -->
<!-- ============================================================ -->

## Backup 4: Rank Histogram Analysis

![Rank Histograms](../paper/final_figures/rank_histograms.png)

| Method | $\chi^2$ | Flatness |
|--------|-----|----------|
| Seq-EnKF | 173,195 | 1.861 |
| 4D-EnKF | 32,269 | 1.796 |
| QPCA-EnDCF | 396.8 | 0.199 |

- Flatness: normalized std of bin frequencies
- QPCA-EnDCF: ~10× better than stochastic methods
- U-shape in EnKF = severe underdispersion

<!-- .notes:
Rank histograms test full distributional calibration beyond second moments. Under perfect calibration, the truth should be uniformly distributed among ensemble members. QPCA-EnDCF achieves flatness of 0.199 — nearly uniform. Stochastic methods show severe U-shaped histograms with flatness near 2, indicating the truth frequently falls outside the ensemble support. The chi-squared values confirm: QPCA-EnDCF's departure from uniformity is two to three orders of magnitude smaller.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 5: Additive Inflation Results -->
<!-- ============================================================ -->

## Backup 5: Additive Inflation Analysis

![Additive Inflation](../paper/final_figures/inflation_additive_20.png)

- QPCA-EnDCF optimal at $\alpha_{\mathrm{add}} = 0$ for all <span>$N$</span>
- Additive inflation degrades QPCA-EnDCF (disrupts correlations)
- For stochastic: additive underperforms multiplicative by 5-10%
- Isotropic noise lacks dynamical structure

<!-- .notes:
Additive inflation results tell the same story as multiplicative. QPCA-EnDCF is optimal with zero additive inflation for every ensemble size. Adding isotropic noise actually hurts because it disrupts the dynamically consistent correlation structure that spectral regularization preserves. For stochastic methods, additive inflation provides marginal improvement over no inflation but consistently underperforms multiplicative inflation, because isotropic perturbations inject variance in dynamically irrelevant directions.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 6: Non-Gaussian Full Table -->
<!-- ============================================================ -->

## Backup 6: Full Non-Gaussian Results

| Distribution | QPCA | Seq-EnKF | 4D-EnKF | vs Seq | vs 4D |
|-------------|------|----------|---------|--------|-------|
| Gaussian | **3.63** | 4.45 | 4.51 | −18.3% | −19.4% |
| Student-t ($\nu=3$) | **3.67** | 4.68 | 4.46 | −21.6% | −17.8% |
| Student-t ($\nu=5$) | **3.55** | 4.48 | 4.58 | −20.7% | −22.4% |
| Student-t ($\nu=10$) | **3.51** | 4.54 | 4.40 | −22.8% | −20.3% |
| Laplace | **3.69** | 4.51 | 4.49 | −18.3% | −18.0% |
| Gamma (k=2) | **3.56** | 4.72 | 4.45 | −24.5% | −19.9% |
| Gamma (k=5) | **3.66** | 4.51 | 4.43 | −18.8% | −17.3% |
| LogNorm ($\sigma=0.5$) | **3.60** | 4.44 | 4.66 | −18.9% | −22.7% |
| LogNorm ($\sigma=0.8$) | **3.61** | 4.49 | 4.55 | −19.6% | −20.6% |

Cross-distribution std: QPCA 0.052, Seq 0.092, 4D 0.131

<!-- .notes:
The full non-Gaussian table. Nine distributions, three trials each. QPCA-EnDCF wins every single comparison, with improvements ranging from 17.3 to 24.5 percent. Its cross-distribution standard deviation is 0.052 — half that of sequential EnKF and a third of 4D-EnKF. The largest improvement is 24.5 percent against sequential EnKF under Gamma(k=2) errors, and the most consistent advantage is the approximately 20 percent mean improvement across all distributions.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 7: Correlated Error Implementation -->
<!-- ============================================================ -->

## Backup 7: Correlated Observation Error Details

**Three covariance structures:**
- Diagonal: $\mathrm{cond}(\mathbf{R}) = 1$ (baseline)
- Exponential: $R_{ij} = \sigma^2 \exp(-d_{ij}/\ell)$, $\mathrm{cond}(\mathbf{R}) = 649$
- Gaussian: $R_{ij} = \sigma^2 \exp(-d_{ij}^2/2\ell^2)$, $\mathrm{cond}(\mathbf{R}) \approx 3.7 \times 10^5$

**Whitening implementation:** Cholesky factorization $\mathbf{R} = \mathbf{L}\mathbf{L}^\top$, $\mathbf{W} = \mathbf{L}^{-\top}$

**Key results:**
- QPCA-EnDCF degradation: less than 7% across 5 orders of magnitude
- 4D-EnKF degradation: 15.3% under Gaussian correlation
- QPCA advantage grows: 25.2% → 24.7% → 31.9%
- Regularization $\varepsilon = 10^{-3} \,\mathrm{tr}(\mathbf{R})$ for Gaussian case

<!-- .notes:
The correlated error study tests three covariance structures with condition numbers from 1 to 370,000. We use Cholesky whitening — R equals L L-transpose, W equals L-inverse-transpose. QPCA-EnDCF stays within 7 percent of the uncorrelated baseline, while 4D-EnKF degrades by 15 percent under severe ill-conditioning. The advantage of QPCA-EnDCF actually increases with correlation strength because whitening effectively decorrelates the observation space, restoring the favorable spectral structure.
-->


---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 9: Window Length Table -->
<!-- ============================================================ -->

## Backup 9: Window Length Detailed Results

| L | Seq-EnKF | 4D-EnKF | QPCA-EnDCF | QPCA vs 4D |
|---|----------|---------|------------|------------|
| 1 | 4.72 | 4.64 | 4.87 | −5.1% |
| 3 | 4.58 | 4.44 | 3.69 | +16.9% |
| 5 | 4.63 | 4.48 | 3.64 | +18.8% |
| 7 | 4.61 | 4.49 | 3.68 | +18.0% |
| 10 | 4.67 | 4.42 | 3.66 | +17.2% |
| 15 | 4.59 | 4.40 | 3.72 | +15.5% |

- Sharp transition between <span>$L=1$</span> and <span>$L=3$</span>
- <span>$L=1$</span>: spectral regularization underperforms (insufficient temporal structure)
- <span>$L \geq 3$</span>: consistent 16–21% advantage
- Diminishing returns beyond $L \approx 10$

<!-- .notes:
The detailed window length table shows the sharp transition. At L=1, QPCA-EnDCF actually underperforms 4D-EnKF by 5 percent. At L=3, it outperforms by 17 percent. This transition occurs because at L=1, the residual covariance is only 20-by-20 with rank at most 9, insufficient for reliable spectral separation. At L=3, the residual space is 60-dimensional, providing enough structure for the leading mode to be stably identified. Beyond L=10, returns diminish as additional observations exceed the decorrelation timescale.
-->

---

<!-- ============================================================ -->
<!-- BACKUP SLIDE 10: Computational Cost Analysis -->
<!-- ============================================================ -->

## Backup 10: Computational Cost Comparison

| Operation | Seq-EnKF | 4D-EnKF | QPCA-EnDCF |
|-----------|----------|---------|------------|
| Model propagation | $NK \cdot \mathcal{O}(n^2)$ | $NK \cdot \mathcal{O}(n^2)$ | $NK \cdot \mathcal{O}(n^2)$ |
| Gain computation | $K \cdot \mathcal{O}(nm^2)$ | $W \cdot \mathcal{O}(nd^2)$ | $W \cdot \mathcal{O}(nd^2)$ |
| Eigendecomposition | — | — | $W \cdot \mathcal{O}(d^3)$ |
| Perturbation sampling | $KN \cdot \mathcal{O}(m)$ | $WN \cdot \mathcal{O}(d)$ | **None** |
| Inflation | $K \cdot \mathcal{O}(nN)$ | $W \cdot \mathcal{O}(nN)$ | **None** |

**Dominant cost:** model propagation (identical across methods)

**QPCA-EnDCF overhead:** one $d \times d$ eigendecomposition per window

**QPCA-EnDCF savings:** no perturbation RNG, no inflation tuning

<!-- .notes:
Computational cost comparison. The dominant cost for all methods is model propagation — identical. QPCA-EnDCF adds one d-by-d eigendecomposition per window, which is O(d-cubed). For d=100, this is negligible relative to model propagation. It saves on perturbation sampling — no random number generation needed — and eliminates inflation, removing both the computational cost and the tuning burden. The net overhead is minimal; the net benefit from smaller viable ensemble sizes is substantial.
-->
