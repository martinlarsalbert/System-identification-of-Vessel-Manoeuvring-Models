from typing import Any, Dict

import numpy as np
from kedro.io import AbstractDataSet
from vessel_manoeuvring_models.extended_kalman_vmm import ExtendedKalman
import os


class ExtendedKalmanDataSet(AbstractDataSet):
    """``ExtendedKalmanDataSet`` loads / save ExtendedKalman class objects"""

    def __init__(self, filepath: str):
        """Creates a new instance of ExtendedKalmanDataSet to load / save image data at the given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        self._filepath = filepath

    def _load(self) -> np.ndarray:
        """Loads data from the image file.

        Returns:
            Data from the image file as a numpy array.
        """
        return ExtendedKalman.load(self._filepath)

    def _save(self, data: np.ndarray) -> None:
        """Saves image data to the specified filepath"""
        assert isinstance(data, ExtendedKalman)

        dir_path = os.path.split(self._filepath)[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        data.save(self._filepath)

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset"""
        return dict(filepath=self._filepath)
