"""Snippets for scikit-learn."""
from typing import List

from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
import sklearn.compose
from sklearn.pipeline import Pipeline
import sklearn.pipeline
import sklearn.impute


def make_preprocess_pipe(
    cont_features: List[str], cat_features: List[str], drop_features: List[str]
) -> ColumnTransformer:
    """
    A scikit-learn preprocess pipeline.

    Splits features into three general tracks—continuous, categorical,
    and dropped.

    Parameters
    ----------
    cont_features : List[str]
        The names of the continuous features.
    cat_features : List[str]
        The names of categorical features.
    drop_features : List[str]
        The names of features to drop.

    Returns
    -------
    ColumnTransformer
        A scikit-learn pipeline that independently transforms feature sets.
    """
    cont_pipe = sklearn.pipeline.Pipeline(
        [
            (
                "impute",
                sklearn.impute.SimpleImputer(strategy="mean", add_indicator=True),
            ),
            ("scale", sklearn.preprocessing.StandardScaler()),
        ]
    )
    cat_pipe = sklearn.pipeline.Pipeline(
        [
            (
                "impute",
                sklearn.impute.SimpleImputer(
                    strategy="most_frequent", add_indicator=True
                ),
            ),
            (
                "encode",
                sklearn.preprocessing.OneHotEncoder(
                    categories="auto", handle_unknown="ignore"
                ),
            ),
        ]
    )
    preprocess_pipe = sklearn.compose.ColumnTransformer(
        [
            ("cont_features", cont_pipe, cont_features),
            ("cat_features", cat_pipe, cat_features),
            ("drop", "drop", drop_features),
        ],
        n_jobs=-1,
    )
    return preprocess_pipe


def make_full_pipeline(
    preprocess_pipe: ColumnTransformer, model: BaseEstimator
) -> Pipeline:
    """
    A template scikit-learn pipeline.

    The preprocess pipe is run before the model.

    Parameters
    ----------
    preprocess_pipe : ColumnTransformer
        A preprocessing pipeline.
    model : BaseEstimator
        A model following the scikit-learn api.

    Returns
    -------
    Pipeline
        A scikit-learn pipeline that runs the preprocessing pipeline before the
        model.
    """
    full_pipe = sklearn.pipeline.Pipeline(
        [("preprocess", preprocess_pipe), ("model", model)]
    )
    return full_pipe


def get_continuous_feature_names(
    pipeline: Pipeline, transformer_name: str, feature_names: List[str]
) -> List[str]:
    """
    Get the names for the transformed continuous features.

    Parameters
    ----------
    pipeline : Pipeline
        The full pipeline.
    transformer_name : str
        The name of the transformer in the pipeline.
    feature_names : List[str]
        The names of the features associated with the transformer_name.

    Returns
    -------
    List[str]
        A list of processed column names.
    """
    return feature_names + [
        f"{feature_names[idx]}_missing"
        for idx in pipeline["preprocess"]
        .named_transformers_[transformer_name]["impute"]
        .indicator_.features_
    ]


def get_categorical_feature_names(
    pipeline: Pipeline, transformer_name: str, feature_names: List[str]
) -> List[str]:
    """
    Get the names of the transformed categorial features.

    Parameters
    ----------
    pipeline : Pipeline
        The full pipeline.
    transformer_name : str
        The name of the transformer in the pipeline.
    feature_names : List[str]
        The names of the features associated with the transformer_name.

    Returns
    -------
    List[str]
        A list of processed column names.
    """
    full_feature_names = feature_names + [
        f"{feature_names[idx]}_missing"
        for idx in pipeline["preprocess"]
        .named_transformers_[transformer_name]["impute"]
        .indicator_.features_
    ]
    feature_names_mapping = {
        f"x{idx}": feature_name for idx, feature_name in enumerate(full_feature_names)
    }
    encoded_feature_names = (
        pipeline["preprocess"]
        .named_transformers_["cat_features"]["encode"]
        .get_feature_names()
    )
    categorical_feature_names = []
    for feature_name in encoded_feature_names:
        prefix, name = feature_name.split("_", maxsplit=1)
        categorical_feature_names.append(f"{feature_names_mapping[prefix]}_{name}")
    return categorical_feature_names


# Param grid for pipeline
param_grid = {"model__alpha": [1, 2]}
