"""
Spectral diagnostics utilities for QPCA analysis.

These helpers provide lightweight routines for computing eigenvalue spectra,
effective ranks, cumulative variance profiles, and fitting exponential decay
models to eigenvalues. They are used by the spectral-regularization notebooks
to summarize the behaviour of whitened residual covariances.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

import numpy as np


def _sanitize_eigenvalues(eigenvalues: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Return eigenvalues clipped to be positive and sorted in descending order."""
    eig = np.asarray(eigenvalues, dtype=float).copy()
    eig = np.maximum(eig, eps)
    eig.sort()
    return eig[::-1]


def compute_eigenvalue_spectrum(
    matrix: np.ndarray,
    n_modes: int | None = None,
    eps: float = 1e-10,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the eigenvalue spectrum of a symmetric matrix.

    Parameters
    ----------
    matrix : ndarray, shape (n, n)
        Real symmetric matrix (e.g., covariance) whose spectrum we need.
    n_modes : int, optional
        Number of leading modes to return. If None, all modes are returned.
    eps : float
        Small jitter added to the diagonal for numerical stability.

    Returns
    -------
    eigenvalues : ndarray
        Sorted eigenvalues (descending order).
    eigenvectors : ndarray
        Corresponding eigenvectors (columns), matching the returned eigenvalues.
    """
    sym_matrix = 0.5 * (matrix + matrix.T) + eps * np.eye(matrix.shape[0])
    eigvals, eigvecs = np.linalg.eigh(sym_matrix)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    if n_modes is not None:
        eigvals = eigvals[:n_modes]
        eigvecs = eigvecs[:, :n_modes]
    return eigvals, eigvecs


def compute_effective_rank(
    eigenvalues: np.ndarray,
    method: Literal["entropy", "energy"] = "entropy",
    energy_threshold: float = 0.95,
    eps: float = 1e-12,
) -> float:
    """
    Compute effective rank of a spectrum.

    Two variants are supported:

    * ``method='entropy'`` uses the information-theoretic effective rank
      (a.k.a. eRank): exp(-∑ p_i log p_i), where p_i are normalized eigenvalues.
    * ``method='energy'`` returns the minimal number of modes required to
      explain ``energy_threshold`` of the total variance.
    """
    eigvals = _sanitize_eigenvalues(eigenvalues, eps=eps)
    if method == "entropy":
        probs = eigvals / eigvals.sum()
        entropy = -np.sum(probs * np.log(probs + eps))
        return float(np.exp(entropy))
    if method == "energy":
        cumulative = np.cumsum(eigvals) / eigvals.sum()
        k = np.searchsorted(cumulative, energy_threshold) + 1
        return float(k)
    raise ValueError(f"Unknown method '{method}'. Expected 'entropy' or 'energy'.")


def compute_cumulative_variance(
    eigenvalues: np.ndarray,
    normalize: bool = True,
    eps: float = 1e-12,
) -> np.ndarray:
    """
    Compute cumulative variance explained by eigenvalues.

    Parameters
    ----------
    eigenvalues : ndarray
        Eigenvalues sorted in descending order.
    normalize : bool
        If True, normalize by total variance to return fractions in [0, 1].
    """
    eigvals = _sanitize_eigenvalues(eigenvalues, eps=eps)
    cumulative = np.cumsum(eigvals)
    if normalize:
        cumulative /= cumulative[-1]
    return cumulative


@dataclass
class DecayFitResult:
    """Container for exponential decay fit parameters."""

    amplitude: float
    decay_rate: float
    slope: float
    intercept: float
    r_squared: float


def fit_eigenvalue_decay(
    eigenvalues: np.ndarray,
    n_fit: int = 10,
    eps: float = 1e-12,
) -> DecayFitResult:
    """
    Fit an exponential decay model λ_k ≈ A * exp(-β k) to leading eigenvalues.

    Parameters
    ----------
    eigenvalues : ndarray
        Eigenvalues sorted in descending order.
    n_fit : int
        Number of modes to include in the fit (defaults to 10).

    Returns
    -------
    DecayFitResult
        Named tuple containing amplitude, decay rate, slope/intercept of the
        linear fit in log-space, and coefficient of determination (R²).
    """
    eigvals = _sanitize_eigenvalues(eigenvalues, eps=eps)
    n_use = min(n_fit, len(eigvals))
    if n_use < 2:
        raise ValueError("Need at least two eigenvalues to fit a decay curve.")
    k = np.arange(n_use, dtype=float)
    log_vals = np.log(eigvals[:n_use])
    slope, intercept = np.polyfit(k, log_vals, 1)
    fitted = slope * k + intercept
    ss_res = np.sum((log_vals - fitted) ** 2)
    ss_tot = np.sum((log_vals - log_vals.mean()) ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    amplitude = float(np.exp(intercept))
    decay_rate = float(-slope)
    return DecayFitResult(
        amplitude=amplitude,
        decay_rate=decay_rate,
        slope=float(slope),
        intercept=float(intercept),
        r_squared=float(r_squared),
    )


__all__ = [
    "compute_eigenvalue_spectrum",
    "compute_effective_rank",
    "compute_cumulative_variance",
    "fit_eigenvalue_decay",
    "DecayFitResult",
]
