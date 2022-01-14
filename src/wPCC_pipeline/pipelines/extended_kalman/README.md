# Pipeline ek

## Overview

This pipeline runs the model test data through a Extended Kalman Filter (EKF) and after that passes the estimated states into a RTS smoother.

## Pipeline inputs

* Hydrodynamic parameters to the VMM (Vessel Manoeuvring Model) which acts as the predictor in the EKF.
* Ship loading condition with mass properties

## Pipeline outputs

* Filtered and smoothened data
* EKF filter and RTS smoother (in case you want to reuse the filter, for instance in the EM-algorithm.)
