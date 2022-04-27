"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman, SystemMatrixes
from src.models.vmm import VMM
import numpy as np


def create_extended_kalman(
    parameters: dict,
    ship_data: dict,
    vmm: VMM,
    system_matrixes: SystemMatrixes,
) -> ExtendedKalman:
    """Create an Extended Kalman Filter (EKF)

    Parameters
    ----------
    parameters : dict
        Hydrodynamic derivatives in the Vessel Manoeuvring Model (VMM)
    ship_data : dict
        Ship data about mass properties etc.
    vmm : VMM
        Vessel Manoeuvring Model (VMM)

    Returns
    -------
    ExtendedKalman
        object of Extendedkalman class, that can be used to predict measured states.
    """

    ek = ExtendedKalman(
        vmm=vmm,
        parameters=parameters,
        ship_parameters=ship_data,
        system_matrixes=system_matrixes,
    )

    return ek
