# Pipeline motion_regression

## Overview

Motion regression is performed with the *MotionRegression* class.
This is a way to create a simulation model from motion measurements. This is an alternative to the: [force_regression-pipeline](../force_regression/README.md).

## Pipeline inputs

* Estimated model test states from the RTS smoother
* Ship mass properties
* Ship added masses (can be estimated in the [brix-pipeline](../brix/README.md)).


## Pipeline outputs

* motion regression
* estimated hydrodynamic parameters
* summaries of the regressions
