"""
Correlated observation errors figure pipeline.

Generates 2 publication figures:
  - correlation_structures.png   (heatmaps of 3 R matrices)
  - reconstruction_errors.png    (dumbbell plot of QPCA vs 4D-EnKF)

Usage:
    python correlated_obs.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "paper" / "final_figures"
STYLE_FILE = PROJECT_ROOT / "notebooks" / "publication_style.mplstyle"


# ---------------------------------------------------------------------------
# Correlation matrix generation
# ---------------------------------------------------------------------------


def generate_obs_error_covariance(m, sigma_obs=1.5, correlation_type="exponential",
                                   length_scale=5.0):
    """Generate observation error covariance R with spatial correlation."""
    positions = np.linspace(0, 2 * np.pi, m, endpoint=False)

    distances = np.zeros((m, m))
    period = 2 * np.pi
    for i in range(m):
        for j in range(m):
            diff = abs(positions[i] - positions[j])
            distances[i, j] = min(diff, period - diff)

    if correlation_type == "exponential":
        C = np.exp(-distances / length_scale)
    elif correlation_type == "gaussian":
        C = np.exp(-(distances / length_scale) ** 2)
    elif correlation_type == "ar1":
        rho = np.exp(-1.0 / length_scale)
        C = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                C[i, j] = rho ** abs(i - j)
    else:
        raise ValueError(f"Unknown correlation type: {correlation_type}")

    R = sigma_obs**2 * C
    R = 0.5 * (R + R.T)
    w, V = np.linalg.eigh(R)
    w = np.maximum(w, 1e-4)
    R = (V * w) @ V.T
    return R


# ---------------------------------------------------------------------------
# Figure: correlation_structures.png
# ---------------------------------------------------------------------------


def plot_correlation_structures():
    """Heatmaps of 3 observation error covariance structures."""
    m = 20
    R_exp = generate_obs_error_covariance(m, correlation_type="exponential", length_scale=3.0)
    R_gauss = generate_obs_error_covariance(m, correlation_type="gaussian", length_scale=3.0)
    R_ar1 = generate_obs_error_covariance(m, correlation_type="ar1", length_scale=3.0)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor="white")
    cmap = "RdYlBu_r"

    titles = ["Exponential Correlation", "Gaussian Correlation", "Diagonal Correlation"]
    matrices = [R_exp, R_gauss, R_ar1]

    for ax, R, title in zip(axes, matrices, titles):
        im = ax.imshow(R, cmap=cmap, aspect="auto", interpolation="bilinear")
        ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Observation Index", fontsize=12, fontweight="bold")
        ax.set_ylabel("Observation Index", fontsize=12, fontweight="bold")
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=10)
        for lbl in cbar.ax.get_yticklabels():
            lbl.set_fontweight("bold")
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontweight("bold")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUTPUT_DIR / "correlation_structures.png",
                dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure: reconstruction_errors.png
# ---------------------------------------------------------------------------


def plot_reconstruction_errors():
    """Dumbbell plot comparing QPCA-EnDCF vs 4D-EnKF RMSE across correlation types."""
    plt.rcParams.update({
        "font.family": "serif", "font.size": 11, "font.weight": "bold",
        "axes.labelweight": "bold", "axes.titleweight": "bold",
        "axes.labelsize": 12, "axes.titlesize": 13,
        "xtick.labelsize": 11, "ytick.labelsize": 11,
        "figure.facecolor": "white", "axes.linewidth": 1.5,
    })

    correlations = ["Diagonal", "Exponential (\u2113=4)", "Gaussian (\u2113=4)"]
    qpca_rmse = [3.47, 3.71, 3.65]
    enkf_rmse = [4.64, 4.93, 5.35]
    improvements = [-25.2, -24.7, -31.9]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(correlations))

    for i, (q, e) in enumerate(zip(qpca_rmse, enkf_rmse)):
        ax.plot([q, e], [i, i], "o-", linewidth=3, markersize=10,
                color="#34495e", alpha=0.6, zorder=1)
        ax.scatter(q, i, s=200, c="#2ecc71", edgecolor="black", linewidth=2,
                   zorder=3, label="QPCA-Cholesky" if i == 0 else "")
        ax.scatter(e, i, s=200, c="#e74c3c", edgecolor="black", linewidth=2,
                   zorder=3, label="4D-EnKF" if i == 0 else "")

        mid_x = (q + e) / 2
        ax.text(mid_x, i + 0.15, f"{improvements[i]:.1f}%", ha="center", va="bottom",
                fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

    ax.set_yticks(y_pos)
    ax.set_yticklabels(correlations, fontsize=11)
    ax.set_xlabel("RMSE", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(axis="x", alpha=0.3)
    ax.set_ylim(-0.5, len(correlations) - 0.5)
    ax.invert_yaxis()

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "reconstruction_errors.png",
                dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    plot_correlation_structures()
    plot_reconstruction_errors()

    expected = ["correlation_structures.png", "reconstruction_errors.png"]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
