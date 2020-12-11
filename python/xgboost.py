"""Snippets for XGBoost https://github.com/dmlc/xgboost."""

from typing import Literal
from typing import Union


from numpy import ndarray
from pandas import DataFrame
from pandas import Series
import xgboost
from xgboost import XGBClassifier
from xgboost import XGBRegressor


def early_stop_xgb(
    X: Union[DataFrame, ndarray],
    y: Union[Series, ndarray],
    eval_metric: str,
    early_stopping_rounds: int,
    test_size: float,
    model_type: Literal["classifier", "regressor"],
    *args,
    **kwargs,
) -> Union[XGBClassifier, XGBRegressor]:
    """
    Run early stopping using XGBoost.

    Parameters
    ----------
    X : Union[DataFrame, ndarray]
        The train data feature matrix.
    y : Union[Series, ndarray]
        The train data labels.
    eval_metric : str
        The evaluation metric to use on early stopping. A full list may
        be found at
        https://xgboost.readthedocs.io/en/latest/parameter.html#learning-task-parameters.
    early_stopping_rounds : int
        The number of early stopping rounds.
    model_type : Literal["classifier", "regressor"]
        Whether the model is a regressor or classifier.
    *args
        Arguments to pass on to XGBClassifier or XGBRegressor.
    **kwargs
        Keyword arguments to pass on to XGBClassifier or XGBRegressor.
    """
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X,
        y,
        test_size=test_size,
    )
    if "classifier".startswith(model_type.lower()) or "clf".startswith(
        model_type.lower()
    ):
        xgb = xgboost.XGBClassifier(n_jobs=-1, *args, **kwargs)
    elif "regressor".startswith(model_type.lower()):
        xgb = xgboost.XGBRegressor(n_jobs=-1, *args, **kwargs)
    else:
        raise ValueError(
            f"{model_type} is an invalid model_type value."
            " Input 'classifier' or 'regressor'"
        )
    xgb.fit(
        X_train,
        y_train,
        eval_metric=eval_metric,
        early_stopping_rounds=early_stopping_rounds,
        eval_set=[(X_test, y_test)],
        verbose=True,
    )
    return xgb
