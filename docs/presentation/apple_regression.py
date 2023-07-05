import statsmodels.api as sm
import pandas as pd


def features_simple(result: pd.DataFrame, parameters: dict):

    m = parameters["m"]
    a = result["a"]
    y = m * a
    X = pd.DataFrame(index=result.index)
    X["g"] = -m
    return X, y


def features_drag(result: pd.DataFrame, parameters: dict):

    m = parameters["m"]
    a = result["a"]
    v = result["v"]

    y = m * a
    X = pd.DataFrame(index=result.index)
    X["g"] = -m
    X["Cd"] = v ** 2
    return X, y


def features_overfit(result: pd.DataFrame, parameters: dict):

    m = parameters["m"]
    x = result["x"]
    a = result["a"]
    v = result["v"]

    y = m * a
    X = pd.DataFrame(index=result.index)
    X["g"] = -m
    X["Cd"] = v ** 2
    X["k"] = x

    return X, y


def fit(result: pd.DataFrame, parameters: dict, func_features=features_simple):

    X, y = func_features(result=result, parameters=parameters)
    model = sm.OLS(y, X).fit()

    parameters1 = {"m": parameters["m"]}
    parameters1.update(model.params)

    return model, parameters1
