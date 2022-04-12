"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman, SystemMatrixes
from src.models.vmm import VMM
import numpy as np




def create_extended_kalman(
    parameters: dict, ship_data: dict, vmm: VMM, system_matrixes: SystemMatrixes,
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

    ek = ExtendedKalman(vmm=vmm, parameters=parameters, ship_parameters=ship_data, system_matrixes=system_matrixes)

    return ek


def guess_covariance_matrixes() -> dict:

    variance_u = 0.1
    variance_v = 0.1
    variance_r = np.deg2rad(0.1)
    Qd = np.diag([variance_u, variance_v, variance_r])  # process variances: u,v,r

    error_max_pos = 0.05
    sigma_pos = error_max_pos / 3
    variance_pos = sigma_pos ** 2

    error_max_psi = np.deg2rad(0.5)
    sigma_psi = error_max_psi / 3
    variance_psi = sigma_psi ** 2

    Rd = np.diag([variance_pos, variance_pos, variance_psi])
    P_prd = np.diag(
        [
            variance_pos,
            variance_pos,
            variance_psi,
            variance_u,
            variance_v,
            variance_r,
        ]
    )

    covariance_matrixes = {
        "P_prd": P_prd.tolist(),
        "Qd": Qd.tolist(),
        "Rd": Rd.tolist(),
    }

    return covariance_matrixes
