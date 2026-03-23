---
title: "Math Rendering Torture Test"
---

---

## Group A: Confirmed Mangling Scenarios

**Test 1 — Multi-underscore (emphasis mangling):**

$\hat{x}_{ij} + \tilde{y}_{mn}$

**Test 2 — Greater-than:**

$\delta > 0$

**Test 3 — Less-than:**

$x < y$

**Test 4 — Backslash-paren source delimiter:**

\(\alpha + \beta\)

**Test 5 — Backslash-bracket source delimiter:**

\[x = y\]

**Test 6 — Norm in table:**

| Expression | Value |
|---|---|
| $\|x\|$ | norm bars |

---

## Group B: Delimiter Styles

**Test 7 — Display (div-wrapped):**

<div>$$\frac{a}{b}$$</div>

**Test 8 — Display (bare):**

$$\sum_{i=1}^{N} x_i$$

**Test 9 — Inline (span-wrapped):**

The value <span>$\alpha + \beta$</span> is positive.

**Test 10 — Inline (bare):**

The vector $\mathbf{x}_i^2$ is large.

**Test 11 — Adjacent display:**

$$a = b$$

$$c = d$$

---

## Group C: Container Contexts

- Test 12 — Unordered list: Value is $\kappa = 1$
- Test 13 — Bold context: **where $\delta_\kappa > 0$**
- Test 14 — Nested bold+list: **Key:** $\gamma = 0.81$ confirmed

1. Test 15 — Ordered list: Bound is $\mathcal{O}(1/N)$

| Context | Math |
|---|---|
| Table cell (Test 16) | $\mathcal{O}(d/N)$ |
| Table header math | $\delta_\kappa$ |

---

## Results for $\kappa = 1$

Test 18 — Math in heading (above)

---

## Group D: Complex TeX

**Test 20 — Aligned environment:**

$$\begin{aligned} a &= b + c \\ d &= e + f \end{aligned}$$

**Test 21 — Nested braces:**

$\mathbb{E}[\|\hat{\mathbf{v}}\|^2]$

**Test 22 — Text in math:**

$\mathrm{Bias}^2(\kappa)$

**Test 23 — Bold Greek:**

$\boldsymbol{\Sigma}_E$

---

## Group E: Negative Tests

**Test 24 — Code block (should NOT render):**

```
x^2 + y^2 = z^2
$\alpha$ should be plain text
```

**Test 25 — Escaped dollar:**

\$100 should be literal dollar

**Test 26 — No-metachar (KNOWN LIMITATION):**

$N$ — this will NOT auto-render after Phase 2. Use \(N\) instead.

**Test 29 — Aligned in display math:**

$$\begin{aligned} a &= b \end{aligned}$$

**Test 30 — Link with math:**

[See $\alpha$ here](https://example.com)

<!-- .notes:
Test 19 — Speaker note math: Rate is $\mathcal{O}(1/N)$ and $\delta_\kappa > 0$.
-->
