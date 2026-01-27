"""
Four-dimensional stochastic ensemble Kalman filter.
"""

import numpy as np
from numpy.linalg import cholesky
from .base_filter import BaseFilter
from ..utils.linalg import cov_and_anoms, sym_posdef_inverse, block_diag_repeat


class StochasticEnKF4D(BaseFilter):
    """
    4D joint update (stacked observations) stochastic EnKF.
    - At window end, build stacked HX over the L obs times: Yhat_stack (mL x N)
    - Build block-diagonal R_block = diag(R, ..., R)
    - Use ensemble covariances: P_xy and P_yy over stacked space.
    - Perturb stacked observations columnwise and update at window end.
    """

    def __init__(self, H, R, window_len):
        """
        Initialize 4D stochastic EnKF.

        Parameters
        ----------
        H : ndarray, shape (m, n)
            Observation operator.
        R : ndarray, shape (m, m)
            Observation error covariance.
        window_len : int
            Number of observation times per assimilation window.
        """
        super().__init__(H, R)
        self.window_len = window_len
        self.m = R.shape[0]
        self.R_block = block_diag_repeat(R, window_len)  # (mL x mL)
        self.R_block_chol = cholesky(self.R_block)

    def update(self, X_path, z_stack):
        """
        Perform 4D analysis update with stacked observations.

        Parameters
        ----------
        X_path : list of ndarray
            List of length L with state ensembles at each obs time in the window.
            Each element is X_t with shape (n, N).
        z_stack : ndarray, shape (mL,)
            Stacked observation vector at those times.

        Returns
        -------
        X_a_end : ndarray, shape (n, N)
            Updated ensemble at window end.
        """
        H = self.H
        L = self.window_len
        n, N = X_path[-1].shape
        m = self.m

        # Build stacked H X for each time in the window
        HX_blocks = [H @ X_path[t] for t in range(L)]  # each (m x N)
        HX_stack = np.vstack(HX_blocks)  # (mL x N)

        # Ensemble anomalies at window end and in stacked obs space
        _, A_x_end = cov_and_anoms(X_path[-1])  # (n x N)
        _, A_y = cov_and_anoms(HX_stack)  # (mL x N)

        # Cross- and auto-covariances in ensemble space
        P_xy = (A_x_end @ A_y.T) / (N - 1)  # (n x mL)
        P_yy = (A_y @ A_y.T) / (N - 1)  # (mL x mL)

        # Innovation covariance: add R_block (stochastic EnKF)
        S = P_yy + self.R_block  # (mL x mL)
        S_inv = sym_posdef_inverse(S)

        # Perturb stacked observations columnwise
        Eps = self.R_block_chol @ np.random.standard_normal(size=(m * L, N))
        Y_stack = z_stack[:, None] + Eps  # (mL x N)

        # Update at window end
        X_a_end = X_path[-1] + P_xy @ (S_inv @ (Y_stack - HX_stack))
        return X_a_end
