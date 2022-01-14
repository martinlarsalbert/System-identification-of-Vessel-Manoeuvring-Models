# Pipeline lowpass

## Overview

Lowpass filter is used on the model test data as a preprocessor. This is intended to estimate the initial state (for EKF-filter and simulations). It is also intended to give a second opinion on the velocity states estimated by the EKF.

The filter settings are defined in:
 [lowpass.yml](../../../../conf/base/parameters/lowpass.yml).

## Pipeline inputs

* raw model test data

## Pipeline outputs

* lowpass filtered model test data
