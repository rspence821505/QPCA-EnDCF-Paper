"""
Ensemble size study figure pipeline.

Runs ensemble-size experiments for three filters (Seq-EnKF, 4D-EnKF,
QPCA-EnDCF) on Lorenz-96 and generates 3 publication figures:
  - performance_degradation.png
  - performance_zone_timeline_enhanced.png
  - fig_ensemble_size_spread_skill.png

Usage:
    python ensemble_size.py
"""

import time
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.patches import FancyBboxPatch, Rectangle
from numpy.linalg import svd

from src.config import PAPER_FIGURES_DIR
from src.filters.enkf_4d import StochasticEnKF4D
from src.filters.qpca_endcf import QPCAEnDCF
from src.filters.seq_enkf import StochasticEnKF
from src.models.lorenz96 import integrate_model, l96_rhs, rk4_step
from src.utils.linalg import sym_posdef_inverse
from src.utils.metrics import rel_data_misfit, rmse
from src.utils.observations import build_obs_operator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"

# Lorenz-96 parameters
N_STATE = 40
OBSERVE_EVERY = 2
F_PARAM = 8.0
DT_MODEL = 0.01
STEPS_PER_OBS = 10

# Assimilation parameters
WINDOW_LEN = 5
N_WINDOWS = 50
OBS_NOISE_STD = 1.5
QPCA_K = 1

# Ensemble size study parameters
ENSEMBLE_SIZES = [5, 10, 15, 20, 30, 50, 100]
SEEDS = [42, 123, 456]
INFLATION_FACTOR = 1.05
QPCA_INFLATION = 1.0

FILTER_KEYS = ["seq", "enkf4d", "qpca4d"]
FILTER_LABELS = {"seq": "Seq-EnKF", "enkf4d": "4D-EnKF", "qpca4d": "QPCA-EnDCF"}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _apply_inflation(X, factor):
    if factor == 1.0:
        return X
    x_mean = X.mean(axis=1, keepdims=True)
    return x_mean + factor * (X - x_mean)


def _ensemble_spread(X):
    return np.sqrt(np.mean(np.var(X, axis=1, ddof=1)))


def _generate_truth_and_obs(seed):
    rng = np.random.default_rng(seed)
    K_total = N_WINDOWS * WINDOW_LEN
    steps_total = K_total * STEPS_PER_OBS

    x0 = rng.normal(0.0, 1.0, size=N_STATE)
    truth_traj = integrate_model(x0, DT_MODEL, steps_total, F=F_PARAM)
    obs_steps = np.arange(STEPS_PER_OBS, steps_total + 1, STEPS_PER_OBS)
    truth_at_obs = truth_traj[obs_steps]

    H, _ = build_obs_operator(N_STATE, OBSERVE_EVERY)
    m = H.shape[0]
    Z = np.empty((K_total, m))
    for k in range(K_total):
        Z[k] = H @ truth_at_obs[k] + OBS_NOISE_STD * rng.standard_normal(m)

    return truth_at_obs, Z, H, rng


def _create_initial_ensemble(truth_at_obs, N_ens, rng):
    n = truth_at_obs.shape[1]
    x0 = truth_at_obs[0]
    return (x0 + 0.5 * rng.standard_normal(n))[:, None] + 0.5 * rng.standard_normal(
        (n, N_ens)
    )


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_experiment(seed, N_ens):
    """Run one ensemble-size experiment and return per-window metrics."""
    H, _ = build_obs_operator(N_STATE, OBSERVE_EVERY)
    m = H.shape[0]
    R = OBS_NOISE_STD**2 * np.eye(m)
    R_inv_sqrt = np.linalg.cholesky(sym_posdef_inverse(R))

    truth_at_obs, Z, H, rng = _generate_truth_and_obs(seed)
    X0 = _create_initial_ensemble(truth_at_obs, N_ens, rng)

    seq_enkf = StochasticEnKF(H, R, stabilize=False)
    enkf4d = StochasticEnKF4D(H, R, window_len=WINDOW_LEN)
    qpca4d = QPCAEnDCF(H, R, window_len=WINDOW_LEN, k=QPCA_K, stabilize=True)

    results = {k: {"rmse": [], "spread": []} for k in FILTER_KEYS}

    X_seq, X_enkf4d, X_qpca4d = X0.copy(), X0.copy(), X0.copy()

    obs_ptr = 0
    for w in range(N_WINDOWS):
        # --- Sequential EnKF ---
        for ell in range(WINDOW_LEN):
            for _ in range(STEPS_PER_OBS):
                for j in range(N_ens):
                    X_seq[:, j] = rk4_step(l96_rhs, X_seq[:, j], DT_MODEL, F=F_PARAM)
            X_seq = seq_enkf.update(X_seq, Z[obs_ptr + ell], rng=rng)
            X_seq = _apply_inflation(X_seq, INFLATION_FACTOR)

        # --- 4D-EnKF ---
        X_path_4d = []
        for ell in range(WINDOW_LEN):
            for _ in range(STEPS_PER_OBS):
                for j in range(N_ens):
                    X_enkf4d[:, j] = rk4_step(
                        l96_rhs, X_enkf4d[:, j], DT_MODEL, F=F_PARAM
                    )
            X_path_4d.append(X_enkf4d.copy())

        z_stack = Z[obs_ptr : obs_ptr + WINDOW_LEN].reshape(-1)
        X_enkf4d = enkf4d.update(X_path_4d, z_stack)
        X_enkf4d = _apply_inflation(X_enkf4d, INFLATION_FACTOR)

        # --- QPCA-EnDCF ---
        X_path_qpca = []
        for ell in range(WINDOW_LEN):
            for _ in range(STEPS_PER_OBS):
                for j in range(N_ens):
                    X_qpca4d[:, j] = rk4_step(
                        l96_rhs, X_qpca4d[:, j], DT_MODEL, F=F_PARAM
                    )
            X_path_qpca.append(X_qpca4d.copy())

        X_qpca4d = qpca4d.update(X_path_qpca, z_stack)
        X_qpca4d = _apply_inflation(X_qpca4d, QPCA_INFLATION)

        obs_ptr += WINDOW_LEN

        # --- Metrics ---
        x_true = truth_at_obs[obs_ptr - 1]
        for fname, X in [
            ("seq", X_seq),
            ("enkf4d", X_enkf4d),
            ("qpca4d", X_qpca4d),
        ]:
            xm = X.mean(axis=1)
            results[fname]["rmse"].append(rmse(xm, x_true))
            results[fname]["spread"].append(_ensemble_spread(X))

    for fname in FILTER_KEYS:
        for metric in results[fname]:
            results[fname][metric] = np.array(results[fname][metric])

    return results


# ---------------------------------------------------------------------------
# Aggregate experiments
# ---------------------------------------------------------------------------


def run_all_experiments():
    """Run all ensemble-size experiments and return aggregated statistics."""
    # Raw storage: ensemble_results[filter][N_ens][metric] = list of per-seed means
    ensemble_results = {
        k: {N: {"rmse": [], "spread": []} for N in ENSEMBLE_SIZES}
        for k in FILTER_KEYS
    }

    total = len(ENSEMBLE_SIZES) * len(SEEDS)
    count = 0
    for N_ens in ENSEMBLE_SIZES:
        for seed in SEEDS:
            results = run_experiment(seed, N_ens)
            for fname in FILTER_KEYS:
                for metric in ["rmse", "spread"]:
                    ensemble_results[fname][N_ens][metric].append(
                        results[fname][metric].mean()
                    )
            count += 1
            print(f"  [{count}/{total}] N={N_ens}, seed={seed} done")

    # Compute mean/std statistics
    ensemble_stats = {k: {} for k in FILTER_KEYS}
    for fname in FILTER_KEYS:
        for N_ens in ENSEMBLE_SIZES:
            ensemble_stats[fname][N_ens] = {}
            for metric in ["rmse", "spread"]:
                vals = ensemble_results[fname][N_ens][metric]
                ensemble_stats[fname][N_ens][metric] = {
                    "mean": np.mean(vals),
                    "std": np.std(vals),
                }

    # Compute spread-skill ratios
    spread_skill_ratios = {}
    for fname in FILTER_KEYS:
        spread_skill_ratios[fname] = []
        for N_ens in ENSEMBLE_SIZES:
            sp = ensemble_stats[fname][N_ens]["spread"]["mean"]
            rm = ensemble_stats[fname][N_ens]["rmse"]["mean"]
            spread_skill_ratios[fname].append(sp / rm if rm > 0 else 0.0)

    return ensemble_stats, spread_skill_ratios


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------


def _save(fig, name):
    fig.savefig(OUTPUT_DIR / name, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure: performance_degradation.png
# ---------------------------------------------------------------------------


def plot_performance_degradation(ensemble_stats):
    """Two-panel: absolute RMSE (log) + relative degradation vs N=100."""
    filters_cfg = {
        "seq": {"label": "Seq-EnKF", "color": "#E74C3C", "marker": "o"},
        "enkf4d": {"label": "4D-EnKF", "color": "#3498DB", "marker": "s"},
        "qpca4d": {"label": "QPCA-EnDCF", "color": "#2ECC71", "marker": "^"},
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # --- Left: Absolute RMSE ---
    for fname, props in filters_cfg.items():
        rmse_vals = [ensemble_stats[fname][N]["rmse"]["mean"] for N in ENSEMBLE_SIZES]
        rmse_std = [ensemble_stats[fname][N]["rmse"]["std"] for N in ENSEMBLE_SIZES]
        ax1.errorbar(
            ENSEMBLE_SIZES, rmse_vals, yerr=rmse_std,
            label=props["label"], color=props["color"], marker=props["marker"],
            markersize=10, capsize=5, linewidth=2.5,
            markeredgewidth=2, markeredgecolor="white",
        )

    ax1.set_xlabel("Ensemble Size (N)", fontweight="bold", fontsize=14)
    ax1.set_ylabel("RMSE ", fontweight="bold", fontsize=14)
    ax1.grid(True, alpha=0.3, linestyle="--", linewidth=0.8, which="both")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xticks(ENSEMBLE_SIZES)
    ax1.set_xticklabels([str(n) for n in ENSEMBLE_SIZES])
    ax1.text(0.0, 1.05, "(A)", transform=ax1.transAxes,
             fontsize=18, fontweight="bold", va="top", ha="left")
    for lbl in ax1.get_xticklabels() + ax1.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(12)

    # --- Right: Relative degradation ---
    for fname, props in filters_cfg.items():
        baseline = ensemble_stats[fname][100]["rmse"]["mean"]
        degradation = [
            max((ensemble_stats[fname][N]["rmse"]["mean"] - baseline) / baseline * 100, 0.1)
            for N in ENSEMBLE_SIZES
        ]
        ax2.plot(
            ENSEMBLE_SIZES, degradation, color=props["color"],
            marker=props["marker"], markersize=10, linewidth=2.5,
            markeredgewidth=2, markeredgecolor="white",
        )

    ax2.axhspan(0.1, 5, alpha=0.2, color="#BCD100", label="Excellent (<5%)")
    ax2.axhspan(5, 15, alpha=0.2, color="#9370DB", label="Good (5-15%)")
    ax2.axhspan(15, 30, alpha=0.2, color="#FF8C69", label="Acceptable (15-30%)")
    ax2.axhspan(30, 100, alpha=0.2, color="#8B4513", label="Poor (>30%)")
    ax2.axhline(y=1, color="black", linestyle="--", linewidth=1.5, alpha=0.5)

    ax2.set_xlabel("Ensemble Size (N)", fontweight="bold", fontsize=14)
    ax2.set_ylabel("Performance Degradation (%)", fontweight="bold", fontsize=14)
    ax2.set_ylim([0.1, 800])
    zone_handles, zone_labels = ax2.get_legend_handles_labels()
    ax2.legend(zone_handles, zone_labels, loc="upper right", framealpha=0.95, edgecolor="black")
    ax2.grid(True, alpha=0.3, linestyle="--", linewidth=0.8, which="both")
    ax2.set_xscale("log")
    ax2.set_yscale("symlog", linthresh=1)
    ax2.set_xticks(ENSEMBLE_SIZES)
    ax2.set_xticklabels([str(n) for n in ENSEMBLE_SIZES])
    for lbl in ax2.get_xticklabels() + ax2.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(12)
    ax2.text(0.0, 1.05, "(B)", transform=ax2.transAxes,
             fontsize=18, fontweight="bold", va="top", ha="left")

    # Shared methods legend below subplots
    method_handles, method_labels = ax1.get_legend_handles_labels()
    fig.tight_layout(rect=[0, 0.12, 1, 1])
    legend_methods = fig.legend(
        method_handles, method_labels, loc="lower center",
        ncol=3, framealpha=0.95, fontsize=12, bbox_to_anchor=(0.5, 0.02),
    )
    legend_methods.get_title().set_fontweight("bold")
    legend_methods.get_frame().set_edgecolor("black")

    _save(fig, "performance_degradation.png")


# ---------------------------------------------------------------------------
# Figure: performance_zone_timeline_enhanced.png
# ---------------------------------------------------------------------------


def plot_performance_zone_timeline_enhanced(ensemble_stats):
    """Enhanced heatmap-style timeline of performance zones per filter/N."""
    filters_cfg = {
        "seq": {"label": "Seq-EnKF", "color": "#E63946"},
        "enkf4d": {"label": "4D-EnKF", "color": "#457B9D"},
        "qpca4d": {"label": "QPCA-EnDCF", "color": "#2A9D8F"},
    }
    y_positions = {"seq": 2, "enkf4d": 1, "qpca4d": 0}
    zone_colors = {
        "excellent": "#06D6A0",
        "good": "#4CC9F0",
        "acceptable": "#FFB627",
        "poor": "#F72585",
    }

    fig, ax = plt.subplots(figsize=(16, 9), facecolor="#F8F9FA")
    ax.set_facecolor("#FFFFFF")

    for fname, props in filters_cfg.items():
        y_pos = y_positions[fname]
        color = props["color"]
        baseline = ensemble_stats[fname][100]["rmse"]["mean"]

        for i, N in enumerate(ENSEMBLE_SIZES):
            degradation = max(
                (ensemble_stats[fname][N]["rmse"]["mean"] - baseline) / baseline * 100,
                0.1,
            )

            if degradation < 5:
                zc, zn = zone_colors["excellent"], "excellent"
            elif degradation < 15:
                zc, zn = zone_colors["good"], "good"
            elif degradation < 30:
                zc, zn = zone_colors["acceptable"], "acceptable"
            else:
                zc, zn = zone_colors["poor"], "poor"

            # Shadow
            ax.add_patch(FancyBboxPatch(
                (i - 0.38, y_pos - 0.33), 0.76, 0.66,
                boxstyle="round,pad=0.08", facecolor="black",
                edgecolor="none", linewidth=0, alpha=0.15, zorder=1,
            ))
            # Main box
            ax.add_patch(FancyBboxPatch(
                (i - 0.4, y_pos - 0.35), 0.8, 0.7,
                boxstyle="round,pad=0.08", facecolor=zc,
                edgecolor=color, linewidth=2.8, alpha=0.9, zorder=2,
            ))
            # Inner glow
            ax.add_patch(FancyBboxPatch(
                (i - 0.38, y_pos - 0.33), 0.76, 0.66,
                boxstyle="round,pad=0.08", facecolor="none",
                edgecolor="white", linewidth=1.5, alpha=0.4, zorder=3,
            ))

            text_color = "#1A1A1A" if zn != "poor" else "white"
            txt = ax.text(
                i, y_pos, f"{degradation:.0f}%", ha="center", va="center",
                fontweight="bold", fontsize=11, color=text_color, zorder=4,
            )
            txt.set_path_effects([
                patheffects.Stroke(
                    linewidth=3,
                    foreground="white" if text_color == "#1A1A1A" else "black",
                    alpha=0.3,
                ),
                patheffects.Normal(),
            ])

    ax.set_xlim(-0.6, len(ENSEMBLE_SIZES) - 0.4)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xticks(range(len(ENSEMBLE_SIZES)))
    ax.set_xticklabels(
        [str(n) for n in ENSEMBLE_SIZES], fontweight="600", fontsize=12, color="#2C3E50",
    )
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(
        [filters_cfg[k]["label"] for k in y_positions],
        fontweight="600", fontsize=13, color="#2C3E50",
    )
    ax.set_xlabel(
        "Ensemble Size (N)", fontweight="bold", fontsize=15, color="#2C3E50", labelpad=12,
    )

    legend_elements = [
        mpatches.Patch(facecolor=zone_colors["excellent"], label="Excellent (<5%)",
                       edgecolor="#2C3E50", linewidth=1.5, alpha=0.9),
        mpatches.Patch(facecolor=zone_colors["good"], label="Good (5\u201315%)",
                       edgecolor="#2C3E50", linewidth=1.5, alpha=0.9),
        mpatches.Patch(facecolor=zone_colors["acceptable"], label="Acceptable (15\u201330%)",
                       edgecolor="#2C3E50", linewidth=1.5, alpha=0.9),
        mpatches.Patch(facecolor=zone_colors["poor"], label="Poor (>30%)",
                       edgecolor="#2C3E50", linewidth=1.5, alpha=0.9),
    ]
    legend = ax.legend(
        handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, -0.12),
        fontsize=11, framealpha=0.97, edgecolor="#BDC3C7", fancybox=True,
        shadow=True, title="Performance Zones", title_fontsize=12, ncol=4,
    )
    legend.get_frame().set_facecolor("#F8F9FA")
    legend.get_title().set_fontweight("bold")
    legend.get_title().set_color("#2C3E50")

    ax.grid(True, alpha=0.15, axis="x", linestyle="--", linewidth=1, color="#95A5A6")
    ax.grid(True, alpha=0.08, axis="y", linestyle="--", linewidth=1, color="#95A5A6")
    for spine in ax.spines.values():
        spine.set_edgecolor("#BDC3C7")
        spine.set_linewidth(1.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for fname, y_pos in y_positions.items():
        ax.add_patch(Rectangle(
            (-0.6, y_pos - 0.45), len(ENSEMBLE_SIZES) + 0.2, 0.9,
            facecolor=filters_cfg[fname]["color"], alpha=0.03, zorder=0, edgecolor="none",
        ))

    plt.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "performance_zone_timeline_enhanced.png",
        dpi=300, bbox_inches="tight", facecolor="#F8F9FA",
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure: fig_ensemble_size_spread_skill.png
# ---------------------------------------------------------------------------


def plot_ensemble_size_spread_skill(spread_skill_ratios):
    """Spread-skill ratio vs ensemble size for all filters."""
    fig, ax = plt.subplots(figsize=(12, 7))

    colors = {"seq": "#2E86AB", "enkf4d": "#A23B72", "qpca4d": "#F18F01"}
    markers = {"seq": "o", "enkf4d": "s", "qpca4d": "D"}

    for fname in FILTER_KEYS:
        ax.plot(
            ENSEMBLE_SIZES, spread_skill_ratios[fname],
            marker=markers[fname], color=colors[fname],
            label=FILTER_LABELS[fname], linewidth=3.5, markersize=12,
            markeredgewidth=2.5, markeredgecolor="white", alpha=0.95, zorder=3,
        )

    ax.axhline(1.0, color="#666666", linestyle="--", linewidth=2.5,
               alpha=0.7, label="Ideal Calibration", zorder=2)
    ax.axhspan(0.95, 1.05, color="#666666", alpha=0.08, zorder=1)

    ax.set_xlabel("Ensemble Size", fontsize=20, fontweight="bold", labelpad=12)
    ax.set_ylabel("Spread-Skill Ratio", fontsize=20, fontweight="bold", labelpad=12)

    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(16)

    ax.legend(
        fontsize=15, frameon=True, fancybox=False, shadow=False,
        framealpha=0.95, edgecolor="#CCCCCC", loc="best",
        prop={"weight": "bold"},
    )

    ax.grid(True, alpha=0.25, linewidth=1.0, color="#DDDDDD", zorder=0)
    ax.set_xscale("log")
    ax.set_xticks(ENSEMBLE_SIZES)
    ax.set_xticklabels([str(n) for n in ENSEMBLE_SIZES])
    ax.set_ylim([0, 2])

    plt.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "fig_ensemble_size_spread_skill.png",
        dpi=400, bbox_inches="tight", facecolor="white", edgecolor="none",
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    np.random.seed(42)

    print("Running ensemble size experiments...")
    ensemble_stats, spread_skill_ratios = run_all_experiments()

    print("Generating figures...")
    plot_performance_degradation(ensemble_stats)
    plot_performance_zone_timeline_enhanced(ensemble_stats)
    plot_ensemble_size_spread_skill(spread_skill_ratios)

    expected = [
        "performance_degradation.png",
        "performance_zone_timeline_enhanced.png",
        "fig_ensemble_size_spread_skill.png",
    ]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
