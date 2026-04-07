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

# A Data-Consistent approach to Ensemble Filtering

### A Unified Theoretical Framework

**Rylan Spence**

<!-- Dissertation Defense — 2026 -->

CHG Presentation - 2026

<!-- .notes:
Welcome everyone, and thank you for being here. Today I'm presenting my presentation on Data-Consistent Inversion for ensemble data assimilation. The core question: can we build ensemble filters that give reliable uncertainty estimates — not just accurate point predictions — under severe computational constraints? I'll show that deterministic spectral projection achieves this, with both rigorous theory and comprehensive experiments.
-->

---

## The Promise of Ensemble Filtering

<div style="display:flex; flex-direction:column; align-items:center; margin-top:0.15em;">
<svg viewBox="0 0 1600 500" style="width:94%; max-width:1600px;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="pef-fa" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0.5,8 3,0 5.5" fill="#8a7e72"/>
    </marker>
    <radialGradient id="pef-pg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8899aa" stop-opacity="0.25"/>
      <stop offset="60%" stop-color="#8899aa" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#8899aa" stop-opacity="0"/>
    </radialGradient>
    <g id="pef-rays" stroke="#7a8fa3">
      <line x1="-115" y1="0" x2="115" y2="0" stroke-width="1.1" opacity="0.24"/>
      <line x1="-111" y1="-30" x2="111" y2="30" stroke-width="1.0" opacity="0.20"/>
      <line x1="-100" y1="-58" x2="100" y2="58" stroke-width="0.9" opacity="0.17"/>
      <line x1="-81" y1="-81" x2="81" y2="81" stroke-width="0.8" opacity="0.14"/>
      <line x1="-58" y1="-100" x2="58" y2="100" stroke-width="0.7" opacity="0.11"/>
      <line x1="-30" y1="-111" x2="30" y2="111" stroke-width="0.7" opacity="0.09"/>
      <line x1="0" y1="-115" x2="0" y2="115" stroke-width="0.6" opacity="0.07"/>
      <line x1="30" y1="-111" x2="-30" y2="111" stroke-width="0.6" opacity="0.06"/>
      <line x1="58" y1="-100" x2="-58" y2="100" stroke-width="0.5" opacity="0.05"/>
      <line x1="81" y1="-81" x2="-81" y2="81" stroke-width="0.5" opacity="0.05"/>
      <line x1="100" y1="-58" x2="-100" y2="58" stroke-width="0.4" opacity="0.04"/>
      <line x1="111" y1="-30" x2="-111" y2="30" stroke-width="0.4" opacity="0.04"/>
    </g>
  </defs>
  <g transform="translate(235,248)">
    <use href="#pef-rays"/>
    <ellipse cx="0" cy="0" rx="140" ry="118" fill="url(#pef-pg)"/>
    <ellipse cx="0" cy="0" rx="118" ry="98" fill="none" stroke="#7a8fa3" stroke-width="0.9" opacity="0.25"/>
    <ellipse cx="0" cy="0" rx="90" ry="74" fill="none" stroke="#7a8fa3" stroke-width="1.0" opacity="0.35"/>
    <ellipse cx="0" cy="0" rx="62" ry="50" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.46"/>
    <ellipse cx="0" cy="0" rx="34" ry="26" fill="none" stroke="#7a8fa3" stroke-width="1.2" opacity="0.58"/>
    <ellipse cx="0" cy="0" rx="12" ry="8" fill="none" stroke="#7a8fa3" stroke-width="1.3" opacity="0.70"/>
    <text x="-120" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="14" fill="#9a8d7e" font-weight="500">(a)</text>
    <text x="0" y="152" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="16.5" fill="#6b5d4e" font-style="italic">p(x | z)</text>
    <text x="0" y="172" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="13.5" fill="#9a8d7e" font-style="italic">x ∈ ℝ<tspan baseline-shift="super" font-size="10">d</tspan></text>
  </g>
  <line x1="392" y1="248" x2="498" y2="248" stroke="#8a7e72" stroke-width="1" marker-end="url(#pef-fa)"/>
  <g transform="translate(710,248)">
    <use href="#pef-rays" opacity="0.22"/>
    <ellipse cx="0" cy="0" rx="118" ry="98" fill="none" stroke="#7a8fa3" stroke-width="0.6" opacity="0.12"/>
    <ellipse cx="0" cy="0" rx="90" ry="74" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.14"/>
    <ellipse cx="0" cy="0" rx="62" ry="50" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.16"/>
    <ellipse cx="0" cy="0" rx="34" ry="26" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.18"/>
    <circle cx="-40" cy="-55" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="25" cy="-68" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="68" cy="-28" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="-72" cy="-5" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="-10" cy="-16" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="40" cy="22" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="-45" cy="35" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="18" cy="58" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="65" cy="48" r="7" fill="#2a8585" opacity="0.85"/>
    <circle cx="-20" cy="72" r="7" fill="#2a8585" opacity="0.85"/>
    <text x="-118" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="14" fill="#9a8d7e" font-weight="500">(b)</text>
    <text x="0" y="130" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="16.5" fill="#2a8585" font-weight="500" font-style="italic">N samples</text>
    <text x="0" y="150" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="12.5" fill="#b0a898">weather · ocean · climate</text>
  </g>
  <line x1="898" y1="248" x2="1018" y2="248" stroke="#8a7e72" stroke-width="1" marker-end="url(#pef-fa)"/>
  <g transform="translate(1290,248)">
    <use href="#pef-rays" opacity="0.15"/>
    <ellipse cx="0" cy="0" rx="118" ry="98" fill="none" stroke="#7a8fa3" stroke-width="0.6" opacity="0.10"/>
    <ellipse cx="0" cy="0" rx="90" ry="74" fill="none" stroke="#7a8fa3" stroke-width="0.6" opacity="0.12"/>
    <ellipse cx="0" cy="0" rx="62" ry="50" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.14"/>
    <ellipse cx="0" cy="0" rx="34" ry="26" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.16"/>
    <circle cx="-18" cy="-8" r="7" fill="#c4653a" opacity="0.82"/>
    <circle cx="25" cy="18" r="7" fill="#c4653a" opacity="0.82"/>
    <circle cx="-3" cy="35" r="7" fill="#c4653a" opacity="0.82"/>
    <circle cx="60" cy="-30" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="-58" cy="10" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="40" cy="42" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="-46" cy="-32" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="15" cy="-45" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="72" cy="14" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="-32" cy="55" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <circle cx="48" cy="-10" r="5.5" fill="none" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="2,2" opacity="0.45"/>
    <text x="-118" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="14" fill="#9a8d7e" font-weight="500">(c)</text>
    <text x="0" y="138" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="19" font-weight="600" fill="#c4653a">N ≪ d</text>
  </g>
</svg>
<div class="fragment" style="margin-top:0.4em; text-align:center; font-size:1.05em; font-weight:550; color:#c4653a; letter-spacing:0.01em;">
What happens when N ≪ d ?
</div>
</div>

<!-- .notes:
Ensemble Kalman filtering is the backbone of operational data assimilation — used in weather prediction, ocean modeling, and climate science. The idea is elegant: represent posterior uncertainty through a small collection of state vectors, avoiding the need to store or manipulate full covariance matrices. But operational constraints force us to use very small ensembles — often 10 to 50 members for systems with millions of unknowns. What happens to uncertainty quantification in that regime is the central question of this work.
-->

---

## The Undersampling Crisis

<div style="display:flex; flex-direction:column; align-items:center; margin-top:0.1em;">
<svg viewBox="0 0 1700 560" style="width:96%; max-width:1700px;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="uc-a" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#8b4513"/>
    </marker>
  </defs>
  <!-- ── STAGE 1: Undersampled Regime ── -->
  <g transform="translate(50, 20)">
    <text x="190" y="14" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="22" font-weight="660" fill="#2c2418" letter-spacing="0.02em">Undersampled Regime</text>
    <!-- Dimensional hierarchy bars -->
    <rect x="0" y="52" width="340" height="40" rx="3" fill="#2a8585" fill-opacity="0.10" stroke="#2a8585" stroke-width="1.1"/>
    <text x="14" y="78" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="17" font-weight="600" fill="#2a8585">n = 40</text>
    <text x="352" y="78" font-family="Charter,Georgia,serif" font-size="14.5" fill="#6b5d4e" font-style="italic">state dimension</text>
    <rect x="0" y="104" width="170" height="40" rx="3" fill="#2a8585" fill-opacity="0.16" stroke="#2a8585" stroke-width="1.1"/>
    <text x="14" y="130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="17" font-weight="600" fill="#2a8585">m = 20</text>
    <text x="182" y="130" font-family="Charter,Georgia,serif" font-size="14.5" fill="#6b5d4e" font-style="italic">obs per time</text>
    <rect x="0" y="156" width="85" height="40" rx="3" fill="#c4653a" fill-opacity="0.13" stroke="#c4653a" stroke-width="1.3"/>
    <text x="14" y="182" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="17" font-weight="650" fill="#c4653a">N = 10</text>
    <text x="97" y="182" font-family="Charter,Georgia,serif" font-size="14.5" fill="#6b5d4e" font-style="italic">ensemble</text>
    <rect x="0" y="208" width="76" height="40" rx="3" fill="none" stroke="#c4653a" stroke-width="1.3" stroke-dasharray="5,3"/>
    <text x="14" y="234" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="16" font-weight="600" fill="#c4653a">rank ≤ 9</text>
    <text x="88" y="234" font-family="Charter,Georgia,serif" font-size="14.5" fill="#6b5d4e" font-style="italic">cov. rank</text>
    <text x="190" y="300" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="18" font-weight="650" fill="#c4653a" letter-spacing="0.01em">n ≫ N : severely undersampled</text>
  </g>
  <!-- ── ARROW 1→2 ── -->
  <line x1="475" y1="175" x2="530" y2="175" stroke="#8b4513" stroke-width="1.5" marker-end="url(#uc-a)"/>
  <text x="503" y="162" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="13.5" fill="#6b5d4e" font-style="italic">implies</text>
  <!-- ── STAGE 2: Broken Covariance Spectrum ── -->
  <g transform="translate(555, 20)">
    <text x="260" y="14" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="22" font-weight="660" fill="#2c2418" letter-spacing="0.02em">Broken Covariance Spectrum</text>
    <g transform="translate(20, 40)">
      <!-- Axes -->
      <line x1="32" y1="16" x2="32" y2="280" stroke="#5a4e40" stroke-width="0.8"/>
      <line x1="30" y1="280" x2="480" y2="280" stroke="#5a4e40" stroke-width="0.8"/>
      <text x="14" y="150" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15" fill="#6b5d4e" font-style="italic" transform="rotate(-90 14 150)">eigenvalue λᵢ</text>
      <text x="256" y="300" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="13" fill="#9a8d7e" font-style="italic">mode index i = 1 … 40</text>
      <!-- True population spectrum (faded area) -->
      <path d="M 42,35 C 80,48 115,82 150,120 C 185,158 215,188 250,215 C 285,235 325,252 375,264 C 410,270 445,275 475,278 L 475,280 L 42,280 Z" fill="#2a8585" fill-opacity="0.05" stroke="#2a8585" stroke-width="0.9" stroke-dasharray="4,3" stroke-opacity="0.22"/>
      <text x="355" y="248" font-family="Charter,Georgia,serif" font-size="11.5" fill="#2a8585" opacity="0.40" font-style="italic">true population</text>
      <!-- Empirical eigenvalue bars (9 nonzero) -->
      <rect x="42"  y="48"  width="11" height="232" rx="2" fill="#2a8585" opacity="0.52"/>
      <rect x="56"  y="88"  width="11" height="192" rx="2" fill="#2a8585" opacity="0.48"/>
      <rect x="70"  y="122" width="11" height="158" rx="2" fill="#2a8585" opacity="0.44"/>
      <rect x="84"  y="155" width="11" height="125" rx="2" fill="#2a8585" opacity="0.40"/>
      <rect x="98"  y="185" width="11" height="95"  rx="2" fill="#2a8585" opacity="0.36"/>
      <rect x="112" y="210" width="11" height="70"  rx="2" fill="#2a8585" opacity="0.32"/>
      <rect x="126" y="232" width="11" height="48"  rx="2" fill="#2a8585" opacity="0.28"/>
      <rect x="140" y="252" width="11" height="28"  rx="2" fill="#2a8585" opacity="0.25"/>
      <rect x="154" y="266" width="11" height="14"  rx="2" fill="#c4653a" opacity="0.30"/>
      <!-- Noise jitter on leading bars -->
      <path d="M 44,44 l 2,-5 l 2,5 l 2,-4 l 2,4" fill="none" stroke="#c4653a" stroke-width="0.9" opacity="0.55"/>
      <path d="M 58,84 l 2,-4 l 2,4 l 2,-3 l 2,3" fill="none" stroke="#c4653a" stroke-width="0.9" opacity="0.45"/>
      <path d="M 72,118 l 1.5,-3.5 l 2,3.5 l 1.5,-3" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.38"/>
      <!-- Bias annotation -->
      <text x="115" y="36" font-family="Charter,Georgia,serif" font-size="12.5" fill="#c4653a" font-style="italic" opacity="0.7">noisy + biased ↓</text>
      <path d="M 112,38 L 72,48" fill="none" stroke="#c4653a" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
      <!-- Zero eigenvalue flat region -->
      <line x1="170" y1="280" x2="470" y2="280" stroke="#c4653a" stroke-width="2.5" opacity="0.15"/>
      <!-- Tick marks for zero positions -->
      <g opacity="0.18" stroke="#c4653a" stroke-width="0.8">
        <line x1="175" y1="278" x2="175" y2="282"/><line x1="185" y1="278" x2="185" y2="282"/>
        <line x1="195" y1="278" x2="195" y2="282"/><line x1="205" y1="278" x2="205" y2="282"/>
        <line x1="215" y1="278" x2="215" y2="282"/><line x1="225" y1="278" x2="225" y2="282"/>
        <line x1="235" y1="278" x2="235" y2="282"/><line x1="245" y1="278" x2="245" y2="282"/>
        <line x1="255" y1="278" x2="255" y2="282"/><line x1="265" y1="278" x2="265" y2="282"/>
        <line x1="275" y1="278" x2="275" y2="282"/><line x1="285" y1="278" x2="285" y2="282"/>
        <line x1="295" y1="278" x2="295" y2="282"/><line x1="305" y1="278" x2="305" y2="282"/>
        <line x1="315" y1="278" x2="315" y2="282"/><line x1="325" y1="278" x2="325" y2="282"/>
        <line x1="335" y1="278" x2="335" y2="282"/><line x1="345" y1="278" x2="345" y2="282"/>
        <line x1="355" y1="278" x2="355" y2="282"/><line x1="365" y1="278" x2="365" y2="282"/>
        <line x1="375" y1="278" x2="375" y2="282"/><line x1="385" y1="278" x2="385" y2="282"/>
        <line x1="395" y1="278" x2="395" y2="282"/><line x1="405" y1="278" x2="405" y2="282"/>
        <line x1="415" y1="278" x2="415" y2="282"/><line x1="425" y1="278" x2="425" y2="282"/>
        <line x1="435" y1="278" x2="435" y2="282"/><line x1="445" y1="278" x2="445" y2="282"/>
        <line x1="455" y1="278" x2="455" y2="282"/><line x1="465" y1="278" x2="465" y2="282"/>
        <line x1="470" y1="278" x2="470" y2="282"/>
      </g>
      <!-- Bracket for zero region -->
      <path d="M 170,290 L 170,296 L 320,296 L 320,302 M 320,296 L 470,296 L 470,290" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.55"/>
      <text x="320" y="318" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="14.5" fill="#c4653a" font-weight="560">31 zero eigenvalues</text>
      <!-- Rank label -->
      <text x="105" y="318" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="14" fill="#2a8585" font-weight="560">rank(Ĉ) ≤ 9</text>
    </g>
  </g>
  <!-- ── ARROW 2→3 ── -->
  <line x1="1100" y1="175" x2="1155" y2="175" stroke="#8b4513" stroke-width="1.5" marker-end="url(#uc-a)"/>
  <text x="1128" y="162" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="13.5" fill="#6b5d4e" font-style="italic">therefore</text>
  <!-- ── STAGE 3: Operational Impact ── -->
  <g transform="translate(1185, 20)">
    <text x="220" y="14" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="22" font-weight="660" fill="#2c2418" letter-spacing="0.02em">Operational Failure</text>
    <!-- Weather -->
    <g transform="translate(55, 85)">
      <circle cx="0" cy="0" r="30" fill="none" stroke="#c4653a" stroke-width="1.2" opacity="0.45"/>
      <path d="M -19,-9 Q 0,-20 19,-9" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.35"/>
      <path d="M -21,2 Q 0,-7 21,2" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.35"/>
      <path d="M -19,13 Q 0,4 19,13" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.35"/>
      <text x="46" y="2" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="16" fill="#2c2418" font-weight="570">weather</text>
      <text x="46" y="20" font-family="Charter,Georgia,serif" font-size="13.5" fill="#6b5d4e" font-style="italic">wrong warning thresholds</text>
    </g>
    <!-- Ocean -->
    <g transform="translate(55, 175)">
      <circle cx="0" cy="0" r="30" fill="none" stroke="#c4653a" stroke-width="1.2" opacity="0.45"/>
      <path d="M -19,-5 Q -9,-15 0,-5 Q 9,5 19,-5" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.35"/>
      <path d="M -19,7 Q -9,-2 0,7 Q 9,16 19,7" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.35"/>
      <text x="46" y="2" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="16" fill="#2c2418" font-weight="570">ocean</text>
      <text x="46" y="20" font-family="Charter,Georgia,serif" font-size="13.5" fill="#6b5d4e" font-style="italic">corrupted reanalysis</text>
    </g>
    <!-- Climate -->
    <g transform="translate(55, 265)">
      <circle cx="0" cy="0" r="30" fill="none" stroke="#c4653a" stroke-width="1.2" opacity="0.45"/>
      <ellipse cx="0" cy="0" rx="12" ry="30" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.3"/>
      <line x1="-30" y1="0" x2="30" y2="0" stroke="#c4653a" stroke-width="0.8" opacity="0.3"/>
      <text x="46" y="2" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="16" fill="#2c2418" font-weight="570">climate</text>
      <text x="46" y="20" font-family="Charter,Georgia,serif" font-size="13.5" fill="#6b5d4e" font-style="italic">biased confidence bands</text>
    </g>
  </g>
  <!-- ── CONCLUSION ── -->
  <line x1="80" y1="425" x2="1620" y2="425" stroke="#d8d0c4" stroke-width="1" stroke-dasharray="6,4"/>
  <text x="850" y="475" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="26" font-weight="720" fill="#c4653a" letter-spacing="0.01em">Overconfident ensembles are worse than no uncertainty</text>
  <text x="850" y="515" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="16.5" fill="#6b5d4e" font-style="italic" letter-spacing="0.01em">n ≫ N   →   rank-deficient covariance   →   overconfident uncertainty   →   unreliable decisions</text>
</svg>
</div>

<!-- .notes:
Here's the regime I study. In the Lorenz-96 system with 40 state variables, we observe 20 components but have only 10 ensemble members. The empirical covariance has rank at most 9 — it's missing information in 31 directions. And the eigenvalues it does estimate are biased downward. This is a mathematical certainty, not an implementation failure. Why should we care? Because downstream decisions depend on this uncertainty. In weather forecasting, ensemble spread directly controls warning thresholds — if spread is 15 times too small, extreme events go unwarned. In ocean reanalysis, misspecified uncertainty corrupts initialization. In climate, it biases confidence bands. Overconfident uncertainty isn't just imprecise — it's actively misleading. It's worse than admitting you don't know.
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

## QPCA-EnDCF: Computational Pipeline

<div style="display:flex; align-items:center; gap:0; width:100%; font-size:0.48em; line-height:1.4;">
<div style="flex:1; text-align:center; padding:0 0.15em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.3em; letter-spacing:0.03em;">FORECAST</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Propagate ensemble</strong><br><span>$\mathbf{x}^{(j)} \leftarrow \mathcal{M}(\mathbf{x}^{(j)}),\; j=1,\ldots,N$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Observation operator</strong><br><span>$\mathbf{Y}_k = \mathbf{H}\mathbf{X}_k,\;\; k = k_0{+}1,\ldots,k_w$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Stack observations</strong><br><span>$\mathbf{Z}^{(w)} \in \mathbb{R}^{d \times N}$</span></div>
<div style="color:#999; font-size:0.8em; margin-top:0.2em;"><span>$\mathbb{R}^{n \times N}$</span> state space</div>
</div>
<div style="display:flex; align-items:center; color:#5a7a6d; font-size:1.8em; padding:0 0.08em;">→</div>
<div style="flex:1.15; text-align:center; padding:0 0.15em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.3em; letter-spacing:0.03em;">WHITEN</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Residuals</strong><br><span>$\mathbf{D} = \mathbf{Z}^{(w)} - \mathbf{z}^{(w)}\mathbf{1}^\top$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;"><strong>Whiten + Center</strong><br><span>$\mathbf{E} = (\mathbf{R}^{(L)})^{-1/2}\mathbf{D}$</span><br><span>$\mathbf{E}_c = \mathbf{E} - \tfrac{1}{N}(\mathbf{E}\mathbf{1})\mathbf{1}^\top$</span></div>
<div style="color:#888; font-size:0.85em; border:1px dashed #aaa; border-radius:3px; display:inline-block; padding:0.1em 0.3em; margin-top:0.15em;"><span>$\mathbf{R}^{(L)} = \mathbf{I}_L \otimes \mathbf{R}$</span></div>
<div style="color:#999; font-size:0.8em; margin-top:0.2em;"><span>$\mathbb{R}^{d \times N}$</span> obs space (<span>$d = mL$</span>)</div>
</div>
<div style="display:flex; align-items:center; color:#5a7a6d; font-size:1.8em; padding:0 0.08em;">→</div>
<div style="flex:1.15; text-align:center; padding:0 0.15em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.3em; letter-spacing:0.03em;">SPECTRAL DECOMP.</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Sample covariance</strong><br><span>$\mathbf{C}_E = \tfrac{1}{N{-}1}\mathbf{E}_c\mathbf{E}_c^\top$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;"><strong>Eigendecompose + Truncate</strong><br><span>$\hat{\mathbf{V}}_\kappa = [\hat{\mathbf{v}}_1,\ldots,\hat{\mathbf{v}}_\kappa]$</span></div>
<div style="color:#999; font-size:0.8em; margin-top:0.2em;"><span>$\mathbb{R}^{d \times d} \to$</span> rank <span>$\kappa \ll d$</span></div>
</div>
<div style="display:flex; align-items:center; color:#5a7a6d; font-size:1.8em; padding:0 0.08em;">→</div>
<div style="flex:1.15; text-align:center; padding:0 0.15em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.3em; letter-spacing:0.03em;">CORRECTION</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Project onto signal subspace</strong><br><span>$\mathbf{Q}_{\mathrm{PCA}} = -\hat{\mathbf{V}}_\kappa\hat{\mathbf{V}}_\kappa^\top\mathbf{E}$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;"><strong>Unwhiten to obs space</strong><br><span>$\boldsymbol{\Delta}_{\mathrm{obs}} = (\mathbf{R}^{(L)})^{1/2}\mathbf{Q}_{\mathrm{PCA}}$</span></div>
<div style="color:#999; font-size:0.8em; margin-top:0.2em;"><span>$\mathbb{R}^{d \times N}$</span> restricted to <span>$\kappa$</span> modes</div>
</div>
<div style="display:flex; align-items:center; color:#5a7a6d; font-size:1.8em; padding:0 0.08em;">→</div>
<div style="flex:1.15; text-align:center; padding:0 0.15em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.3em; letter-spacing:0.03em;">UPDATE</div>
<div style="border:1.5px solid #5a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0;"><strong>Data-consistent gain</strong><br><span>$\mathbf{P}_{xz} = \tfrac{1}{N{-}1}\mathbf{A}_x\mathbf{A}_z^\top$</span>, <span>$\mathbf{P}_{zz} = \tfrac{1}{N{-}1}\mathbf{A}_z\mathbf{A}_z^\top$</span><br><span>$\mathbf{K}^{\mathrm{DC}} = \mathbf{P}_{xz}\mathbf{P}_{zz}^\dagger$</span></div>
<div style="color:#5a7a6d; font-size:1.2em; line-height:1;">↓</div>
<div style="border:2px solid #1a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:rgba(26,122,109,0.1);"><strong>Deterministic state update</strong><br><span>$\mathbf{X}_{k_w} \leftarrow \mathbf{X}_{k_w} + \mathbf{K}^{\mathrm{DC}}\boldsymbol{\Delta}_{\mathrm{obs}}$</span></div>
<div style="color:#999; font-size:0.8em; margin-top:0.2em;"><span>$\mathbb{R}^{n \times N}$</span> analysis ensemble</div>
</div>
</div>
<div style="text-align:center; margin-top:0.3em; padding:0.25em 1em; border-top:1.5px dashed #5a7a6d; font-size:0.45em; color:#5a7a6d; font-style:italic;">↺ <span>$\mathbf{X} \leftarrow \mathbf{X}_{k_w}$</span> — advance to next window <span>$w + 1$</span>. Fully deterministic; cost dominated by <span>$\mathcal{M}$</span> propagation.</div>

<!-- .notes:
This diagram shows the complete QPCA-EnDCF computational pipeline as implemented in Algorithm 1 of the paper. Five phases execute per assimilation window. First, the forecast phase propagates all N ensemble members through L observation times using the forward model M, then applies the observation operator H to get forecast observations Y-k at each time. These are stacked into Z-w. Second, whitening normalizes residuals by the block-diagonal observation covariance R-L = I-L tensor R, producing whitened residuals E with identity noise covariance, then centers them. Third, spectral decomposition eigendecomposes the sample covariance C-E and retains the leading kappa eigenvectors V-hat-kappa. Fourth, the correction projects whitened residuals onto the signal subspace via Q-PCA = minus V-hat-kappa V-hat-kappa-transpose E, then unwhitens to get observation-space increments Delta-obs. Fifth, the update computes the data-consistent gain K-DC = P-xz times P-zz-pseudoinverse from empirical cross-covariances and applies the deterministic update X-kw gets X-kw plus K-DC Delta-obs. The feedback loop advances the analysis ensemble to the next window.
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

## Variance Collapse in Action

![Spread vs RMSE Temporal](figures/spread_vs_rmse_temporal.png)

- **Stochastic EnKF**: spread ≈ 0.3, RMSE ≈ 4.5
- Ensemble claims $\sigma = 0.3$, actual error = 4.5
- **15× overconfident** uncertainty estimates

<!-- .notes:
This figure tells the whole story of the problem. The solid lines are ensemble spread — what the filter thinks the error is. The dashed lines are RMSE — the actual error. For sequential EnKF, the spread flatlines near 0.3 while the true error fluctuates between 3 and 6. That means the filter is 15 times more confident than it should be. The 4D-EnKF is slightly better but still severely underdispersed. This isn't just an academic concern — overconfident uncertainty renders ensemble forecasts unreliable for decision-making.
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

| Parameter                        | Value                                                                                 |
| -------------------------------- | ------------------------------------------------------------------------------------- |
| State dimension <span>$n$</span> | 40 (<span>$x_i$</span>: state variable at index <span>$i$</span>)                     |
| Forcing <span>$F$</span>         | 8 (chaotic regime, 13 positive Lyapunov exponents)                                    |
| Observations <span>$m$</span>    | 20 every-other component, <span>$\sigma_{\mathrm{obs}} = 1.5$</span>                  |
| Ensemble size <span>$N$</span>   | 10 (severe undersampling)                                                             |
| Window length <span>$L$</span>   | 5 (spanning 0.83 Lyapunov times — time for errors to grow by factor <span>$e$</span>) |
| Methods                          | Seq-EnKF, 4D-EnKF, QPCA-EnDCF (<span>$\kappa=1$</span>)                               |
| Trials                           | 5 independent Monte Carlo realizations                                                |

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

## Result 3: Inflation-Free Operation — Additive

<div>$$\mathbf{x}^{(j)}_{\alpha_{\mathrm{add}}} = \mathbf{x}^{(j),f} + \boldsymbol{\varepsilon}^{(j)}, \qquad \boldsymbol{\varepsilon}^{(j)} \sim \mathcal{N}(\mathbf{0},\; \alpha_{\mathrm{add}}^2\,\mathbf{Q}_{\mathrm{add}}), \qquad \mathbf{Q}_{\mathrm{add}} = \mathbf{I}_n$$</div>

- Injects isotropic noise to alleviate rank deficiency — but disrupts dynamical correlations unless <span>$\mathbf{Q}_{\mathrm{add}}$</span> reflects true dynamics
- QPCA-EnDCF preserves correlation structure spectrally, making additive inflation unnecessary

![Additive Inflation](figures/inflation_additive_20.png)

- QPCA-EnDCF optimal at <span>$\alpha_{\mathrm{add}} = 0$</span> for all <span>$N$</span>; any <span>$\alpha_{\mathrm{add}} > 0$</span> degrades performance
- Stochastic methods: additive underperforms multiplicative by 5–10%

<!-- .notes:
Additive inflation perturbs each ensemble member with independent Gaussian noise drawn from alpha-add-squared times Q-add. With the standard isotropic choice Q-add equals I-n, this injects variance uniformly across all state dimensions — including directions orthogonal to the ensemble subspace. Unlike multiplicative inflation, it can partially address rank deficiency, but unless Q-add reflects dynamical correlations, the injected variance is physically implausible. QPCA-EnDCF is optimal with zero additive inflation for every ensemble size tested. Adding isotropic noise actually hurts because it disrupts the dynamically consistent correlation structure that spectral regularization preserves. For stochastic methods, additive inflation provides marginal improvement over no inflation but consistently underperforms multiplicative inflation by 5 to 10 percent, because isotropic perturbations inject variance in dynamically irrelevant directions.
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

## Result 4: Robustness — Correlated Observation Errors

**Given known <span>$\mathbf{R}$</span>, QPCA-EnDCF degrades ≤ 7% across 5 orders of magnitude in <span>$\mathrm{cond}(\mathbf{R})$</span>.**

Correlated covariance structures (<span>$d_{ij}$</span>: periodic index distance, <span>$\ell$</span>: correlation length), whitened via <span>$\mathbf{R} = \mathbf{L}\mathbf{L}^\top$</span>, <span>$\mathbf{W} = \mathbf{L}^{-\top}$</span>:

<div>$$[\mathbf{R}]_{ij} = \sigma_{\mathrm{obs}}^2 \exp\!\left(-\frac{d_{ij}}{\ell}\right) \;\text{(exponential, cond = 649)}, \qquad [\mathbf{R}]_{ij} = \sigma_{\mathrm{obs}}^2 \exp\!\left(-\frac{d_{ij}^2}{2\ell^2}\right) \;\text{(Gaussian, cond} \approx 3.7 \times 10^5\text{)}$$</div>

<div style="display: flex; gap: 1.5em; align-items: center;">
<div style="flex: 1;">
<img src="figures/correlation_structures.png" alt="Correlation Structures" style="max-height: 50vh; max-width: 100%;">
</div>
<div style="flex: 1;">
<img src="figures/reconstruction_errors.png" alt="Reconstruction Errors" style="max-height: 50vh; max-width: 100%;">
</div>
</div>

- QPCA-EnDCF within 7% of diagonal baseline; 4D-EnKF degrades 15% — advantage grows from 25% → 32%
- **Mechanism:** Cholesky whitening restores <span>$\mathbf{W}\mathbf{R}\mathbf{W}^\top = \mathbf{I}$</span> before spectral analysis; stochastic perturbations lose efficiency as correlations reduce independent information
- **Scope:** true <span>$\mathbf{R}$</span> provided to filter (no misspecification); tests algorithmic stability, not robustness to unknown correlations

<!-- .notes:
This slide tests algorithmic robustness: given the true observation covariance R, does QPCA-EnDCF maintain performance as correlation strength and conditioning increase? This is explicitly not a misspecification test — the filter receives R matching the data-generating process. We test three structures spanning five orders of magnitude in condition number: diagonal baseline with cond-R equals 1, exponential with cond-R equals 649, and Gaussian with cond-R approximately 370,000. Here d-ij is the periodic index distance between observed components, and ell is the correlation length scale, set to 4 in all experiments. QPCA-EnDCF degrades only modestly — within 7 percent of the uncorrelated baseline even at cond-R of 370,000. By contrast, 4D-EnKF degrades by 15.3 percent. The advantage grows from 25 to 32 percent under severe ill-conditioning. The mechanism: Cholesky whitening maps the correlated observation space to identity covariance — W R W-transpose equals I — restoring the isotropic noise structure that makes subsequent PCA meaningful. Stochastic perturbations sampled from the correlated structure become less efficient because correlated observations contribute less independent information, yet perturbation noise scales with the full dimension d.
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
