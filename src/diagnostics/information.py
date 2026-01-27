"""
Information-theoretic diagnostics for Gaussian random variables.

This module provides helper routines for entropy, conditional entropy,
mutual information, and Fisher information computations under Gaussian
assumptions. These are used by the information-gain notebooks to quantify
the informative content of whitened residuals and observation operators.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


def _symmetrize(matrix: np.ndarray) -> np.ndarray:
    """Return the symmetric part of a matrix."""
    return 0.5 * (matrix + matrix.T)


def _logdet_spd(matrix: np.ndarray, eps: float = 1e-12) -> float:
    """Compute log-determinant of a symmetric positive definite matrix."""
    matrix = _symmetrize(matrix) + eps * np.eye(matrix.shape[0])
    sign, logdet = np.linalg.slogdet(matrix)
    if sign <= 0:
        raise ValueError("Matrix must be positive definite for log-determinant.")
    return float(logdet)


def compute_entropy_gaussian(covariance: np.ndarray, base: float = np.e) -> float:
    """
    Differential entropy of a multivariate Gaussian N(0, Σ).

    Parameters
    ----------
    covariance : ndarray, shape (n, n)
        Covariance matrix Σ.
    base : float
        Logarithm base (e for nats, 2 for bits).
    """
    n = covariance.shape[0]
    logdet = _logdet_spd(covariance)
    entropy = 0.5 * (n * (1.0 + np.log(2 * np.pi)) + logdet)
    if base != np.e:
        entropy /= np.log(base)
    return entropy


def compute_conditional_entropy(
    covariance_joint: np.ndarray,
    covariance_cond: np.ndarray | None = None,
    base: float = np.e,
) -> float:
    """
    Differential entropy H(X|Y) for jointly Gaussian variables.

    Either supply the conditional covariance Σ_{X|Y} directly via
    ``covariance_cond`` or pass the joint covariance matrix and let this
    function compute the conditional covariance using block matrix formulas.
    When the joint covariance is provided, the blocks are assumed to be ordered
    as:

    Σ = [[Σ_xx, Σ_xy],
         [Σ_yx, Σ_yy]]
    """
    if covariance_cond is None:
        n = covariance_joint.shape[0] // 2
        sigma_xx = covariance_joint[:n, :n]
        sigma_xy = covariance_joint[:n, n:]
        sigma_yy = covariance_joint[n:, n:]
        sigma_yx = sigma_xy.T
        sigma_yy_inv = np.linalg.pinv(sigma_yy)
        covariance_cond = sigma_xx - sigma_xy @ sigma_yy_inv @ sigma_yx
    return compute_entropy_gaussian(covariance_cond, base=base)


def compute_mutual_information_gaussian(
    covariance_x: np.ndarray,
    covariance_noise: np.ndarray,
    observation_matrix: np.ndarray,
    base: float = np.e,
) -> float:
    """
    Mutual information I(X; Y) where Y = H X + ε, ε ~ N(0, R).

    Parameters
    ----------
    covariance_x : ndarray
        Prior covariance Σ_x of the state X.
    covariance_noise : ndarray
        Observation noise covariance R.
    observation_matrix : ndarray
        Observation operator H.
    base : float
        Logarithm base (default natural log -> nats).
    """
    sigma_y = (
        observation_matrix @ covariance_x @ observation_matrix.T + covariance_noise
    )
    entropy_y = compute_entropy_gaussian(sigma_y, base=base)
    entropy_noise = compute_entropy_gaussian(covariance_noise, base=base)
    return entropy_y - entropy_noise


@dataclass
class FisherInformationResult:
    """Result container for Fisher information of a linear-Gaussian model."""

    information_matrix: np.ndarray
    chol_factor: np.ndarray


def compute_fisher_information(
    observation_matrix: np.ndarray,
    covariance_noise: np.ndarray,
    prior_covariance: np.ndarray | None = None,
    eps: float = 1e-10,
) -> FisherInformationResult:
    """
    Compute Fisher information matrix for observations Y = H X + ε.

    Parameters
    ----------
    observation_matrix : ndarray (m, n)
        Observation operator H.
    covariance_noise : ndarray (m, m)
        Observation noise covariance R.
    prior_covariance : ndarray (n, n), optional
        Prior covariance Σ_x. If provided, the Fisher information is H^T R^{-1} H.
        Otherwise only the observation contribution is considered.
    eps : float
        Regularization for solving linear systems.
    """
    R_inv = np.linalg.pinv(_symmetrize(covariance_noise) + eps * np.eye(covariance_noise.shape[0]))
    info = observation_matrix.T @ R_inv @ observation_matrix
    if prior_covariance is not None:
        info = info + np.linalg.pinv(prior_covariance + eps * np.eye(prior_covariance.shape[0]))
    chol = np.linalg.cholesky(_symmetrize(info) + eps * np.eye(info.shape[0]))
    return FisherInformationResult(information_matrix=info, chol_factor=chol)


__all__ = [
    "compute_entropy_gaussian",
    "compute_conditional_entropy",
    "compute_mutual_information_gaussian",
    "compute_fisher_information",
    "FisherInformationResult",
]
