"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline
import anyconfig
import os.path

from .pipelines import preprocess as preprocess
from .pipelines import brix as brix
from .pipelines import extended_kalman as extended_kalman
from .pipelines import filter_data_extended_kalman as filter_data_extended_kalman
from .pipelines import motion_regression as motion_regression
from .pipelines import prediction as prediction
from .pipelines import join_runs
from .pipelines import force_regression
from .pipelines import vessel_manoeuvring_models
from .pipelines import vct_data
from wPCC_pipeline import pipelines


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    # Read configs:
    conf_path = os.path.join(
        os.path.split(os.path.split(os.path.dirname(__file__))[0])[0],
        "conf",
        "base",
    )
    runs_globals_path = os.path.join(
        conf_path,
        "runs_globals.yml",
    )

    runs_globals = anyconfig.load(runs_globals_path)
    model_test_ids = runs_globals["model_test_ids"]

    join_globals_path = os.path.join(
        conf_path,
        "join_globals.yml",
    )
    join_runs_dict = anyconfig.load(join_globals_path)

    globals_path = os.path.join(
        conf_path,
        "globals.yml",
    )
    vmms = anyconfig.load(globals_path)["vmms"]

    ########## Pipelines:

    ship_pipeline = pipeline(
        brix.create_pipeline() + extended_kalman.create_pipeline(),
        inputs={
            "vmm": "vmm_martin",
        },
    )

    vct_data_pipeline = pipeline(
        vct_data.create_pipeline(),
        namespace="force_regression",
        inputs={"ship_data": "ship_data"},
    )

    ## Preprocess model tests:
    runs_pipelines = {}
    for id in model_test_ids:
        runs_pipelines[id] = pipeline(
            preprocess.create_pipeline()
            + filter_data_extended_kalman.create_pipeline(),
            namespace=f"{id}",
            inputs={
                f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
            },
        )

    ## Join the tests:
    joined_pipelines = {}
    # All runs:
    # joined_pipelines["joined"] = pipeline(
    #    join_runs.create_pipeline(model_test_ids=model_test_ids, namespace="joined", )
    # )

    join_runs_dict["joined"] = model_test_ids
    # other selections:
    for join_name, runs_selection in join_runs_dict.items():
        joined_pipelines[join_name] = pipeline(
            join_runs.create_pipeline(model_test_ids=runs_selection),
            namespace=join_name,
            inputs={
                f"{run}.data_ek_smooth": f"{run}.data_ek_smooth"
                for run in runs_selection
            },
        )

    ## Vessel Manoeuvring Models (VMMs)
    vessel_manoeuvring_models_pipeline = vessel_manoeuvring_models.create_pipeline()

    ## Motion regression pipeline:
    # "motion_regression"
    motion_regression_pipelines = {}
    motion_model_ids = model_test_ids + list(joined_pipelines.keys())

    for vmm in vmms:
        for id in motion_model_ids:
            p = pipeline(
                motion_regression.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"vmm": vmm,
                },
            )
            p2 = pipeline(
                p,
                namespace=f"motion_regression",
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    vmm: vmm,
                },
            )
            key = f"regress.{vmm}.motion_regression.{id}"
            motion_regression_pipelines[key] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    vmm: vmm,
                },
            )

    ## Force regression:
    # "force_regression"
    force_regression_pipelines = {}
    for vmm in vmms:
        key = f"{vmm}.force_regression"
        force_regression_pipelines[key] = pipeline(
            force_regression.create_pipeline(),
            namespace=f"{vmm}.force_regression",
            inputs={
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
                "vmm": vmm,
                "data_scaled": "force_regression.data_scaled",
            },
        )

    ## Predictions:
    # motion models:
    # model tests:
    prediction_pipelines = {}
    for vmm in vmms:
        for id in model_test_ids:
            p = pipeline(
                prediction.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    f"ship_data": "ship_data",
                },
            )
            p2 = pipeline(
                p,
                namespace="motion_regression",
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )
            prediction_id = f"predict.{vmm}.motion_regression.{id}"
            prediction_pipelines[prediction_id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"motion_regression.{id}.force_regression.data_scaled": "force_regression.data_scaled",
                },
            )
        # joined:
        for join_name in joined_pipelines.keys():
            for id in model_test_ids:
                p = pipeline(
                    prediction.create_pipeline(),
                    namespace=f"{id}",
                    inputs={
                        f"ship_data": "ship_data",
                    },
                )
                p2 = pipeline(
                    p,
                    namespace=f"motion_regression.{join_name}",
                    inputs={
                        f"ship_data": "ship_data",
                        f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                        f"{id}.model": f"{vmm}.motion_regression.{join_name}.model",
                    },
                )
                prediction_id = f"predict.{vmm}.motion_regression.{join_name}.{id}"
                prediction_pipelines[prediction_id] = pipeline(
                    p2,
                    namespace=vmm,
                    inputs={
                        f"ship_data": "ship_data",
                        f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                        f"{vmm}.motion_regression.{join_name}.model": f"{vmm}.motion_regression.{join_name}.model",
                        f"motion_regression.{join_name}.{id}.force_regression.data_scaled": "force_regression.data_scaled",
                    },
                )

        # force models:
        for id in model_test_ids:
            p = pipeline(
                prediction.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    f"ship_data": "ship_data",
                },
            )
            p2 = pipeline(
                p,
                namespace="force_regression",
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{id}.model": f"{vmm}.force_regression.model",
                },
            )
            prediction_id = f"predict.{vmm}.force_regression.{id}"
            prediction_pipelines[prediction_id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{vmm}.force_regression.model": f"{vmm}.force_regression.model",
                    f"force_regression.{id}.force_regression.data_scaled": "force_regression.data_scaled",
                },
            )

    return_dict = {}
    return_dict["__default__"] = (
        ship_pipeline
        + reduce(add, runs_pipelines.values())
        + reduce(add, joined_pipelines.values())
        + vessel_manoeuvring_models_pipeline
        + reduce(add, motion_regression_pipelines.values())
        + vct_data_pipeline
        + reduce(add, force_regression_pipelines.values())
        + reduce(add, prediction_pipelines.values())
    )
    return_dict["ship"] = ship_pipeline
    return_dict["motion_regression"] = reduce(add, motion_regression_pipelines.values())
    return_dict["force_regression"] = reduce(add, force_regression_pipelines.values())
    return_dict["regression"] = (
        return_dict["motion_regression"] + return_dict["force_regression"]
    )

    return_dict["predict"] = reduce(add, prediction_pipelines.values())
    return_dict["vmm"] = vessel_manoeuvring_models_pipeline
    return_dict["join"] = reduce(add, joined_pipelines.values())
    # return_dict["runs"] = reduce(add, runs_pipelines.values())

    return_dict.update(runs_pipelines)
    return_dict.update(motion_regression_pipelines)
    return_dict.update(force_regression_pipelines)
    return_dict.update(prediction_pipelines)
    return_dict.update(joined_pipelines)

    """
    kedro run --pipeline ship
    kedro run --pipeline motion_regression
    kedro run --pipeline force_regression
    kedro run --pipeline regression
    kedro run --pipeline predict
    
    It is also possible to be even more specific:
    
    # Specific regression:
    kedro run --pipeline regress.vmm_martins_simple.motion_regression.22774
    kedro run --pipeline regress.vmm_martins_simple.motion_regression.joined

    # Specific precition:
    kedro run --pipeline predict.vmm_martins_simple.motion_regression.22774
    kedro run --pipeline predict.vmm_martins_simple.motion_regression.joined.22774
    (The last one is predicting test 22774 with a model regressed on joined model tests)

    """

    return return_dict
