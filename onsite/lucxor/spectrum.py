"""
Spectrum module.

This module contains the Spectrum class for handling mass spectrometry data.
"""

import logging
import numpy as np
from typing import Tuple

logger = logging.getLogger(__name__)


class Spectrum:
    """Class representing a mass spectrum."""

    def __init__(self, mz_array=None, intensity_array=None):
        """
        Initialize a new Spectrum instance.

        Args:
            mz_array: Array of m/z values
            intensity_array: Array of intensity values
        """
        self.N = 0  # number of peaks
        self.max_i_index = 0  # index of max intensity peak
        self.max_i = 0.0  # max intensity value

        # Peak arrays - use NumPy arrays for better performance
        self.mz = np.array([])  # m/z values
        self.raw_intensity = np.array([])  # raw intensity values
        self.rel_intensity = np.array([])  # relative intensity values (0-100)
        self.norm_intensity = np.array([])  # normalized intensity values (log scale)

        # Pre-computed indices for faster searching
        self._mz_sorted_indices = None
        self._mz_sorted = None

        if mz_array is not None and intensity_array is not None:
            self._init_peaks(mz_array, intensity_array)

    def _init_peaks(self, mz_array, intensity_array):
        """Initialize peak arrays from input data."""
        # Convert to NumPy arrays if not already
        mz_array = np.asarray(mz_array)
        intensity_array = np.asarray(intensity_array)

        # Ensure arrays have same length
        N = min(len(mz_array), len(intensity_array))

        # Filter out zero intensity peaks using vectorized operations
        valid_mask = intensity_array[:N] > 0

        if not np.any(valid_mask):
            # No valid peaks
            self.N = 0
            return

        # Extract valid peaks
        self.mz = mz_array[:N][valid_mask]
        self.raw_intensity = intensity_array[:N][valid_mask]
        self.N = len(self.mz)

        # Find max intensity
        max_idx = np.argmax(self.raw_intensity)
        self.max_i = self.raw_intensity[max_idx]
        self.max_i_index = max_idx

        # Initialize other arrays
        self.rel_intensity = np.zeros(self.N)
        self.norm_intensity = np.zeros(self.N)

        # Calculate relative intensities
        self.calc_relative_intensity()

        # Pre-compute sorted indices for faster searching
        self._update_sorted_indices()

    def calc_relative_intensity(self):
        """Calculate relative intensities (0-100) based on max intensity."""
        if self.max_i > 0:
            self.rel_intensity = (self.raw_intensity / self.max_i) * 100.0

    def median_normalize_spectra(self):
        """
        Normalize intensities using median.
        Computes log(rel_intensity/median_intensity).
        """
        if self.N == 0:
            return

        # Use NumPy median for better performance
        median_i = np.median(self.rel_intensity)

        # Vectorized calculation of normalized intensities
        with np.errstate(divide="ignore", invalid="ignore"):
            d = self.rel_intensity / median_i
            self.norm_intensity = np.where(d > 0, np.log(d), float("-inf"))

    def get_peaks(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get peak arrays.

        Returns:
            Tuple of (m/z array, intensity array)
        """
        return self.mz, self.raw_intensity

    def is_empty(self) -> bool:
        """
        Check if spectrum is empty.

        Returns:
            True if spectrum has no peaks
        """
        return self.N == 0

    def _update_sorted_indices(self):
        """Update sorted indices for faster searching."""
        if self.N > 0:
            self._mz_sorted_indices = np.argsort(self.mz)
            self._mz_sorted = self.mz[self._mz_sorted_indices]
