"""
This is a boilerplate pipeline 'vessel_manoeuvring_models'
generated using Kedro 0.17.6
"""

from src.models.vmm import VMM


def martins_model() -> VMM:
    from src.models.vmm_martin import martins_model

    return martins_model


def vmm_linear() -> VMM:
    from src.models.vmm_linear import vmm_linear

    return vmm_linear


def vmm_martins_simple_model() -> VMM:
    from src.models.vmm_martin_simple import martins_simple_model

    return martins_simple_model


def vmm_abkowitz_model() -> VMM:
    from src.models.vmm_abkowitz import abkowitz_model

    return abkowitz_model
