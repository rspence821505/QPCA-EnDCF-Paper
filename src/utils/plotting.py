"""
Standardized plotting utilities for data assimilation experiments.
"""

import numpy as np
import matplotlib.pyplot as plt


def make_summary_plots(results, save_path=None):
    """
    Generate summary plots for baseline comparison experiment.

    Parameters
    ----------
    results : dict
        Results dictionary from run_experiment_4d.
    save_path : str, optional
        If provided, save figures to this directory.

    Returns
    -------
    figs : list of matplotlib.figure.Figure
        List of generated figures.
    """
    rmse_enkf4d = results["rmse_enkf4d"]
    rmse_qpca4d = results["rmse_qpca4d"]
    rmse_seq = results["rmse_seq"]
    misfit_enkf4d = results["misfit_enkf4d"]
    misfit_qpca4d = results["misfit_qpca4d"]
    misfit_seq = results["misfit_seq"]

    W = rmse_enkf4d.size
    t = np.arange(1, W + 1)

    figs = []

    # RMSE plot
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(t, rmse_seq, label="RMSE – Seq Stoch EnKF", linewidth=2)
    ax1.plot(t, rmse_enkf4d, label="RMSE – 4D Stoch EnKF", linewidth=2)
    ax1.plot(t, rmse_qpca4d, label="RMSE – 4D QPCA–EnDCF", linewidth=2)
    ax1.set_xlabel("Assimilation window", fontsize=12)
    ax1.set_ylabel("State RMSE (window end)", fontsize=12)
    ax1.set_title("RMSE per 4D Window", fontsize=14)
    ax1.legend(loc="upper right", fontsize=10)
    ax1.grid(alpha=0.3)
    plt.tight_layout()
    figs.append(fig1)

    if save_path:
        fig1.savefig(f"{save_path}/rmse_comparison.pdf", dpi=300, bbox_inches="tight")

    # Misfit plot
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(t, misfit_seq, label="Rel. misfit – Seq Stoch EnKF", linewidth=2)
    ax2.plot(t, misfit_enkf4d, label="Rel. misfit – 4D Stoch EnKF", linewidth=2)
    ax2.plot(t, misfit_qpca4d, label="Rel. misfit – 4D QPCA–EnDCF", linewidth=2)
    ax2.set_xlabel("Assimilation window", fontsize=12)
    ax2.set_ylabel(
        r"Relative data misfit ($R^{-1/2}$-weighted, window end)", fontsize=12
    )
    ax2.set_title("Relative Data Misfit per 4D Window", fontsize=14)
    ax2.legend(loc="upper right", fontsize=10)
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    figs.append(fig2)

    if save_path:
        fig2.savefig(f"{save_path}/misfit_comparison.pdf", dpi=300, bbox_inches="tight")

    # Print summary statistics
    print("\n===== Summary (means over all windows) =====")
    print(
        f"Seq EnKF     | RMSE: {rmse_seq.mean():.4f} | Misfit: {misfit_seq.mean():.4f}"
    )
    print(
        f"4D Stoch EnKF| RMSE: {rmse_enkf4d.mean():.4f} | Misfit: {misfit_enkf4d.mean():.4f}"
    )
    print(
        f"4D QPCA–EnDCF| RMSE: {rmse_qpca4d.mean():.4f} | Misfit: {misfit_qpca4d.mean():.4f}"
    )

    return figs
