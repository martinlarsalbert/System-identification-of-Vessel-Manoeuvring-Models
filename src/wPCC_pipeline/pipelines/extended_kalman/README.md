# Pipeline ek

## Overview

Create an Extended Kalman Filter (EKF) with a prediction model with guessed parameters for one ship. This filter can then be reused for many model tests, as long as the ship model is the same (and the guessed model is accurate enought.).

## Pipeline inputs

* Hydrodynamic parameters to the VMM (Vessel Manoeuvring Model) which acts as the predictor in the EKF.
* Ship loading condition with mass properties

## Pipeline outputs

* EKF filter and RTS smoother (in case you want to reuse the filter, for instance in the EM-algorithm.)
