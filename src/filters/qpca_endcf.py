"""
QPCA Ensemble Data Consistency Filter (4D variant).
"""

import numpy as np
from numpy.linalg import eigh, cholesky
from .base_filter import BaseFilter
from ..utils.linalg import (
    cov_and_anoms,
    sym_posdef_inverse,
    stabilize_spd_like,
    block_diag_repeat,
)


class QPCAEnDCF(BaseFilter):
    """
      QPCA–EnDCF consistent with seq_mud:
    - Build stacked, per-particle residuals E_stack = R_block^{-1/2} (HX_stack - z_stack 1^T)
    - PCA in data (stacked) coordinates on centered whitened residuals
    - Project residuals onto top-k eigenvectors
    - De-whiten projected residuals and apply 4D gain K = P_xy S^{-1}
      with S = P_yy (optionally stabilized vs R_block)
    """

    def __init__(self, H, R, window_len, k=1, stabilize=True):
        """
        Initialize QPCA-EnDCF 4D filter.

        Parameters
        ----------
        H : ndarray, shape (m, n)
            Observation operator.
        R : ndarray, shape (m, m)
            Observation error covariance.
        window_len : int
            Number of observation times per assimilation window.
        k : int, optional
            Number of PCA modes to retain (default: 1).
        stabilize : bool, optional
            Whether to stabilize innovation covariance (default: True).
        """
        super().__init__(H, R)
        self.window_len = window_len
        self.k = k
        self.stabilize = stabilize
        self.m = R.shape[0]

        # Block structures
        self.R_block = block_diag_repeat(R, window_len)  # (mL x mL)
        # Add small jitter to ensure positive definiteness
        jitter = 1e-10
        R_block_reg = self.R_block + jitter * np.eye(self.R_block.shape[0])
        self.R_block_chol = cholesky(R_block_reg)  # R_block^{1/2} = L
        # Compute R_block^{-1/2} = (L^{-1})^T directly from Cholesky factor
        # This is more numerically stable than computing inverse then Cholesky
        L_inv = np.linalg.solve(self.R_block_chol, np.eye(self.R_block_chol.shape[0]))
        self.R_block_inv_sqrt = L_inv.T  # (R_block^{-1/2})^T

    def update(self, X_path, z_stack):
        """
        Perform 4D analysis update with whitened PCA filtering.

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

        # Whitened residuals in stacked data space
        E = self.R_block_inv_sqrt.T @ (HX_stack - z_stack[:, None])  # (mL x N)
        Ec = E - E.mean(axis=1, keepdims=True)
        C = (Ec @ Ec.T) / (N - 1)  # (mL x mL)

        # Top-k eigenvectors (largest eigenvalues)
        w, V = eigh(C)  # ascending
        Vk = V[:, -self.k :]  # (mL x k)

        # QPCA map (whitened space), WME sign
        Q_qpca = -Vk @ (Vk.T @ E)  # (mL x N)

        # Ensemble anomalies at window end and in stacked obs space
        _, A_x_end = cov_and_anoms(X_path[-1])  # (n x N)
        _, A_y = cov_and_anoms(HX_stack)  # (mL x N)

        # Cross- and auto-covariances
        P_xy = (A_x_end @ A_y.T) / (N - 1)  # (n x mL)
        P_yy = (A_y @ A_y.T) / (N - 1)  # (mL x mL)

        # Innovation covariance for EnDCF-style gain
        S = P_yy
        if self.stabilize:
            S = stabilize_spd_like(S, self.R_block)
        S_inv = sym_posdef_inverse(S)

        # Gain and de-whitened correction
        K = P_xy @ S_inv  # (n x mL)
        corr_obs = self.R_block_chol @ Q_qpca  # (mL x N)
        X_a_end = X_path[-1] + K @ corr_obs  # (n x N)
        return X_a_end
