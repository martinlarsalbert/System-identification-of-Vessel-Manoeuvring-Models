# System-identification-of-Vessel-Manoeuvring-Models
This repository was used to carry out the research as well as the generation of the paper:"System-identification-of-Vessel-Manoeuvring-Models".
The LaTeX part of the paper is however stored in another repository: [LaTeX](https://github.com/martinlarsalbert/System-identification-of-Vessel-Manoeuvring-Models-LaTex).

## Setup the environment:
* Python >=3.7
* ```pip install -r .\src\requirements.txt```

## Reproduce results
* Download the wPCC data from [here](https://data.mendeley.com/datasets/j5zdrhr9bf)
* Copy all the files into [wpcc data folder](data/01_raw/wpcc/). The files in the ''model_tests'' folder should also be moved to the subfolder.
* The analysis has been defined as a [Kedro pipeline](https://kedro.readthedocs.io)
* The various pilelines can be listed as: ```kedro registry list``` giving:
```
- __default__
- kvlcc2_hsva
- kvlcc2_hsva_create      
- lowpass_study
- plot
- plot_filters_kvlcc2     
- plot_filters_kvlcc2_hsva
- plot_filters_wpcc       
- plot_kvlcc2
- plot_kvlcc2_hsva
- plot_wpcc
- work
- wpcc
```
* The KVLCC2 data from HSVA needs to be preprocessed: ```kedro run --pipeline kvlcc2_hsva_create```
* The whole analysis can be run with: ```kedro run``` (it takes quite a while to run)

## Results:
* [Track plots of raw data](data/08_reporting)
* [Kalman filtered and RTS smoothened data](data/03_primary)
* [Identified models](data/06_models)
* [Simulation results with models](data/07_model_output)

## Post process results
* Plot simulations with wPCC: ```kedro run --pipeline plot_wpcc```
* Plot simulations with KVLCC2: ```kedro run --pipeline plot_kvlcc2_hsva```
* [Plots end up here](data/07_model_output)
* The paper is generated with jupyter notebooks [here](docs/paper/). These must be launched with kedro prefix: ```kedro jupyter lab```


## Build paper
Build jupyter book to LaTeX, apply some fixes and then create PDF wit xelatex.
[build.bat](/docs/paper/build.bat)

## Overview
This is your new Kedro project, which was generated using `Kedro 0.17.6`.
Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.
More information about Kedro can be found further below.


### JupyterLab
You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://kedro.readthedocs.io/en/stable/03_tutorial/05_package_a_project.html)
