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
from .pipelines import accuracy
from .pipelines import setup
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

    joins = runs_globals["joins"]
    join_runs_dict = anyconfig.load(join_globals_path)

    globals_path = os.path.join(
        conf_path,
        "globals.yml",
    )
    global_variables = anyconfig.load(globals_path)
    vmms = global_variables["vmms"]
    regressions = global_variables["regressions"]
    create_track_plot = global_variables["create_track_plot"]

    ########## Pipelines:

    ship_pipeline = brix.create_pipeline()
    setup_pipeline = setup.create_pipeline()

    ek_pipelines = {}
    for vmm in vmms:
        key = f"ek.{vmm}"
        ek_pipelines[key] = pipeline(
            extended_kalman.create_pipeline(),
            namespace=f"{vmm}",
            inputs={
                "vmm": vmm,
                "initial_parameters": "initial_parameters",
                "ship_data": "ship_data",
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
                f"ek": "vmm_martin.ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
                "covariance_matrixes": "vmm_martin.covariance_matrixes",
            },
        )

    ## Join the tests:
    joined_pipelines = {}
    # All runs:
    # joined_pipelines["joined"] = pipeline(
    #    join_runs.create_pipeline(model_test_ids=model_test_ids, namespace="joined", )
    # )

    join_runs_dict["joined"] = model_test_ids
    join_runs_dict = {join_name: join_runs_dict[join_name] for join_name in joins}
    # other selections:
    for dataset_name, runs_selection in join_runs_dict.items():
        joined_pipelines[dataset_name] = pipeline(
            join_runs.create_pipeline(model_test_ids=runs_selection),
            namespace=dataset_name,
            inputs={
                f"{run}.data_ek_smooth": f"{run}.data_ek_smooth"
                for run in runs_selection
            },
        )

    ## Vessel Manoeuvring Models (VMMs)
    vessel_manoeuvring_models_pipeline = vessel_manoeuvring_models.create_pipeline()

    ## Motion regression pipeline:
    # "motion_regression"
    motion_regression_pipelines = []
    dataset_names = list(joined_pipelines.keys())
    
    for id in dataset_names:
        
        p = pipeline(
                motion_regression.create_pipeline(),
                namespace=id,
                inputs={
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"vmm": "vmm",
                    f"data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )


        for vmm in vmms:
            p2 = pipeline(
            p,
            namespace=f"{vmm}",
            inputs={
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
                "vmm": vmm,
                f"{id}.data_ek_smooth":f"{id}.data_ek_smooth",
            },)            
            
            motion_regression_pipelines.append(p2)
    #
    ## Predictions:
    # motion models:
    # model tests:
    prediction_pipelines = {}
    for vmm in vmms:
        for dataset_name in dataset_names:
            for id in model_test_ids:

                p = pipeline(
                    prediction.create_pipeline(create_track_plot=create_track_plot),
                    namespace=f"{id}",
                    inputs={
                        f"ship_data": "ship_data",
                    },
                )
                p2 = pipeline(
                    p,
                    namespace=f"motion_regression.{dataset_name}",
                    inputs={
                        f"ship_data": "ship_data",
                        f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                        f"{id}.model": f"{vmm}.motion_regression.{dataset_name}.model",
                    },
                )
                prediction_id = f"predict.{vmm}.motion_regression.{dataset_name}.{id}"
                prediction_pipelines[prediction_id] = pipeline(
                    p2,
                    namespace=vmm,
                    inputs={
                        f"ship_data": "ship_data",
                        f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                        f"{vmm}.motion_regression.{dataset_name}.model": f"{vmm}.motion_regression.{dataset_name}.model",
                        f"motion_regression.{dataset_name}.{id}.force_regression.data_scaled_resistance_corrected": "force_regression.data_scaled_resistance_corrected",
                        f"motion_regression.{dataset_name}.{id}.ek": f"{vmm}.ek",
                    },
                )

        # force models:
        if "force_regression" in regressions:
            for id in model_test_ids:
                p = pipeline(
                    prediction.create_pipeline(create_track_plot=create_track_plot),
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
                        f"force_regression.{id}.force_regression.data_scaled_resistance_corrected": "force_regression.data_scaled_resistance_corrected",
                        f"force_regression.{id}.ek": f"{vmm}.ek",
                    },
                )

    ## accuracy:
    accuracy_pipelines = {}

    for vmm in vmms:

        for dataset_name in join_runs_dict.keys():

            for id in model_test_ids:

                key = f"accuracy.{vmm}.motion_regression.{dataset_name}.{id}"
                accuracy_pipelines[key] = pipeline(
                    accuracy.create_pipeline(),
                    namespace=f"{vmm}.motion_regression.{dataset_name}.{id}",
                    inputs={
                        "data_ek_smooth": f"{id}.data_ek_smooth",
                        "ek": f"{vmm}.ek",
                        "model": f"{ vmm }.motion_regression.{ dataset_name }.model",
                        "ship_data": "ship_data",
                    },
                )

    return_dict = {}
    return_dict["__default__"] = (
        ship_pipeline
        + setup_pipeline
        + reduce(add, runs_pipelines.values())
        + reduce(add, joined_pipelines.values())
        + vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + reduce(add, motion_regression_pipelines)
        #+ vct_data_pipeline
        #+ reduce(add, prediction_pipelines.values())
        #+ reduce(add, accuracy_pipelines.values())
    )

    

    return return_dict
