from scipy.integrate import solve_ivp
import pandas as pd
import numpy as np


def acceleration(x, parameters) -> np.ndarray:

    g = parameters["g"]
    Cd = parameters.get("Cd", 0)
    m = parameters["m"]

    if x.ndim == 1:
        x1d = x[1]
    else:
        x1d = x[:, 1]

    fx = -g * m + Cd * x1d ** 2
    x2d = fx / m
    return x2d


def step(t, x, parameters) -> np.ndarray:
    """
    x = [x,x1d]
    dxdt = [x1d,x2d]
    """
    x1d = x[1]
    x2d = acceleration(x=x, parameters=parameters)
    dx = [x1d, x2d]
    return dx


def _simulate(
    t: np.ndarray,
    x0=[0, 0],
    parameters: dict = {
        "g": 9.81,
        "Cd": 0.000,
        "m": 1.0,
    },
):
    t_span = [t[0], t[-1]]

    solution = solve_ivp(
        fun=step,
        t_span=t_span,
        y0=x0,
        t_eval=t,
        args=(parameters,),
    )

    # assert solution.success is True
    return solution


def solution_to_df(t: np.ndarray, solution, parameters: dict) -> pd.DataFrame:

    result = pd.DataFrame(
        index=t[0 : len(solution.y.T)], data=solution.y.T, columns=["x", "v"]
    )
    result["a"] = acceleration(x=result[["x", "v"]].values, parameters=parameters)
    return result


def simulate(
    t: np.ndarray,
    x0=[0, 0],
    parameters: dict = {
        "g": 9.81,
        "Cd": 0.000,
        "m": 1.0,
    },
) -> pd.DataFrame:

    solution = _simulate(t=t, x0=x0, parameters=parameters)
    result = solution_to_df(t=t, solution=solution, parameters=parameters)

    return result
