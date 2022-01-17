# Pipeline filter_data_extended_kalman


## Overview

This pipeline runs the model test data through a Extended Kalman Filter (EKF) and after that passes the estimated states into a RTS smoother. The kalman filter used can be generated in the pipeline: [extended_kalman](../extended_kalman/README.md).

## Pipeline inputs

* Extended Kalman Filter ([extended_kalman](../extended_kalman/README.md))
* Model test data

## Pipeline outputs

* EKF filtered data and estimated velocities and accelerations
* EKF smoothened data and estimated velocities and accelerations

