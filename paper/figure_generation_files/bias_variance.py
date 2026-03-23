"""
Bias-variance decomposition figure pipeline.

Generates 2 publication figures from Monte Carlo filter realizations:
  - bias_variance_evolution.png
  - mse_decomposition_bars.png

Usage:
    python bias_variance.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
from typing import Dict, Tuple
from scipy import linalg

from src.models.lorenz96 import Lorenz96
from src.utils.observations import (
    build_obs_operator,
    generate_truth,
    generate_observations,
)
from src.utils.config import load_experiment_config
from src.config import DIAGNOSTICS_EXPERIMENT_DIR

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"

FILTER_NAMES = ["Seq-EnKF", "4D-EnKF", "QPCA-EnDCF"]


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------


def generate_truth_and_observations(
    config: dict, seed: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate truth trajectory and observations."""
    rng = np.random.default_rng(seed)

    n = config["model"]["n"]
    F = config["model"]["F"]
    dt = config["model"]["dt"]
    spinup = config["model"].get("spinup_steps", 0)
    L = config["assimilation"]["window_length"]
    W = config["assimilation"]["n_windows"]
    K = W * L
    steps_per_obs = config["observations"]["steps_per_obs"]

    x0 = rng.normal(0.0, 1.0, size=n)
    truth = generate_truth(x0, K, steps_per_obs, dt, F=F, spinup_steps=spinup)

    obs_every = config["observations"]["observe_every"]
    H, _ = build_obs_operator(n, obs_every)
    noise_std = config["observations"]["noise_std"]
    observations = generate_observations(truth, H, noise_std, seed=seed)

    return truth, observations, H


# ---------------------------------------------------------------------------
# Filter runners
# ---------------------------------------------------------------------------


def _init_ensemble(truth_0, n, N, rng_seed):
    """Shared ensemble initialization."""
    np.random.seed(rng_seed)
    xi_0 = np.random.randn(n)
    X = np.zeros((n, N))
    for j in range(N):
        xi_j = np.random.randn(n)
        X[:, j] = truth_0 + 0.5 * xi_0 + 0.5 * xi_j
    return X


def run_seq_enkf(config, truth, observations, H, ensemble_seed):
    """Run Sequential EnKF and return analysis trajectory."""
    n = config["model"]["n"]
    m = config["observations"]["m"]
    noise_std = config["observations"]["noise_std"]
    L = config["assimilation"]["window_length"]
    W = config["assimilation"]["n_windows"]
    N = config["assimilation"]["ensemble_size"]
    steps_per_obs = config["observations"]["steps_per_obs"]

    model = Lorenz96(n=n, F=config["model"]["F"], dt=config["model"]["dt"])
    X = _init_ensemble(truth[0], n, N, ensemble_seed)
    R = noise_std**2 * np.eye(m)

    analysis = np.zeros((W + 1, n))
    analysis[0] = X.mean(axis=1)

    obs_idx = 0
    for w in range(W):
        for ell in range(L):
            for step in range(steps_per_obs):
                for j in range(N):
                    model.set_state(X[:, j])
                    X[:, j] = model.step()

            z = observations[obs_idx]
            obs_idx += 1

            x_mean = X.mean(axis=1)
            A_y = H @ X - (H @ X).mean(axis=1)[:, np.newaxis]
            P_xy = ((X - x_mean[:, np.newaxis]) @ A_y.T) / (N - 1)
            S = (A_y @ A_y.T) / (N - 1) + R + 1e-6 * np.eye(m)
            K = P_xy @ linalg.pinv(S)

            for j in range(N):
                epsilon_j = noise_std * np.random.randn(m)
                X[:, j] = X[:, j] + K @ (z + epsilon_j - H @ X[:, j])

        analysis[w + 1] = X.mean(axis=1)

    return analysis


def run_4d_enkf(config, truth, observations, H, ensemble_seed):
    """Run 4D-EnKF and return analysis trajectory."""
    n = config["model"]["n"]
    m = config["observations"]["m"]
    noise_std = config["observations"]["noise_std"]
    L = config["assimilation"]["window_length"]
    W = config["assimilation"]["n_windows"]
    N = config["assimilation"]["ensemble_size"]
    steps_per_obs = config["observations"]["steps_per_obs"]

    model = Lorenz96(n=n, F=config["model"]["F"], dt=config["model"]["dt"])
    X = _init_ensemble(truth[0], n, N, ensemble_seed)
    R = noise_std**2 * np.eye(m)
    R_L = np.kron(np.eye(L), R)

    analysis = np.zeros((W + 1, n))
    analysis[0] = X.mean(axis=1)

    for w in range(W):
        X_window = []
        Y_window = []

        for ell in range(L):
            for step in range(steps_per_obs):
                for j in range(N):
                    model.set_state(X[:, j])
                    X[:, j] = model.step()
            X_window.append(X.copy())
            Y_window.append(H @ X)

        z_stack = observations[w * L : (w + 1) * L].flatten()
        Y_stack = np.vstack(Y_window)
        X_L = X_window[-1]

        x_mean = X_L.mean(axis=1)
        A_x = X_L - x_mean[:, np.newaxis]
        y_mean = Y_stack.mean(axis=1)
        A_y = Y_stack - y_mean[:, np.newaxis]

        P_xy = (A_x @ A_y.T) / (N - 1)
        S = (A_y @ A_y.T) / (N - 1) + R_L + 1e-6 * np.eye(m * L)
        K = P_xy @ linalg.pinv(S)

        for j in range(N):
            epsilon_j = linalg.cholesky(R_L, lower=True) @ np.random.randn(m * L)
            X_L[:, j] = X_L[:, j] + K @ (z_stack + epsilon_j - Y_stack[:, j])

        X = X_L
        analysis[w + 1] = X.mean(axis=1)

    return analysis


def run_qpca_endcf(config, truth, observations, H, ensemble_seed, kappa=1):
    """Run QPCA-EnDCF and return analysis trajectory."""
    n = config["model"]["n"]
    m = config["observations"]["m"]
    noise_std = config["observations"]["noise_std"]
    L = config["assimilation"]["window_length"]
    W = config["assimilation"]["n_windows"]
    N = config["assimilation"]["ensemble_size"]
    steps_per_obs = config["observations"]["steps_per_obs"]

    model = Lorenz96(n=n, F=config["model"]["F"], dt=config["model"]["dt"])
    X = _init_ensemble(truth[0], n, N, ensemble_seed)
    R = noise_std**2 * np.eye(m)
    R_L = np.kron(np.eye(L), R)
    R_L_chol = linalg.cholesky(R_L, lower=True)
    R_L_inv_chol = linalg.solve_triangular(R_L_chol, np.eye(m * L), lower=True)

    analysis = np.zeros((W + 1, n))
    analysis[0] = X.mean(axis=1)

    for w in range(W):
        X_window = []
        Y_window = []

        for ell in range(L):
            for step in range(steps_per_obs):
                for j in range(N):
                    model.set_state(X[:, j])
                    X[:, j] = model.step()
            X_window.append(X.copy())
            Y_window.append(H @ X)

        z_stack = observations[w * L : (w + 1) * L].flatten()
        Y_stack = np.vstack(Y_window)

        E = R_L_inv_chol.T @ (Y_stack - z_stack[:, np.newaxis])
        e_mean = E.mean(axis=1, keepdims=True)
        E_c = E - e_mean

        C_E = (E_c @ E_c.T) / (N - 1)
        eigenvals, eigenvecs = linalg.eigh(C_E)
        idx = np.argsort(eigenvals)[::-1]
        eigenvecs = eigenvecs[:, idx]

        V_kappa = eigenvecs[:, :kappa]
        Q_pca = -V_kappa @ (V_kappa.T @ E)
        Delta_obs = R_L_chol @ Q_pca

        X_L = X_window[-1]
        x_mean = X_L.mean(axis=1)
        A_x = X_L - x_mean[:, np.newaxis]
        y_mean = Y_stack.mean(axis=1)
        A_y = Y_stack - y_mean[:, np.newaxis]

        P_xy = (A_x @ A_y.T) / (N - 1)
        P_yy = (A_y @ A_y.T) / (N - 1)
        S = P_yy + 1e-6 * np.eye(m * L)
        K = P_xy @ linalg.pinv(S)

        X = X_L + K @ Delta_obs
        analysis[w + 1] = X.mean(axis=1)

    return analysis


# ---------------------------------------------------------------------------
# Bias-variance computation
# ---------------------------------------------------------------------------

FILTER_FUNCS = {
    "Seq-EnKF": run_seq_enkf,
    "4D-EnKF": run_4d_enkf,
    "QPCA-EnDCF": run_qpca_endcf,
}


def compute_bias_variance_metrics(config, truth, observations, H, n_mc):
    """Run all filters n_mc times and return bias-variance decomposition."""
    W = config["assimilation"]["n_windows"]
    L = config["assimilation"]["window_length"]
    n = config["model"]["n"]
    truth_windows = truth[::L]  # shape (W+1, n)

    results = {}
    for name, func in FILTER_FUNCS.items():
        print(f"  {name}: ", end="", flush=True)
        realizations = np.empty((n_mc, W + 1, n))
        for i in range(n_mc):
            realizations[i] = func(config, truth, observations, H, 10000 + i)
            if (i + 1) % 5 == 0:
                print(f"{i + 1}", end=" ", flush=True)
        print("done")

        expectation = realizations.mean(axis=0)
        bias = expectation - truth_windows
        bias_squared = bias**2
        variance = ((realizations - expectation[np.newaxis]) ** 2).mean(axis=0)
        mse = ((realizations - truth_windows[np.newaxis]) ** 2).mean(axis=0)

        results[name] = {
            "bias_squared_trace": bias_squared.mean(axis=1),
            "variance_trace": variance.mean(axis=1),
            "mse_trace": mse.mean(axis=1),
        }

    return results


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def _save(fig, name):
    fig.savefig(OUTPUT_DIR / name, bbox_inches="tight", dpi=300)
    plt.close(fig)


def plot_bias_variance_evolution(results_dict: Dict):
    """Stacked area chart: MSE = Bias^2 + Variance per filter."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    colors = {
        "Seq-EnKF": {"primary": "#2E86AB", "secondary": "#1B4965"},
        "4D-EnKF": {"primary": "#F18F01", "secondary": "#C73E1D"},
        "QPCA-EnDCF": {"primary": "#06A77D", "secondary": "#005F73"},
    }

    global_ylim_top = max(
        res["mse_trace"].max() for res in results_dict.values()
    ) * 1.2

    for idx, (name, res) in enumerate(results_dict.items()):
        ax = axes[idx]
        windows = np.arange(len(res["mse_trace"]))

        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        gradient = np.vstack((gradient, gradient))
        ax.imshow(
            gradient,
            extent=[windows[0], windows[-1], ax.get_ylim()[0], ax.get_ylim()[1]],
            aspect="auto", alpha=0.03, cmap="gray", zorder=0,
        )

        ax.fill_between(
            windows, 0, res["bias_squared_trace"],
            alpha=0.7, color=colors[name]["primary"], label="Bias²",
            edgecolor=colors[name]["primary"], linewidth=2, zorder=2,
        )
        ax.fill_between(
            windows, 0, res["bias_squared_trace"],
            alpha=0.2, color="white", zorder=3,
        )
        ax.fill_between(
            windows, res["bias_squared_trace"], res["mse_trace"],
            alpha=0.6, color=colors[name]["secondary"], label="Variance",
            hatch="///", edgecolor=colors[name]["secondary"], linewidth=1.5, zorder=4,
        )
        ax.plot(
            windows, res["bias_squared_trace"],
            color=colors[name]["primary"], linewidth=2, alpha=0.8, zorder=5,
        )
        ax.plot(
            windows, res["mse_trace"],
            color="black", linewidth=3.5, alpha=0.15, zorder=5.5,
        )

        ax.grid(True, alpha=0.25, linestyle="--", linewidth=1.2, color="gray", zorder=1)
        ax.set_axisbelow(True)
        ax.set_xlabel("Assimilation Window", fontsize=13, fontweight="bold", labelpad=10)
        ax.set_ylabel("Error Magnitude", fontsize=13, fontweight="bold", labelpad=10)
        ax.set_title(name, fontsize=15, fontweight="bold", pad=15)

        legend = ax.legend(
            loc="upper right", fontsize=11, framealpha=0.95,
            edgecolor="gray", fancybox=True, shadow=True, frameon=True,
        )
        legend.get_frame().set_linewidth(1.5)
        for text in legend.get_texts():
            text.set_fontweight("bold")

        ax.tick_params(axis="both", which="major", labelsize=11,
                       width=2, length=6, direction="out", pad=8)
        ax.set_ylim(top=global_ylim_top)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight("bold")
        for spine in ax.spines.values():
            spine.set_linewidth(2)
            spine.set_edgecolor("#2a2a2a")

    fig.patch.set_facecolor("white")
    plt.tight_layout(pad=2.0)
    _save(fig, "bias_variance_evolution.png")


def plot_mse_decomposition_bars(results_dict: Dict):
    """Two-panel stacked bar chart: absolute and percentage MSE decomposition."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    bar_colors = {
        "bias": {"main": "#E63946", "gradient": "#F77F00", "shadow": "#8B1E3F"},
        "variance": {"main": "#457B9D", "gradient": "#1D3557", "shadow": "#2C5F7E"},
    }

    filter_names = list(results_dict.keys())
    x = np.arange(len(filter_names))
    width = 0.65
    shadow_offset = 0.02

    bias2_means = [results_dict[f]["bias_squared_trace"].mean() for f in filter_names]
    var_means = [results_dict[f]["variance_trace"].mean() for f in filter_names]
    mse_means = [results_dict[f]["mse_trace"].mean() for f in filter_names]

    # --- Panel 1: Absolute values ---
    ax1 = axes[0]

    ax1.imshow(
        [[0, 0], [1, 1]],
        extent=[x[0] - 0.5, x[-1] + 0.5, ax1.get_ylim()[0], ax1.get_ylim()[1]],
        aspect="auto", alpha=0.03, cmap="gray", zorder=0,
    )

    for i, (b, v) in enumerate(zip(bias2_means, var_means)):
        ax1.bar(x[i] + shadow_offset, b, width, color="black", alpha=0.15, zorder=1)
        ax1.bar(x[i] + shadow_offset, v, width, bottom=b, color="black", alpha=0.15, zorder=1)

    bars_bias = ax1.bar(
        x, bias2_means, width, label="Bias²",
        color=bar_colors["bias"]["main"], alpha=0.9,
        edgecolor=bar_colors["bias"]["shadow"], linewidth=2.5, zorder=2,
    )
    bars_var = ax1.bar(
        x, var_means, width, bottom=bias2_means, label="Variance",
        color=bar_colors["variance"]["main"], alpha=0.9,
        edgecolor=bar_colors["variance"]["shadow"], linewidth=2.5, zorder=2,
    )

    for bar_b, bar_v in zip(bars_bias, bars_var):
        for bar, key in [(bar_b, "bias"), (bar_v, "variance")]:
            bbox = bar.get_bbox()
            ax1.add_patch(Rectangle(
                (bbox.x0, bbox.y0), bbox.width, bbox.height,
                facecolor=bar_colors[key]["gradient"], alpha=0.2,
                edgecolor="none", zorder=3,
            ))

    ax1.set_ylabel("Mean Error Component", fontsize=14, fontweight="bold", labelpad=12)
    ax1.set_title("MSE Decomposition (Absolute)", fontsize=16, fontweight="bold", pad=20, color="#1a1a1a")
    ax1.set_xticks(x)
    ax1.set_xticklabels(filter_names, fontsize=12, fontweight="bold")

    legend1 = ax1.legend(loc="upper right", fontsize=12, framealpha=0.95,
                         edgecolor="gray", fancybox=True, shadow=True, frameon=True)
    legend1.get_frame().set_linewidth(2)
    for text in legend1.get_texts():
        text.set_fontweight("bold")

    ax1.grid(True, alpha=0.25, axis="y", linestyle="--", linewidth=1.2, color="gray", zorder=1)
    ax1.set_axisbelow(True)

    for i, (b, v) in enumerate(zip(bias2_means, var_means)):
        for val, y_pos, edge_col in [(b, b / 2, bar_colors["bias"]["shadow"]),
                                     (v, b + v / 2, bar_colors["variance"]["shadow"])]:
            ax1.text(
                i, y_pos, f"{val:.3f}", ha="center", va="center",
                fontsize=11, fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor=edge_col, alpha=0.9, linewidth=2),
            )

    ax1.tick_params(axis="both", which="major", width=2, length=6, pad=8)
    for label in ax1.get_xticklabels() + ax1.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
        spine.set_edgecolor("#2a2a2a")

    # --- Panel 2: Percentage values ---
    ax2 = axes[1]

    ax2.imshow(
        [[0, 0], [1, 1]],
        extent=[x[0] - 0.5, x[-1] + 0.5, 0, 100],
        aspect="auto", alpha=0.03, cmap="gray", zorder=0,
    )

    bias2_pct = [100 * b / m for b, m in zip(bias2_means, mse_means)]
    var_pct = [100 * v / m for v, m in zip(var_means, mse_means)]

    for i, (b, v) in enumerate(zip(bias2_pct, var_pct)):
        ax2.bar(x[i] + shadow_offset, b, width, color="black", alpha=0.15, zorder=1)
        ax2.bar(x[i] + shadow_offset, v, width, bottom=b, color="black", alpha=0.15, zorder=1)

    bars_bias_pct = ax2.bar(
        x, bias2_pct, width, label="Bias²",
        color=bar_colors["bias"]["main"], alpha=0.9,
        edgecolor=bar_colors["bias"]["shadow"], linewidth=2.5, zorder=2,
    )
    bars_var_pct = ax2.bar(
        x, var_pct, width, bottom=bias2_pct, label="Variance",
        color=bar_colors["variance"]["main"], alpha=0.9,
        edgecolor=bar_colors["variance"]["shadow"], linewidth=2.5, zorder=2,
    )

    for bar_b, bar_v in zip(bars_bias_pct, bars_var_pct):
        for bar, key in [(bar_b, "bias"), (bar_v, "variance")]:
            bbox = bar.get_bbox()
            ax2.add_patch(Rectangle(
                (bbox.x0, bbox.y0), bbox.width, bbox.height,
                facecolor=bar_colors[key]["gradient"], alpha=0.2,
                edgecolor="none", zorder=3,
            ))

    ax2.set_ylabel("Contribution to MSE (%)", fontsize=14, fontweight="bold", labelpad=12)
    ax2.set_title("MSE Decomposition (Percentage)", fontsize=16, fontweight="bold", pad=20, color="#1a1a1a")
    ax2.set_xticks(x)
    ax2.set_xticklabels(filter_names, fontsize=12, fontweight="bold")
    ax2.set_ylim(top=120)

    legend2 = ax2.legend(loc="upper right", fontsize=12, framealpha=0.95,
                         edgecolor="gray", fancybox=True, shadow=True, frameon=True)
    legend2.get_frame().set_linewidth(2)
    for text in legend2.get_texts():
        text.set_fontweight("bold")

    ax2.grid(True, alpha=0.25, axis="y", linestyle="--", linewidth=1.2, color="gray", zorder=1)
    ax2.set_axisbelow(True)

    for i, (b, v) in enumerate(zip(bias2_pct, var_pct)):
        for val, y_pos, edge_col, fmt in [
            (b, b / 2, bar_colors["bias"]["shadow"], "{:.1f}%"),
            (v, b + v / 2, bar_colors["variance"]["shadow"], "{:.1f}%"),
        ]:
            ax2.text(
                i, y_pos, fmt.format(val), ha="center", va="center",
                fontsize=11, fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor=edge_col, alpha=0.9, linewidth=2),
            )

    ax2.tick_params(axis="both", which="major", width=2, length=6, pad=8)
    for label in ax2.get_xticklabels() + ax2.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
        spine.set_edgecolor("#2a2a2a")

    fig.patch.set_facecolor("white")
    plt.tight_layout(pad=2.5)
    _save(fig, "mse_decomposition_bars.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    config = load_experiment_config(
        DIAGNOSTICS_EXPERIMENT_DIR / "bias_variance_analysis.yaml"
    )

    seed = config["experiment"]["seeds"][0]
    n_mc = config["bias_variance"]["n_monte_carlo"]

    print(f"Generating truth/observations (seed={seed})...")
    truth, observations, H = generate_truth_and_observations(config, seed)

    print(f"Running bias-variance decomposition ({n_mc} MC realizations)...")
    results = compute_bias_variance_metrics(config, truth, observations, H, n_mc)

    print("Generating figures...")
    plot_bias_variance_evolution(results)
    plot_mse_decomposition_bars(results)

    expected = ["bias_variance_evolution.png", "mse_decomposition_bars.png"]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
