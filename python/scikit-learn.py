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


class SectionKFold:
    """
    Split the dataset into folds based on sections. Each set of k
    train/test splits is isolated to a single section of data.

    Parameters
    ----------
    n_splits : int, default=5
        Number of folds per section. Must be at least 2.
    shuffle : bool, default=False
        Whether to shuffle the data before splitting into batches.
        Note that the samples within each split will not be shuffled.
    random_state : int or RandomState instance, default=None
        When `shuffle` is True, `random_state` affects the ordering of
        the indices, which controls the randomness of each fold.
        Otherwise, this parameter has no effect.
        Pass an int for reproducible output across multiple function
        calls.
    """

    def __init__(
        self,
        n_splits: int = 5,
        *,
        shuffle: bool = True,
        random_state: Optional[int] = None,
    ) -> None:
        """Constructor."""
        self.n_splits = n_splits
        self.shuffle: bool = shuffle
        self.random_state = random_state
        pass

    def get_n_splits(
        self,
        X: DataFrame,
        sections: Union[str, List[str]],
        y: Optional[Union[Series, ndarray]] = None,
        groups: Optional[Union[Series, ndarray]] = None,
    ) -> int:
        """
        Returns the number of splitting iterations in the cross-validator.

        Parameters
        ----------
        X : DataFrame
            The data to calculate the number of splits.
        sections : Union[str, List[str]]
            The column name to section off the data.
        y : Optional[Union[Series, ndarray]]
            Always ignored, exists for compatibility.
        groups : Optional[Union[Series, ndarray]]
            Always ignored, exists for compatibility.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return X.groupby(sections).count().index.shape[0] * self.n_splits

    def split(
        self,
        X: DataFrame,
        sections: Union[Series, ndarray],
        y: Optional[Union[Series, ndarray]] = None,
        groups: Optional[Union[Series, ndarray]] = None,
    ) -> Generator[Tuple[ndarray, ndarray], None, None]:
        """
        Generate indices to split data into training and test set.

        Parameters
        ----------
        X : DataFrame
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        sections : Union[str, List[str]]
            The column name to section off the data.
        y : array-like of shape (n_samples,), default=None
            The target variable for supervised learning problems.
        groups : array-like of shape (n_samples,), default=None
            Group labels for the samples used while splitting the
            dataset into train/test set.

        Yields
        ------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.
        """
        X = X.copy().reset_index()
        cv = sklearn.model_selection.KFold(
            n_splits=self.n_splits, shuffle=self.shuffle, random_state=self.random_state
        )
        for section_name, section_data in X.groupby(sections):
            if (n_samples := section_data.shape[0]) < self.n_splits:
                raise ValueError(
                    "Cannot have the number of splits"
                    f" n_splits={self.n_splits} greater than the number"
                    f" of samples n_samples={n_samples} in"
                    f" {section_name}"
                )
            for section_train, section_test in cv.split(section_data):
                yield section_data.iloc[
                    section_train
                ].index.to_numpy(), section_data.iloc[section_test].index.to_numpy()
