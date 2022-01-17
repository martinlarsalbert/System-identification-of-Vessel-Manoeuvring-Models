"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman
import src.models.vmm_martin as vmm


def create_extended_kalman(parameters: dict, ship_data: dict) -> ExtendedKalman:

    ek = ExtendedKalman(vmm=vmm, parameters=parameters, ship_parameters=ship_data)

    return ek
