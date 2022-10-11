"""
This is a boilerplate pipeline 'vessel_manoeuvring_models'
generated using Kedro 0.17.6
"""

from vessel_manoeuvring_models.models.vmm import VMM
from .vmm_simple_no_thrust import simple_model
from .vmm_complex_no_thrust import complex_model


def martins_model() -> VMM:
    from vessel_manoeuvring_models.models.vmm_martin import martins_model

    return martins_model


def vmm_linear() -> VMM:
    from vessel_manoeuvring_models.models.vmm_linear import vmm_linear

    return vmm_linear


def vmm_martins_simple_model() -> VMM:
    from vessel_manoeuvring_models.models.vmm_martin_simple import martins_simple_model

    return martins_simple_model


def vmm_abkowitz_model() -> VMM:
    from vessel_manoeuvring_models.models.vmm_abkowitz import abkowitz_model

    return abkowitz_model


def vmm_abkowitz_expanded() -> VMM:
    from vessel_manoeuvring_models.models.vmm_abkowitz_expanded import (
        abkowitz_model_expanded,
    )

    return abkowitz_model_expanded


def vmm_simple_no_thrust() -> VMM:
    return simple_model


def vmm_complex_no_thrust() -> VMM:
    return complex_model
