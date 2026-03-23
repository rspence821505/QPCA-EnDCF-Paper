"""
Ensemble spread analysis figure pipeline.

Generates 5 publication figures from baseline experiment results:
  - reliability_diagrams.png
  - spread_vs_rmse_temporal.png
  - spread_skill_ratio.png
  - combined_calibration_analysis.png
  - rank_histograms.png

Usage:
    python ensemble_spread.py
"""

import pickle
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.config import BASELINE_EXPERIMENT_DIR, BASELINE_RESULTS_DIR
from src.utils.config import load_experiment_config
from src.utils.metrics import compute_rank_histogram

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
RESULTS_ARCHIVE = BASELINE_RESULTS_DIR / "lorenz96_baseline.yaml"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"

FILTERS = ["seq_enkf", "enkf_4d", "qpca_endcf"]
FILTER_LABELS = {
    "seq_enkf": "Seq-EnKF",
    "enkf_4d": "4D-EnKF",
    "qpca_endcf": "QPCA-EnDCF",
}
COLORS = {
    "seq_enkf": "#2E86AB",
    "enkf_4d": "#A23B72",
    "qpca_endcf": "#F18F01",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_data(config: dict) -> Dict[str, List[dict]]:
    """Load all per-filter/seed results from the baseline archive."""
    if not RESULTS_ARCHIVE.exists():
        raise FileNotFoundError(f"Baseline archive not found: {RESULTS_ARCHIVE}")

    with RESULTS_ARCHIVE.open("rb") as f:
        archive = pickle.load(f)

    seeds = config["experiment"]["seeds"]
    all_results: Dict[str, List[dict]] = {f: [] for f in FILTERS}

    for filter_name in FILTERS:
        filter_key = FILTER_LABELS[filter_name]
        if filter_key not in archive["all_results"]:
            raise ValueError(f"Unknown filter '{filter_name}' in archive")

        results_by_seed = archive["all_results"][filter_key]
        for seed_idx in range(len(seeds)):
            if seed_idx >= len(results_by_seed):
                raise ValueError(
                    f"Archive missing results for {filter_key} at seed index {seed_idx}"
                )
            all_results[filter_name].append(results_by_seed[seed_idx])

    return all_results


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------


def compute_metrics(
    all_results: Dict[str, List[dict]], config: dict
) -> dict:
    """Compute all intermediate metrics needed across figures.

    Returns a dict with:
      spread_stats, rmse_stats  — per-filter temporal statistics
      rank_histograms           — per-filter rank histograms
      ratio_per_window          — per-filter array of shape (n_seeds, n_windows)
    """
    n_ensemble = config["assimilation"]["ensemble_size"]
    window_len = config["assimilation"]["window_length"]
    n_windows = config["assimilation"]["n_windows"]

    spread_stats = {}
    rmse_stats = {}
    rank_histograms = {}
    ratio_per_window = {}

    for fname in FILTERS:
        # --- temporal stats ---
        spreads = [r["spread"] for r in all_results[fname]]
        rmses = [r["rmse"] for r in all_results[fname]]

        spread_stats[fname] = {
            "mean": np.mean(spreads, axis=0),
            "q25": np.percentile(spreads, 25, axis=0),
            "q75": np.percentile(spreads, 75, axis=0),
        }
        rmse_stats[fname] = {
            "mean": np.mean(rmses, axis=0),
            "q25": np.percentile(rmses, 25, axis=0),
            "q75": np.percentile(rmses, 75, axis=0),
        }

        # --- spread-skill ratio per window ---
        ratios = []
        for results in all_results[fname]:
            spread = np.asarray(results["spread"], dtype=float).ravel()
            rmse = np.asarray(results["rmse"], dtype=float).ravel()
            min_len = min(spread.size, rmse.size)
            if min_len == 0:
                continue
            spread, rmse = spread[:min_len], rmse[:min_len]

            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = np.divide(
                    spread, rmse, out=np.zeros_like(spread), where=rmse != 0
                )

            if fname == "seq_enkf":
                expected_len = n_windows * window_len
                if ratio.size < expected_len:
                    continue
                ratio = ratio[:expected_len].reshape(n_windows, window_len).mean(axis=1)
            else:
                if ratio.size < n_windows:
                    continue
                ratio = ratio[:n_windows]

            ratios.append(ratio)

        if ratios:
            ratio_per_window[fname] = np.stack(ratios, axis=0)

        # --- rank histograms ---
        total_histogram = np.zeros(n_ensemble + 1)
        for results in all_results[fname]:
            truth = results.get("truth")
            ensemble = results.get("ensemble")
            if truth is None or ensemble is None:
                continue
            total_histogram += compute_rank_histogram(
                truth, ensemble, n_bins=n_ensemble + 1
            )
        rank_histograms[fname] = total_histogram

    return {
        "spread_stats": spread_stats,
        "rmse_stats": rmse_stats,
        "rank_histograms": rank_histograms,
        "ratio_per_window": ratio_per_window,
    }


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------


def _style_ax(ax, xlabel, ylabel, fontsize=20):
    """Apply common axis styling."""
    ax.set_xlabel(xlabel, fontweight="bold", fontsize=fontsize, labelpad=12)
    ax.set_ylabel(ylabel, fontweight="bold", fontsize=fontsize, labelpad=12)
    ax.grid(True, alpha=0.25, linestyle="-", linewidth=1.0, color="#DDDDDD", zorder=0)
    ax.set_axisbelow(True)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(16)


def _style_legend(ax, **kwargs):
    """Apply common legend styling."""
    defaults = dict(
        frameon=True, fancybox=False, edgecolor="#CCCCCC",
        framealpha=0.95, fontsize=15, loc="best",
    )
    defaults.update(kwargs)
    leg = ax.legend(**defaults)
    for text in leg.get_texts():
        text.set_fontweight("bold")
    leg.get_frame().set_linewidth(1.5)
    return leg


def _save(fig, name):
    """Save figure to output directory."""
    fig.savefig(
        OUTPUT_DIR / name,
        dpi=400, bbox_inches="tight", facecolor="white", edgecolor="none",
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure: spread_vs_rmse_temporal
# ---------------------------------------------------------------------------


def plot_spread_vs_rmse_temporal(spread_stats, rmse_stats):
    """Temporal evolution of spread and RMSE with IQR bands."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    x = np.arange(spread_stats["qpca_endcf"]["mean"].shape[0])

    for fname in FILTERS:
        label = FILTER_LABELS[fname]
        color = COLORS[fname]

        rmse_mean = np.asarray(rmse_stats[fname]["mean"]).reshape(-1)
        rmse_q25 = np.asarray(rmse_stats[fname]["q25"]).reshape(-1)
        rmse_q75 = np.asarray(rmse_stats[fname]["q75"]).reshape(-1)
        spread_mean = np.asarray(spread_stats[fname]["mean"]).reshape(-1)
        spread_q25 = np.asarray(spread_stats[fname]["q25"]).reshape(-1)
        spread_q75 = np.asarray(spread_stats[fname]["q75"]).reshape(-1)

        if fname == "seq_enkf":
            rmse_mean, rmse_q25, rmse_q75 = rmse_mean[::5], rmse_q25[::5], rmse_q75[::5]
            spread_mean, spread_q25, spread_q75 = (
                spread_mean[::5], spread_q25[::5], spread_q75[::5],
            )

        markevery = max(1, len(x) // 15)
        ax.plot(
            x, rmse_mean, label=f"{label} RMSE", color=color,
            linewidth=3.5, linestyle="--", alpha=0.85,
            marker="s", markersize=6, markevery=markevery,
            markeredgewidth=1.5, markeredgecolor="white", zorder=3,
        )
        ax.fill_between(x, rmse_q25, rmse_q75, alpha=0.12, color=color, zorder=1)

        ax.plot(
            x, spread_mean, label=f"{label} Spread", color=color,
            linewidth=3.5, linestyle="-", alpha=0.95,
            markersize=6, markevery=markevery,
            markeredgewidth=1.5, markeredgecolor="white", zorder=4,
        )
        ax.fill_between(x, spread_q25, spread_q75, alpha=0.2, color=color, zorder=2)

    _style_ax(ax, "Assimilation Window", "Value")
    _style_legend(ax, ncol=2, columnspacing=1.5, handlelength=3.0, fontsize=14)

    plt.tight_layout()
    _save(fig, "spread_vs_rmse_temporal.png")


# ---------------------------------------------------------------------------
# Figure: reliability_diagrams
# ---------------------------------------------------------------------------


def plot_reliability_diagrams(all_results):
    """Scatter of ensemble spread vs RMSE with 1:1 calibration line."""
    fig, ax = plt.subplots(1, 1, figsize=(11, 9))
    global_max = 0

    for fname in FILTERS:
        color = COLORS[fname]
        spread_chunks, rmse_chunks = [], []
        for results in all_results[fname]:
            spread_chunks.append(np.ravel(np.asarray(results["spread"])))
            rmse_chunks.append(np.ravel(np.asarray(results["rmse"])))
        if not spread_chunks:
            continue

        all_spreads = np.concatenate(spread_chunks)
        all_rmses = np.concatenate(rmse_chunks)
        global_max = max(global_max, all_spreads.max(), all_rmses.max())

        ax.scatter(
            all_spreads, all_rmses, alpha=0.6, s=50, color=color,
            edgecolors="white", linewidth=0.5, label=FILTER_LABELS[fname], zorder=3,
        )

    ax.plot(
        [0, global_max], [0, global_max], color="#333333", linestyle="--",
        linewidth=3.5, label="Perfect Calibration (1:1)", zorder=2, alpha=0.8,
    )
    margin = 0.05
    ax.fill_between(
        [0, global_max],
        [0, global_max * (1 - margin)],
        [0, global_max * (1 + margin)],
        color="#666666", alpha=0.08, zorder=1,
    )

    _style_ax(ax, "Ensemble Spread", "RMSE")
    _style_legend(ax, loc="lower right", markerscale=1.5)
    ax.set_aspect("equal", adjustable="box")

    plt.tight_layout()
    _save(fig, "reliability_diagrams.png")


# ---------------------------------------------------------------------------
# Figure: spread_skill_ratio
# ---------------------------------------------------------------------------


def plot_spread_skill_ratio(ratio_per_window, config):
    """Spread/RMSE ratio time series with uncertainty bands."""
    fig, ax = plt.subplots(figsize=(12, 9))
    n_windows = config["assimilation"]["n_windows"]
    window_indices = np.arange(1, n_windows + 1)

    for fname in FILTERS:
        if fname not in ratio_per_window:
            continue
        ratios = ratio_per_window[fname]
        mean_ratio = ratios.mean(axis=0)
        std_ratio = ratios.std(axis=0)

        ax.plot(
            window_indices, mean_ratio, label=FILTER_LABELS[fname],
            color=COLORS[fname], linewidth=3.5, markersize=8,
            markeredgewidth=2, markeredgecolor="white", alpha=0.95, zorder=3,
        )
        ax.fill_between(
            window_indices, mean_ratio - std_ratio, mean_ratio + std_ratio,
            alpha=0.2, color=COLORS[fname], zorder=2,
        )

    ax.axhline(y=1, color="#333333", linestyle="--", linewidth=3.0,
               label="Perfect Calibration", alpha=0.8, zorder=1)
    ax.axhspan(0.95, 1.05, color="#666666", alpha=0.08, zorder=0)

    _style_ax(ax, "Assimilation Window", "Spread / RMSE Ratio")
    _style_legend(ax)
    ax.set_ylim([0, 2])

    plt.tight_layout()
    _save(fig, "spread_skill_ratio.png")


# ---------------------------------------------------------------------------
# Figure: combined_calibration_analysis
# ---------------------------------------------------------------------------


def plot_combined_calibration(all_results, ratio_per_window, config):
    """Two-panel figure: (A) spread-skill ratio, (B) reliability diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 9))
    fig.patch.set_facecolor("white")

    n_windows = config["assimilation"]["n_windows"]
    window_indices = np.arange(1, n_windows + 1)

    # --- Panel A: spread-skill ratio ---
    for fname in FILTERS:
        if fname not in ratio_per_window:
            continue
        ratios = ratio_per_window[fname]
        mean_ratio = ratios.mean(axis=0)
        std_ratio = ratios.std(axis=0)

        ax1.plot(
            window_indices, mean_ratio, label=FILTER_LABELS[fname],
            color=COLORS[fname], linewidth=3.5, markersize=8,
            markeredgewidth=2, markeredgecolor="white", alpha=0.95, zorder=3,
        )
        ax1.fill_between(
            window_indices, mean_ratio - std_ratio, mean_ratio + std_ratio,
            alpha=0.2, color=COLORS[fname], zorder=2,
        )

    ax1.axhline(y=1, color="#333333", linestyle="--", linewidth=3.0,
                label="Perfect Calibration", alpha=0.8, zorder=1)
    ax1.axhspan(0.95, 1.05, color="#666666", alpha=0.08, zorder=0)
    _style_ax(ax1, "Assimilation Window", "Spread / RMSE Ratio")
    _style_legend(ax1)
    ax1.set_ylim([0, 2])
    ax1.text(0.0, 1.05, "(A)", transform=ax1.transAxes,
             fontsize=24, fontweight="bold", va="top", ha="left")

    # --- Panel B: reliability diagram ---
    global_max = 0
    for fname in FILTERS:
        spread_chunks, rmse_chunks = [], []
        for results in all_results[fname]:
            spread_chunks.append(np.ravel(np.asarray(results["spread"])))
            rmse_chunks.append(np.ravel(np.asarray(results["rmse"])))
        if not spread_chunks:
            continue

        all_spreads = np.concatenate(spread_chunks)
        all_rmses = np.concatenate(rmse_chunks)
        global_max = max(global_max, all_spreads.max(), all_rmses.max())

        ax2.scatter(
            all_spreads, all_rmses, alpha=0.6, s=50, color=COLORS[fname],
            edgecolors="white", linewidth=0.5, label=FILTER_LABELS[fname], zorder=3,
        )

    ax2.plot(
        [0, global_max], [0, global_max], color="#333333", linestyle="--",
        linewidth=3.5, label="Perfect Calibration (1:1)", zorder=2, alpha=0.8,
    )
    _style_ax(ax2, "Ensemble Spread", "RMSE")
    _style_legend(ax2, loc="lower right", markerscale=1.5)
    ax2.set_aspect("equal", adjustable="box")
    ax2.text(0.0, 1.05, "(B)", transform=ax2.transAxes,
             fontsize=24, fontweight="bold", va="top", ha="left")

    plt.tight_layout()
    _save(fig, "combined_calibration_analysis.png")


# ---------------------------------------------------------------------------
# Figure: rank_histograms
# ---------------------------------------------------------------------------


def plot_rank_histograms(rank_hists, n_ensemble):
    """Three-panel rank histogram with chi-square uniformity test annotations."""
    fig = plt.figure(figsize=(18, 6))
    gs = fig.add_gridspec(1, 3, hspace=0.35, wspace=0.35)

    for i, fname in enumerate(FILTERS):
        ax = fig.add_subplot(gs[i])
        histogram = rank_hists[fname]
        n_samples = histogram.sum()
        expected_count = n_samples / (n_ensemble + 1)

        bins = np.arange(n_ensemble + 1)
        bars = ax.bar(
            bins, histogram, color=COLORS[fname], alpha=0.85,
            edgecolor="#1B1111", linewidth=2.5, zorder=3,
        )
        for bar in bars:
            bar.set_edgecolor("#1B1111")
            bar.set_linewidth(3.5)

        ci_upper = expected_count + 1.96 * np.sqrt(expected_count)
        ci_lower = expected_count - 1.96 * np.sqrt(expected_count)
        ax.axhspan(ci_lower, ci_upper, alpha=0.12, color="#666666",
                   label="95% CI (uniform)", zorder=1)
        ax.axhline(y=expected_count, color="#333333", linestyle="--",
                   linewidth=3.0, label="Expected (uniform)", zorder=2, alpha=0.8)

        ax.set_xlabel("Rank Bin", fontweight="bold", fontsize=18, labelpad=10)
        if i == 0:
            ax.set_ylabel("Frequency", fontweight="bold", fontsize=18, labelpad=10)
        ax.set_title(FILTER_LABELS[fname], fontweight="bold", fontsize=20, pad=15)

        leg = ax.legend(
            loc="upper center", frameon=True, fancybox=False,
            edgecolor="#CCCCCC", framealpha=0.95, fontsize=13,
        )
        for text in leg.get_texts():
            text.set_fontweight("bold")
        leg.get_frame().set_linewidth(1.5)

        ax.grid(True, alpha=0.25, axis="y", linestyle="-", linewidth=1.0,
                color="#DDDDDD", zorder=0)
        ax.set_axisbelow(True)
        ax.set_xticks(bins)
        ax.set_xticklabels([str(b) for b in bins], fontweight="bold", fontsize=14)
        for lbl in ax.get_yticklabels():
            lbl.set_fontweight("bold")
            lbl.set_fontsize(14)
        ax.set_ylim([0, max(histogram.max(), ci_upper) * 1.15])

    plt.tight_layout()
    _save(fig, "rank_histograms.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Setup
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    # Load
    config = load_experiment_config(
        BASELINE_EXPERIMENT_DIR / "lorenz96_baseline.yaml"
    )
    all_results = load_data(config)

    # Compute all metrics once
    metrics = compute_metrics(all_results, config)
    n_ensemble = config["assimilation"]["ensemble_size"]

    # Generate figures
    plot_spread_vs_rmse_temporal(
        metrics["spread_stats"], metrics["rmse_stats"],
    )
    plot_reliability_diagrams(all_results)
    plot_spread_skill_ratio(metrics["ratio_per_window"], config)
    plot_combined_calibration(all_results, metrics["ratio_per_window"], config)
    plot_rank_histograms(metrics["rank_histograms"], n_ensemble)

    # Verify outputs
    expected = [
        "reliability_diagrams.png",
        "spread_vs_rmse_temporal.png",
        "spread_skill_ratio.png",
        "combined_calibration_analysis.png",
        "rank_histograms.png",
    ]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
