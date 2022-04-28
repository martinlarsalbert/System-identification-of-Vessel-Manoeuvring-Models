"""
This is a boilerplate pipeline 'generic_data'
generated using Kedro 0.17.6
"""

import python_vehicle_simulator as pvs
from python_vehicle_simulator import plotVehicleStates, plotControls, simulate
import pandas as pd
from src.visualization.plot import track_plots, plot, captive_plot
import numpy as np
from src.prime_system import PrimeSystem
from python_vehicle_simulator.vehicles import tanker

sampleTime = 1
N = 5000


class Ship(pvs.vehicles.tanker.tanker):

    n = 20
    index = np.linspace(0, N * sampleTime, n)
    deltas = pd.Series(np.deg2rad(np.linspace(-35, 35, n)), index=index)

    def replay_rudder(self, t):

        i = (self.deltas.index >= t).argmax()
        delta = self.deltas.iloc[i]
        return np.array([delta], float)


def generate_data1() -> pd.DataFrame:

    ship = Ship()

    ship.n_c / 90.0  # propeller shaft speed (rps)
    ship.controlMode = "turning circle"

    nu0 = [7, 0, 0, 0, 0, 0]
    time, data = simulate(N, sampleTime, ship, nu0=nu0)

    df = sim_to_df(time=time, data=data, ship=ship)
    return df


def generate_data2() -> pd.DataFrame:

    ship = Ship()

    ship.n_c / 90.0  # propeller shaft speed (rps)
    ship.controlMode = "replay rudder"

    nu0 = [7, 0, 0, 0, 0, 0]
    time, data = simulate(N, sampleTime, ship, nu0=nu0)

    df = sim_to_df(time=time, data=data, ship=ship)
    return df


def sim_to_df(time, data, ship):

    columns = [
        "x0",
        "y0",
        "z0",
        "phi",
        "theta",
        "psi",
        "u",
        "v",
        "w",
        "p",
        "q",
        "r",
        "delta_order",
        "delta",
    ]

    df = pd.DataFrame(index=time.flatten(), data=data, columns=columns)
    u_r = df["u"]
    n = ship.n_c

    L = ship.L
    gT = (
        1 / L * tanker.Tuu * u_r ** 2
        + tanker.Tun * u_r * n
        + L * tanker.Tnn * abs(n) * n
    )

    U = np.sqrt(df["u"] ** 2 + df["v"] ** 2)
    thrust_prime = gT * L / (U ** 2)
    rho = 1000
    ps = PrimeSystem(L=ship.L, rho=rho)

    df["thrust"] = ps._unprime(thrust_prime, unit="force", U=U)
    return df


def add_noise(df: pd.DataFrame, noises: dict) -> pd.DataFrame:

    for key, noise in noises.items():
        df[key] += np.random.normal(scale=noise, size=len(df))

    return df[["x0", "y0", "psi", "delta", "thrust"]]


def get_ship_data() -> dict:

    ship = Ship()
    lpp = ship.L

    rho = 1000
    ps = PrimeSystem(L=lpp, rho=rho)
    CB = 0.8
    B = lpp / 15
    volume = CB * lpp * ship.T * B
    mass = rho * volume

    I_z = (0.25 * lpp) ** 2 * mass
    ship_data = {
        "L": lpp,
        "rho": rho,
        "T": ship.T,
        "B": B,
        "CB": CB,
        "volume": volume,
        "m": mass,
        "x_G": 0,
        "I_z": I_z,
    }

    return ship_data
