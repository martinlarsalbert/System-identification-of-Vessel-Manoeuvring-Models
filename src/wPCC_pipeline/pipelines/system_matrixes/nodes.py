"""
This is a boilerplate pipeline 'system_matrixes'
generated using Kedro 0.17.6
"""

from vessel_manoeuvring_models.extended_kalman_vmm import SystemMatrixes
from vessel_manoeuvring_models.models.vmm import VMM


def create_system_matrixes(vmm: VMM) -> SystemMatrixes:
    """Create system matrixes that can be reused for several KalmanFilters (as long as the VMM is the same)

    Parameters
    ----------
    vmm : VMM
        Vessel Manoeuvring Model (VMM)

    Returns
    -------
    SystemMatrixes
        object of SystemMatrixes class, that can be passed to th ExtendedKalman class
    """

    system_matrixes = SystemMatrixes(vmm=vmm)

    return system_matrixes
