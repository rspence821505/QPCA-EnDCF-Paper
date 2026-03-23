"""
Window length sensitivity figure pipeline.

Runs assimilation experiments across window lengths [1,3,5,7,10,15] for
three filters (Seq-EnKF, 4D-EnKF, QPCA-EnDCF) and generates 1 figure:
  - combined_window_rmse_analysis.png

Usage:
    python window_length.py
"""

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.config import PAPER_FIGURES_DIR
from src.filters.enkf_4d import StochasticEnKF4D
from src.filters.qpca_endcf import QPCAEnDCF as QPCA_Filter
from src.filters.seq_enkf import StochasticEnKF
from src.models.lorenz96 import Lorenz96
from src.utils.config import load_experiment_config
from src.utils.metrics import compute_ensemble_spread, compute_rmse, compute_relative_misfit
from src.utils.observations import (
    _propagate_ensemble,
    build_obs_operator,
    multiplicative_inflation,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"
CONFIG_PATH = PROJECT_ROOT / "experiments" / "sensitivity" / "window_length.yaml"

FILTER_KEYS = ["seq_enkf", "4d_enkf", "qpca_endcf"]
FILTER_LABELS = {"seq_enkf": "Seq-EnKF", "4d_enkf": "4D-EnKF", "qpca_endcf": "QPCA-EnDCF"}


# ---------------------------------------------------------------------------
# Filter wrappers
# ---------------------------------------------------------------------------


class _SeqEnKF:
    def __init__(self, ensemble, H, R, model_params, inflation=1.0,
                 stabilize=True, seed=None):
        self.ensemble = ensemble.copy()
        self.H, self.R = H, R
        self.dt, self.F = model_params["dt"], model_params["F"]
        self.inflation = inflation
        self.filter = StochasticEnKF(H, R, stabilize=stabilize)
        self.rng = np.random.default_rng(seed)

    def forecast(self, steps_per_obs):
        _propagate_ensemble(self.ensemble, steps_per_obs, self.dt, self.F)
        multiplicative_inflation(self.ensemble, self.inflation)

    def analysis(self, z):
        self.ensemble = self.filter.update(self.ensemble, z, rng=self.rng)

    def get_ensemble_mean(self):
        return self.ensemble.mean(axis=1)


class _FourDEnKF:
    def __init__(self, ensemble, H, R, window_length, model_params,
                 inflation=1.0, stabilize=True, seed=None):
        self.ensemble = ensemble.copy()
        self.H, self.R = H, R
        self.window_length = window_length
        self.dt, self.F = model_params["dt"], model_params["F"]
        self.inflation = inflation
        self.filter = StochasticEnKF4D(H, R, window_len=window_length)
        self.rng = np.random.default_rng(seed)
        self._path = None

    def forecast_window(self, steps_per_obs):
        path = []
        for _ in range(self.window_length):
            _propagate_ensemble(self.ensemble, steps_per_obs, self.dt, self.F)
            multiplicative_inflation(self.ensemble, self.inflation)
            path.append(self.ensemble.copy())
        self._path = path

    def analysis_4d(self, obs_window):
        z_stack = obs_window.reshape(-1)
        if self.rng is not None:
            np.random.seed(self.rng.integers(0, 2**32 - 1))
        self.ensemble = self.filter.update(self._path, z_stack)
        self._path = None

    def get_ensemble_mean(self):
        return self.ensemble.mean(axis=1)


class _QPCAEnDCF:
    def __init__(self, ensemble, H, R, window_length, model_params,
                 k=1, stabilize=True, inflation=1.0, seed=None):
        self.ensemble = ensemble.copy()
        self.H, self.R = H, R
        self.window_length = window_length
        self.dt, self.F = model_params["dt"], model_params["F"]
        self.inflation = inflation
        self.filter = QPCA_Filter(H, R, window_len=window_length, k=k, stabilize=stabilize)
        self.rng = np.random.default_rng(seed)
        self._path = None

    def forecast_window(self, steps_per_obs):
        path = []
        for _ in range(self.window_length):
            _propagate_ensemble(self.ensemble, steps_per_obs, self.dt, self.F)
            multiplicative_inflation(self.ensemble, self.inflation)
            path.append(self.ensemble.copy())
        self._path = path

    def analysis_4d(self, obs_window):
        z_stack = obs_window.reshape(-1)
        self.ensemble = self.filter.update(self._path, z_stack)
        self._path = None

    def get_ensemble_mean(self):
        return self.ensemble.mean(axis=1)


# ---------------------------------------------------------------------------
# Experiment helpers
# ---------------------------------------------------------------------------


def _generate_truth_and_obs(config, seed):
    """Generate truth trajectory and observations."""
    np.random.seed(seed)
    n = config["model"]["n"]
    m = config["observations"]["m"]
    K = config["assimilation"]["total_observations"]
    noise_std = config["observations"]["noise_std"]
    steps_per_obs = config["observations"]["steps_per_obs"]

    model = Lorenz96(n=n, F=config["model"]["F"], dt=config["model"]["dt"])
    x0 = np.random.randn(n)
    model.set_state(x0)
    for _ in range(config["model"]["spinup_steps"]):
        model.step()

    truth = np.zeros((K, n))
    for k in range(K):
        for _ in range(steps_per_obs):
            model.step()
        truth[k] = model.get_state()

    H = np.zeros((m, n))
    for i in range(m):
        H[i, 2 * i] = 1.0

    R = noise_std**2 * np.eye(m)
    observations = (H @ truth.T).T + np.random.randn(K, m) * noise_std

    return truth, observations, H, R


def _init_ensemble(truth, N, seed):
    np.random.seed(seed + 1000)
    n = truth.shape[1]
    xi_0 = np.random.randn(n)
    X0 = np.zeros((n, N))
    for j in range(N):
        X0[:, j] = truth[0] + 0.5 * xi_0 + 0.5 * np.random.randn(n)
    return X0


def _run_filter(filter_class, filter_name, X0, truth, observations,
                H, R, L, model_params, filter_params, steps_per_obs):
    """Run one filter and return mean RMSE."""
    K = len(observations)

    if filter_name == "seq_enkf":
        num_windows = K
        fobj = filter_class(
            ensemble=X0.copy(), H=H, R=R, model_params=model_params,
            inflation=filter_params["inflation"], stabilize=filter_params["stabilize"],
        )
    else:
        num_windows = K // L
        fobj = filter_class(
            ensemble=X0.copy(), H=H, R=R, window_length=L,
            model_params=model_params, **filter_params,
        )

    n = X0.shape[0]
    analyses = np.zeros((num_windows, n))

    if filter_name == "seq_enkf":
        for k in range(K):
            fobj.forecast(steps_per_obs)
            fobj.analysis(observations[k])
            analyses[k] = fobj.get_ensemble_mean()
        truth_at = truth
    else:
        for w in range(num_windows):
            obs_window = observations[w * L : (w + 1) * L]
            fobj.forecast_window(steps_per_obs)
            fobj.analysis_4d(obs_window)
            analyses[w] = fobj.get_ensemble_mean()
        truth_at = truth[L - 1 :: L][:num_windows]

    rmse = compute_rmse(analyses, truth_at)
    return np.mean(rmse)


# ---------------------------------------------------------------------------
# Run all experiments
# ---------------------------------------------------------------------------


def run_all_experiments(config):
    """Run window length sensitivity experiments, return summary_stats."""
    model_params = {
        "n": config["model"]["n"],
        "F": config["model"]["F"],
        "dt": config["model"]["dt"],
    }
    window_lengths = config["window_lengths"]
    seeds = config["experiment"]["seeds"]
    N = config["assimilation"]["ensemble_size"]
    steps_per_obs = config["observations"]["steps_per_obs"]

    # results[filter][L] = list of mean RMSE per seed
    results_rmse = {k: {L: [] for L in window_lengths} for k in FILTER_KEYS}

    filter_classes = {
        "seq_enkf": _SeqEnKF,
        "4d_enkf": _FourDEnKF,
        "qpca_endcf": _QPCAEnDCF,
    }

    total = len(seeds) * len(window_lengths) * 3
    count = 0

    for seed in seeds:
        truth, observations, H, R = _generate_truth_and_obs(config, seed)
        X0 = _init_ensemble(truth, N, seed)

        for L in window_lengths:
            for fname in FILTER_KEYS:
                count += 1
                mean_rmse = _run_filter(
                    filter_classes[fname], fname, X0, truth, observations,
                    H, R, L, model_params, config["filters"][fname], steps_per_obs,
                )
                results_rmse[fname][L].append(mean_rmse)
                print(f"  [{count}/{total}] seed={seed}, L={L}, {fname}: RMSE={mean_rmse:.4f}")

    # Aggregate into summary stats
    summary = {fname: {"mean": [], "std": []} for fname in FILTER_KEYS}
    for fname in FILTER_KEYS:
        for L in window_lengths:
            vals = results_rmse[fname][L]
            summary[fname]["mean"].append(np.mean(vals))
            summary[fname]["std"].append(np.std(vals))

    return summary, window_lengths


# ---------------------------------------------------------------------------
# Figure: combined_window_rmse_analysis.png
# ---------------------------------------------------------------------------


def plot_combined_window_rmse_analysis(summary, window_lengths):
    """Two-panel figure: (A) RMSE vs L, (B) RMSE improvement bars."""
    filter_colors = {"seq_enkf": "#2E86AB", "4d_enkf": "#A23B72", "qpca_endcf": "#F18F01"}
    filter_markers = {"seq_enkf": "o", "4d_enkf": "s", "qpca_endcf": "^"}
    bar_colors = {"vs_seq": "#27AE60", "vs_4d": "#E67E22"}

    plt.rcParams["font.family"] = "serif"
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(16, 7),
        gridspec_kw={"width_ratios": [1.5, 1]},
        constrained_layout=True,
    )
    fig.set_constrained_layout_pads(w_pad=0.05, h_pad=0.05, wspace=0.15)
    fig.patch.set_facecolor("white")

    # --- Panel A: RMSE vs window length ---
    for fname in FILTER_KEYS:
        means = summary[fname]["mean"]
        stds = summary[fname]["std"]
        ax1.plot(
            window_lengths, means, label=FILTER_LABELS[fname],
            marker=filter_markers[fname], color=filter_colors[fname],
            linewidth=3.0, markersize=10, markeredgewidth=2.0,
            markeredgecolor="white", alpha=0.95, zorder=3,
        )
        ax1.fill_between(
            window_lengths, np.array(means) - np.array(stds),
            np.array(means) + np.array(stds),
            alpha=0.18, color=filter_colors[fname], zorder=2,
        )

    ax1.set_xlabel(r"Window Length $L$", fontsize=14, fontweight="bold", labelpad=10)
    ax1.set_ylabel(r"RMSE", fontsize=14, fontweight="bold", labelpad=10)
    for lbl in ax1.get_xticklabels() + ax1.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(15)
    ax1.legend(
        loc="upper right", fontsize=17, frameon=True, fancybox=False,
        edgecolor="black", framealpha=0.98, shadow=True,
        prop={"weight": "bold"}, borderpad=0.8,
    )
    ax1.grid(True, alpha=0.25, linewidth=0.8, linestyle="--", zorder=1)
    ax1.set_axisbelow(True)
    ax1.set_xticks(window_lengths)
    ax1.minorticks_on()
    ax1.tick_params(which="major", length=6, width=1.5, labelsize=15)
    ax1.tick_params(which="minor", length=3, width=1.0)
    ax1.text(0.0, 1.07, "(A)", transform=ax1.transAxes,
             fontsize=24, fontweight="bold", va="top", ha="left")

    # --- Panel B: RMSE improvement bars ---
    qpca = np.array(summary["qpca_endcf"]["mean"])
    seq = np.array(summary["seq_enkf"]["mean"])
    enkf4d = np.array(summary["4d_enkf"]["mean"])

    imp_vs_seq = (seq - qpca) / seq * 100
    imp_vs_4d = (enkf4d - qpca) / enkf4d * 100

    x = np.arange(len(window_lengths))
    width = 0.38

    bars1 = ax2.bar(
        x - width / 2, imp_vs_seq, width, label="vs Seq-EnKF",
        color=bar_colors["vs_seq"], alpha=0.9, edgecolor="white",
        linewidth=1.5, zorder=3,
    )
    bars2 = ax2.bar(
        x + width / 2, imp_vs_4d, width, label="vs 4D-EnKF",
        color=bar_colors["vs_4d"], alpha=0.9, edgecolor="white",
        linewidth=1.5, zorder=3,
    )
    for bar in bars1:
        bar.set_hatch("//")
    for bar in bars2:
        bar.set_hatch("\\\\")

    def _add_labels(ax, bars, values, color):
        for bar, v in zip(bars, values):
            xc = bar.get_x() + bar.get_width() / 2.0
            y = bar.get_height()
            offset = 4 if v >= 0 else -6
            ax.annotate(
                f"{v:.0f}%", xy=(xc, y), xytext=(0, offset),
                textcoords="offset points", ha="center",
                va="bottom" if v >= 0 else "top",
                fontsize=14, fontweight="bold", color=color,
                clip_on=False, zorder=10,
            )

    _add_labels(ax2, bars1, imp_vs_seq, bar_colors["vs_seq"])
    _add_labels(ax2, bars2, imp_vs_4d, bar_colors["vs_4d"])

    ax2.axhline(0, color="black", linewidth=2.0, alpha=0.8, zorder=2)
    ax2.set_xlabel(r"Window Length $L$", fontsize=14, fontweight="bold", labelpad=10)
    ax2.set_ylabel(r"RMSE Improvement (\%)", fontsize=14, fontweight="bold", labelpad=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(L) for L in window_lengths], fontweight="bold", fontsize=15)
    for lbl in ax2.get_yticklabels():
        lbl.set_fontweight("bold")
        lbl.set_fontsize(15)
    ax2.legend(
        loc="lower right", fontsize=17, frameon=True, fancybox=False,
        edgecolor="black", framealpha=0.98, shadow=True,
        prop={"weight": "bold"}, borderpad=0.8,
    )
    ax2.grid(True, alpha=0.25, axis="y", linewidth=0.8, linestyle="--", zorder=1)
    ax2.set_axisbelow(True)
    ax2.tick_params(which="major", length=6, width=1.5)
    ax2.tick_params(which="minor", length=3, width=1.0)
    ax2.text(0.0, 1.07, "(B)", transform=ax2.transAxes,
             fontsize=24, fontweight="bold", va="top", ha="left")

    ymin, ymax = ax2.get_ylim()
    pad = 0.08 * (ymax - ymin)
    ax2.set_ylim(ymin - pad, ymax + pad)

    fig.savefig(
        OUTPUT_DIR / "combined_window_rmse_analysis.png",
        dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none",
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")

    config = load_experiment_config(str(CONFIG_PATH))

    print("Running window length sensitivity experiments...")
    summary, window_lengths = run_all_experiments(config)

    print("Generating figure...")
    plot_combined_window_rmse_analysis(summary, window_lengths)

    path = OUTPUT_DIR / "combined_window_rmse_analysis.png"
    if not path.exists():
        raise RuntimeError(f"Expected output missing: {path}")

    print(f"Figure written to {path}")


if __name__ == "__main__":
    main()
