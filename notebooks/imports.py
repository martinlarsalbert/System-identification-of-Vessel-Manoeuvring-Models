%load_ext autoreload
%autoreload 2
%reload_kedro
import pandas as pd
from src.models.vmm import ModelSimulator
import matplotlib.pyplot as plt
from src.visualization.plot import track_plots, plot, captive_plot
import kedro
import numpy as np

import matplotlib
matplotlib.rcParams["figure.figsize"] = (15,4)