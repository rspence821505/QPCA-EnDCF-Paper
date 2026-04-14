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

<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:70vh;">
<div style="font-size:2.2em; font-weight:700; color:#2c2418; line-height:1.3; text-align:center;">A Data-Consistent Approach<br>to Ensemble Filtering</div>
<div style="margin-top:0.6em; font-size:0.85em; color:#5a4e40; font-style:italic; text-align:center;">Calibrated uncertainty quantification via spectral regularization</div>
<div style="margin-top:2em; font-size:1.1em; font-weight:600; color:#3a3024;">Rylan Spence</div>
<div style="margin-top:0.3em; font-size:0.85em; color:#5a4e40;">CHG Presentation · 2026</div>
</div>

<!-- .notes:
Thank you all for being here. The central question of this talk: can we build ensemble filters that produce reliable uncertainty estimates — not just accurate point predictions — under severe computational constraints? I'll show that a deterministic, spectrally regularized approach achieves this, with both comprehensive experiments and a clear mechanistic explanation.
-->

---

## The Promise of Ensemble Filtering

<div style="display:flex; flex-direction:column; align-items:center; margin-top:0.15em;">
<svg viewBox="0 0 1250 570" style="width:100%; max-width:1920px;" xmlns="http://www.w3.org/2000/svg">
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
  <g transform="translate(190,235)">
    <!-- Axes -->
    <line x1="-130" y1="0" x2="130" y2="0" stroke="#c8c0b4" stroke-width="0.7"/>
    <line x1="0" y1="-120" x2="0" y2="120" stroke="#c8c0b4" stroke-width="0.7"/>
    <text x="135" y="5" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">1</tspan></text>
    <text x="5" y="-122" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">2</tspan></text>
    <!-- Tilted posterior contours (2D Gaussian, rotated ~25°) -->
    <ellipse cx="0" cy="0" rx="120" ry="55" fill="#5a7a9a" fill-opacity="0.04" stroke="#5a7a9a" stroke-width="0.8" opacity="0.25" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="95" ry="42" fill="#5a7a9a" fill-opacity="0.06" stroke="#5a7a9a" stroke-width="0.9" opacity="0.35" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="70" ry="30" fill="#5a7a9a" fill-opacity="0.09" stroke="#5a7a9a" stroke-width="1.0" opacity="0.45" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="45" ry="18" fill="#5a7a9a" fill-opacity="0.14" stroke="#5a7a9a" stroke-width="1.1" opacity="0.58" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="20" ry="8" fill="#5a7a9a" fill-opacity="0.22" stroke="#5a7a9a" stroke-width="1.2" opacity="0.72" transform="rotate(-25)"/>
    <!-- MAP point -->
    <circle cx="0" cy="0" r="3.5" fill="#3a5a7a" opacity="0.85"/>
    <!-- Contour level labels removed -->
    <text x="-120" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="24" fill="#5a4e40" font-weight="600">(a)</text>
    <text x="0" y="150" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="22" fill="#6b5d4e" font-style="italic">posterior  p(x | z)</text>
    <text x="0" y="178" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#5a4e40">x : state ∈ ℝ<tspan baseline-shift="super" font-size="12">n</tspan>,   z : observations</text>
  </g>
  <g class="fragment" data-fragment-index="0">
  <line x1="348" y1="235" x2="440" y2="235" stroke="#8a7e72" stroke-width="1.2" marker-end="url(#pef-fa)"/>
  <g transform="translate(620,235)">
    <!-- Axes (matching (a)) -->
    <line x1="-130" y1="0" x2="130" y2="0" stroke="#c8c0b4" stroke-width="0.7"/>
    <line x1="0" y1="-120" x2="0" y2="120" stroke="#c8c0b4" stroke-width="0.7"/>
    <text x="135" y="5" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">1</tspan></text>
    <text x="5" y="-122" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">2</tspan></text>
    <!-- Ghost posterior contours (same shape as (a)) -->
    <ellipse cx="0" cy="0" rx="120" ry="55" fill="none" stroke="#5a7a9a" stroke-width="1.0" opacity="0.35" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="95" ry="42" fill="none" stroke="#5a7a9a" stroke-width="1.0" opacity="0.40" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="70" ry="30" fill="none" stroke="#5a7a9a" stroke-width="1.1" opacity="0.45" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="45" ry="18" fill="none" stroke="#5a7a9a" stroke-width="1.1" opacity="0.50" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <!-- N=10 samples scattered along the tilted posterior -->
    <circle cx="-8" cy="6" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="22" cy="-12" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="-30" cy="18" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="48" cy="-28" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="-55" cy="30" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="12" cy="2" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="70" cy="-38" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="-18" cy="28" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="38" cy="-8" r="8" fill="#2a8585" opacity="0.85"/>
    <circle cx="-42" cy="42" r="8" fill="#2a8585" opacity="0.85"/>
    <text x="-118" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="24" fill="#5a4e40" font-weight="600">(b)</text>
    <text x="0" y="135" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="22" fill="#2a8585" font-weight="500" font-style="italic">N samples</text>
  </g>
  </g>
  <g class="fragment" data-fragment-index="1">
  <line x1="798" y1="235" x2="890" y2="235" stroke="#8a7e72" stroke-width="1.2" marker-end="url(#pef-fa)"/>
  <g transform="translate(1060,235)">
    <!-- Axes (matching (a) and (b)) -->
    <line x1="-130" y1="0" x2="130" y2="0" stroke="#c8c0b4" stroke-width="0.7"/>
    <line x1="0" y1="-120" x2="0" y2="120" stroke="#c8c0b4" stroke-width="0.7"/>
    <text x="135" y="5" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">1</tspan></text>
    <text x="5" y="-122" fill="#3a3024" font-size="14" font-weight="600" font-family="Georgia,serif" font-style="italic">x<tspan baseline-shift="sub" font-size="10">2</tspan></text>
    <!-- Ghost posterior contours (same as (b)) -->
    <ellipse cx="0" cy="0" rx="120" ry="55" fill="none" stroke="#5a7a9a" stroke-width="1.0" opacity="0.35" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="95" ry="42" fill="none" stroke="#5a7a9a" stroke-width="1.0" opacity="0.40" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="70" ry="30" fill="none" stroke="#5a7a9a" stroke-width="1.1" opacity="0.45" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <ellipse cx="0" cy="0" rx="45" ry="18" fill="none" stroke="#5a7a9a" stroke-width="1.1" opacity="0.50" stroke-dasharray="5,3" transform="rotate(-25)"/>
    <!-- Only 3 actual samples (severely undersampled) — along the tilt -->
    <circle cx="-5" cy="4" r="8" fill="#c4653a" opacity="0.85"/>
    <circle cx="20" cy="-10" r="8" fill="#c4653a" opacity="0.85"/>
    <circle cx="-25" cy="16" r="8" fill="#c4653a" opacity="0.85"/>
    <!-- Missing samples — dashed hollow where (b) had dots -->
    <circle cx="48" cy="-28" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="-55" cy="30" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="70" cy="-38" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="-42" cy="42" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="38" cy="-8" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="-18" cy="28" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <circle cx="60" cy="15" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" stroke-dasharray="2.5,2" opacity="0.50"/>
    <text x="-118" y="-130" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="24" fill="#5a4e40" font-weight="600">(c)</text>
    <text x="0" y="140" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="26" font-weight="600" fill="#c4653a">N ≪ d</text>
    <text x="0" y="166" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#5a4e40" font-style="italic">d = observation dimension</text>
  </g>
  </g>
  <line x1="60" y1="450" x2="780" y2="450" stroke="#d0c8bc" stroke-width="0.5" stroke-dasharray="4,3"/>
  <g transform="translate(190,460) scale(1.8)">
    <path d="M-14,-8 Q0,-14 14,-8" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
    <path d="M-14,0 Q0,-6 14,0" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
    <path d="M-14,8 Q0,2 14,8" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
  </g>
  <text x="190" y="506" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="19" font-weight="600" fill="#6b5d4e">weather</text>
  <text x="190" y="527" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">x : wind, pressure, humidity</text>
  <text x="190" y="546" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">z : satellite, radar, station</text>
  <g transform="translate(440,460) scale(1.8)">
    <path d="M-14,4 Q-7,-3 0,4 Q7,11 14,4" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
    <circle cx="0" cy="-5" r="5" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
    <line x1="0" y1="-10" x2="0" y2="-15" stroke="#7a8fa3" stroke-width="0.8" opacity="0.5"/>
  </g>
  <text x="440" y="506" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="19" font-weight="600" fill="#6b5d4e">ocean</text>
  <text x="440" y="527" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">x : currents, temperature</text>
  <text x="440" y="546" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">z : buoys, altimetry</text>
  <g transform="translate(680,460) scale(1.8)">
    <circle cx="0" cy="0" r="10" fill="none" stroke="#7a8fa3" stroke-width="1.1" opacity="0.5"/>
    <ellipse cx="0" cy="0" rx="5" ry="10" fill="none" stroke="#7a8fa3" stroke-width="0.7" opacity="0.35"/>
    <line x1="-10" y1="0" x2="10" y2="0" stroke="#7a8fa3" stroke-width="0.7" opacity="0.35"/>
  </g>
  <text x="680" y="506" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="19" font-weight="600" fill="#6b5d4e">climate</text>
  <text x="680" y="527" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">x : temperature, ice extent</text>
  <text x="680" y="546" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="15.5" fill="#5a4e40">z : ice cores, station records</text>
</svg>
<div class="fragment" data-fragment-index="1" style="margin-top:0.4em; text-align:center; font-size:1.3em; font-weight:600; color:#c4653a; letter-spacing:0.01em;">
What happens when N ≪ d ?
</div>
</div>

<!-- .notes:
Ensemble Kalman filtering is the backbone of operational data assimilation — used in weather prediction, ocean modeling, and climate science. The idea is elegant: represent posterior uncertainty through a small collection of state vectors, avoiding the need to store or manipulate full covariance matrices. But operational constraints force us to use very small ensembles — often 10 to 50 members for systems with millions of unknowns. What happens to uncertainty quantification in that regime is the central question of this work.
-->

---

## The Undersampling Crisis

<div style="display:flex; flex-direction:column; align-items:center; margin-top:0.1em;">
<svg viewBox="0 0 1580 430" style="width:100%; max-width:1920px;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="uc-a" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#8b4513"/>
    </marker>
  </defs>
  <!-- ═══ STAGE 1: REGIME — n > m > N ═══ -->
  <g transform="translate(30, 50)">
    <text x="130" y="14" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="26" font-weight="660" fill="#2c2418" letter-spacing="0.02em">Undersampled Regime</text>
    <rect x="0" y="40" width="260" height="38" rx="3" fill="#2a8585" fill-opacity="0.10" stroke="#2a8585" stroke-width="1"/>
    <text x="10" y="65" font-family="-apple-system,'Inter',sans-serif" font-size="20" font-weight="620" fill="#2a8585">n = 40</text>
    <text x="268" y="65" font-family="Charter,Georgia,serif" font-size="18" fill="#6b5d4e" font-style="italic">state</text>
    <rect x="0" y="90" width="130" height="38" rx="3" fill="#2a8585" fill-opacity="0.16" stroke="#2a8585" stroke-width="1"/>
    <text x="10" y="115" font-family="-apple-system,'Inter',sans-serif" font-size="20" font-weight="620" fill="#2a8585">m = 20</text>
    <text x="138" y="115" font-family="Charter,Georgia,serif" font-size="18" fill="#6b5d4e" font-style="italic">observed</text>
    <rect x="0" y="140" width="95" height="38" rx="3" fill="#c4653a" fill-opacity="0.14" stroke="#c4653a" stroke-width="1.3"/>
    <text x="10" y="165" font-family="-apple-system,'Inter',sans-serif" font-size="20" font-weight="660" fill="#c4653a">N = 10</text>
    <text x="103" y="165" font-family="Charter,Georgia,serif" font-size="18" fill="#c4653a" font-style="italic">ensemble</text>
    <text x="130" y="222" text-anchor="middle" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif" font-size="21" font-weight="650" fill="#c4653a" letter-spacing="0.01em">n ≫ N : severely undersampled</text>
  </g>
  <g class="fragment" data-fragment-index="0">
  <!-- ARROW 1→2 -->
  <line x1="315" y1="175" x2="345" y2="175" stroke="#8b4513" stroke-width="1.3" marker-end="url(#uc-a)"/>
  <!-- ═══ STAGE 2: SPECTRUM — noisy retained + structurally missing ═══ -->
  <g transform="translate(360, 25)">
    <text x="230" y="14" text-anchor="middle" font-family="-apple-system,'Inter',sans-serif" font-size="23" font-weight="640" fill="#2c2418">Empirical Covariance Spectrum</text>
    <g transform="translate(10, 35)">
      <!-- Axes -->
      <line x1="28" y1="12" x2="28" y2="275" stroke="#5a4e40" stroke-width="0.7"/>
      <line x1="26" y1="275" x2="440" y2="275" stroke="#5a4e40" stroke-width="0.7"/>
      <text x="10" y="145" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="22" fill="#3a3024" font-weight="600" font-style="italic" transform="rotate(-90 10 145)">λᵢ</text>
      <!-- True population spectrum (faded area) -->
      <path d="M 36,28 C 68,40 95,75 130,112 C 160,145 190,175 225,205 C 255,225 290,242 335,255 C 370,262 405,268 435,272 L 435,275 L 36,275 Z" fill="#2a8585" fill-opacity="0.04" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="3,3" stroke-opacity="0.18"/>
      <text x="355" y="248" font-family="Charter,Georgia,serif" font-size="16" fill="#2a8585" opacity="0.90" font-style="italic" font-weight="600">true distribution</text>
      <!-- Ghost bars: structurally missing eigenvalues (modes 10–18) — grey dashed outlines rising to true spectrum -->
      <rect x="150" y="263" width="9" height="12"  rx="1" fill="none" stroke="#555" stroke-width="1.6" stroke-dasharray="4,2.5" opacity="0.80"/>
      <rect x="162" y="266" width="9" height="9"   rx="1" fill="none" stroke="#555" stroke-width="1.6" stroke-dasharray="4,2.5" opacity="0.75"/>
      <rect x="174" y="268" width="9" height="7"   rx="1" fill="none" stroke="#555" stroke-width="1.5" stroke-dasharray="4,2.5" opacity="0.70"/>
      <rect x="186" y="270" width="9" height="5"   rx="1" fill="none" stroke="#555" stroke-width="1.5" stroke-dasharray="4,2.5" opacity="0.65"/>
      <rect x="198" y="271" width="9" height="4"   rx="1" fill="none" stroke="#555" stroke-width="1.4" stroke-dasharray="4,2.5" opacity="0.60"/>
      <rect x="210" y="272" width="9" height="3"   rx="1" fill="none" stroke="#555" stroke-width="1.4" stroke-dasharray="4,2.5" opacity="0.55"/>
      <rect x="222" y="273" width="9" height="2"   rx="1" fill="none" stroke="#555" stroke-width="1.3" stroke-dasharray="4,2.5" opacity="0.50"/>
      <rect x="234" y="274" width="9" height="1"   rx="1" fill="none" stroke="#555" stroke-width="1.3" stroke-dasharray="4,2.5" opacity="0.45"/>
      <rect x="246" y="274" width="9" height="1"   rx="1" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="4,2.5" opacity="0.40"/>
      <!-- Faint baseline ticks for modes 19–40 -->
      <g opacity="0.35" stroke="#555" stroke-width="1.0">
        <line x1="261" y1="273" x2="261" y2="275"/><line x1="273" y1="273" x2="273" y2="275"/>
        <line x1="285" y1="273" x2="285" y2="275"/><line x1="297" y1="273" x2="297" y2="275"/>
        <line x1="309" y1="273" x2="309" y2="275"/><line x1="321" y1="273" x2="321" y2="275"/>
        <line x1="333" y1="273" x2="333" y2="275"/><line x1="345" y1="273" x2="345" y2="275"/>
        <line x1="357" y1="273" x2="357" y2="275"/><line x1="369" y1="273" x2="369" y2="275"/>
        <line x1="381" y1="273" x2="381" y2="275"/><line x1="393" y1="273" x2="393" y2="275"/>
        <line x1="405" y1="273" x2="405" y2="275"/><line x1="417" y1="273" x2="417" y2="275"/>
        <line x1="429" y1="273" x2="429" y2="275"/>
      </g>
      <!-- Empirical bars: 9 noisy retained modes — teal with orange noise jitter -->
      <rect x="36"  y="32"  width="10" height="243" rx="2" fill="#2a8585" opacity="0.50"/>
      <rect x="48"  y="68"  width="10" height="207" rx="2" fill="#2a8585" opacity="0.46"/>
      <rect x="60"  y="102" width="10" height="173" rx="2" fill="#2a8585" opacity="0.42"/>
      <rect x="72"  y="135" width="10" height="140" rx="2" fill="#2a8585" opacity="0.38"/>
      <rect x="84"  y="167" width="10" height="108" rx="2" fill="#2a8585" opacity="0.34"/>
      <rect x="96"  y="195" width="10" height="80"  rx="2" fill="#2a8585" opacity="0.30"/>
      <rect x="108" y="220" width="10" height="55"  rx="2" fill="#2a8585" opacity="0.27"/>
      <rect x="120" y="242" width="10" height="33"  rx="2" fill="#2a8585" opacity="0.24"/>
      <rect x="132" y="258" width="10" height="17"  rx="2" fill="#2a8585" opacity="0.21"/>
      <!-- Noise jitter on retained bars -->
      <path d="M 38,28 l 2,-5 l 2,5 l 2,-4 l 2,4" fill="none" stroke="#c4653a" stroke-width="0.9" opacity="0.50"/>
      <path d="M 50,64 l 2,-4 l 2,4 l 2,-3 l 2,3" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.42"/>
      <path d="M 62,98 l 1.5,-3 l 2,3 l 1.5,-3" fill="none" stroke="#c4653a" stroke-width="0.7" opacity="0.35"/>
      <path d="M 74,132 l 1,-2.5 l 1.5,2.5 l 1,-2" fill="none" stroke="#c4653a" stroke-width="0.7" opacity="0.28"/>
      <!-- Dual annotations: noisy retained vs missing -->
      <text x="84" y="20" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#c4653a" font-weight="600" opacity="0.90" font-style="italic">noisy + biased</text>
      <text x="300" y="178" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#666" font-weight="600" opacity="0.85" font-style="italic">missing directions</text>
      <!-- Bracket for missing region -->
      <path d="M 148,284 L 148,289 L 290,289 L 290,294 M 290,289 L 432,289 L 432,284" fill="none" stroke="#5a4e40" stroke-width="1.2" opacity="0.7"/>
      <text x="290" y="308" text-anchor="middle" font-family="-apple-system,'Inter',sans-serif" font-size="16" fill="#5a4e40" font-weight="650">31 zero eigenvalues</text>
      <!-- Rank label under retained bars -->
      <text x="84" y="308" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="16" fill="#2a8585" font-weight="550">rank(Ĉ) ≤ 9</text>
    </g>
  </g>
  </g>
  <g class="fragment" data-fragment-index="1">
  <!-- ARROW 2→3 -->
  <line x1="810" y1="175" x2="850" y2="175" stroke="#8b4513" stroke-width="1.3" marker-end="url(#uc-a)"/>
  <!-- ═══ STAGE 3: OVERCONFIDENCE — true vs ensemble spread ═══ -->
  <g transform="translate(870, 25)">
    <text x="185" y="14" text-anchor="middle" font-family="-apple-system,'Inter',sans-serif" font-size="23" font-weight="640" fill="#2c2418">Overconfident Spread</text>
    <!-- True posterior uncertainty (large faded teal ellipse) -->
    <ellipse cx="185" cy="190" rx="150" ry="122" fill="#2a8585" fill-opacity="0.03" stroke="#2a8585" stroke-width="0.9" stroke-dasharray="5,4" stroke-opacity="0.20"/>
    <!-- Ghost samples: where ensemble SHOULD be sampling -->
    <circle cx="78" cy="125" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="280" cy="135" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="95"  cy="250" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="270" cy="255" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="55"  cy="190" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="310" cy="195" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="140" cy="85"  r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="225" cy="290" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="115" cy="280" r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <circle cx="250" cy="98"  r="4" fill="none" stroke="#2a8585" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.16"/>
    <!-- True posterior label -->
    <text x="185" y="328" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#2a8585" opacity="0.90" font-style="italic" font-weight="600">true posterior</text>
    <!-- Ensemble estimate (tiny orange ellipse — dramatically smaller) -->
    <ellipse cx="185" cy="190" rx="22" ry="16" fill="#c4653a" fill-opacity="0.06" stroke="#c4653a" stroke-width="1.4" stroke-opacity="0.60"/>
    <!-- Tight ensemble dot cluster -->
    <circle cx="178" cy="185" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="188" cy="181" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="195" cy="188" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="182" cy="195" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="190" cy="197" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="175" cy="191" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="185" cy="187" r="3.5" fill="#c4653a" opacity="0.60"/>
    <circle cx="192" cy="193" r="3.5" fill="#c4653a" opacity="0.60"/>
    <!-- Ensemble spread label -->
    <text x="185" y="220" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="17" fill="#c4653a" font-weight="550">ensemble spread</text>
  </g>
  </g>
  <g class="fragment" data-fragment-index="2">
  <!-- ARROW 3→4 -->
  <line x1="1245" y1="175" x2="1285" y2="175" stroke="#8b4513" stroke-width="1.3" marker-end="url(#uc-a)"/>
  <!-- ═══ STAGE 4: CONSEQUENCES — connected to overconfidence ═══ -->
  <g transform="translate(1305, 50)">
    <!-- Weather -->
    <g transform="translate(30, 55)">
      <circle cx="0" cy="0" r="24" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.40"/>
      <path d="M -15,-7 Q 0,-16 15,-7" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.30"/>
      <path d="M -16,1 Q 0,-5 16,1" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.30"/>
      <path d="M -15,9 Q 0,2 15,9" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.30"/>
      <text x="36" y="2" font-family="-apple-system,'Inter',sans-serif" font-size="18" fill="#2c2418" font-weight="560">weather</text>
      <text x="36" y="19" font-family="Charter,Georgia,serif" font-size="14" fill="#6b5d4e" font-style="italic">wrong warning thresholds</text>
    </g>
    <!-- Ocean -->
    <g transform="translate(30, 135)">
      <circle cx="0" cy="0" r="24" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.40"/>
      <path d="M -15,-4 Q -7,-12 0,-4 Q 7,4 15,-4" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.30"/>
      <path d="M -15,5 Q -7,-2 0,5 Q 7,12 15,5" fill="none" stroke="#c4653a" stroke-width="0.8" opacity="0.30"/>
      <text x="36" y="2" font-family="-apple-system,'Inter',sans-serif" font-size="18" fill="#2c2418" font-weight="560">ocean</text>
      <text x="36" y="19" font-family="Charter,Georgia,serif" font-size="14" fill="#6b5d4e" font-style="italic">corrupted reanalysis</text>
    </g>
    <!-- Climate -->
    <g transform="translate(30, 215)">
      <circle cx="0" cy="0" r="24" fill="none" stroke="#c4653a" stroke-width="1" opacity="0.40"/>
      <ellipse cx="0" cy="0" rx="10" ry="24" fill="none" stroke="#c4653a" stroke-width="0.7" opacity="0.25"/>
      <line x1="-24" y1="0" x2="24" y2="0" stroke="#c4653a" stroke-width="0.7" opacity="0.25"/>
      <text x="36" y="2" font-family="-apple-system,'Inter',sans-serif" font-size="18" fill="#2c2418" font-weight="560">climate</text>
      <text x="36" y="19" font-family="Charter,Georgia,serif" font-size="14" fill="#6b5d4e" font-style="italic">biased confidence bands</text>
    </g>
  </g>
  <!-- ═══ CONCLUSION ═══ -->
  <line x1="50" y1="415" x2="1530" y2="415" stroke="#d8d0c4" stroke-width="0.8" stroke-dasharray="5,4"/>
  <text x="790" y="455" text-anchor="middle" font-family="-apple-system,'Inter',sans-serif" font-size="27" font-weight="700" fill="#c4653a" letter-spacing="0.01em">Overconfident ensembles are worse than no uncertainty</text>
  <text x="790" y="488" text-anchor="middle" font-family="Charter,Georgia,serif" font-size="18" fill="#6b5d4e" font-style="italic" letter-spacing="0.01em">n ≫ N   →   rank-deficient covariance   →   systematic overconfidence   →   unreliable decisions</text>
  </g>
</svg>
</div>

<!-- .notes:
Here's the regime I study. In the Lorenz-96 system with 40 state variables, we observe 20 components but have only 10 ensemble members. The empirical covariance has rank at most 9 — that means 31 directions of uncertainty are missing entirely, and the 9 eigenvalues it does retain are corrupted by sampling noise. Look at what this means for uncertainty quantification: the large faded ellipse shows the true posterior — where ensemble members should be sampling. The tiny orange cluster is where they actually are. The filter is 15 times more confident than it should be. This isn't a minor numerical artifact; it's a structural mathematical failure with real consequences — wrong warning thresholds in weather, corrupted reanalysis in ocean modeling, biased confidence bands in climate projections. Overconfident uncertainty isn't just imprecise — it's actively misleading. It's worse than admitting you don't know.
-->

---

## The Stochastic Perturbation Problem

<div>$$\underbrace{\mathbf{x}^{(j),a}}_{\text{analysis}} = \underbrace{\mathbf{x}^{(j),f}}_{\text{forecast}} + \underbrace{\mathbf{K}}_{\text{gain}}\Bigl(\underbrace{\mathbf{z}}_{\text{obs}} + \underbrace{\boldsymbol{\epsilon}^{(j)}}_{\color{#c4653a}{\text{perturbation}}} - \underbrace{\mathbf{H}\mathbf{x}^{(j),f}}_{\text{predicted obs}}\Bigr), \qquad \boldsymbol{\epsilon}^{(j)} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$$</div>

<div class="fragment" data-fragment-index="0">
<div style="display:flex; gap:2em; margin-top:0.5em; align-items:flex-start;">
<div style="flex:1;">
<div style="font-weight:700; color:#1a7a6d; font-size:1.0em; margin-bottom:0.2em;">Why perturb?</div>
<div style="border-left:4px solid #1a7a6d; padding-left:0.8em; font-size:0.92em; line-height:1.55; color:#3a3024;">
Perturbations enforce covariance consistency <strong>in expectation</strong>:<br>
<span>$\mathbb{E}[\hat{\mathbf{P}}^a] = (\mathbf{I} - \mathbf{K}\mathbf{H})\mathbf{P}^f$</span><br>
Without them, analysis covariance collapses.
</div>
</div>
<div style="flex:1.3;">
<div style="font-weight:700; color:#c4653a; font-size:1.0em; margin-bottom:0.2em;">What it costs</div>
<div style="border-left:4px solid #c4653a; padding-left:0.8em; font-size:0.92em; line-height:1.55; color:#3a3024;">
<strong>Irreducible variance:</strong> <span>$\;\mathrm{Var}_{\mathrm{pert}} = \mathcal{O}\!\bigl(\|\mathbf{K}\|^2 \cdot d \,/\, N\bigr)$</span><br>
Scales with observation dimension <span>$d = mL$</span>, inversely with <span>$N$</span><br>
<strong>Non-adaptive:</strong> noise injected uniformly across <em>all</em> <span>$d$</span> directions — no distinction between signal and noise subspaces
</div>
</div>
</div>
</div>

<div class="fragment" data-fragment-index="1" style="margin-top:0.6em; text-align:center; font-size:1.05em; color:#c4653a; font-weight:600; line-height:1.5; max-width:92%; margin-left:auto; margin-right:auto;">The method pays for variance preservation by injecting non-adaptive noise — and that cost scales with dimension, not signal content.</div>

<!-- .notes:
The stochastic EnKF perturbs observations to preserve ensemble covariance — this is correct in expectation, ensuring the analysis covariance matches the Kalman filter result on average. But each realization injects sampling noise through the gain. The variance of this noise scales as K-squared times d over N — it grows with observation dimension and shrinks only with ensemble size. For windowed methods with d equals mL equals 100, this is a substantial floor. Critically, the noise is isotropic in observation space: it does not distinguish signal-dominated directions from noise-dominated directions. Every dimension receives the same perturbation magnitude. This is a geometric mismatch with the problem structure — the few directions carrying real forecast-observation discrepancy are swamped by noise injected into the many directions carrying only sampling artifacts. For small N, this uninformed noise becomes the dominant error source.
-->

---

## Open Problems in Undersampled Ensemble Filtering

<!-- Layer 1: Governing constraint -->
<div style="text-align:center; margin-top:0.15em; margin-bottom:0.2em;">
<div style="display:inline-block; border:2.5px solid #5a4e40; border-radius:6px; padding:0.35em 1.5em; background:#5a4e4008;">
<span style="font-size:1.2em; font-weight:700; color:#2c2418;">rank(<span>$\hat{\mathbf{C}}$</span>) ≤ <span>$N{-}1$</span> ≪ <span>$d$</span></span>
<span style="font-size:1.0em; color:#5a4e40; margin-left:0.8em;">— every filter must regularize</span>
</div>
</div>

<!-- Layer 2: Existing methods -->
<div class="fragment" data-fragment-index="0">
<div style="display:flex; gap:0.8em; margin-top:0.3em; text-align:center;">
<div style="flex:1; border:2px solid #c4653a; border-radius:6px; padding:0.35em 0.4em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.95em; margin-bottom:0.1em;">Stochastic EnKF</div>
<div style="font-size:0.82em; color:#3a3024; line-height:1.35;">isotropic noise in all <span>$d$</span> directions<br><span>$\mathcal{O}(\|\mathbf{K}\|^2 d/N)$</span></div>
</div>
<div style="flex:1; border:2px solid #5a7a9a; border-radius:6px; padding:0.35em 0.4em; background:#5a7a9a08;">
<div style="font-weight:700; color:#5a7a9a; font-size:0.95em; margin-bottom:0.1em;">Square-root filters</div>
<div style="font-size:0.82em; color:#3a3024; line-height:1.35;">no noise, but confined to<br>ensemble subspace; needs inflation</div>
</div>
<div style="flex:1; border:2px solid #8a7e72; border-radius:6px; padding:0.35em 0.4em; background:#8a7e7208;">
<div style="font-weight:700; color:#8a7e72; font-size:0.95em; margin-bottom:0.1em;">Additive inflation</div>
<div style="font-size:0.82em; color:#3a3024; line-height:1.35;">uniform variance scaling<br>spectrally blind</div>
</div>
</div>
<div style="text-align:center; margin-top:0.25em; font-size:0.9em; color:#c4653a; font-weight:600;">Shared weakness: none connect regularization choice to uncertainty calibration</div>
</div>

<!-- Layer 3: The gap -->
<div class="fragment" data-fragment-index="1" style="margin-top:0.35em;">
<div style="border:3px solid #1a7a6d; border-radius:8px; padding:0.45em 1em; background:#1a7a6d0c; text-align:center;">
<div style="font-weight:700; color:#1a7a6d; font-size:1.15em; margin-bottom:0.25em; letter-spacing:0.02em;">THE GAP — no spectral-calibration theory</div>
<div style="display:flex; gap:1.2em; justify-content:center; font-size:0.92em; color:#3a3024; line-height:1.45;">
<div style="border-left:4px solid #1a7a6d; padding-left:0.6em; text-align:left;"><strong>How does <span>$\kappa$</span> control MSE?</strong><br><span style="font-size:0.88em; color:#5a4e40;">spectral truncation ↔ bias-variance</span></div>
<div style="border-left:4px solid #1a7a6d; padding-left:0.6em; text-align:left;"><strong>When does <span>$\kappa$</span> yield calibrated spread?</strong><br><span style="font-size:0.88em; color:#5a4e40;">truncation rank ↔ calibration</span></div>
<div style="border-left:4px solid #1a7a6d; padding-left:0.6em; text-align:left;"><strong>Signal-aware filter?</strong><br><span style="font-size:0.88em; color:#5a4e40;">directional, inflation-free design</span></div>
</div>
</div>
</div>

<!-- Layer 4: Research question -->
<div class="fragment" data-fragment-index="2" style="margin-top:0.5em; text-align:center; max-width:94%; margin-left:auto; margin-right:auto;">
<div style="border-top:2px solid #2c2418; padding-top:0.35em; font-size:1.1em; color:#2c2418; font-weight:700; line-height:1.45;">Under what conditions does observation-space spectral truncation yield calibrated ensemble spread — and how does <span>$\kappa$</span> govern the bias-variance tradeoff when <span>$N \ll d$</span>?</div>
</div>

<!-- .notes:
This slide maps the landscape and isolates the gap. The top constraint is the governing reality: rank deficiency forces every filter to regularize. The three methods each impose a different regularization. Stochastic EnKF adds isotropic noise scaling with d over N. Square-root filters avoid noise but require inflation to prevent collapse. Additive inflation uniformly scales variance. The shared weakness: none of these methods come with a theory connecting their regularization to calibration. Stochastic EnKF and inflation are spectrally isotropic — they treat every direction identically. Square-root filters preserve subspace structure but are confined to the ensemble span and still require isotropic inflation to survive. The green box is the gap: no existing theory connects spectral truncation to calibration. Three specific pieces are missing: a bias-variance decomposition for truncation rank kappa, a theoretical result linking kappa to spread-skill ratio, and a practical filter that exploits spectral structure without inflation or perturbations. The research question is precise: under what conditions does spectral truncation yield calibrated spread, and how does kappa govern the tradeoff. The rest of the talk answers this.
-->

---

<!-- ============================================================ -->
<!-- SECTION 2: METHOD (Slides 8-14) -->
<!-- ============================================================ -->

## QPCA-EnDCF: Core Idea

<div style="text-align:center; margin-top:0.1em; margin-bottom:0.3em;">
<span style="font-size:1.05em; font-weight:700; color:#2c2418;">Replace stochastic perturbations with </span><span style="font-size:1.05em; font-weight:700; color:#1a7a6d;">deterministic spectral projection</span>
</div>

<svg viewBox="0 0 1100 335" style="width:100%; max-height:65vh; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ci-ar" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#1a7a6d"/></marker>
  </defs>
  <!-- ══ STAGE 1: WHITEN ══ -->
  <rect x="20" y="30" width="300" height="240" rx="8" fill="#1a7a6d06" stroke="#1a7a6d" stroke-width="1.5"/>
  <text x="170" y="55" text-anchor="middle" fill="#1a7a6d" font-size="18" font-weight="700" font-family="-apple-system,sans-serif">1. WHITEN</text>
  <!-- Anisotropic ellipse → circle -->
  <ellipse cx="110" cy="150" rx="65" ry="28" fill="#c4653a" fill-opacity="0.06" stroke="#c4653a" stroke-width="1.2" opacity="0.5" transform="rotate(-20 110 150)"/>
  <circle cx="95" cy="142" r="3" fill="#c4653a" opacity="0.5"/>
  <circle cx="110" cy="150" r="3.5" fill="#c4653a" opacity="0.5"/>
  <circle cx="125" cy="157" r="3" fill="#c4653a" opacity="0.5"/>
  <circle cx="100" cy="162" r="3" fill="#c4653a" opacity="0.5"/>
  <text x="110" y="208" text-anchor="middle" fill="#5a4e40" font-size="13" font-weight="600">Cov(noise) = R</text>
  <!-- Arrow -->
  <line x1="178" y1="150" x2="210" y2="150" stroke="#5a4e40" stroke-width="1.8" marker-end="url(#ci-ar)"/>
  <!-- Isotropic circle -->
  <circle cx="260" cy="150" r="42" fill="#1a7a6d" fill-opacity="0.04" stroke="#1a7a6d" stroke-width="1.2" opacity="0.5"/>
  <circle cx="248" cy="138" r="3" fill="#1a7a6d" opacity="0.6"/>
  <circle cx="260" cy="150" r="3.5" fill="#1a7a6d" opacity="0.6"/>
  <circle cx="272" cy="160" r="3" fill="#1a7a6d" opacity="0.6"/>
  <circle cx="252" cy="165" r="3" fill="#1a7a6d" opacity="0.6"/>
  <text x="260" y="208" text-anchor="middle" fill="#5a4e40" font-size="13" font-weight="600">Cov(noise) = I</text>
  <text x="170" y="240" text-anchor="middle" fill="#3a3024" font-size="14" font-weight="600" font-family="-apple-system,sans-serif">Remove noise geometry</text>
  <text x="170" y="258" text-anchor="middle" fill="#3a3024" font-size="12" font-weight="600" font-family="Georgia,serif" font-style="italic">remaining structure = real mismatch</text>
  <!-- ══ CONNECTOR 1→2 ══ -->
  <line x1="330" y1="155" x2="390" y2="155" stroke="#1a7a6d" stroke-width="2.0" marker-end="url(#ci-ar)"/>
  <!-- ══ STAGE 2: PCA ══ -->
  <rect x="400" y="30" width="300" height="240" rx="8" fill="#1a7a6d08" stroke="#1a7a6d" stroke-width="1.5"/>
  <text x="550" y="55" text-anchor="middle" fill="#1a7a6d" font-size="18" font-weight="700" font-family="-apple-system,sans-serif">2. SPECTRAL DECOMPOSITION</text>
  <!-- Circle with dominant axis -->
  <circle cx="550" cy="150" r="50" fill="#1a7a6d" fill-opacity="0.03" stroke="#1a7a6d" stroke-width="0.8" opacity="0.35"/>
  <!-- Leading eigenmode — bold line -->
  <line x1="490" y1="175" x2="610" y2="125" stroke="#1a7a6d" stroke-width="2.5" opacity="0.7"/>
  <text x="618" y="122" fill="#1a7a6d" font-size="12" font-weight="700" font-family="Georgia,serif">v̂₁</text>
  <!-- Noise mode — thin dashed -->
  <line x1="525" y1="100" x2="575" y2="200" stroke="#999" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.4"/>
  <text x="580" y="205" fill="#5a4e40" font-size="11" font-weight="600" font-family="Georgia,serif" font-style="italic">noise</text>
  <!-- Dots along signal direction -->
  <circle cx="510" cy="166" r="3.5" fill="#1a7a6d" opacity="0.65"/>
  <circle cx="530" cy="158" r="3.5" fill="#1a7a6d" opacity="0.65"/>
  <circle cx="555" cy="148" r="3.5" fill="#1a7a6d" opacity="0.65"/>
  <circle cx="575" cy="140" r="3.5" fill="#1a7a6d" opacity="0.65"/>
  <circle cx="595" cy="132" r="3.5" fill="#1a7a6d" opacity="0.65"/>
  <text x="550" y="228" text-anchor="middle" fill="#3a3024" font-size="14" font-weight="600" font-family="-apple-system,sans-serif">Extract dominant mismatch via PCA</text>
  <text x="550" y="244" text-anchor="middle" fill="#3a3024" font-size="12" font-weight="600" font-family="Georgia,serif" font-style="italic">eigenspectrum separates signal from noise</text>
  <!-- ══ CONNECTOR 2→3 ══ -->
  <line x1="710" y1="155" x2="770" y2="155" stroke="#1a7a6d" stroke-width="2.0" marker-end="url(#ci-ar)"/>
  <!-- ══ STAGE 3: CORRECT ══ -->
  <defs><marker id="ci-or" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#c4653a"/></marker></defs>
  <rect x="780" y="30" width="300" height="240" rx="8" fill="#1a7a6d0c" stroke="#1a7a6d" stroke-width="2.0"/>
  <text x="930" y="55" text-anchor="middle" fill="#1a7a6d" font-size="18" font-weight="700" font-family="-apple-system,sans-serif">3. CORRECT</text>
  <!-- v-perp axis -->
  <line x1="930" y1="75" x2="930" y2="215" stroke="#c8c0b4" stroke-width="0.7"/>
  <!-- Signal axis highlighted -->
  <rect x="830" y="148" width="200" height="10" rx="1" fill="#1a7a6d" fill-opacity="0.08"/>
  <line x1="830" y1="153" x2="1030" y2="153" stroke="#1a7a6d" stroke-width="1.5" opacity="0.4"/>
  <text x="1038" y="150" fill="#1a7a6d" font-size="11" font-weight="700">v̂₁</text>
  <!-- Residual vector -->
  <circle cx="930" cy="153" r="3" fill="#5a4e40" opacity="0.5"/>
  <line x1="930" y1="153" x2="1000" y2="100" stroke="#5a4e40" stroke-width="1.8" opacity="0.5"/>
  <!-- Projection along signal -->
  <line x1="930" y1="153" x2="1000" y2="153" stroke="#1a7a6d" stroke-width="2.2" opacity="0.6"/>
  <!-- Orthogonal drop -->
  <line x1="1000" y1="153" x2="1000" y2="100" stroke="#999" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.45"/>
  <!-- Correction arrow (reversed) -->
  <line x1="998" y1="170" x2="938" y2="170" stroke="#c4653a" stroke-width="2.8" marker-end="url(#ci-or)"/>
  <text x="968" y="188" text-anchor="middle" fill="#c4653a" font-size="12" font-weight="700">correction</text>
  <!-- "no update" labels -->
  <text x="860" y="90" fill="#5a4e40" font-size="12" font-weight="600" font-family="-apple-system,sans-serif">v⊥: no update</text>
  <text x="860" y="104" fill="#3a3024" font-size="11" font-weight="600" font-family="Georgia,serif" font-style="italic">diversity preserved</text>
  <text x="930" y="240" text-anchor="middle" fill="#3a3024" font-size="14" font-weight="600" font-family="-apple-system,sans-serif">Signal corrected, noise untouched</text>
  <text x="930" y="258" text-anchor="middle" fill="#3a3024" font-size="12" font-weight="600" font-family="Georgia,serif" font-style="italic">no perturbation noise injected</text>
  <!-- ══ BOTTOM BAR ══ -->
  <rect x="20" y="290" width="1060" height="36" rx="5" fill="#1a7a6d0a" stroke="#1a7a6d" stroke-width="1.0"/>
  <text x="550" y="314" text-anchor="middle" fill="#1a7a6d" font-size="15" font-weight="700" font-family="-apple-system,sans-serif">No random perturbations  ·  No inflation  ·  Fully deterministic  ·  Subspace-aware</text>
</svg>

<!-- .notes:
QPCA-EnDCF is a three-stage deterministic pipeline. Whiten: normalize residuals so noise becomes isotropic — remaining structure is real mismatch. Decompose: eigendecompose to find the dominant direction of forecast-observation discrepancy. Correct: update only along that signal direction; leave everything else untouched. No perturbation noise. No inflation. The key property: corrections are confined to the signal subspace, preserving ensemble diversity in all other directions. Let me walk through each stage.
-->

---

## Stage 1: Whitening

<div style="position:relative;">
<svg viewBox="0 0 1050 310" style="width:100%; max-height:68vh; display:block; margin:0.1em auto 0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="w-ar" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#5a4e40"/></marker>
  </defs>
  <!-- ══ BEFORE: anisotropic ══ -->
  <text x="180" y="28" text-anchor="middle" fill="#c4653a" font-size="17" font-weight="700" font-family="-apple-system,sans-serif">Before whitening</text>
  <!-- Noise ellipse (anisotropic) -->
  <ellipse cx="180" cy="175" rx="140" ry="60" fill="#c4653a" fill-opacity="0.06" stroke="#c4653a" stroke-width="1.2" stroke-dasharray="5,3" stroke-opacity="0.5" transform="rotate(-20 180 175)"/>
  <!-- Ensemble dots scattered along ellipse -->
  <circle cx="100" cy="155" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="130" cy="135" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="160" cy="148" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="195" cy="165" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="220" cy="180" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="250" cy="195" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="150" cy="185" r="4.5" fill="#c4653a" opacity="0.6"/>
  <circle cx="210" cy="155" r="4.5" fill="#c4653a" opacity="0.6"/>
  <!-- Labels -->
  <!-- Cov label rendered via MathJax overlay -->
  <text x="180" y="288" text-anchor="middle" fill="#3a3024" font-size="13" font-weight="600" font-family="Georgia,serif" font-style="italic">anisotropic noise</text>
  <text x="180" y="306" text-anchor="middle" fill="#5a4e40" font-size="12" font-weight="600" font-family="Georgia,serif" font-style="italic">direction-dependent variance</text>
  <!-- ══ ARROW: whitening transform ══ -->
  <line x1="340" y1="175" x2="430" y2="175" stroke="#5a4e40" stroke-width="1.8" marker-end="url(#w-ar)"/>
  <rect x="348" y="128" width="78" height="32" rx="4" fill="#f5f0eb" stroke="#5a4e40" stroke-width="0.8"/>
  <!-- R^{-1/2} rendered via MathJax overlay -->
  <!-- ══ AFTER: isotropic ══ -->
  <text x="590" y="28" text-anchor="middle" fill="#1a7a6d" font-size="17" font-weight="700" font-family="-apple-system,sans-serif">After whitening</text>
  <!-- Noise circle (isotropic) -->
  <circle cx="590" cy="175" r="90" fill="#1a7a6d" fill-opacity="0.04" stroke="#1a7a6d" stroke-width="1.2" stroke-dasharray="5,3" stroke-opacity="0.4"/>
  <!-- Signal structure visible: elongated cluster along one direction -->
  <ellipse cx="590" cy="175" rx="75" ry="25" fill="#1a7a6d" fill-opacity="0.08" stroke="#1a7a6d" stroke-width="1.0" stroke-opacity="0.35" transform="rotate(-15 590 175)"/>
  <!-- Ensemble dots along signal direction -->
  <circle cx="530" cy="190" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="555" cy="182" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="575" cy="170" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="600" cy="168" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="620" cy="160" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="645" cy="155" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="560" cy="195" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <circle cx="615" cy="178" r="4.5" fill="#1a7a6d" opacity="0.7"/>
  <!-- Labels -->
  <text x="590" y="288" text-anchor="middle" fill="#1a7a6d" font-size="14" font-weight="600" font-family="Georgia,serif">Cov(ε) = I</text>
  <text x="590" y="306" text-anchor="middle" fill="#3a3024" font-size="13" font-weight="600" font-family="Georgia,serif" font-style="italic">isotropic noise — signal structure visible</text>
  <!-- Signal direction arrow -->
  <line x1="520" y1="195" x2="658" y2="152" stroke="#1a7a6d" stroke-width="1.0" stroke-dasharray="3,2" opacity="0.4"/>
  <text x="670" y="145" fill="#1a7a6d" font-size="11" font-weight="600" font-family="Georgia,serif" opacity="0.7">signal</text>
  <!-- ══ ARROW: to spectrum ══ -->
  <line x1="720" y1="175" x2="790" y2="175" stroke="#5a4e40" stroke-width="1.8" marker-end="url(#w-ar)"/>
  <!-- ══ SPECTRAL IMPLICATION ══ -->
  <text x="920" y="28" text-anchor="middle" fill="#5a4e40" font-size="17" font-weight="700" font-family="-apple-system,sans-serif">Spectral implication</text>
  <!-- Mini eigenspectrum -->
  <line x1="830" y1="60" x2="830" y2="260" stroke="#5a4e40" stroke-width="0.8"/>
  <line x1="828" y1="260" x2="1020" y2="260" stroke="#5a4e40" stroke-width="0.8"/>
  <text x="815" y="165" text-anchor="middle" fill="#3a3024" font-size="12" font-weight="600" font-style="italic" font-family="Georgia,serif" transform="rotate(-90 815 165)">eigenvalue λᵢ</text>
  <text x="925" y="275" text-anchor="middle" fill="#3a3024" font-size="11" font-weight="600" font-style="italic" font-family="Georgia,serif">mode index i</text>
  <!-- Noise floor line at 1 -->
  <line x1="830" y1="225" x2="1020" y2="225" stroke="#c4653a" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.6"/>
  <text x="1030" y="229" fill="#c4653a" font-size="11" font-family="Georgia,serif">λ = 1</text>
  <!-- Bars above noise floor = signal -->
  <rect x="848" y="75" width="20" height="185" rx="2" fill="#1a7a6d" opacity="0.65"/>
  <rect x="878" y="150" width="20" height="110" rx="2" fill="#1a7a6d" opacity="0.50"/>
  <!-- Bars at noise floor -->
  <rect x="908" y="232" width="16" height="28" rx="2" fill="#999" opacity="0.30"/>
  <rect x="930" y="238" width="16" height="22" rx="2" fill="#999" opacity="0.25"/>
  <rect x="952" y="244" width="16" height="16" rx="2" fill="#999" opacity="0.22"/>
  <rect x="974" y="248" width="16" height="12" rx="2" fill="#999" opacity="0.18"/>
  <!-- Labels on mini spectrum -->
  <text x="858" y="68" text-anchor="middle" fill="#1a7a6d" font-size="11" font-weight="700">λ₁</text>
  <text x="888" y="143" text-anchor="middle" fill="#1a7a6d" font-size="11" font-weight="700">λ₂</text>
  <text x="868" y="295" text-anchor="middle" fill="#1a7a6d" font-size="12" font-weight="600">signal</text>
  <text x="868" y="308" text-anchor="middle" fill="#1a7a6d" font-size="10" font-style="italic">(λ > 1)</text>
  <text x="970" y="295" text-anchor="middle" fill="#5a4e40" font-size="12" font-weight="600">noise</text>
  <text x="970" y="308" text-anchor="middle" fill="#5a4e40" font-size="10" font-style="italic">(λ ≈ 1)</text>
</svg>
<div style="position:absolute; top:82%; left:22%; transform:translate(-50%,0); pointer-events:none; font-size:0.5em; color:#c4653a; font-weight:600;"><span>$\operatorname{Cov}(\boldsymbol{\varepsilon}) = \mathbf{R}^{(L)}$</span></div>
<div style="position:absolute; top:47%; left:40%; transform:translate(-50%,-50%); pointer-events:none; font-size:0.45em; color:#5a4e40; font-weight:700;"><span>$\mathbf{R}^{-1/2}$</span></div>
</div>

<div style="text-align:center; margin-top:2.5em; padding:0.35em 1em; border-radius:5px; background:#f5f0eb; border:1px solid #d0c8bc; display:inline-block; margin-left:auto; margin-right:auto; width:fit-content; font-size:0.95em; color:#3a3024;">
<span>$\mathbf{E} = (\mathbf{R}^{(L)})^{-1/2}(\mathbf{Z}^{(w)} - \mathbf{z}^{(w)}\mathbf{1}^\top)$</span>
<span style="margin:0 0.8em; color:#5a4e40;">→</span> noise isotropic
<span style="margin:0 0.8em; color:#5a4e40;">→</span> eigenvalues separate signal from noise
</div>

<div style="text-align:center; margin-top:1.2em; font-size:0.92em; color:#2c2418; font-weight:600;">Whitening makes the spectrum interpretable: <span>$\hat{\lambda}_i > 1$</span> = signal, <span>$\hat{\lambda}_i \approx 1$</span> = noise</div>

<!-- .notes:
Stage 1 transforms raw residuals so PCA becomes statistically meaningful. Before whitening, observation errors have covariance R-L — anisotropic, meaning different directions carry different noise magnitudes. The left panel shows this: residuals form an elongated cloud whose shape reflects noise geometry, not signal. After multiplying by R-inverse-half, noise covariance becomes the identity — isotropic. Now the cloud's shape reflects genuine forecast-observation mismatch, not noise artifacts. The right panel shows the spectral consequence: in whitened space, unit eigenvalue corresponds exactly to the noise floor. Any eigenvalue exceeding one is real signal — coherent dynamical mismatch the ensemble has not captured. Without whitening, large eigenvalues could simply reflect large observation error variances. This is why whitening is not optional: it is what gives the spectral decomposition in Stage 2 its discriminating power.
-->

---

## Stage 2: Spectral Decomposition

<div style="display:flex; gap:1.5em; align-items:flex-start; margin-top:0.1em;">
<div style="flex:1.4;">
<svg viewBox="0 0 520 380" style="width:100%;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sd-sig" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a7a6d" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#1a7a6d" stop-opacity="0.03"/>
    </linearGradient>
    <linearGradient id="sd-noi" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#999" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#999" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <!-- Axes -->
  <line x1="60" y1="20" x2="60" y2="310" stroke="#5a4e40" stroke-width="1.0"/>
  <line x1="58" y1="310" x2="500" y2="310" stroke="#5a4e40" stroke-width="1.0"/>
  <text x="30" y="170" text-anchor="middle" fill="#5a4e40" font-size="15" font-style="italic" font-family="Georgia,serif" transform="rotate(-90 30 170)">eigenvalue  λᵢ</text>
  <text x="280" y="342" text-anchor="middle" fill="#5a4e40" font-size="14" font-family="Georgia,serif">mode index  i</text>
  <!-- Signal region background -->
  <rect x="60" y="20" width="115" height="290" fill="url(#sd-sig)" rx="2"/>
  <!-- Noise region background -->
  <rect x="175" y="20" width="325" height="290" fill="url(#sd-noi)" rx="2"/>
  <!-- Truncation line κ -->
  <line x1="175" y1="18" x2="175" y2="316" stroke="#c4653a" stroke-width="1.8" stroke-dasharray="6,4"/>
  <text x="175" y="358" text-anchor="middle" fill="#c4653a" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">κ = truncation</text>
  <!-- Bars: signal modes (1-3) -->
  <rect x="78" y="42" width="22" height="268" rx="3" fill="#1a7a6d" opacity="0.70"/>
  <rect x="108" y="118" width="22" height="192" rx="3" fill="#1a7a6d" opacity="0.58"/>
  <rect x="138" y="198" width="22" height="112" rx="3" fill="#1a7a6d" opacity="0.46"/>
  <!-- Bars: noise modes (4-9) -->
  <rect x="188" y="268" width="18" height="42" rx="2" fill="#999" opacity="0.35"/>
  <rect x="216" y="278" width="18" height="32" rx="2" fill="#999" opacity="0.30"/>
  <rect x="244" y="285" width="18" height="25" rx="2" fill="#999" opacity="0.25"/>
  <rect x="272" y="290" width="18" height="20" rx="2" fill="#999" opacity="0.22"/>
  <rect x="300" y="294" width="18" height="16" rx="2" fill="#999" opacity="0.20"/>
  <rect x="328" y="297" width="18" height="13" rx="2" fill="#999" opacity="0.18"/>
  <!-- Zero modes (10+) — tick marks -->
  <line x1="360" y1="308" x2="360" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="378" y1="308" x2="378" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="396" y1="308" x2="396" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="414" y1="308" x2="414" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="432" y1="308" x2="432" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="450" y1="308" x2="450" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="468" y1="308" x2="468" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <line x1="486" y1="308" x2="486" y2="310" stroke="#aaa" stroke-width="1.0" opacity="0.5"/>
  <!-- Decay envelope curve -->
  <path d="M 89,40 C 120,95 145,170 159,200 C 180,255 210,275 250,290 C 300,302 380,308 490,310" fill="none" stroke="#5a4e40" stroke-width="1.2" stroke-dasharray="4,3" opacity="0.4"/>
  <!-- Region labels -->
  <text x="118" y="36" text-anchor="middle" fill="#1a7a6d" font-size="13" font-weight="700" font-family="-apple-system,sans-serif">SIGNAL</text>
  <text x="340" y="260" text-anchor="middle" fill="#666" font-size="13" font-weight="600" font-family="-apple-system,sans-serif">NOISE FLOOR</text>
  <text x="340" y="274" text-anchor="middle" fill="#888" font-size="11" font-family="Georgia,serif" font-style="italic">sampling artifacts</text>
  <!-- Bar labels -->
  <text x="89" y="38" text-anchor="middle" fill="#1a7a6d" font-size="10" font-weight="600">λ₁</text>
  <text x="119" y="114" text-anchor="middle" fill="#1a7a6d" font-size="10" font-weight="600">λ₂</text>
  <text x="149" y="194" text-anchor="middle" fill="#1a7a6d" font-size="10" font-weight="600">λ₃</text>
  <!-- Zero label -->
  <text x="425" y="340" text-anchor="middle" fill="#6b5d4e" font-size="11" font-family="-apple-system,'Inter','Segoe UI',Helvetica,sans-serif">rank 0 beyond r = min(d, N−1)</text>
  <!-- 60-80% annotation -->
  <path d="M 78,316 L 78,328 L 160,328 L 160,316" fill="none" stroke="#1a7a6d" stroke-width="0.8" opacity="0.6"/>
  <text x="119" y="344" text-anchor="middle" fill="#1a7a6d" font-size="10" font-weight="600" font-family="-apple-system,sans-serif">60–80% of total variance</text>
</svg>
</div>
<div style="flex:0.8; padding-top:0.3em;">

<div>$$\mathbf{C}_E = \sum_{i=1}^{r} \hat{\lambda}_i \,\hat{\mathbf{v}}_i \hat{\mathbf{v}}_i^\top$$</div>

- Each <span>$\hat{\lambda}_i$</span>: energy in mode <span>$\hat{\mathbf{v}}_i$</span>
- Large <span>$\hat{\lambda}_i$</span>: dynamical mismatch
- Small <span>$\hat{\lambda}_i$</span>: sampling noise
- Rank <span>$r = \min(d, N{-}1)$</span>

**Retain only <span>$\kappa$</span> leading modes — discard the noise floor**

</div>
</div>

<!-- .notes:
Stage 2 decomposes the whitened residual covariance spectrally. The plot on the left shows the eigenspectrum — eigenvalues lambda-i plotted against mode index. The key observation is rapid spectral decay: the first one to three eigenvalues capture 60 to 80 percent of total residual variance. These large eigenvalues correspond to coherent dynamical mismatch between forecast and observations — directions where the ensemble is systematically wrong. Beyond those few dominant modes, eigenvalues drop to a noise floor — these are sampling artifacts from finite ensemble size, not real forecast-observation discrepancies. The dashed line at kappa marks the truncation point. We retain only the leading kappa eigenvectors — the signal subspace — and discard everything below. This is justified because the discarded modes carry sampling noise, not information. The rank of the sample covariance is at most min of d and N minus 1, so with N equals 10, we have at most 9 nonzero eigenvalues in a d equals 100 dimensional space. The rapid decay means aggressive truncation to kappa equals 1 preserves the dominant signal while eliminating the noise that would corrupt the update.
-->

---

## Stage 3: Truncated Correction

<div style="display:flex; gap:1.5em; align-items:flex-start; margin-top:0.1em;">
<div style="flex:1.3;">
<svg viewBox="0 0 560 390" style="width:100%;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="tc-ar" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#5a4e40"/></marker>
    <marker id="tc-tl" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1a7a6d"/></marker>
    <marker id="tc-or" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#c4653a"/></marker>
  </defs>
  <!-- ══ κ = 1 label ══ -->
  <rect x="430" y="18" width="110" height="26" rx="4" fill="#c4653a" fill-opacity="0.10" stroke="#c4653a" stroke-width="1.0"/>
  <text x="485" y="36" text-anchor="middle" fill="#c4653a" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">κ = 1 mode</text>
  <!-- ══ COORDINATE SYSTEM ══ -->
  <!-- v-perp axis (vertical) -->
  <line x1="160" y1="30" x2="160" y2="350" stroke="#c8c0b4" stroke-width="0.8"/>
  <text x="170" y="38" fill="#6b5d4e" font-size="14" font-family="Georgia,serif" font-style="italic">v⊥</text>
  <!-- v1 signal axis (horizontal) — highlighted band -->
  <rect x="20" y="188" width="520" height="14" rx="1" fill="#1a7a6d" fill-opacity="0.06"/>
  <line x1="20" y1="195" x2="540" y2="195" stroke="#1a7a6d" stroke-width="1.4" opacity="0.4"/>
  <text x="530" y="190" fill="#1a7a6d" font-size="14" font-weight="700" font-family="Georgia,serif">v̂₁</text>
  <text x="530" y="206" fill="#1a7a6d" font-size="12" font-family="-apple-system,sans-serif">signal</text>
  <!-- ══ RESIDUAL VECTOR E ══ -->
  <circle cx="160" cy="195" r="5" fill="#5a4e40" opacity="0.5"/>
  <line x1="160" y1="195" x2="390" y2="85" stroke="#5a4e40" stroke-width="2.2" marker-end="url(#tc-ar)"/>
  <text x="305" y="118" fill="#5a4e40" font-size="16" font-weight="700" font-family="Georgia,serif">E</text>
  <text x="305" y="135" fill="#5a4e40" font-size="12" font-family="Georgia,serif" font-style="italic">whitened residual</text>
  <!-- ══ PROJECTION: parallel component along v1 ══ -->
  <line x1="160" y1="195" x2="390" y2="195" stroke="#1a7a6d" stroke-width="2.8" marker-end="url(#tc-tl)"/>
  <!-- Right-angle marker at projection foot -->
  <rect x="382" y="187" width="8" height="8" fill="none" stroke="#5a4e40" stroke-width="0.8"/>
  <!-- ══ ORTHOGONAL component (vertical dashed) ══ -->
  <line x1="390" y1="195" x2="390" y2="85" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="416" y="138" fill="#6b5d4e" font-size="14" font-weight="600" font-family="Georgia,serif">E⊥</text>
  <text x="416" y="154" fill="#6b5d4e" font-size="12" font-family="Georgia,serif" font-style="italic">unchanged</text>
  <!-- Projection label below signal axis -->
  <text x="280" y="222" text-anchor="middle" fill="#1a7a6d" font-size="14" font-weight="700" font-family="Georgia,serif">signal projection</text>
  <!-- ══ CORRECTION ARROW (reversed, from projection tip back to origin, offset below) ══ -->
  <line x1="385" y1="250" x2="168" y2="250" stroke="#c4653a" stroke-width="3.0" marker-end="url(#tc-or)"/>
  <text x="280" y="245" text-anchor="middle" fill="#c4653a" font-size="15" font-weight="700" font-family="-apple-system,sans-serif">CORRECTION  =  −projection</text>
  <text x="280" y="275" text-anchor="middle" fill="#c4653a" font-size="13" font-family="Georgia,serif" font-style="italic">push members toward observations</text>
  <!-- ══ "NO UPDATE" annotations — on v⊥ axis, darker ══ -->
  <text x="50" y="72" fill="#6b5d4e" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">v⊥: no update</text>
  <text x="50" y="90" fill="#6b5d4e" font-size="12" font-family="Georgia,serif" font-style="italic">no noise injected</text>
  <line x1="90" y1="94" x2="155" y2="130" stroke="#999" stroke-width="0.7" stroke-dasharray="3,3"/>
  <text x="50" y="316" fill="#6b5d4e" font-size="14" font-weight="700" font-family="-apple-system,sans-serif">v⊥: preserved</text>
  <text x="50" y="334" fill="#6b5d4e" font-size="12" font-family="Georgia,serif" font-style="italic">ensemble diversity intact</text>
  <line x1="90" y1="300" x2="155" y2="260" stroke="#999" stroke-width="0.7" stroke-dasharray="3,3"/>
</svg>
<div style="margin-top:0.3em; padding:0.25em 0.6em; border-radius:4px; background:#f5f0eb; border:1px solid #d0c8bc; text-align:center; font-size:0.75em; color:#5a4e40;">
<span>$\mathbf{E}$</span> → project onto <span>$\hat{\mathbf{v}}_1$</span> → negate (correct) → unwhiten → update <span>$\mathbf{X}$</span>
</div>
</div>
<div style="flex:0.7; padding-top:0.5em;">

<div>$$\mathbf{Q}_{\mathrm{PCA}} = -\hat{\mathbf{V}}_\kappa \hat{\mathbf{V}}_\kappa^\top \mathbf{E}$$</div>

<div>$$\boldsymbol{\Delta}_{\mathrm{obs}} = (\mathbf{R}^{(L)})^{1/2} \mathbf{Q}_{\mathrm{PCA}}$$</div>

<div>$$\mathbf{X}_{k_w}^a = \mathbf{X}_{k_w}^f + \mathbf{K}^{\mathrm{DC}} \boldsymbol{\Delta}_{\mathrm{obs}}$$</div>

- <span>$\kappa = 1$</span> in all experiments
- **Signal:** correct along <span>$\hat{\mathbf{v}}_1$</span>
- **Orthogonal:** no correction, no noise

</div>
</div>

<!-- .notes:
Stage 3 is the correction step — and it is surgical. The diagram shows a whitened residual vector E decomposed into two components: the projection onto the leading eigenvector v-hat-1 — the signal direction — and the orthogonal remainder. The teal arrow along v-hat-1 is the signal component. We correct only along this direction: Q-PCA equals minus the projection of E onto the leading kappa eigenvectors. The negative sign pushes ensemble members toward the observations. The orange correction arrow shows this reversal. The orthogonal component — everything perpendicular to the signal subspace — receives no correction and no noise injection. This is the key geometric insight: ensemble diversity in noise directions is preserved exactly. We then unwhiten by multiplying by R-to-the-half to get observation-space increments, and apply the data-consistent gain K-DC to map back to state space. In all experiments kappa equals 1 — a single mode captures the dominant mismatch.
-->

---

## QPCA-EnDCF: Computational Pipeline

<div style="display:flex; align-items:stretch; gap:0; width:100%; font-size:0.52em; line-height:1.45;">
<div style="flex:0.8; text-align:center; padding:0 0.12em; opacity:0.85;">
<div style="color:#5a4e40; font-weight:700; font-size:1.1em; margin-bottom:0.25em;">FORECAST</div>
<div style="border:1.5px solid #8a7e72; border-radius:5px; padding:0.35em; margin:0.1em 0;">
<span>$\mathbf{x}^{(j)} \leftarrow \mathcal{M}(\mathbf{x}^{(j)})$</span><br>
<span>$\mathbf{Y}_k = \mathbf{H}\mathbf{X}_k$</span><br>
Stack → <span>$\mathbf{Z}^{(w)} \in \mathbb{R}^{d \times N}$</span>
</div>
<div style="color:#999; font-size:0.85em; margin-top:0.15em;">generate residuals</div>
</div>
<div style="display:flex; align-items:center; color:#1a7a6d; font-size:2em; padding:0 0.06em;">→</div>
<div style="flex:1.1; text-align:center; padding:0 0.12em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.25em;">WHITEN</div>
<div style="border:2px solid #1a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;">
<span>$\mathbf{D} = \mathbf{Z}^{(w)} - \mathbf{z}^{(w)}\mathbf{1}^\top$</span><br>
<strong><span>$\mathbf{E} = (\mathbf{R}^{(L)})^{-1/2}\mathbf{D}$</span></strong><br>
<span>$\mathbf{E}_c = \mathbf{E} - \tfrac{1}{N}(\mathbf{E}\mathbf{1})\mathbf{1}^\top$</span>
</div>
<div style="color:#1a7a6d; font-size:0.85em; font-weight:600; margin-top:0.15em;">fix geometry: Cov(noise) → I</div>
</div>
<div style="display:flex; align-items:center; color:#1a7a6d; font-size:2em; padding:0 0.06em;">→</div>
<div style="flex:1; text-align:center; padding:0 0.12em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.25em;">EXTRACT</div>
<div style="border:2px solid #1a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;">
<span>$\mathbf{C}_E = \tfrac{1}{N{-}1}\mathbf{E}_c\mathbf{E}_c^\top$</span><br>
<strong><span>$\hat{\mathbf{V}}_\kappa = [\hat{\mathbf{v}}_1,\ldots,\hat{\mathbf{v}}_\kappa]$</span></strong>
</div>
<div style="color:#1a7a6d; font-size:0.85em; font-weight:600; margin-top:0.15em;">identify signal subspace (<span>$\kappa \ll d$</span>)</div>
</div>
<div style="display:flex; align-items:center; color:#1a7a6d; font-size:2em; padding:0 0.06em;">→</div>
<div style="flex:1.1; text-align:center; padding:0 0.12em;">
<div style="color:#1a7a6d; font-weight:700; font-size:1.15em; margin-bottom:0.25em;">PROJECT</div>
<div style="border:2px solid #1a7a6d; border-radius:5px; padding:0.4em; margin:0.1em 0; background:#f0f7f5;">
<strong><span>$\mathbf{Q}_{\mathrm{PCA}} = -\hat{\mathbf{V}}_\kappa\hat{\mathbf{V}}_\kappa^\top\mathbf{E}$</span></strong><br>
<span>$\boldsymbol{\Delta}_{\mathrm{obs}} = (\mathbf{R}^{(L)})^{1/2}\mathbf{Q}_{\mathrm{PCA}}$</span>
</div>
<div style="color:#1a7a6d; font-size:0.85em; font-weight:600; margin-top:0.15em;">correct signal, leave noise alone</div>
</div>
<div style="display:flex; align-items:center; color:#1a7a6d; font-size:2em; padding:0 0.06em;">→</div>
<div style="flex:1; text-align:center; padding:0 0.12em; opacity:0.85;">
<div style="color:#5a4e40; font-weight:700; font-size:1.1em; margin-bottom:0.25em;">UPDATE</div>
<div style="border:2px solid #2c2418; border-radius:5px; padding:0.4em; margin:0.1em 0; background:rgba(26,122,109,0.08);">
<span>$\mathbf{K}^{\mathrm{DC}} = \mathbf{P}_{xz}\mathbf{P}_{zz}^\dagger$</span><br>
<strong><span>$\mathbf{X}_{k_w} \leftarrow \mathbf{X}_{k_w} + \mathbf{K}^{\mathrm{DC}}\boldsymbol{\Delta}_{\mathrm{obs}}$</span></strong>
</div>
<div style="color:#5a4e40; font-size:0.85em; font-weight:600; margin-top:0.15em;">pullback to state space</div>
</div>
</div>
<div style="text-align:center; margin-top:0.35em; padding:0.2em 1em; border-top:1.5px dashed #1a7a6d; font-size:0.48em; color:#5a4e40;">
↺ <span>$\mathbf{X} \leftarrow \mathbf{X}_{k_w}$</span> — advance to window <span>$w{+}1$</span>. &ensp; Fully deterministic. &ensp; No perturbations, no inflation. &ensp; Cost dominated by <span>$\mathcal{M}$</span>.
</div>

<!-- .notes:
Five stages per window. Forecast: propagate ensemble through the forward model and observation operator to generate residuals. Whiten: normalize by observation covariance so noise becomes isotropic — this is what makes the subsequent spectral analysis meaningful. Extract: eigendecompose the whitened residual covariance to identify the leading kappa modes — the signal subspace. Project: restrict correction to those modes and unwhiten back to observation space. Update: compute the data-consistent gain via cross-covariance pseudoinverse and apply a deterministic state-space update. No random perturbations anywhere. The key idea: everything happens in whitened observation space, restricted to a learned subspace, then pulled back. The feedback loop advances to the next window.
-->

---

## Geometric Interpretation

<div style="display:flex; gap:0; align-items:flex-start; margin-top:0;">

<svg viewBox="50 5 380 465" style="flex:1; max-height:92vh;">
  <defs>
    <marker id="mr" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#b53a2a"/></marker>
    <marker id="mg" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#999"/></marker>
  </defs>
  <text x="230" y="22" text-anchor="middle" fill="#b53a2a" font-size="14" font-weight="700">(a) Stochastic EnKF</text>
  <!-- TOP: forecast + perturbations -->
  <line x1="230" y1="42" x2="230" y2="258" stroke="#c8c0b4" stroke-width="0.5"/>
  <text x="234" y="40" fill="#6b5d4e" font-size="10" font-style="italic">v̂₂</text>
  <rect x="35" y="142" width="390" height="16" rx="1" fill="#b53a2a" fill-opacity="0.05"/>
  <line x1="35" y1="150" x2="425" y2="150" stroke="#b53a2a" stroke-width="1.2" opacity="0.35"/>
  <text x="430" y="154" fill="#b53a2a" font-size="10" font-weight="600">v̂₁</text>
  <text x="430" y="166" fill="#b53a2a" font-size="9" opacity="0.9">signal</text>
  <circle cx="230" cy="150" r="120" fill="none" stroke="#b53a2a" stroke-width="0.5" stroke-dasharray="2.5,3" opacity="0.2"/>
  <ellipse cx="230" cy="150" rx="100" ry="65" fill="#b53a2a" fill-opacity="0.04" stroke="#b53a2a" stroke-width="0.9" stroke-dasharray="4,3" stroke-opacity="0.4"/>
  <circle cx="178" cy="132" r="3.5" fill="#5a4e40"/>
  <line x1="178" y1="132" x2="210" y2="148" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="205" cy="112" r="3.5" fill="#5a4e40"/>
  <line x1="205" y1="112" x2="172" y2="130" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="242" cy="128" r="3.5" fill="#5a4e40"/>
  <line x1="242" y1="128" x2="260" y2="96" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="275" cy="140" r="3.5" fill="#5a4e40"/>
  <line x1="275" y1="140" x2="248" y2="152" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="262" cy="168" r="3.5" fill="#5a4e40"/>
  <line x1="262" y1="168" x2="290" y2="148" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="215" cy="178" r="3.5" fill="#5a4e40"/>
  <line x1="215" y1="178" x2="238" y2="200" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="188" cy="164" r="3.5" fill="#5a4e40"/>
  <line x1="188" y1="164" x2="162" y2="142" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <circle cx="250" cy="160" r="3.5" fill="#5a4e40"/>
  <line x1="250" y1="160" x2="230" y2="188" stroke="#b53a2a" stroke-width="1.3" marker-end="url(#mr)" opacity="0.8"/>
  <text x="348" y="72" fill="#b53a2a" font-size="11" font-style="italic">ε⁽ʲ⁾ ~ 𝒩(0, R)</text>
  <text x="348" y="86" fill="#b53a2a" font-size="10" opacity="1.0">full d-space</text>
  <!-- Transition -->
  <line x1="230" y1="270" x2="230" y2="300" stroke="#999" stroke-width="1.2" marker-end="url(#mg)"/>
  <text x="248" y="290" fill="#5a4e40" font-size="10" font-style="italic">update + perturb</text>
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
  <text x="230" y="448" text-anchor="middle" fill="#5a4e40" font-size="10" font-style="italic">Var(ε) ~ 1/N  ≪  removed spread</text>
</svg>

<svg viewBox="50 5 380 465" style="flex:1; max-height:92vh;">
  <defs>
    <marker id="mt" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#1a7a6d"/></marker>
    <marker id="mg2" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#999"/></marker>
  </defs>
  <text x="230" y="22" text-anchor="middle" fill="#1a7a6d" font-size="14" font-weight="700">(b) QPCA-EnDCF</text>
  <!-- TOP: forecast + signal-only arrows -->
  <line x1="230" y1="42" x2="230" y2="258" stroke="#c8c0b4" stroke-width="0.5"/>
  <text x="234" y="40" fill="#6b5d4e" font-size="10" font-style="italic">v⊥</text>
  <rect x="35" y="142" width="390" height="16" rx="1" fill="#1a7a6d" fill-opacity="0.05"/>
  <line x1="35" y1="150" x2="425" y2="150" stroke="#1a7a6d" stroke-width="1.2" opacity="0.35"/>
  <text x="430" y="154" fill="#1a7a6d" font-size="10" font-weight="600">v̂₁</text>
  <text x="430" y="166" fill="#1a7a6d" font-size="9" opacity="0.9">signal</text>
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
  <text x="200" y="100" fill="#888" font-size="9" text-anchor="middle">no update</text>
  <line x1="200" y1="103" x2="200" y2="109" stroke="#999" stroke-width="0.6"/>
  <text x="266" y="192" fill="#888" font-size="9" text-anchor="middle">no update</text>
  <line x1="266" y1="184" x2="266" y2="178" stroke="#999" stroke-width="0.6"/>
  <text x="355" y="82" fill="#1a7a6d" font-size="11" font-weight="600">project onto V̂κ</text>
  <text x="355" y="96" fill="#1a7a6d" font-size="10" opacity="1.0">(leading κ modes)</text>
  <!-- Transition -->
  <line x1="230" y1="270" x2="230" y2="300" stroke="#999" stroke-width="1.2" marker-end="url(#mg2)"/>
  <text x="248" y="290" fill="#5a4e40" font-size="10" font-style="italic">spectral projection</text>
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
  <text x="182" y="384" text-anchor="middle" fill="#1a7a6d" font-size="9" font-weight="700" opacity="0.9" transform="rotate(-90 182 384)">v⊥ preserved</text>
  <text x="230" y="454" text-anchor="middle" fill="#1a7a6d" font-size="12" font-weight="600">anisotropic correction</text>
  <text x="230" y="468" text-anchor="middle" fill="#5a4e40" font-size="10" font-style="italic">noise-direction variance unchanged</text>
</svg>

</div>

<div style="margin-top:0.3em; padding:0.1em 1em; text-align:center; font-family:Georgia,'Times New Roman',serif; font-size:0.78em; color:var(--text-secondary,#6b5d4e); line-height:1.2; font-style:italic;">Signal-subspace updates preserve orthogonal variance; isotropic perturbations do not.</div>

<!-- .notes:
This table captures the geometric difference. Stochastic EnKF corrects along signal directions but also injects perturbation noise there. Along noise directions, it injects noise uniformly. The net effect: variance is compressed everywhere because the observation perturbations add noise in all dimensions while the Kalman update removes variance along observed directions. QPCA-EnDCF corrects only along the kappa signal directions — deterministically, without added noise. Noise directions are untouched. This is why it preserves ensemble diversity: it operates surgically on the signal subspace and leaves everything else intact.
-->

---

## Variance Collapse in Action

<div style="display:flex; gap:1.5em; align-items:flex-start;">
<div style="flex:1.4;">
<img src="figures/spread_vs_rmse_temporal.png" alt="Spread vs RMSE Temporal" style="width:100%; max-height:80vh !important;">
<div style="font-size:0.75em; color:#5a4e40; text-align:center; margin-top:0.5em;">Solid = ensemble spread (predicted uncertainty) · Dashed = RMSE (actual error)</div>
</div>
<div style="flex:0.6; padding-top:3em;">
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.5em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.95em; margin-bottom:0.15em;">Diagnosis</div>
<div style="font-size:0.85em; line-height:1.6; color:#3a3024;">
Spread: <span>$\sigma \approx 0.3$</span><br>
RMSE: <span>$\approx 4.5$</span><br>
<strong style="font-size:1.1em;">15× overconfident</strong>
</div>
</div>
<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.5em 0.6em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.95em; margin-bottom:0.15em;">Calibration principle</div>
<div style="font-size:0.85em; line-height:1.6; color:#3a3024;">
Well-calibrated: spread ≈ RMSE<br>
Here: spread ≪ RMSE<br>
<strong>Systematic, persistent, not noise</strong>
</div>
</div>
</div>
</div>

<!-- .notes:
This plot shows what variance collapse looks like in practice. Solid lines are ensemble spread — the filter's internal estimate of its own uncertainty. Dashed lines are RMSE — the actual estimation error. For sequential EnKF, spread flatlines near 0.3 while true error fluctuates between 3 and 6. The ratio is approximately 15 to 1 — the filter is an order of magnitude more confident than it should be. A calibrated ensemble would have spread tracking RMSE. Here they are completely decoupled. This is not a transient effect — it persists across the entire assimilation sequence. The consequence: every downstream decision based on ensemble spread is operating on unreliable uncertainty. This is the practical cost of the mechanism we just described.
-->

---

## MUD ↔ QPCA-EnDCF: Algebraic Correspondence

<div style="text-align:center; margin-top:0.2em; margin-bottom:0.4em;">
<div style="display:inline-block; border:2.5px solid #1a7a6d; border-radius:6px; padding:0.35em 1.2em; background:#1a7a6d08;">
<span style="font-size:1.05em; font-weight:700; color:#1a7a6d;">Shared template:</span>
<span style="font-size:1.0em; color:#2c2418;"> prior + covariance-weighted pullback of subspace-restricted innovation</span>
</div>
</div>

<div style="display:flex; gap:1em; margin-top:0.3em;">
<div style="flex:1; border:2px solid #5a7a9a; border-radius:6px; padding:0.5em 0.6em; background:#5a7a9a08;">
<div style="font-weight:700; color:#5a7a9a; font-size:0.95em; margin-bottom:0.2em;">MUD (parameter estimation)</div>
<div style="font-size:0.82em; color:#3a3024; margin-bottom:0.3em;">Subspace: <span>$A$</span> (QPCA-learned QoI map)</div>
<div>$$\theta_{\mathrm{MUD}} = \underbrace{\theta_{\mathrm{init}}}_{\text{prior}} + \underbrace{\Sigma_\theta A^\top \Sigma_{\mathrm{pred}}^{-1}}_{\text{pullback}}\;\underbrace{(\mathbf{z}_{\mathrm{obs}} - A\,\theta_{\mathrm{init}})}_{\text{innovation}}$$</div>
</div>
<div style="flex:1; border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.95em; margin-bottom:0.2em;">QPCA-EnDCF (state filtering)</div>
<div style="font-size:0.82em; color:#3a3024; margin-bottom:0.3em;">Subspace: <span>$\hat{\mathbf{V}}_\kappa$</span> (leading eigenvectors of whitened residual covariance)</div>
<div>$$\mathbf{x}^{(j),a} = \underbrace{\mathbf{x}^{(j),f}}_{\text{prior}} + \underbrace{\mathbf{K}^{\mathrm{DC}}\mathbf{R}^{1/2}}_{\text{pullback}}\;\underbrace{\hat{\mathbf{V}}_\kappa\hat{\mathbf{V}}_\kappa^\top\mathbf{R}^{-1/2}(\mathbf{z}^{(w)} - \mathbf{z}_f^{(j)})}_{\text{projected innovation}}$$</div>
</div>
</div>

<div class="fragment" style="margin-top:0.5em;">
<div style="display:flex; gap:1em;">
<div style="flex:1; border-left:4px solid #1a7a6d; padding-left:0.7em; font-size:0.9em; line-height:1.55; color:#3a3024;">
<strong>QPCA defines the signal subspace</strong> in both settings — <span>$A$</span> in parameter space, <span>$\hat{\mathbf{V}}_\kappa$</span> in observation space — via spectral decomposition of the data-model mismatch
</div>
<div style="flex:1; border-left:4px solid #c4653a; padding-left:0.7em; font-size:0.9em; line-height:1.55; color:#3a3024;">
<strong>Updates confined to this subspace</strong> — orthogonal directions receive no correction → ensemble diversity preserved → <strong style="color:#c4653a;">calibrated spread</strong>
</div>
</div>
</div>

<!-- .notes:
Both MUD and QPCA-EnDCF follow the same algebraic template: prior plus covariance-weighted pullback of a subspace-restricted innovation. In MUD, the QPCA-learned map A defines a low-rank subspace for parameter inversion using population covariances. In QPCA-EnDCF, the leading eigenvectors of the whitened residual covariance define the signal subspace, and the data-consistent gain maps the projected correction back to state space. The unifying idea: QPCA defines the signal subspace in both cases via spectral decomposition of the data-model mismatch. Updates are confined to this subspace — orthogonal directions receive no correction. This is precisely why ensemble diversity and therefore calibration are preserved. The method is not ad hoc — it is the filtering counterpart of an established inverse problem framework.
-->

---

<!-- ============================================================ -->
<!-- SECTION 3: THEORY (Slides 15-20) -->
<!-- ============================================================ -->

<!-- ## Theoretical Framework: Overview

Three-stage analysis:

1. **Covariance concentration** → sample $\mathbf{C}_E$ approximates population $\boldsymbol{\Sigma}_E$
2. **Spectral perturbation** → empirical projector approximates population projector
3. **Bias-variance decomposition** → $\mathrm{MSE} = \mathrm{Bias}^2(\kappa) + \mathrm{Var}(N,\kappa)$

**Goal: explain WHY spectral regularization yields calibration**

<!-- .notes:
Now let me present the theoretical contribution. The analysis has three stages. First, we show the sample covariance of whitened residuals concentrates around its population counterpart at rate O(1/N). Second, we use Davis-Kahan perturbation theory to show the empirical spectral projector is close to the population projector — controlled by the cutoff gap. Third, we combine these to get a bias-variance decomposition that cleanly separates the effects of truncation, sampling, and approximation. This isn't just a convergence result — it explains mechanistically why spectral regularization produces calibrated ensembles.
-->

<!-- ---

## Key Assumptions

- Forecast ensemble: i.i.d. samples with finite 4th moment
- Observation covariance $\mathbf{R}^{(L)}$ positive definite
- Spectral cutoff gap: <span>$\lambda_\kappa - \lambda_{\kappa+1} \geq \delta_\kappa > 0$</span>

**All assumptions are mild:**

- No Gaussianity required (used only for sharpening)
- i.i.d. is idealization; cycling experiments validate
- Gap condition ensures projector stability -->

<!-- .notes:
The assumptions are deliberately mild. We need i.i.d. ensemble members with finite fourth moments — strictly weaker than Gaussianity. The observation covariance must be positive definite, which is always true in practice. And we need a spectral gap at the truncation cutoff — this ensures the projector is well-defined and stable. The i.i.d. assumption is an idealization that doesn't hold in cycling; we verify empirically that the theoretical predictions hold nonetheless. Gaussianity is only invoked for sharper constants, not for the main results.
-->

<!-- ---

## Main Theorem: Bias-Variance Decomposition

<div>$$\mathbb{E}\|\bar{\mathbf{x}}^a - \mathbf{x}^{\mathrm{true}}\|^2 = \mathrm{Bias}^2(\kappa) + \mathrm{Var}(N, \kappa)$$</div>

**Bias bound:**

<div>$$\mathrm{Bias}^2 \leq 2\,\mathrm{Bias}_{\mathrm{base}}^2 + 4\,\mathbb{E}[\|\mathbf{K}\|^2]\|\mathbf{R}\|\,\|(\mathbf{I} - \mathbf{P}_\kappa)\boldsymbol{\mu}_E\|^2 + \text{sampling, approx}$$</div>

**Variance bound:**

<div>$$\mathrm{Var} \leq \frac{2}{N}\mathbb{E}[\|\mathbf{x}^f - \boldsymbol{\mu}^f\|^2] + \frac{2\|\mathbf{R}\|}{N}\mathbb{E}[\|\mathbf{K}\|^2]\,\mathrm{tr}(\boldsymbol{\Sigma}_E) + \text{projector term}$$</div> -->

<!-- .notes:
Here's the main theorem. The MSE decomposes exactly into squared bias and variance. The bias has several contributions: a base term reflecting how well the untruncated correction would do, a truncation term depending on how much of the mean innovation is discarded — that's the I minus P-kappa mu-E norm — and sampling and approximation terms. The variance has two main pieces: forecast variance scaled by 1/N, and observation-space variance also scaled by 1/N with a gain-dependent prefactor. The projector estimation term involves kappa over delta-kappa-squared, connecting projector stability directly to variance.
-->

<!-- ---

 ## The Critical Comparison

**Stochastic EnKF variance (lower bound):**

<div>$$\mathrm{Var}_{\mathrm{stoch}} \geq \frac{\|\mathbf{K}\|^2 \cdot \mathrm{tr}(\mathbf{R}^{(L)})}{N} = \mathcal{O}\!\left(\frac{d}{N}\right)$$</div>

**QPCA-EnDCF variance:**

<div>$$\mathrm{Var}_{\mathrm{QPCA}} = \mathcal{O}\!\left(\frac{1}{N}\right) \text{ with } \frac{\kappa}{\delta_\kappa^2} \text{ prefactor}$$</div>

- Stochastic: perturbation variance scales with <span>$d = mL$</span>
- QPCA-EnDCF: no perturbation term; projector term scales with $\kappa$
- At $\kappa=1$, <span>$d=100$</span>: up to two orders of magnitude in the perturbation component -->

<!-- .notes:
This is the theoretical punchline. The stochastic EnKF variance has an irreducible lower bound — Corollary 2 in the paper — from observation perturbations that scales with d over N. For windowed methods with d = mL = 100, that's a substantial floor. QPCA-EnDCF eliminates this specific variance component entirely. Its variance is still O(1/N), but the prefactor involves the effective rank kappa and the cutoff gap delta-kappa — not the observation dimension d. I want to be careful here: this comparison is between the perturbation-induced variance component in stochastic methods and its absence in QPCA-EnDCF. Both methods still have forecast sampling variance that scales with 1/N. The net advantage depends on how large the perturbation component is relative to the forecast component — and in our experiments, it's the dominant contributor to the variance gap.

Moving from theory to evidence, the bias-variance decomposition will show this plays out exactly as predicted.
-->

<!-- ---

## Why the Favorable Bias-Variance Tradeoff?

Classical regularization: reduce variance → increase bias

**QPCA-EnDCF achieves a favorable tradeoff when spectra decay rapidly:**

- Leading eigenmode captures 60–80% of residual variance
- Mean innovation <span>$\boldsymbol{\mu}_E$</span> aligns with leading eigenvector
- <span>$\|(\mathbf{I} - \mathbf{P}_\kappa)\boldsymbol{\mu}_E\|^2$</span> is empirically small
- Discarded modes carry sampling noise, not signal

**Condition for this to hold: rapid spectral decay + mean-signal alignment** -->

<!-- .notes:
You might ask: doesn't truncation always introduce bias? In classical Tikhonov or ridge regularization, yes — there's a strict tradeoff. QPCA-EnDCF achieves a more favorable tradeoff, and the theory tells you exactly when and why. The truncation bias depends on the norm of (I minus P-kappa) times mu-E — how much of the mean innovation lies outside the retained subspace. When the mean mismatch aligns with the leading eigenvector, this term is small. Empirically, this alignment is strong in our setting because the dominant eigenmode captures the coherent dynamical forecast-observation discrepancy. The discarded modes are dominated by sampling noise, not signal. I want to be precise: this favorable regime requires rapid spectral decay and mean-signal alignment. The theorem identifies these as sufficient conditions, and the experiments verify they hold in the Lorenz-96 setting. In systems where the eigenspectrum is flat or the mean mismatch is diffuse, the advantage would be reduced — and the theory quantifies exactly how much through the truncation bias term.
-->

<!-- ---

## Theoretical Summary

| Property            | Stochastic EnKF    | QPCA-EnDCF                     |
| ------------------- | ------------------ | ------------------------------ |
| Variance scaling    | $\mathcal{O}(d/N)$ | $\mathcal{O}(\kappa/N)$        |
| Perturbation noise  | Irreducible        | Eliminated                     |
| Regularization      | Uniform via R      | Adaptive spectral              |
| Bias-variance       | Classical tradeoff | Favorable under spectral decay |
| Projector stability | N/A                | Controlled by $\delta_\kappa$  | -->

<!-- .notes:
To summarize the theory: stochastic EnKF has variance scaling with observation dimension over N, irreducible perturbation noise, and uniform regularization. QPCA-EnDCF has variance scaling with effective rank over N, no perturbation noise, adaptive spectral regularization, and a favorable bias-variance tradeoff under spectral decay. The projector stability is controlled by the cutoff gap delta-kappa, which is intrinsic to the problem spectrum, not a tuning parameter.

That's the theory. Now let me show you the experiments that test these predictions. The question is: do the theoretical advantages materialize in practice, under realistic cycling conditions?
<!-- --> -->

<!-- ============================================================ -->
<!-- SECTION 4: EVIDENCE (Slides 21-32) -->
<!-- ============================================================ -->

## Experimental Setup: Lorenz-96

<div style="display:flex; gap:1.2em; align-items:flex-start; margin-top:0.1em;">
<div style="flex:1.2; position:relative;">
<svg viewBox="0 0 480 460" style="width:100%;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="l96-a" markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0,6 2.5,0 5" fill="#5a4e40" opacity="0.6"/></marker>
  </defs>
  <!-- ══ LORENZ-96 RING ══ -->
  <text x="240" y="22" text-anchor="middle" fill="#2c2418" font-size="16" font-weight="700" font-family="-apple-system,sans-serif">Lorenz-96</text>
  <!-- Coupling ring: clean circle -->
  <circle cx="240" cy="215" r="155" fill="none" stroke="#5a4e40" stroke-width="2.0" opacity="0.3"/>
  <!-- Observed nodes (i=0,2,4,...,20): filled teal, on true circle r=155 centered at (240,215) -->
  <circle cx="240" cy="60" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="324" cy="85" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="381" cy="151" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="393" cy="237" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="357" cy="317" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="284" cy="364" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="196" cy="364" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="123" cy="317" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="87" cy="237" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="99" cy="151" r="11" fill="#1a7a6d" opacity="0.85"/>
  <circle cx="156" cy="85" r="11" fill="#1a7a6d" opacity="0.85"/>
  <!-- Unobserved nodes (i=1,3,5,...,21): hollow orange with X -->
  <circle cx="284" cy="66" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="280" y1="62" x2="288" y2="70" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="288" y1="62" x2="280" y2="70" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="357" cy="113" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="353" y1="109" x2="361" y2="117" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="361" y1="109" x2="353" y2="117" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="393" cy="193" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="389" y1="189" x2="397" y2="197" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="397" y1="189" x2="389" y2="197" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="381" cy="279" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="377" y1="275" x2="385" y2="283" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="385" y1="275" x2="377" y2="283" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="324" cy="345" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="320" y1="341" x2="328" y2="349" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="328" y1="341" x2="320" y2="349" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="240" cy="370" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="236" y1="366" x2="244" y2="374" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="244" y1="366" x2="236" y2="374" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="156" cy="345" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="152" y1="341" x2="160" y2="349" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="160" y1="341" x2="152" y2="349" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="99" cy="279" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="95" y1="275" x2="103" y2="283" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="103" y1="275" x2="95" y2="283" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="87" cy="193" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="83" y1="189" x2="91" y2="197" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="91" y1="189" x2="83" y2="197" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="123" cy="113" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="119" y1="109" x2="127" y2="117" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="127" y1="109" x2="119" y2="117" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <circle cx="196" cy="66" r="7" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.6"/>
  <line x1="192" y1="62" x2="200" y2="70" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <line x1="200" y1="62" x2="192" y2="70" stroke="#c4653a" stroke-width="1.0" opacity="0.5"/>
  <!-- Center: chaotic label (equation overlaid via CSS) -->
  <text x="240" y="228" text-anchor="middle" fill="#c4653a" font-size="15" font-weight="700" font-family="-apple-system,sans-serif">CHAOTIC  (F = 8)</text>
  <text x="240" y="248" text-anchor="middle" fill="#c4653a" font-size="12" font-family="-apple-system,sans-serif">13 positive Lyapunov exponents</text>
  <!-- Legend -->
  <circle cx="120" cy="415" r="9" fill="#1a7a6d" opacity="0.85"/>
  <text x="136" y="420" fill="#1a7a6d" font-size="14" font-family="-apple-system,sans-serif" font-weight="700">observed (m = 20)</text>
  <circle cx="310" cy="415" r="6" fill="none" stroke="#c4653a" stroke-width="1.5" opacity="0.7"/>
  <line x1="307" y1="412" x2="313" y2="418" stroke="#c4653a" stroke-width="0.8" opacity="0.6"/>
  <line x1="313" y1="412" x2="307" y2="418" stroke="#c4653a" stroke-width="0.8" opacity="0.6"/>
  <text x="322" y="420" fill="#c4653a" font-size="14" font-family="-apple-system,sans-serif" font-weight="700">unobserved (20)</text>
  <text x="240" y="448" text-anchor="middle" fill="#5a4e40" font-size="13" font-family="Georgia,serif">σ_obs = 1.5  ·  cyclic boundaries  ·  every-other observed</text>
</svg>
<div style="position:absolute; top:37%; left:50%; transform:translate(-50%,-50%); text-align:center; pointer-events:none;"><span>$\dfrac{dx_i}{dt} = (x_{i+1} - x_{i-2})\,x_{i-1} - x_i + F$</span></div>
</div>
<div style="flex:0.8; padding-top:0.2em;">

<div style="border:2px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.5em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.95em; margin-bottom:0.2em;">Undersampling regime</div>
<svg viewBox="0 0 280 60" style="width:100%; margin-bottom:0.2em;" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="5" width="280" height="14" rx="3" fill="#1a7a6d" fill-opacity="0.15" stroke="#1a7a6d" stroke-width="0.6"/>
  <text x="140" y="16" text-anchor="middle" fill="#1a7a6d" font-size="9" font-weight="600">n = 40 state dimensions</text>
  <rect x="0" y="24" width="140" height="14" rx="3" fill="#1a7a6d" fill-opacity="0.25" stroke="#1a7a6d" stroke-width="0.6"/>
  <text x="70" y="35" text-anchor="middle" fill="#1a7a6d" font-size="9" font-weight="600">m = 20 observed</text>
  <rect x="0" y="43" width="70" height="14" rx="3" fill="#c4653a" fill-opacity="0.25" stroke="#c4653a" stroke-width="1.0"/>
  <text x="35" y="54" text-anchor="middle" fill="#c4653a" font-size="9" font-weight="700">N = 10</text>
  <text x="78" y="54" fill="#c4653a" font-size="9" font-weight="600">ensemble</text>
</svg>
<div style="font-size:0.82em; color:#c4653a; font-weight:700; text-align:center;">rank(<span>$\hat{\mathbf{C}}$</span>) ≤ 9  — 31 missing directions</div>
</div>

<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.5em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.95em; margin-bottom:0.15em;">Assimilation windows</div>
<div style="font-size:0.82em; line-height:1.6; color:#3a3024;">
<span>$L = 5$</span> obs times per window<br>
0.83 Lyapunov times (errors grow by <span>$e$</span>)<br>
5 independent Monte Carlo trials
</div>
</div>

<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.95em; margin-bottom:0.15em;">Methods compared</div>
<div style="font-size:0.82em; line-height:1.6; color:#3a3024;">
Seq-EnKF (sequential stochastic)<br>
4D-EnKF (windowed stochastic)<br>
<strong>QPCA-EnDCF</strong> (<span>$\kappa = 1$</span>, no inflation)
</div>
</div>

<div style="text-align:center; font-size:0.88em; font-weight:700; color:#c4653a; margin-top:0.2em;">Ill-posed regime — requires regularization</div>

</div>
</div>

<!-- .notes:
All experiments use the Lorenz-96 system — the canonical testbed in data assimilation. The ring diagram shows the cyclic structure: 40 state variables with nonlinear nearest-neighbor coupling. At forcing F equals 8, the system is fully chaotic with 13 positive Lyapunov exponents. We observe every other variable — the teal nodes — giving 20 observations out of 40 states, with noise standard deviation 1.5. The ensemble has only 10 members, so the empirical covariance has rank at most 9 in a 40-dimensional space — severely undersampled. Assimilation windows span 5 observation times, about 0.83 Lyapunov times — long enough for errors to grow by a factor of e. We compare three methods: sequential EnKF as the standard stochastic baseline, 4D-EnKF as the windowed stochastic baseline, and QPCA-EnDCF with kappa equals 1 and no inflation. This is a deliberately hard regime: chaotic dynamics, partial observations, and extreme undersampling.
-->

---

## Result 1: Probabilistic Calibration

<div style="display:flex; gap:0.6em; align-items:center; margin-bottom:0.2em;">
<div style="flex:1; font-size:0.82em; color:#3a3024;">
<strong>Metric:</strong> <span>$\gamma_w := \sigma_w / \mathrm{RMSE}_w$</span>, &ensp; <span>$\sigma_w := \bigl[\tfrac{1}{n}\,\mathrm{tr}(\hat{\mathbf{P}}^a_{k_w})\bigr]^{1/2}$</span> &ensp; · &ensp; <span>$\bar{\gamma} = 1$</span>: calibrated &ensp; · &ensp; <span>$\bar{\gamma} \ll 1$</span>: overconfident &ensp; · &ensp; <span>$\rho$</span>: temporal tracking
</div>
</div>

<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1.5;">
<img src="figures/combined_calibration_analysis.png" alt="Combined Calibration Analysis" style="width:100%; max-height:65vh !important;">
</div>
<div style="flex:0.55; padding-top:0.3em;">
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.9em; margin-bottom:0.1em;">QPCA-EnDCF</div>
<div style="font-size:0.82em; line-height:1.6; color:#3a3024;">
<span>$\bar{\gamma} \approx 0.81$</span> (near-ideal)<br>
<span>$\rho \approx 0.82$</span> (tracks error)<br>
<strong>20% lower RMSE</strong>
</div>
</div>
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.9em; margin-bottom:0.1em;">Stochastic methods</div>
<div style="font-size:0.82em; line-height:1.6; color:#3a3024;">
<span>$\bar{\gamma} \approx 0.1$</span> (15× overconfident)<br>
<span>$\rho \approx 0$</span> (no tracking)
</div>
</div>
<div style="border:2px solid #2c2418; border-radius:6px; padding:0.4em 0.5em; background:#2c241808;">
<div style="font-size:0.85em; line-height:1.5; color:#2c2418; font-weight:600; text-align:center;">
Calibration + accuracy<br>improve simultaneously<br><em style="font-weight:400;">not a tradeoff</em>
</div>
</div>
</div>
</div>

<!-- .notes:
The spread-skill ratio gamma-w is spread over RMSE — a calibrated ensemble has gamma-bar near 1. The temporal correlation rho measures whether spread tracks error over time. Panel A shows gamma-w per window: QPCA-EnDCF fluctuates around the ideal line at 1.0, averaging 0.81. Stochastic methods flatline near 0.1 — 15 times too confident. Panel B is the reliability diagram: QPCA-EnDCF clusters along the diagonal with rho of 0.82 — when it reports high uncertainty, error is indeed high. Stochastic methods show vertical clustering at low spread regardless of actual error. The key result: QPCA-EnDCF simultaneously achieves near-ideal calibration, strong temporal tracking, and 20 percent lower RMSE. This is not a tradeoff — spectral regularization improves both accuracy and reliability.
-->

---

## Result 2: Bias-Variance Decomposition

<div style="text-align:center; font-size:0.88em; color:#3a3024; margin-bottom:0.2em;"><span>$\mathrm{MSE} = \mathrm{Bias}^2 + \mathrm{Variance}$</span> — what drives the improvement?</div>

<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1.1;">
<img src="figures/bias_variance_evolution.png" alt="Bias Variance Evolution" style="width:100%; max-height:55vh !important;">
</div>
<div style="flex:0.9; padding-top:0.2em;">
<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Unchanged: Bias</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
All methods: <span>$\mathrm{Bias}^2 \approx 10\text{–}11$</span><br>
Spectral truncation does not shift bias
</div>
</div>
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.88em; margin-bottom:0.1em;">Changed: Variance</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Stochastic: Var ≈ 11–12 (variance-limited)<br>
QPCA-EnDCF: <strong>Var ≈ 2</strong> (80% reduction)<br>
<span>$\mathcal{O}(\kappa/N)$</span> vs <span>$\mathcal{O}(d/N)$</span>
</div>
</div>
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.4em 0.5em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.88em; margin-bottom:0.1em;">Mechanism</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Stochastic → <strong>variance-limited</strong> (50/50)<br>
QPCA-EnDCF → <strong>bias-dominated</strong> (82%)<br>
RMSE gain = variance elimination
</div>
</div>
</div>
</div>

<!-- .notes:
MSE decomposes into squared bias plus variance. The key finding: all three methods have nearly identical bias — about 10 to 11. The entire MSE difference comes from variance. Stochastic methods have variance around 11 to 12, making them variance-limited — roughly 50-50 bias and variance. QPCA-EnDCF collapses variance to about 2 — an 80 percent reduction — making it 82 percent bias-dominated. This is the mechanism: spectral truncation removes noise-dominated modes that contribute variance without reducing bias. The scaling difference is O-kappa-over-N versus O-d-over-N. The practical implication: further improvements for QPCA-EnDCF should target the forward model, not ensemble size. Stochastic methods remain fundamentally limited by sampling variance at fixed N.
-->

---

## Result 3: Inflation-Free Operation

<div style="text-align:center; margin-bottom:0.15em;">
<div style="font-size:0.85em; color:#3a3024; margin-bottom:0.1em;"><strong>Additive inflation</strong> — isotropic noise added to each member to compensate rank deficiency:</div>
<span>$\mathbf{x}^{(j)}_{\alpha_{\mathrm{add}}} = \mathbf{x}^{(j),f} + \boldsymbol{\varepsilon}^{(j)}, \qquad \boldsymbol{\varepsilon}^{(j)} \sim \mathcal{N}(\mathbf{0},\; \alpha_{\mathrm{add}}^2\,\mathbf{Q}_{\mathrm{add}}), \qquad \mathbf{Q}_{\mathrm{add}} = \mathbf{I}_n$</span>
</div>

<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1.4;">
<img src="figures/inflation_additive_20.png" alt="Additive Inflation" style="width:100%; max-height:62vh !important;">
</div>
<div style="flex:0.6; padding-top:0.3em;">
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.9em; margin-bottom:0.1em;">QPCA-EnDCF</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Optimal at <span>$\alpha_{\mathrm{add}} = 0$</span> for all <span>$N$</span><br>
Any <span>$\alpha_{\mathrm{add}} > 0$</span> <strong>degrades</strong> performance<br>
<em>Inflation is unnecessary</em>
</div>
</div>
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.9em; margin-bottom:0.1em;">Stochastic methods</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Additive inflation provides limited benefit<br>
Underperforms multiplicative by 5–10%
</div>
</div>
<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.9em; margin-bottom:0.1em;">Why?</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Isotropic noise disrupts dynamically consistent correlations<br>
QPCA-EnDCF already regularizes in the <strong>correct subspace</strong>
</div>
</div>
</div>
</div>

<!-- .notes:
Additive inflation adds isotropic Gaussian noise to each ensemble member — variance alpha-add-squared times identity. It is a standard fix for rank deficiency: inject variance in all directions, including those the ensemble cannot span. The result is decisive: QPCA-EnDCF is optimal at alpha-add equals zero for every ensemble size. Any positive inflation degrades performance. The reason: isotropic noise disrupts the dynamically consistent correlation structure that spectral regularization preserves. QPCA-EnDCF already controls variance in the signal subspace — adding noise on top of that breaks what the method builds. For stochastic methods, additive inflation provides marginal benefit but consistently underperforms multiplicative inflation by 5 to 10 percent. The practical implication: one fewer tuning parameter, one fewer heuristic.
-->

---

## Result 4: Robustness — Non-Gaussian Errors

<div style="text-align:center; font-size:0.85em; color:#3a3024; margin-bottom:0.15em;">9 noise distributions (Gaussian, Student-t, Laplace, Gamma, Log-normal, …) — all standardized to same variance</div>
<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1;">
<img src="figures/noise_distributions.png" alt="Noise Distributions" style="width:100%; max-height:55vh !important;">
<div style="font-size:0.72em; color:#5a4e40; text-align:center; margin-top:0.2em;">Symmetric, heavy-tailed, skewed</div>
</div>
<div style="flex:1;">
<img src="figures/mean_rmse_comparison_nongaussian.png" alt="Mean RMSE Non-Gaussian" style="width:100%; max-height:55vh !important;">
<div style="font-size:0.72em; color:#5a4e40; text-align:center; margin-top:0.2em;">RMSE across all distributions</div>
</div>
<div style="flex:0.5; padding-top:0.3em;">
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.88em; margin-bottom:0.1em;">QPCA-EnDCF</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
RMSE: 3.51–3.69<br>
CV ≈ 1.4%<br>
<strong>18–25% improvement</strong><br>across every distribution
</div>
</div>
<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Why?</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
Method depends on <strong>covariance structure</strong>, not distributional shape
</div>
</div>
</div>
</div>

<!-- .notes:
Real observation errors are rarely Gaussian. We tested 9 distributions spanning symmetric heavy tails, right skewness, and the Gaussian baseline — all standardized to the same variance. QPCA-EnDCF is essentially insensitive to distributional shape: RMSE stays in a tight band from 3.51 to 3.69, coefficient of variation only 1.4 percent. The improvement over stochastic methods is 18 to 25 percent for every distribution tested. The reason: whitening and PCA depend only on second-moment structure — covariances, not higher-order distributional properties. The method is robust because it never assumes Gaussianity.
-->

---

## Result 5: Robustness — Correlated Observation Errors

<div style="text-align:center; font-size:0.85em; color:#3a3024; margin-bottom:0.1em;">
<span>$\mathrm{cond}(\mathbf{R})$</span> from 1 to <span>$3.7 \times 10^5$</span> — given known <span>$\mathbf{R}$</span> (no misspecification)
</div>
<div style="text-align:center; font-size:0.72em; color:#5a4e40; margin-bottom:0.15em;">
<span>$[\mathbf{R}]_{ij} = \sigma_{\mathrm{obs}}^2 \exp(-d_{ij}/\ell)$</span> (exponential) &ensp; · &ensp; <span>$[\mathbf{R}]_{ij} = \sigma_{\mathrm{obs}}^2 \exp(-d_{ij}^2/2\ell^2)$</span> (Gaussian)
</div>
<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1;">
<img src="figures/correlation_structures.png" alt="Correlation Structures" style="width:100%; max-height:50vh !important;">
<div style="font-size:0.72em; color:#5a4e40; text-align:center; margin-top:0.2em;">Diagonal · Exponential · Gaussian</div>
</div>
<div style="flex:1;">
<img src="figures/reconstruction_errors.png" alt="Reconstruction Errors" style="width:100%; max-height:50vh !important;">
<div style="font-size:0.72em; color:#5a4e40; text-align:center; margin-top:0.2em;">RMSE under each structure</div>
</div>
<div style="flex:0.55; padding-top:0.2em;">
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.35em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.88em; margin-bottom:0.1em;">QPCA-EnDCF</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
<strong>≤ 7% degradation</strong><br>across 5 orders of cond(<span>$\mathbf{R}$</span>)<br>
Advantage grows: 25% → 32%
</div>
</div>
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.35em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.88em; margin-bottom:0.1em;">4D-EnKF</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
15% degradation<br>
Perturbations lose efficiency as correlations reduce independent information
</div>
</div>
<div style="border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Mechanism</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
Cholesky whitening:<br>
<span>$\mathbf{W}\mathbf{R}\mathbf{W}^\top = \mathbf{I}$</span><br>
Geometry restored before PCA
</div>
</div>
</div>
</div>

<!-- .notes:
This tests algorithmic stability: given the true observation covariance R, does the method hold as conditioning increases? We test three structures spanning five orders of magnitude in condition number — diagonal baseline, exponential correlation with cond 649, and Gaussian correlation with cond approximately 370,000. QPCA-EnDCF degrades within 7 percent of the uncorrelated baseline even at the worst conditioning. By contrast, 4D-EnKF degrades 15 percent, and the QPCA-EnDCF advantage grows from 25 to 32 percent under severe ill-conditioning. The mechanism: Cholesky whitening maps the correlated space to identity covariance before spectral analysis — W R W-transpose equals I. This restores the isotropic noise structure that makes PCA meaningful. Stochastic perturbations lose efficiency because correlated observations contribute less independent information. Important scope: this tests stability under known R, not robustness to misspecification.
-->

---

## Result 6: Calibration Across Ensemble Sizes

<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1.4;">

![Ensemble Size Spread Skill](figures/fig_ensemble_size_spread_skill.png)

</div>
<div style="flex:0.6; padding-top:0.5em;">
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.92em; margin-bottom:0.1em;">QPCA-EnDCF at <span>$N=10$</span></div>
<div style="font-size:0.85em; line-height:1.5; color:#3a3024;">
<span>$\bar{\gamma} \approx 0.77$</span> (near-calibrated)<br>
By <span>$N=50$</span>: <span>$\bar{\gamma} \approx 0.95$</span>
</div>
</div>
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; margin-bottom:0.4em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.92em; margin-bottom:0.1em;">Stochastic at <span>$N=50$</span></div>
<div style="font-size:0.85em; line-height:1.5; color:#3a3024;">
<span>$\bar{\gamma} \approx 0.12$</span> (still 8× overconfident)<br>
Never approaches calibration
</div>
</div>
<div style="border:2px solid #2c2418; border-radius:6px; padding:0.5em 0.6em; background:#2c241808;">
<div style="font-size:0.88em; line-height:1.5; color:#2c2418; font-weight:700; text-align:center;">
QPCA-EnDCF at <span>$N{=}10$</span><br>beats stochastic at <span>$N{=}50$</span><br>
<span style="font-size:1.15em; color:#1a7a6d;">→ 5× calibration savings</span>
</div>
</div>
</div>
</div>

<!-- .notes:
This is the operational payoff. QPCA-EnDCF at N equals 10 achieves a spread-skill ratio of 0.77 — near-calibrated. By N equals 50, it reaches 0.95, essentially ideal. Stochastic methods at N equals 50 are still at gamma-bar of 0.12 — 8 times overconfident. They never approach calibration even at N equals 100. The direct comparison: QPCA-EnDCF with 10 members outperforms stochastic methods with 50 members. That is a 5 times reduction in required ensemble size for equivalent calibration. Since each ensemble member requires a full model integration, this translates directly to computational savings. This is the most operationally impactful finding: calibrated uncertainty at a fraction of the cost.
-->

---

## Result 7: Window Length Sensitivity

<div style="display:flex; gap:1.2em; align-items:flex-start;">
<div style="flex:1.4;">

![Window RMSE Analysis](figures/combined_window_rmse_analysis.png)

</div>
<div style="flex:0.6; padding-top:0.3em;">
<div style="border:2px solid #c4653a; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.9em; margin-bottom:0.1em;"><span>$L = 1$</span>: no temporal structure</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
Sequential — insufficient residual structure for spectral analysis<br>
QPCA-EnDCF slightly underperforms
</div>
</div>
<div style="border:2px solid #1a7a6d; border-radius:6px; padding:0.4em 0.5em; margin-bottom:0.4em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.9em; margin-bottom:0.1em;"><span>$L \geq 3$</span>: spectral structure emerges</div>
<div style="font-size:0.82em; line-height:1.5; color:#3a3024;">
<strong>16–21% improvement</strong> over 4D-EnKF<br>
Temporal window enables mode extraction
</div>
</div>
<div style="border:2px solid #2c2418; border-radius:6px; padding:0.4em 0.5em; background:#2c241808;">
<div style="font-weight:700; color:#2c2418; font-size:0.9em; margin-bottom:0.1em;">Practical guideline</div>
<div style="font-size:0.85em; line-height:1.5; color:#2c2418; text-align:center;">
Sweet spot: <span>$L \in [5, 10]$</span><br>
<strong>Stable performance, diminishing returns beyond</strong>
</div>
</div>
</div>
</div>

<!-- .notes:
Window length L controls how much temporal information is available for spectral analysis. At L equals 1 — purely sequential — there is no temporal structure in the residuals, so PCA cannot extract meaningful modes. QPCA-EnDCF slightly underperforms in this regime. The threshold is sharp: at L equals 3, sufficient structure emerges and QPCA-EnDCF outperforms 4D-EnKF by 16 to 21 percent. Performance stabilizes for L between 5 and 10 — this is the practical sweet spot. Beyond L equals 10, returns diminish while the eigendecomposition cost grows. The design recommendation: use windows of at least 3 observation times, with 5 as the default.
-->

---

<!-- ============================================================ -->
<!-- SECTION 5: CONTRIBUTIONS & IMPACT (Slides 33-37) -->
<!-- ============================================================ -->

## Contributions

<div style="display:flex; gap:1em; margin-top:0.3em;">
<div style="flex:1; border:2px solid #5a7a9a; border-radius:6px; padding:0.5em 0.6em; background:#5a7a9a08;">
<div style="font-weight:700; color:#5a7a9a; font-size:1.0em; margin-bottom:0.2em;">Theory — explains the mechanism</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
Bias-variance decomposition for spectral ensemble filters<br>
Variance scaling: <span>$\mathcal{O}(\kappa/N)$</span> vs <span>$\mathcal{O}(d/N)$</span><br>
Projector stability via Davis-Kahan
</div>
</div>
<div style="flex:1; border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:1.0em; margin-bottom:0.2em;">Empirics — confirms the theory</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
Near-ideal calibration (<span>$\bar{\gamma} \approx 0.81$</span>) under severe undersampling<br>
Inflation-free across all <span>$N$</span><br>
Robust to non-Gaussian and correlated errors
</div>
</div>
<div style="flex:1; border:2px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:1.0em; margin-bottom:0.2em;">Practice — operational gains</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
2–3× accuracy savings<br>
<strong>5× calibration savings</strong><br>
Guidelines: <span>$L \geq 3$</span>, <span>$\kappa = 1$</span>, no inflation
</div>
</div>
</div>

<div style="margin-top:0.8em; text-align:center; font-size:1.05em; color:#2c2418; font-weight:600; line-height:1.5; max-width:94%; margin-left:auto; margin-right:auto;">Spectral regularization in observation space produces calibrated uncertainty where stochastic methods cannot — with lower RMSE, no tuning, and fewer ensemble members.</div>

<!-- .notes:
Three layers of contribution, all connected. The theory: a bias-variance decomposition showing that spectral truncation reduces variance from O-d-over-N to O-kappa-over-N without increasing bias, with projector stability guaranteed by Davis-Kahan. The empirics confirm this directly: near-ideal calibration under severe undersampling, inflation-free operation for every ensemble size, and robustness across 9 noise distributions and 5 orders of magnitude in condition number. The practical payoff: 2 to 3 times accuracy savings, 5 times calibration savings, and concrete operational guidelines — use windows of at least 3, truncation rank kappa equals 1, no inflation needed. The single-sentence summary: spectral regularization produces calibrated uncertainty where stochastic methods cannot.
-->

---

## Limitations and Scope

<div style="border:2.5px solid #c4653a; border-radius:6px; padding:0.5em 0.8em; margin-bottom:0.5em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:1.0em; margin-bottom:0.1em;">Primary gap: perfect-model assumption</div>
<div style="font-size:0.88em; line-height:1.5; color:#3a3024;">
No structural model error — real systems may spread signal across more eigenvalues, potentially requiring larger <span>$\kappa$</span>
</div>
</div>

<div style="display:flex; gap:0.8em;">
<div style="flex:1; border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Dimension</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
Tested at <span>$n=40$</span><br>
Spectral ops: <span>$\mathcal{O}(dN^2)$</span>, independent of <span>$n$</span>
</div>
</div>
<div style="flex:1; border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Observations</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
Linear <span>$\mathbf{H}$</span> in experiments<br>
Nonlinear via ensemble <span>$\mathbf{H}(\mathbf{x})$</span> — untested
</div>
</div>
<div style="flex:1; border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Theory</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
i.i.d. idealization (standard)<br>
Validated by cycling experiments
</div>
</div>
<div style="flex:1; border:2px solid #5a4e40; border-radius:6px; padding:0.4em 0.5em; background:#5a4e4008;">
<div style="font-weight:700; color:#5a4e40; font-size:0.88em; margin-bottom:0.1em;">Test system</div>
<div style="font-size:0.8em; line-height:1.5; color:#3a3024;">
Lorenz-96 (canonical DA benchmark)<br>
13 positive Lyapunov exponents
</div>
</div>
</div>

<div style="margin-top:0.6em; text-align:center; font-size:0.95em; color:#1a7a6d; font-weight:600;">Each limitation has a concrete mitigation path →</div>

<!-- .notes:
Let me be direct about scope. The most important gap is the perfect-model assumption — real systems have model error that could spread signal across more eigenvalues, potentially requiring adaptive kappa. This is the primary open question. The remaining assumptions are standard or bounded. Dimension: spectral operations scale as O-d-N-squared, independent of state dimension n — the algorithm scales, the open question is whether spectral separation persists in richer dynamics. Observations: linear H in all experiments; nonlinear handled implicitly through ensemble evaluation but not systematically tested. The i.i.d. theoretical framework is standard in EnKF convergence literature; cycling experiments over 50 windows validate the predicted scaling. Lorenz-96 is the canonical benchmark — chaotic with 13 positive Lyapunov exponents — but richer systems are needed. Each of these has a concrete path forward, which I address next.
-->

---

## Future Work

<div style="display:flex; gap:0.8em; margin-top:0.3em;">
<div style="flex:1; border:2.5px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:1.0em; margin-bottom:0.15em;">1. Close the main gap</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
<strong>Model error:</strong> systematic + stochastic perturbations<br>
Tests whether spectral separation survives imperfect dynamics — may require adaptive <span>$\kappa$</span>
</div>
</div>
<div style="flex:1; border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:1.0em; margin-bottom:0.15em;">2. Strengthen the method</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
<strong>Adaptive <span>$\kappa$</span>:</strong> data-driven rank selection via spectral gap or energy criteria<br>
<strong>Nonlinear <span>$\mathbf{H}$</span>:</strong> satellite radiances, retrievals
</div>
</div>
<div style="flex:1; border:2px solid #5a7a9a; border-radius:6px; padding:0.5em 0.6em; background:#5a7a9a08;">
<div style="font-weight:700; color:#5a7a9a; font-size:1.0em; margin-bottom:0.15em;">3. Scale and validate</div>
<div style="font-size:0.88em; line-height:1.6; color:#3a3024;">
<strong>Richer dynamics:</strong> quasi-geostrophic, shallow water equations<br>
<strong>Operational scale:</strong> <span>$n \sim 10^6$</span> with localization
</div>
</div>
</div>

<div style="margin-top:0.8em; text-align:center; font-size:0.95em; color:#5a4e40; line-height:1.5; max-width:94%; margin-left:auto; margin-right:auto;">
<strong>Assumption → Method → System:</strong> each step removes a constraint and moves toward operational deployment
</div>

<!-- .notes:
The roadmap has three stages. First, close the main gap: introduce controlled model error — both systematic and stochastic — to test whether spectral separation survives imperfect dynamics. This directly addresses the primary limitation and may motivate adaptive kappa. Second, strengthen the method: develop data-driven rank selection, possibly using the spectral gap itself as a criterion, and extend to nonlinear observation operators like satellite radiances. Third, scale and validate: move to intermediate-complexity models — quasi-geostrophic, shallow water — as a bridge to full systems, then to operational dimensions with n on the order of a million, where the interaction with localization needs careful study. The spectral regularization principle should carry over — the mechanism depends on residual structure, not the specific test system — but proving that requires each of these steps.
-->

---

## Conclusion

<div style="text-align:center; margin-top:0.3em; margin-bottom:0.5em;">
<span style="font-size:1.2em; font-weight:700; color:#1a7a6d;">Deterministic spectral regularization → calibrated uncertainty</span>
</div>

<div style="display:flex; gap:1em; margin-top:0.2em;">
<div style="flex:1; border:2px solid #5a7a9a; border-radius:6px; padding:0.5em 0.6em; background:#5a7a9a08;">
<div style="font-weight:700; color:#5a7a9a; font-size:0.95em; margin-bottom:0.15em;">Mechanism</div>
<div style="font-size:0.88em; line-height:1.55; color:#3a3024;">
Replace stochastic perturbations with spectral projection<br>
Variance: <span>$\mathcal{O}(d/N) \to \mathcal{O}(\kappa/N)$</span><br>
Signal corrected, noise untouched
</div>
</div>
<div style="flex:1; border:2px solid #1a7a6d; border-radius:6px; padding:0.5em 0.6em; background:#1a7a6d08;">
<div style="font-weight:700; color:#1a7a6d; font-size:0.95em; margin-bottom:0.15em;">Evidence</div>
<div style="font-size:0.88em; line-height:1.55; color:#3a3024;">
Calibration: <span>$\bar{\gamma} = 0.81$</span> vs <span>$0.10$</span><br>
RMSE reduced 20%, no inflation needed<br>
Robust: 9 distributions, 5 orders cond(<span>$\mathbf{R}$</span>)
</div>
</div>
<div style="flex:1; border:2px solid #c4653a; border-radius:6px; padding:0.5em 0.6em; background:#c4653a08;">
<div style="font-weight:700; color:#c4653a; font-size:0.95em; margin-bottom:0.15em;">Impact</div>
<div style="font-size:0.88em; line-height:1.55; color:#3a3024;">
5× calibration savings<br>
No tuning parameters<br>
Operational guidelines: <span>$L \geq 3$</span>, <span>$\kappa = 1$</span>
</div>
</div>
</div>

<div style="margin-top:0.8em; text-align:center; max-width:94%; margin-left:auto; margin-right:auto;">
<div style="border-top:2px solid #2c2418; padding-top:0.4em; font-size:1.05em; color:#2c2418; font-weight:700; line-height:1.5;">In the regime of rapid spectral decay and severe undersampling, deterministic spectral regularization provides calibrated uncertainty quantification where stochastic methods cannot.</div>
</div>

<!-- .notes:
The central idea: replace stochastic perturbations with deterministic spectral projection. The mechanism: variance drops from O-d-over-N to O-kappa-over-N because corrections are confined to the signal subspace — noise directions are left untouched. The evidence: spread-skill ratio of 0.81 versus 0.10, 20 percent lower RMSE, no inflation needed, robust across 9 noise distributions and 5 orders of magnitude in condition number. The impact: 5 times calibration savings, no tuning parameters, and concrete operational guidelines. The geometric insight is what ties it together: by correcting only where the data says there is signal, ensemble diversity is preserved where it matters — and that is what produces calibrated spread. The open question: does this persist under model error and at operational scale? The theory and experiments suggest yes. Proving it is the next step. Thank you.
-->

---

<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:70vh;">
<div style="font-size:2.2em; font-weight:700; color:#2c2418; margin-bottom:0.3em;">Thank You</div>
<div style="font-size:1.1em; color:#5a4e40; margin-bottom:2em;">Questions?</div>
<div style="font-size:1.0em; font-weight:600; color:#3a3024;">Rylan Spence</div>
<div style="margin-top:1.5em; font-size:0.8em; color:#1a7a6d;">Code and reproducible experiments available on request</div>
</div>

<!-- .notes:
Thank you. I'm happy to take questions. The code and all experimental configurations are available if you'd like to explore further.
-->
