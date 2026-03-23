"""
Inflation study figure pipeline.

Runs multiplicative and additive inflation experiments across ensemble
sizes [5, 10, 20] for three filters and generates 2 publication figures:
  - inflation_multiplicative_20.png
  - inflation_additive_20.png

Usage:
    python inflation_study.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky

from src.filters.enkf_4d import StochasticEnKF4D
from src.filters.qpca_endcf import QPCAEnDCF
from src.filters.seq_enkf import StochasticEnKF
from src.models.lorenz96 import integrate_model, l96_rhs, rk4_step
from src.utils.linalg import sym_posdef_inverse
from src.utils.metrics import rmse
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
WINDOW_LEN = 5
N_WINDOWS = 50
OBS_NOISE_STD = 1.5
QPCA_K = 1

# Inflation study parameters
MULT_FACTORS = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25]
ADD_LEVELS = [0, 0.01, 0.05, 0.1, 0.15, 0.2]
ENSEMBLE_SIZES = [5, 10, 20]
SEEDS = [42, 123, 456]

FILTER_KEYS = ["seq", "enkf4d", "qpca4d"]
FILTER_LABELS = {"seq": "Seq-EnKF", "enkf4d": "4D-EnKF", "qpca4d": "QPCA-EnDCF"}
FILTER_COLORS = {"seq": "#0173B2", "enkf4d": "#DE8F05", "qpca4d": "#029E73"}
FILTER_STYLES = {
    "seq": dict(marker="o", linestyle="-", markerfacecolor="white", markeredgecolor="#0173B2"),
    "enkf4d": dict(marker="s", linestyle="-", markerfacecolor="white", markeredgecolor="#DE8F05"),
    "qpca4d": dict(marker="^", linestyle="-", markerfacecolor="white", markeredgecolor="#029E73"),
}


# ---------------------------------------------------------------------------
# Inflation helpers
# ---------------------------------------------------------------------------


def _mult_inflate(X, factor):
    if factor == 1.0:
        return X
    xm = X.mean(axis=1, keepdims=True)
    return xm + factor * (X - xm)


def _add_inflate(X, std, rng):
    if std == 0.0:
        return X
    return X + std * rng.standard_normal(X.shape)


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------


def run_experiment(seed, N_ens, inflation_type, inflation_value):
    """Run one inflation experiment for all 3 filters, return mean RMSE per filter."""
    rng = np.random.default_rng(seed)

    H, _ = build_obs_operator(N_STATE, OBSERVE_EVERY)
    m = H.shape[0]
    R = OBS_NOISE_STD**2 * np.eye(m)

    x0 = rng.normal(0.0, 1.0, size=N_STATE)
    K_total = N_WINDOWS * WINDOW_LEN
    steps_total = K_total * STEPS_PER_OBS
    truth_traj = integrate_model(x0, DT_MODEL, steps_total, F=F_PARAM)

    obs_steps = np.arange(STEPS_PER_OBS, steps_total + 1, STEPS_PER_OBS)
    true_at_obs = truth_traj[obs_steps]

    Z = np.empty((K_total, m))
    for k in range(K_total):
        Z[k] = H @ true_at_obs[k] + OBS_NOISE_STD * rng.standard_normal(m)

    X0 = (true_at_obs[0] + 0.5 * rng.standard_normal(N_STATE))[:, None] \
         + 0.5 * rng.standard_normal((N_STATE, N_ens))

    enkf4d = StochasticEnKF4D(H, R, window_len=WINDOW_LEN)
    qpca4d = QPCAEnDCF(H, R, window_len=WINDOW_LEN, k=QPCA_K, stabilize=True)
    seq_enkf = StochasticEnKF(H, R, stabilize=False)

    X_enkf4d, X_qpca4d, X_seq = X0.copy(), X0.copy(), X0.copy()
    rmse_e, rmse_q, rmse_s = [], [], []

    def _inflate(X):
        if inflation_type == "multiplicative":
            return _mult_inflate(X, inflation_value)
        return _add_inflate(X, inflation_value, rng)

    obs_ptr = 0
    for w in range(N_WINDOWS):
        X_path_e, X_path_q = [], []

        for ell in range(WINDOW_LEN):
            for _ in range(STEPS_PER_OBS):
                for j in range(N_ens):
                    X_enkf4d[:, j] = rk4_step(l96_rhs, X_enkf4d[:, j], DT_MODEL, F=F_PARAM)
                    X_qpca4d[:, j] = rk4_step(l96_rhs, X_qpca4d[:, j], DT_MODEL, F=F_PARAM)
                    X_seq[:, j] = rk4_step(l96_rhs, X_seq[:, j], DT_MODEL, F=F_PARAM)

            X_path_e.append(X_enkf4d.copy())
            X_path_q.append(X_qpca4d.copy())

            X_seq = seq_enkf.update(X_seq, Z[obs_ptr + ell], rng=rng)
            X_seq = _inflate(X_seq)

        z_stack = Z[obs_ptr : obs_ptr + WINDOW_LEN].reshape(-1)
        obs_ptr += WINDOW_LEN

        X_enkf4d = _inflate(enkf4d.update(X_path_e, z_stack))
        X_qpca4d = _inflate(qpca4d.update(X_path_q, z_stack))

        x_true = true_at_obs[obs_ptr - 1]
        rmse_e.append(rmse(X_enkf4d.mean(axis=1), x_true))
        rmse_q.append(rmse(X_qpca4d.mean(axis=1), x_true))
        rmse_s.append(rmse(X_seq.mean(axis=1), x_true))

    return {
        "seq": np.mean(rmse_s),
        "enkf4d": np.mean(rmse_e),
        "qpca4d": np.mean(rmse_q),
    }


# ---------------------------------------------------------------------------
# Run all experiments
# ---------------------------------------------------------------------------


def run_all_experiments():
    """Run multiplicative + additive experiments, return stats dicts."""

    def _sweep(inflation_type, values):
        # raw[filter][N_ens][value] = list of mean RMSE per seed
        raw = {k: {N: {v: [] for v in values} for N in ENSEMBLE_SIZES} for k in FILTER_KEYS}
        total = len(ENSEMBLE_SIZES) * len(values) * len(SEEDS)
        count = 0
        for N_ens in ENSEMBLE_SIZES:
            for val in values:
                for seed in SEEDS:
                    count += 1
                    res = run_experiment(seed, N_ens, inflation_type, val)
                    for k in FILTER_KEYS:
                        raw[k][N_ens][val].append(res[k])
                    print(f"  [{count}/{total}] {inflation_type} N={N_ens} val={val} seed={seed}")

        # Aggregate to mean/std
        stats = {k: {} for k in FILTER_KEYS}
        for k in FILTER_KEYS:
            for N_ens in ENSEMBLE_SIZES:
                stats[k][N_ens] = {}
                for val in values:
                    arr = raw[k][N_ens][val]
                    stats[k][N_ens][val] = {
                        "rmse_mean": np.mean(arr),
                        "rmse_std": np.std(arr, ddof=1) if len(arr) > 1 else 0.0,
                    }
        return stats

    print("Running multiplicative inflation experiments...")
    mult_stats = _sweep("multiplicative", MULT_FACTORS)
    print("Running additive inflation experiments...")
    add_stats = _sweep("additive", ADD_LEVELS)
    return mult_stats, add_stats


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def _plot_inflation(stats, x_values, xlabel, filename, x_tick_labels=None):
    """Shared 1×3 panel plot for inflation study."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    for idx, (ax, N_ens) in enumerate(zip(axes, ENSEMBLE_SIZES)):
        for key in FILTER_KEYS:
            means = np.array([stats[key][N_ens][v]["rmse_mean"] for v in x_values])
            stds = np.array([stats[key][N_ens][v]["rmse_std"] for v in x_values])

            ax.plot(
                x_values, means, color=FILTER_COLORS[key], label=FILTER_LABELS[key],
                linewidth=2.5, zorder=3, **FILTER_STYLES[key],
            )
            ax.fill_between(
                x_values, means - stds, means + stds,
                alpha=0.15, color=FILTER_COLORS[key], linewidth=0, zorder=1,
            )

        ax.set_xlabel(xlabel, fontweight="bold", fontsize=18)
        ax.set_ylabel("RMSE", fontweight="bold", fontsize=16)
        ax.set_title(rf"$N={N_ens}$", pad=12, fontsize=18, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.8, color="gray", zorder=0)
        ax.set_axisbelow(True)

        if x_tick_labels is not None:
            ax.set_xticks(x_values[1:] if x_values[0] == 0 else x_values)
            ax.set_xticklabels(x_tick_labels, fontweight="bold")
        else:
            ax.set_xticks(x_values)
            ax.set_xticklabels([f"{x:.2f}" for x in x_values])

        ax.tick_params(axis="both", which="major", labelsize=15)
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontweight("bold")
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
            spine.set_edgecolor("black")
        ax.margins(x=0.05)

        if idx == 0:
            legend = ax.legend(
                loc="upper right", frameon=True, framealpha=0.95,
                edgecolor="black", fancybox=False, shadow=False, fontsize=11,
            )
            legend.get_frame().set_linewidth(1.5)
            for text in legend.get_texts():
                text.set_fontweight("bold")

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    fig.savefig(
        OUTPUT_DIR / filename, dpi=600, bbox_inches="tight",
        facecolor="white", edgecolor="none",
    )
    plt.close(fig)


def plot_multiplicative(mult_stats):
    _plot_inflation(mult_stats, MULT_FACTORS, r"$\lambda$",
                    "inflation_multiplicative_20.png")


def plot_additive(add_stats):
    _plot_inflation(add_stats, ADD_LEVELS, r"$\alpha$",
                    "inflation_additive_20.png",
                    x_tick_labels=["0.01", "0.05", "0.10", "0.15", "0.20"])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if STYLE_FILE.exists():
        plt.style.use(str(STYLE_FILE))

    np.random.seed(42)

    mult_stats, add_stats = run_all_experiments()

    print("Generating figures...")
    plot_multiplicative(mult_stats)
    plot_additive(add_stats)

    expected = ["inflation_multiplicative_20.png", "inflation_additive_20.png"]
    for name in expected:
        path = OUTPUT_DIR / name
        if not path.exists():
            raise RuntimeError(f"Expected output missing: {path}")

    print(f"All {len(expected)} figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
