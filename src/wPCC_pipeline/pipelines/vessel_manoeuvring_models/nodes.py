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
