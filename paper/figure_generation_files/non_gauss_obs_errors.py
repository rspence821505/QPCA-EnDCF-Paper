"""
Non-Gaussian observation errors figure pipeline.

Runs assimilation experiments under 9 non-Gaussian noise distributions
and generates 3 publication figures:
  - noise_distributions.png
  - rmse_trajectories_nongaussian.png
  - mean_rmse_comparison_nongaussian.png

Usage:
    python non_gauss_obs_errors.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
from typing import Callable, Dict, Tuple

from src.models.lorenz96 import Lorenz96
from src.filters.seq_enkf import StochasticEnKF
from src.filters.enkf_4d import StochasticEnKF4D
from src.filters.qpca_endcf import QPCAEnDCF
from src.utils.observations import (
    build_obs_operator,
    generate_truth,
    generate_observations,
    initialize_ensemble,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"

SEEDS = [42, 123, 456]
FILTER_NAMES = ["Seq-EnKF", "4D-EnKF", "QPCA-EnDCF"]


# ---------------------------------------------------------------------------
# Noise generators
# ---------------------------------------------------------------------------


class NoiseGenerator:
    """Non-Gaussian noise distributions with variance matched to Gaussian."""

    @staticmethod
    def gaussian(size: Tuple[int, ...], scale: float = 1.5) -> np.ndarray:
        return np.random.normal(0, scale, size=size)

    @staticmethod
    def student_t(size, df=3.0, scale=1.5):
        t_scale = scale * np.sqrt((df - 2) / df) if df > 2 else scale
        return stats.t.rvs(df=df, scale=t_scale, size=size)

    @staticmethod
    def laplace(size, scale=1.5):
        return np.random.laplace(0, scale / np.sqrt(2), size=size)

    @staticmethod
    def gamma_shifted(size, shape=2.0, scale=1.5):
        gamma_scale = scale / np.sqrt(shape)
        return np.random.gamma(shape, gamma_scale, size=size) - shape * gamma_scale

    @staticmethod
    def lognormal_shifted(size, sigma=0.5, scale=1.5):
        mu = -0.5 * sigma**2
        noise = np.random.lognormal(mu, sigma, size=size)
        mean = np.exp(mu + 0.5 * sigma**2)
        var = (np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)
        return (noise - mean) * (scale / np.sqrt(var))


# 6 distributions for the noise_distributions figure
NOISE_TYPES_VIS = {
    "Gaussian": lambda: NoiseGenerator.gaussian((1000,)),
    "Student-t (df=3)": lambda: NoiseGenerator.student_t((1000,), df=3),
    "Student-t (df=5)": lambda: NoiseGenerator.student_t((1000,), df=5),
    "Laplace": lambda: NoiseGenerator.laplace((1000,)),
    "Gamma (shape=2)": lambda: NoiseGenerator.gamma_shifted((1000,), shape=2),
    "Log-Normal (σ=0.5)": lambda: NoiseGenerator.lognormal_shifted((1000,), sigma=0.5),
}

# 9 distributions for the assimilation experiments
NOISE_CONFIGS = {
    "Gaussian": lambda size, scale: NoiseGenerator.gaussian(size, scale),
    "Student-t (df=3)": lambda size, scale: NoiseGenerator.student_t(size, df=3, scale=scale),
    "Student-t (df=5)": lambda size, scale: NoiseGenerator.student_t(size, df=5, scale=scale),
    "Student-t (df=10)": lambda size, scale: NoiseGenerator.student_t(size, df=10, scale=scale),
    "Laplace": lambda size, scale: NoiseGenerator.laplace(size, scale),
    "Gamma (shape=2)": lambda size, scale: NoiseGenerator.gamma_shifted(size, shape=2, scale=scale),
    "Gamma (shape=5)": lambda size, scale: NoiseGenerator.gamma_shifted(size, shape=5, scale=scale),
    "Log-Normal (σ=0.5)": lambda size, scale: NoiseGenerator.lognormal_shifted(size, sigma=0.5, scale=scale),
    "Log-Normal (σ=0.8)": lambda size, scale: NoiseGenerator.lognormal_shifted(size, sigma=0.8, scale=scale),
}


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_assimilation_experiment(
    noise_generator: Callable,
    n_windows: int = 50,
    L: int = 5,
    N: int = 10,
    kappa: int = 1,
    seed: int = 42,
) -> Dict[str, np.ndarray]:
    """Run DA experiment with specified noise and return RMSE trajectories."""
    rng = np.random.default_rng(seed)

    n, m = 40, 20
    F, dt = 8.0, 0.01
    steps_per_obs = 10
    sigma_obs = 1.5

    H, _ = build_obs_operator(n, 2)
    R = sigma_obs**2 * np.eye(m)

    total_obs = n_windows * L
    x0 = rng.standard_normal(n)
    truth = generate_truth(x0, total_obs, steps_per_obs, dt, F=F, spinup_steps=2000)

    base_obs = generate_observations(truth, H, 0.0, seed=seed)
    observations = base_obs.copy()
    for k in range(total_obs):
        observations[k] += noise_generator((m,), scale=sigma_obs)

    X0 = initialize_ensemble(truth[0], N, seed=seed)

    seq_filter = StochasticEnKF(H, R, stabilize=True)
    enkf_4d = StochasticEnKF4D(H, R, window_len=L)
    qpca_filter = QPCAEnDCF(H, R, window_len=L, k=kappa, stabilize=True)

    rmse_seq, rmse_4d, rmse_qpca = [], [], []
    X_seq, X_4d, X_qpca = X0.copy(), X0.copy(), X0.copy()

    def forecast_ensemble(X, steps):
        X_new = X.copy()
        for j in range(X.shape[1]):
            model = Lorenz96(n=n, F=F, dt=dt)
            model.set_state(X[:, j])
            model.step(steps)
            X_new[:, j] = model.get_state()
        return X_new

    obs_idx = 0
    for w in range(n_windows):
        # Seq-EnKF
        for ell in range(L):
            X_seq = forecast_ensemble(X_seq, steps_per_obs)
            X_seq = seq_filter.update(X_seq, observations[obs_idx], rng)
            obs_idx += 1

        rmse_seq.append(np.sqrt(np.mean(
            (X_seq.mean(axis=1) - truth[w * L + L]) ** 2
        )))

        obs_idx_4d = w * L

        # 4D-EnKF
        X_4d_list = []
        X_temp = X_4d.copy()
        for ell in range(L):
            X_temp = forecast_ensemble(X_temp, steps_per_obs)
            X_4d_list.append(X_temp.copy())

        z_stack = observations[obs_idx_4d : obs_idx_4d + L].flatten()
        X_4d = enkf_4d.update(X_4d_list, z_stack)
        rmse_4d.append(np.sqrt(np.mean(
            (X_4d.mean(axis=1) - truth[w * L + L]) ** 2
        )))

        # QPCA-EnDCF
        X_qpca_list = []
        X_temp = X_qpca.copy()
        for ell in range(L):
            X_temp = forecast_ensemble(X_temp, steps_per_obs)
            X_qpca_list.append(X_temp.copy())

        X_qpca = qpca_filter.update(X_qpca_list, z_stack)
        rmse_qpca.append(np.sqrt(np.mean(
            (X_qpca.mean(axis=1) - truth[w * L + L]) ** 2
        )))

    return {
        "Seq-EnKF": np.array(rmse_seq),
        "4D-EnKF": np.array(rmse_4d),
        "QPCA-EnDCF": np.array(rmse_qpca),
    }


def run_all_experiments():
    """Run experiments for all noise types and seeds. Returns results_all dict."""
    results_all = {}
    total = len(NOISE_CONFIGS) * len(SEEDS)
    count = 0

    for noise_name, noise_func in NOISE_CONFIGS.items():
        results_all[noise_name] = {}
        for seed in SEEDS:
            count += 1
            print(f"  [{count}/{total}] {noise_name}, seed={seed}")
            results_all[noise_name][seed] = run_assimilation_experiment(
                noise_generator=noise_func, seed=seed,
            )

    return results_all


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------


def _save(fig, name, **kwargs):
    defaults = dict(dpi=400, bbox_inches="tight", facecolor="white", edgecolor="none")
    defaults.update(kwargs)
    fig.savefig(OUTPUT_DIR / name, **defaults)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure: noise_distributions.png
# ---------------------------------------------------------------------------


def plot_noise_distributions(noise_samples: Dict[str, np.ndarray]):
    """2x3 histogram panel of 6 noise distributions with Gaussian reference."""
    noise_colors = {
        0: "#2E86AB", 1: "#F18F01", 2: "#029E73",
        3: "#D55E00", 4: "#A23B72", 5: "#949494",
    }

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()

    for idx, (name, noise) in enumerate(noise_samples.items()):
        ax = axes[idx]
        color = noise_colors[idx]

        ax.hist(
            noise, bins=50, density=True, alpha=0.75, color=color,
            edgecolor="#333333", linewidth=1.5, zorder=3,
        )

        x = np.linspace(noise.min(), noise.max(), 300)
        ax.plot(x, stats.norm.pdf(x, 0, 1.5), color="#333333",
                linestyle="--", linewidth=3.0, alpha=0.8, zorder=4)

        mean_val, std_val = np.mean(noise), np.std(noise)
        skew_val = stats.skew(noise)
        ax.text(
            0.97, 0.97,
            f"\u03bc = {mean_val:.3f}\n\u03c3 = {std_val:.3f}\nSkew = {skew_val:.3f}",
            transform=ax.transAxes, fontsize=12, va="top", ha="right",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="white",
                      alpha=0.95, edgecolor="#CCCCCC", linewidth=1.5),
            fontweight="bold", family="monospace", zorder=5,
        )

        ax.set_xlabel("Observation Error Value", fontsize=16, fontweight="bold", labelpad=10)
        ax.set_ylabel("Probability Density", fontsize=16, fontweight="bold", labelpad=10)
        ax.set_title(f"({chr(65 + idx)}) {name}", fontsize=18, fontweight="bold", pad=15)
        ax.grid(True, alpha=0.25, linestyle="-", linewidth=1.0, color="#DDDDDD", zorder=0)
        ax.set_axisbelow(True)

        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontweight("bold")
            lbl.set_fontsize(14)

        ax.minorticks_on()
        ax.tick_params(which="both", direction="in", top=False, right=False)
        ax.tick_params(which="major", length=6, width=1.5)
        ax.tick_params(which="minor", length=4, width=1.0)

    plt.tight_layout(rect=[0, 0, 1, 0.99])
    _save(fig, "noise_distributions.png")


# ---------------------------------------------------------------------------
# Figure: rmse_trajectories_nongaussian.png
# ---------------------------------------------------------------------------


def plot_rmse_trajectories(results_all):
    """3x3 panel of RMSE trajectories for each noise type."""
    filter_styles = {
        "Seq-EnKF": {"color": "#2E86AB", "linestyle": "-", "marker": "o"},
        "4D-EnKF": {"color": "#A23B72", "linestyle": "--", "marker": "s"},
        "QPCA-EnDCF": {"color": "#F18F01", "linestyle": "-.", "marker": "^"},
    }

    fig, axes = plt.subplots(3, 3, figsize=(22, 18))
    axes = axes.flatten()
    n_seeds = len(SEEDS)

    for idx, noise_name in enumerate(NOISE_CONFIGS.keys()):
        ax = axes[idx]

        for filter_name in FILTER_NAMES:
            trajs = np.array([
                results_all[noise_name][seed][filter_name] for seed in SEEDS
            ])
            mean_traj = trajs.mean(axis=0)
            sem_traj = trajs.std(axis=0) / np.sqrt(n_seeds)
            windows = np.arange(1, len(mean_traj) + 1)
            style = filter_styles[filter_name]

            ax.plot(
                windows, mean_traj, color=style["color"],
                linestyle=style["linestyle"], linewidth=3.5,
                label=filter_name, marker=style["marker"],
                markevery=max(1, len(windows) // 12), markersize=9,
                markeredgecolor="white", markeredgewidth=2.0,
                alpha=0.95, zorder=3,
            )
            ax.fill_between(
                windows, mean_traj - 1.96 * sem_traj,
                mean_traj + 1.96 * sem_traj,
                color=style["color"], alpha=0.2, linewidth=0, zorder=2,
            )

        ax.set_xlabel("Assimilation Window", fontsize=16, fontweight="bold", labelpad=10)
        ax.set_ylabel("RMSE", fontsize=16, fontweight="bold", labelpad=10)
        ax.set_title(f"({chr(65 + idx)}) {noise_name}", fontsize=18, fontweight="bold", pad=15)

        leg = ax.legend(
            fontsize=13, loc="best", frameon=True, framealpha=0.95,
            edgecolor="#CCCCCC", fancybox=False, prop={"weight": "bold"},
        )
        leg.get_frame().set_linewidth(1.5)

        ax.grid(True, alpha=0.25, linestyle="-", linewidth=1.0, color="#DDDDDD", zorder=0)
        ax.set_axisbelow(True)
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontweight("bold")
            lbl.set_fontsize(14)

    plt.tight_layout(rect=[0, 0, 1, 0.99])
    _save(fig, "rmse_trajectories_nongaussian.png")


# ---------------------------------------------------------------------------
# Figure: mean_rmse_comparison_nongaussian.png
# ---------------------------------------------------------------------------


def plot_mean_rmse_comparison(results_all):
    """Grouped bar chart of mean RMSE across noise types."""
    filter_styles = {
        "Seq-EnKF": {"color": "#D55E00", "hatch": "///"},
        "4D-EnKF": {"color": "#029E73", "hatch": "\\\\\\"},
        "QPCA-EnDCF": {"color": "#0173B2", "hatch": "xxx"},
    }

    fig, ax = plt.subplots(figsize=(15, 8))

    x = np.arange(len(NOISE_CONFIGS))
    width = 0.25

    for i, filter_name in enumerate(FILTER_NAMES):
        means, stds = [], []
        for noise_name in NOISE_CONFIGS:
            rmse_vals = [
                np.mean(results_all[noise_name][seed][filter_name])
                for seed in SEEDS
            ]
            means.append(np.mean(rmse_vals))
            stds.append(np.std(rmse_vals))

        style = filter_styles[filter_name]
        bars = ax.bar(
            x + i * width, means, width, yerr=stds,
            label=filter_name, color=style["color"], alpha=0.8,
            edgecolor="white", linewidth=1.5, capsize=5,
            error_kw={"linewidth": 2, "elinewidth": 2, "capthick": 2, "alpha": 0.8},
            zorder=3,
        )
        for bar in bars:
            bar.set_hatch(style["hatch"])

    ax.set_xlabel("Observation Error Distribution Type", fontsize=14, fontweight="bold")
    ax.set_ylabel("Mean Root Mean Square Error (RMSE)", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width)
    ax.set_xticklabels(NOISE_CONFIGS.keys(), rotation=45, ha="right", fontweight="bold")
    for lbl in ax.get_yticklabels():
        lbl.set_fontweight("bold")

    ax.legend(
        fontsize=12, loc="upper left", frameon=True, framealpha=0.95,
        edgecolor="black", fancybox=False, prop={"weight": "bold"},
    )
    ax.grid(axis="y", alpha=0.2, linestyle="-", linewidth=0.8, color="gray", zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    _save(fig, "mean_rmse_comparison_nongaussian.png", dpi=300)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    # Fix seed for reproducible noise samples (noise_distributions figure)
    np.random.seed(42)
    noise_samples = {name: gen() for name, gen in NOISE_TYPES_VIS.items()}

    print("Generating noise distributions figure...")
    plot_noise_distributions(noise_samples)

    print("Running assimilation experiments...")
    results_all = run_all_experiments()

    print("Generating RMSE trajectories figure...")
    plot_rmse_trajectories(results_all)

    print("Generating mean RMSE comparison figure...")
    plot_mean_rmse_comparison(results_all)

    expected = [
        "noise_distributions.png",
        "rmse_trajectories_nongaussian.png",
        "mean_rmse_comparison_nongaussian.png",
    ]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
