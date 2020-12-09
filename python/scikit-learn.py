"""Snippets for scikit-learn."""
from typing import List

from sklearn.pipeline import Pipeline
import sklearn.pipeline
import sklearn.impute


def make_pipeline(
    cont_features: List[str], cat_features: List[str], drop_features: List[str], 
) -> Pipeline:
    """
    A template scikit-learn pipeline.

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
    Pipeline
        A scikit-learn pipeline.
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
            ("onehot", sklearn.preprocessing.OneHotEncoder(categories="auto")),
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
    full_pipe = sklearn.pipeline.Pipeline(
        [("preprocess", preprocess_pipe), ("model", sklearn.linear_model.Ridge())]
    )
    return full_pipe


def get_feature_names(
    pipeline: Pipeline, transformer_name: str, feature_names: List[str]
) -> List[str]:
    """
    Get the names for the transformed features.

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
