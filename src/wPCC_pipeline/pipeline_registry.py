"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline

from .pipelines import lowpass as lp
from .pipelines import brix as bx
from .pipelines import extended_kalman as ek


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    lowpass = lp.create_pipeline()
    brix = bx.create_pipeline()
    extended_kalman = ek.create_pipeline()

    return {"__default__": lowpass + brix + extended_kalman}
