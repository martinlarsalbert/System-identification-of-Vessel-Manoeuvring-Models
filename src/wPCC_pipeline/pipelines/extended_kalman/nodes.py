"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman
from src.models.vmm import VMM


def create_extended_kalman(
    parameters: dict, ship_data: dict, vmm: VMM
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

    ek = ExtendedKalman(vmm=vmm, parameters=parameters, ship_parameters=ship_data)

    return ek
