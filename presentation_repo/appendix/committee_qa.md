# Committee Q&A Pack — 25 Hard Questions

## Defense Risk Score: 4/10
The defense is strong. The main vulnerabilities are: (1) Lorenz-96 only, (2) perfect model, (3) small n. The theory is rigorous, the experiments comprehensive within scope, and the contributions clear.

## Most Likely Attack Paths
1. **Scalability** — "Does this work at operational scale?" (slides 34-35)
2. **Single test system** — "Why only Lorenz-96?" (slide 34)
3. **i.i.d. assumption** — "Your theory assumes i.i.d. but cycling violates it" (slide 16)
4. **κ=1 universality** — "Is κ=1 always right?" (slide 12)
5. **Perfect model** — "Real systems have model error" (slide 34)

## Weak Slides Likely Attacked
- Slide 16 (Key Assumptions) — i.i.d. idealization
- Slide 34 (Limitations) — self-identified gaps
- Slide 12 (Stage 3: Truncated Correction) — κ=1 choice
- Slide 20 (Theoretical Summary) — completeness of theory

---

## QUESTION 1
**Q:** Your theory assumes i.i.d. ensemble members, but cycling induces dependence. How do you reconcile this?

**Why asked:** Tests whether the candidate understands the gap between theory and practice.

**Target weakness:** Assumption (iii) in the regularity conditions.

**Strong answer:** The i.i.d. assumption is standard in the theoretical EnKF literature — it's the same idealization used by Le Gland, Mandel, Tong, and others. We invoke it to derive clean convergence rates. The key question is whether the qualitative predictions hold under cycling. Our experiments run 50 full cycling windows and confirm: the O(1/N) variance scaling, the bias-variance decomposition structure, and the calibration advantages all persist. Under ergodic dynamics with sufficient mixing, consecutive windows become approximately independent, and the formal rates hold asymptotically. The theory provides correct qualitative guidance even when strict i.i.d. doesn't hold.

---

## QUESTION 2
**Q:** Why only Lorenz-96? How do you know these results generalize?

**Why asked:** Tests scope awareness and intellectual honesty.

**Target weakness:** Single test system.

**Strong answer:** Lorenz-96 is the standard benchmark in the data assimilation community precisely because it captures key challenges — sustained chaos, multiple positive Lyapunov exponents, scale interactions — at manageable computational cost. The mechanisms underlying QPCA-EnDCF's advantages are general: spectral separation of signal and noise in whitened residuals, variance reduction through projection, and preservation of ensemble diversity in orthogonal directions. These don't depend on Lorenz-96 specifics. That said, validation on intermediate-complexity models (quasi-geostrophic, shallow water) is an explicit and important next step. The dissertation establishes the theoretical framework and validates on a canonical system; scaling is future work.

---

## QUESTION 3
**Q:** The state dimension is 40. Operational systems have 10⁶ to 10⁹ unknowns. Why should anyone believe this scales?

**Why asked:** Tests practical relevance and scaling awareness.

**Target weakness:** Low dimensionality of test system.

**Strong answer:** At operational scale, the key difference is that localization becomes essential. QPCA-EnDCF's spectral operations are in observation space (dimension d=mL), not state space (dimension n). The eigendecomposition cost is O(d³), which doesn't depend on n at all. The gain computation uses the same cross-covariance structure as standard EnKF and can be localized identically. The theoretical variance scaling O(κ/N) vs O(d/N) is dimension-independent — it's about effective rank vs observation dimension, not state dimension. That said, the interaction between spectral truncation and localization needs careful study, and I wouldn't claim this works at scale without testing it.

---

## QUESTION 4
**Q:** What happens with model error? All your experiments assume a perfect model.

**Why asked:** Tests the most operationally relevant limitation.

**Target weakness:** Perfect-model assumption.

**Strong answer:** Model error is the most important limitation, and I'm transparent about it. In the perfect-model setting, the forecast-observation mismatch comes entirely from initial condition uncertainty and observation noise. With model error, there's an additional systematic component that may not align with the leading eigenmode. However, the whitening step normalizes by observation uncertainty, not model uncertainty, so moderate model error should be absorbed into the residual structure. The spectral decomposition would then capture both initial-condition and model-error contributions. The concern is whether aggressive truncation (κ=1) remains appropriate — model error might spread signal across more modes. Adaptive κ selection, which I list as future work, would directly address this.

---

## QUESTION 5
**Q:** Is κ=1 always the right choice? When would it fail?

**Why asked:** Tests understanding of method limitations.

**Target weakness:** Fixed truncation throughout all experiments.

**Strong answer:** κ=1 works in our setting because the leading eigenvalue captures 60-80% of residual variance — there's rapid spectral decay with a large gap between λ₁ and λ₂. It would fail when: (1) the eigenspectrum is flat, meaning no dominant mode — this can happen with very dense observations or weak dynamics; (2) there are multiple comparably important mismatch directions, e.g., with strongly multimodal forecast errors; (3) model error distributes signal across many modes. The right approach is adaptive κ selection — possibly using the eigenvalue gap δ_κ = λ_κ − λ_{κ+1} as a criterion, retaining modes until the gap drops below a threshold. This is explicitly future work.

---

## QUESTION 6
**Q:** You claim the bias-variance tradeoff is "broken." Isn't this just favorable alignment that might not hold generally?

**Why asked:** Tests depth of theoretical understanding.

**Target weakness:** The favorable bias depends on mean innovation alignment.

**Strong answer:** You're right that the favorable tradeoff depends on ‖(I − P_κ)μ_E‖² being small — the mean innovation must align with the leading eigenspace. I don't claim this holds universally. What I show is: (1) the theorem identifies exactly when it holds and when it doesn't, (2) in the Lorenz-96 setting this alignment is empirically strong, and (3) there's a mechanistic reason — the leading eigenmode captures the dominant coherent forecast-observation discrepancy, which is closely related to the mean mismatch. In systems where the mean innovation is orthogonal to the covariance structure, QPCA-EnDCF would incur bias. The theory gives you the tools to diagnose this a priori by examining ‖(I − P_κ)μ_E‖.

---

## QUESTION 7
**Q:** How does QPCA-EnDCF relate to other deterministic ensemble filters like ETKF or LETKF?

**Why asked:** Tests awareness of related work.

**Target weakness:** Positioning relative to deterministic square-root filters.

**Strong answer:** ETKF and LETKF are deterministic in the sense of avoiding perturbed observations, but they achieve this through square-root updates that preserve the Kalman update covariance exactly. QPCA-EnDCF takes a fundamentally different approach: it doesn't try to match the Kalman update. Instead, it applies spectral regularization in observation space, deliberately discarding noise-dominated directions. The key distinction is: ETKF/LETKF preserve the full-rank update structure; QPCA-EnDCF imposes a low-rank truncation that constitutes explicit regularization. The theoretical advantage comes from this truncation — it's what gives the O(κ/N) rather than O(d/N) variance scaling.

---

## QUESTION 8
**Q:** Your comparison is against stochastic EnKF with fixed inflation. What if you used adaptive inflation or hybrid methods?

**Why asked:** Tests fairness of experimental comparison.

**Target weakness:** Baseline methods may not be optimally tuned.

**Strong answer:** Fair point. We use fixed multiplicative inflation of 1.05 for stochastic methods, which is a standard choice. The inflation study (Section 6) shows that even at the optimal inflation for each N, stochastic methods remain inferior. At N=5, optimal inflation (λ=1.10) gives Sequential EnKF RMSE of 2.15 vs QPCA-EnDCF's 1.68 — a 22% advantage even against the best-tuned stochastic baseline. Adaptive inflation would narrow the gap somewhat, but it can't eliminate the irreducible O(d/N) perturbation variance. The fundamental source of QPCA-EnDCF's advantage — eliminating perturbation noise — persists regardless of inflation strategy. That said, comparison against ETKF, LETKF, and adaptive schemes is valuable future work.

---

## QUESTION 9
**Q:** The pseudoinverse K^DC = P_xz P_zz† — isn't this numerically unstable when P_zz is severely rank-deficient?

**Why asked:** Tests numerical awareness.

**Target weakness:** Pseudoinverse in singular regime.

**Strong answer:** When N−1 < d, which is always the case in our setting (9 < 100), P_zz is singular. The pseudoinverse is well-defined and computed via SVD truncation — we zero singular values below a numerical tolerance. This is numerically stable because the SVD itself is backward-stable. Alternatively, one can use Tikhonov regularization (P_zz + εI)⁻¹, and the theory extends verbatim — the only requirement is Assumption 2, that E[‖K^DC‖²] < ∞, which holds under either implementation. In practice, we observed no numerical issues across all experiments.

---

## QUESTION 10
**Q:** You use only 5 trials for Monte Carlo estimation of bias and variance. Is that enough?

**Why asked:** Tests statistical rigor.

**Target weakness:** Small number of independent trials.

**Strong answer:** Five trials is admittedly small for precise Monte Carlo estimates. The bias estimator has positive bias (‖average − truth‖² overestimates ‖E[average] − truth‖²) that decreases as 1/N_trial. However, several factors mitigate this: (1) we also use 10 trials for the bias-variance evolution figure; (2) we aggregate over 50 windows per trial, giving 250 window-level samples; (3) the qualitative conclusions — particularly the 5× variance reduction and the 80/20 bias/variance split — are robust to trial count; and (4) the results are consistent with the theoretical predictions, providing external validation. More trials would sharpen confidence intervals but wouldn't change conclusions.

---

## QUESTION 11
**Q:** What is the sensitivity to the spectral gap δ_κ? What if it's small?

**Why asked:** Tests understanding of the key theoretical parameter.

**Target weakness:** Theory degrades when gap is small.

**Strong answer:** When δ_κ is small, the projector stability bound ‖P̂_κ − P_κ‖_F ≤ √(2κ)/δ_κ · ‖C_E − Σ_E‖_F becomes loose, and the variance term picks up a large κ/δ_κ² prefactor. Practically, a small gap means the κ-th and (κ+1)-th eigenvalues are close, so the boundary between "signal" and "noise" is ambiguous. In this regime, the specific choice of κ matters less — retaining κ or κ+1 modes gives similar results. The solution is to choose κ where a clear gap exists, which in our experiments is always at κ=1. If no clear gap exists, the method still works but its theoretical advantage is reduced.

---

## QUESTION 12
**Q:** How do you handle the temporal structure within assimilation windows? The tangent-linear assumption seems strong.

**Why asked:** Tests understanding of 4D formulation assumptions.

**Target weakness:** TLM linearization for theoretical analysis.

**Strong answer:** The tangent-linear model is used only in the theoretical analysis — specifically in Definition 5, where H^(L) is defined as a linearized stacked observation operator. The numerical experiments propagate the full nonlinear Lorenz-96 model. The TLM is a standard linearization used throughout 4D-Var and EnKF theory; it's exact for linear dynamics and valid to first order when ensemble spread is small relative to nonlinearity. In our setting, windows span 0.83 Lyapunov times with temporal autocorrelation of 0.61, so the linearization is a reasonable approximation. The experiments confirm that theoretical predictions hold despite using the full nonlinear model.

---

## QUESTION 13
**Q:** The calibration ratio γ̄ = 0.81 still indicates 19% underdispersion. Why not achieve γ̄ = 1.0?

**Why asked:** Tests honest assessment of residual limitations.

**Target weakness:** Not perfectly calibrated.

**Strong answer:** The residual underdispersion has two sources. First, the theory shows bias is 82% of MSE — this systematic component can't be captured by ensemble spread, which only reflects sampling variability. Second, κ=1 truncation discards some genuine covariance information in the tail modes. Perfect calibration (γ̄=1.0) would require either zero bias or an ensemble that accounts for both statistical and systematic uncertainty. Increasing N helps — at N=50, we achieve γ̄=0.95. The important comparison is relative: γ̄=0.81 vs 0.10. The remaining 19% gap is diagnostic: it tells us the residual error is dominated by systematic model-observation mismatch, not sampling noise.

---

## QUESTION 14
**Q:** Could localization achieve similar results without spectral truncation?

**Why asked:** Tests awareness of alternative regularization strategies.

**Target weakness:** Localization is the standard operational approach.

**Strong answer:** Localization and spectral truncation are complementary, not competing, regularization strategies. Localization restricts covariance updates spatially — it addresses rank deficiency by assuming distant state-observation correlations are spurious. Spectral truncation restricts updates in observation space — it addresses rank deficiency by assuming low-variance residual modes are noise. Localization requires specifying a length scale (analogous to our κ); getting it wrong causes tapering artifacts. In practice, both would likely be used together at operational scale. The contribution here is showing that spectral regularization alone suffices for calibration in moderate-dimensional systems, and providing theoretical understanding of why.

---

## QUESTION 15
**Q:** Your whitening assumes R is known exactly. What about R misspecification?

**Why asked:** Tests robustness to a common operational challenge.

**Target weakness:** Correctly specified R in all experiments.

**Strong answer:** All our correlated-error experiments use correctly specified R. R misspecification is a genuine operational challenge. The whitening transform is W = R^{−1/2}, so if R is wrong, the "whitened" residuals aren't truly isotropic. Moderate misspecification would bias the eigenspectrum but wouldn't break the spectral structure entirely — the leading mode would still capture dominant mismatch. Severe misspecification could cause the wrong directions to be selected for correction. This is analogous to how standard EnKF degrades with R misspecification, but QPCA-EnDCF might be more sensitive because the spectral decomposition directly depends on whitening quality. Testing R misspecification is important future work.

---

## QUESTION 16
**Q:** What is the relationship between your work and optimal interpolation or 3D-Var?

**Why asked:** Tests breadth of methodological awareness.

**Target weakness:** Positioning in broader DA landscape.

**Strong answer:** Optimal interpolation and 3D-Var use prescribed background error covariances, typically from climatological statistics. They don't adapt to flow-dependent uncertainty. Ensemble methods — including QPCA-EnDCF — estimate covariances from the ensemble itself, providing flow-dependent uncertainty. The connection is that spectral truncation in QPCA-EnDCF is analogous to truncating the background error covariance in reduced-rank methods or the control variable transformation in 3D/4D-Var. The distinction is that QPCA-EnDCF's truncation is adaptive — it's determined by the current ensemble's residual structure, not prescribed a priori.

---

## QUESTION 17
**Q:** The Lorenz-96 system has homogeneous dynamics. How would spatial heterogeneity affect the method?

**Why asked:** Tests generality beyond toy systems.

**Target weakness:** Lorenz-96 is spatially homogeneous.

**Strong answer:** Lorenz-96's spatial homogeneity means the observation operator H (every-other component) treats all locations symmetrically. With spatial heterogeneity — different dynamics in different regions, or non-uniform observation coverage — the whitened residual covariance would have more complex eigenstructure. The leading mode might be localized in certain regions rather than spanning the full domain. This could require larger κ to capture the dominant mismatch structure, or it could motivate localized spectral truncation. The framework itself doesn't assume homogeneity — the eigendecomposition adapts to whatever structure the residuals exhibit.

---

## QUESTION 18
**Q:** You mention O(κ/N) variance but also acknowledge κ/δ_κ² prefactors. Can these prefactors dominate?

**Why asked:** Tests whether the theoretical advantage is real or asymptotic.

**Target weakness:** Hidden constants in bounds.

**Strong answer:** Yes, if δ_κ is very small, the prefactor κ/δ_κ² can be large. But there's a self-correcting mechanism: when δ_κ is small, it means eigenvalues κ and κ+1 are close, which means the "boundary" between signal and noise is unclear. In that regime, the advantage of truncation is genuinely smaller. When δ_κ is large — which is the regime where truncation provides clear benefit — the prefactor is moderate. In our experiments with κ=1, the gap δ₁ = λ₁ − λ₂ is typically large (the leading eigenvalue captures 60-80% of variance), so the prefactor is well-behaved. The theory correctly identifies that the advantage depends on the gap.

---

## QUESTION 19
**Q:** How would you select κ adaptively in practice?

**Why asked:** Tests practical thinking beyond the dissertation.

**Target weakness:** κ=1 used throughout without adaptive selection.

**Strong answer:** Several strategies are natural. First, eigenvalue gap: retain modes until δ_κ = λ_κ − λ_{κ+1} drops below a threshold, selecting the largest natural gap. Second, explained variance: retain modes capturing, say, 90% of total residual variance. Third, cross-validation: for each candidate κ, evaluate forecast skill on held-out observations. Fourth, the theoretical bound itself could serve as a guide: choose κ to minimize the estimated bias-variance tradeoff. In our experiments, all of these would select κ=1 because the leading mode dominates. The interesting regime is when they disagree — that's when adaptive selection matters most.

---

## QUESTION 20
**Q:** The Lorenz-96 Lyapunov time is 0.6 and your windows span 0.83τ. What happens with longer windows?

**Why asked:** Tests understanding of dynamical limits.

**Target weakness:** Limited window length range tested.

**Strong answer:** At L=15 (spanning 2.5 Lyapunov times), RMSE increases slightly to 3.72 from the minimum of 3.64 at L=5. Beyond the Lyapunov time, forecast trajectories diverge significantly, making the tangent-linear relationship between window-initial states and observations weaker. The residual structure becomes more diffuse, with less concentration in the leading mode. Additionally, the stacked observation dimension grows (d=mL=300 at L=15), exacerbating undersampling. The practical sweet spot L∈[5,10] balances temporal information content against these degradation mechanisms. For systems with shorter Lyapunov times, shorter windows would be needed.

---

## QUESTION 21
**Q:** Your observation operator extracts every other component. What about more realistic observation scenarios?

**Why asked:** Tests generality of experimental design.

**Target weakness:** Simple, uniform observation operator.

**Strong answer:** The every-other-component operator is standard for Lorenz-96 experiments. It creates a specific null-space structure: 20 unobserved variables that must be inferred through dynamics. More realistic scenarios would include: sparse irregular observations, indirect observations (e.g., radiance instead of temperature), and time-varying observation networks. The QPCA-EnDCF framework handles any linear H — the whitening and PCA work in observation space regardless of H's structure. Nonlinear observation operators would require ensemble-based H (as in the standard EnKF), which the algorithm already supports through the stacked forecast observations Z^(w). Testing with more complex operators is future work.

---

## QUESTION 22
**Q:** What is the computational bottleneck if you scale d to, say, 10⁶?

**Why asked:** Tests computational scalability understanding.

**Target weakness:** Eigendecomposition cost.

**Strong answer:** The eigendecomposition of C_E ∈ ℝ^{d×d} costs O(d³), which becomes prohibitive for d > 10⁴ or so. However, C_E has rank at most N−1, so we never need the full eigendecomposition — only the leading κ eigenpairs. This can be computed via the "thin" SVD of E_c ∈ ℝ^{d×N}, which costs O(dN²) — linear in d. For d=10⁶ and N=50, that's 50²×10⁶ = 2.5×10⁹ operations, comparable to a single model integration. So the algorithm scales linearly in observation dimension through the thin SVD trick. This is noted in the implementation but not emphasized in the presentation.

---

## QUESTION 23
**Q:** How sensitive is the method to the initial ensemble?

**Why asked:** Tests practical robustness.

**Target weakness:** Not explicitly studied.

**Strong answer:** The 5 independent trials with different initial ensembles provide indirect evidence of robustness to initialization. The standard deviations across trials are modest: RMSE 3.55 ± 0.70 for QPCA-EnDCF. The first few windows show transient behavior as the ensemble adjusts from the initial distribution to the dynamically consistent spread, but convergence is rapid — within about 5-10 windows. More importantly, because QPCA-EnDCF doesn't require inflation, there's less sensitivity to the initial spread: if the initial ensemble is too tight, the spectral projection doesn't artificially inflate it, but the next forecast cycle's dynamics naturally restore spread. Stochastic methods are more sensitive because inflation amplifies initialization errors.

---

## QUESTION 24
**Q:** Could you achieve similar results by simply using a smaller Kalman gain (e.g., gain scaling)?

**Why asked:** Tests whether the spectral approach is necessary.

**Target weakness:** Simpler alternatives might suffice.

**Strong answer:** Gain scaling (multiplying K by α < 1) is a form of uniform damping — it reduces all updates proportionally. This is similar to multiplicative inflation in reverse. It would reduce variance but also reduce the correction magnitude uniformly, including in the signal direction. QPCA-EnDCF is adaptive: it applies full correction along the leading eigenmode and zero correction elsewhere. This selectivity is what allows variance reduction without bias increase. Uniform gain scaling would necessarily increase bias proportional to the damping. The theoretical framework makes this distinction precise: spectral truncation targets the bias-variance tradeoff optimally when the eigenspectrum has rapid decay.

---

## QUESTION 25
**Q:** What is the most important next experiment you would run if you had another year?

**Why asked:** Tests research maturity and vision.

**Target weakness:** Measures forward thinking.

**Strong answer:** The single most important experiment is QPCA-EnDCF with controlled model error on a quasi-geostrophic model. This tests the two biggest limitations simultaneously: (1) model error changes the residual structure in ways that may require adaptive κ, and (2) a QG model has rich enough dynamics (baroclinic instability, Rossby waves) to test whether the spectral separation mechanism generalizes beyond Lorenz-96. I would also implement localization, since that's the bridge to operational scale. If the method works on QG with model error and localization, the path to operational systems becomes concrete.
