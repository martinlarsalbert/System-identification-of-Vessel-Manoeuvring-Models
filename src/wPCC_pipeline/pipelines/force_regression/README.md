# Pipeline force_regression


## Overview

Force regression is performed with the *ForceRegression* class.
This is a way to create a simulation model from force measurements (Captive tests or Virtual Captive Tests [VCT]). This is an alternative to the: [motion_regression-pipeline](../motion_regression/README.md).

## Pipeline inputs

* Force measurements from captive model tests of Virtual Captive Tests (VCT)
* Ship mass properties
* Ship added masses (can be estimated in the [brix-pipeline](../brix/README.md)).

## Pipeline outputs

* estimated hydrodynamic parameters
* summaries of the regressions
