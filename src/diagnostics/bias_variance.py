"""
Bias-variance diagnostics utilities.

These helpers compute pointwise bias/variance across Monte Carlo realizations
of an estimator and aggregate the statistics used in the bias–variance
analysis notebook.
"""

from __future__ import annotations

from typing import Dict, Iterable

import numpy as np

Array = np.ndarray


def _move_axis_to_front(arr: Array, axis: int) -> Array:
    """Move the Monte Carlo axis to the front (axis=0)."""
    return np.moveaxis(arr, axis, 0)


def compute_pointwise_bias(
    realizations: Array,
    truth: Array,
    sample_axis: int = 0,
) -> Array:
    """
    Compute pointwise bias between ensemble realizations and truth.

    Parameters
    ----------
    realizations : ndarray
        Monte Carlo realizations with shape (n_samples, ...).
    truth : ndarray
        Reference truth array with the same shape as a single realization.
    sample_axis : int
        Axis corresponding to the Monte Carlo samples.

    Returns
    -------
    bias : ndarray
        Expectation over realizations minus truth, matching ``truth`` shape.
    """
    realizations = np.asarray(realizations, dtype=float)
    truth = np.asarray(truth, dtype=float)
    realizations = _move_axis_to_front(realizations, sample_axis)
    expectation = realizations.mean(axis=0)
    if expectation.shape != truth.shape:
        raise ValueError(
            f"Truth shape {truth.shape} does not match realization shape {expectation.shape}."
        )
    return expectation - truth


def compute_pointwise_variance(
    realizations: Array,
    sample_axis: int = 0,
    mean: Array | None = None,
) -> Array:
    """
    Compute variance across Monte Carlo realizations for each entry.

    Parameters
    ----------
    realizations : ndarray
        Monte Carlo realizations.
    sample_axis : int
        Axis corresponding to the Monte Carlo samples.
    mean : ndarray, optional
        Precomputed expectation. If not provided it is computed internally.

    Returns
    -------
    variance : ndarray
        Pointwise variance with the same shape as a single realization.
    """
    realizations = np.asarray(realizations, dtype=float)
    realizations = _move_axis_to_front(realizations, sample_axis)
    if mean is None:
        mean = realizations.mean(axis=0)
    return np.mean((realizations - mean) ** 2, axis=0)


def _mean_over_axes(array: Array, axes: Iterable[int]) -> Array:
    """Average over one or multiple axes."""
    result = array
    for ax in sorted({a % array.ndim for a in axes}, reverse=True):
        result = result.mean(axis=ax)
    return result


def compute_bias_variance_decomposition(
    realizations: Array,
    truth: Array,
    sample_axis: int = 0,
    state_axes: int | Iterable[int] | None = -1,
    eps: float = 1e-12,
) -> Dict[str, Array]:
    """
    Perform bias–variance decomposition for Monte Carlo realizations.

    Parameters
    ----------
    realizations : ndarray
        Monte Carlo realizations of the estimator with shape
        ``(n_samples, n_times, n_states, ...)``.
    truth : ndarray
        Reference truth array matching the shape of a single realization.
    sample_axis : int, default=0
        Axis containing the Monte Carlo samples.
    state_axes : int, iterable, or None
        Axes over which to aggregate spatial statistics (e.g., state dimension).
        If ``None`` no aggregation is performed.
    eps : float
        Small constant to avoid division by zero when forming ratios.

    Returns
    -------
    dict
        Dictionary containing realizations, expectation, truth, pointwise bias,
        variance, MSE, and aggregated metrics.
    """
    realizations = np.asarray(realizations, dtype=float)
    truth = np.asarray(truth, dtype=float)
    realizations = _move_axis_to_front(realizations, sample_axis)
    expectation = realizations.mean(axis=0)

    if expectation.shape != truth.shape:
        raise ValueError(
            f"Truth shape {truth.shape} does not match realization shape {expectation.shape}."
        )

    bias = expectation - truth
    bias_squared = bias**2
    variance = np.mean((realizations - expectation) ** 2, axis=0)
    mse = np.mean((realizations - truth) ** 2, axis=0)

    aggregation_axes = None
    if state_axes is not None:
        if isinstance(state_axes, int):
            aggregation_axes = (state_axes,)
        else:
            aggregation_axes = tuple(state_axes)
        aggregation_axes = tuple(ax % bias.ndim for ax in aggregation_axes)

    if aggregation_axes is None:
        bias_norm = np.sqrt(bias_squared)
        variance_trace = variance
        mse_trace = mse
        bias_squared_trace = bias_squared
    else:
        bias_norm = np.sqrt(_mean_over_axes(bias_squared, aggregation_axes))
        variance_trace = _mean_over_axes(variance, aggregation_axes)
        mse_trace = _mean_over_axes(mse, aggregation_axes)
        bias_squared_trace = _mean_over_axes(bias_squared, aggregation_axes)

    bias_mse_ratio = bias_squared_trace / (mse_trace + eps)

    return {
        "realizations": realizations,
        "expectation": expectation,
        "truth": truth,
        "bias": bias,
        "bias_norm": bias_norm,
        "variance": variance,
        "variance_trace": variance_trace,
        "bias_squared": bias_squared,
        "bias_squared_trace": bias_squared_trace,
        "mse": mse,
        "mse_trace": mse_trace,
        "bias_mse_ratio": bias_mse_ratio,
    }


__all__ = [
    "compute_bias_variance_decomposition",
    "compute_pointwise_bias",
    "compute_pointwise_variance",
]
