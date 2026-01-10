"""
Решающие деревья для регрессии.
"""

from typing import Literal

from pydantic import BaseModel, Field
from sklearn.tree import DecisionTreeRegressor  # noqa.


class DecisionTreeRegressorParameters(BaseModel):
    criterion: Literal[
        "squared_error",
        "friedman_mse",
        "absolute_error",
        "poisson",
    ] = Field(
        default="squared_error",
        description="""
The function to measure the quality of a split. Supported criteria
are “squared_error” for the mean squared error, which is equal to
variance reduction as feature selection criterion and minimizes the
L2 loss using the mean of each terminal node, “friedman_mse”, which
uses mean squared error with Friedman’s improvement score for
potential splits, “absolute_error” for the mean absolute error,
which minimizes the L1 loss using the median of each terminal node,
and “poisson” which uses reduction in the half mean Poisson deviance
to find splits.
""",
    )
    splitter: Literal["best", "random"] = Field(
        default="best",
        description="""
The strategy used to choose the split at each node.
Supported strategies are “best” to choose the best split
and “random” to choose the best random split.
""",
    )
    max_depth: int | None = Field(
        default=None,
        ge=1,
        description="""
The maximum depth of the tree. If None, then nodes are
expanded until all leaves are pure or until all leaves
contain less than min_samples_split samples.

For an example of how max_depth influences the model,
see Decision Tree Regression.
""",
    )
    min_samples_split: int | float = Field(
        default=2,
        gt=0,
        description="""
The minimum number of samples required to split an
internal node:

- If int, then consider min_samples_split as the
minimum number.

- If float, then min_samples_split is a fraction
and ceil(min_samples_split * n_samples) are the
minimum number of samples for each split.
""",
    )
    min_samples_leaf: int | float = Field(
        default=1,
        gt=0,
        description="""
The minimum number of samples required to be at a leaf node.
A split point at any depth will only be considered if it leaves
at least min_samples_leaf training samples in each of the left
and right branches. This may have the effect of smoothing the model,
especially in regression.

- If int, then consider min_samples_leaf as the minimum number.

- If float, then min_samples_leaf is a fraction and
ceil(min_samples_leaf * n_samples) are the minimum number
of samples for each node.
""",
    )
    min_weight_fraction_leaf: float = Field(
        default=0.0,
        ge=0.0,
        le=0.5,
        description="""
The minimum weighted fraction of the sum total of weights
(of all the input samples) required to be at a leaf node.
Samples have equal weight when sample_weight is not provided.
""",
    )
    max_features: int | float | Literal["sqrt", "log2"] | None = Field(
        default=None,
        description="""
The number of features to consider when looking for the best split:

- If int, then consider max_features features at each split.

- If float, then max_features is a fraction and
max(1, int(max_features * n_features_in_)) features
are considered at each split.

- If “sqrt”, then max_features=sqrt(n_features).

- If “log2”, then max_features=log2(n_features).

- If None, then max_features=n_features.

Note: the search for a split does not stop until at least one
valid partition of the node samples is found, even if it requires
to effectively inspect more than max_features features.
""",
    )
    random_state: int | None = Field(
        default=None,
        description="""
Controls the randomness of the estimator. The features are always
randomly permuted at each split, even if splitter is set to "best".
When max_features < n_features, the algorithm will select
max_features at random at each split before finding the best split
among them. But the best found split may vary across different runs,
even if max_features=n_features. That is the case, if the improvement
of the criterion is identical for several splits and one split has to
be selected at random. To obtain a deterministic behaviour during fitting,
random_state has to be fixed to an integer. See Glossary for details.
""",
    )
    max_leaf_nodes: int | None = Field(
        default=None,
        ge=2,
        description="""
Grow a tree with max_leaf_nodes in best-first fashion.
Best nodes are defined as relative reduction in impurity.
If None then unlimited number of leaf nodes.
""",
    )
    min_impurity_decrease: float = Field(
        default=0.0,
        ge=0.0,
        description="""
A node will be split if this split induces a decrease of
the impurity greater than or equal to this value.

The weighted impurity decrease equation is the following:

```
N_t / N * (impurity - N_t_R / N_t * right_impurity
                    - N_t_L / N_t * left_impurity)
```

where N is the total number of samples, N_t is the number
of samples at the current node, N_t_L is the number of
samples in the left child, and N_t_R is the number of
samples in the right child.

N, N_t, N_t_R and N_t_L all refer to the weighted sum,
if sample_weight is passed.
""",
    )
    ccp_alpha: float = Field(
        default=0.0,
        ge=0.0,
        description="""
Complexity parameter used for Minimal Cost-Complexity Pruning.
The subtree with the largest cost complexity that is smaller
than ccp_alpha will be chosen. By default, no pruning is performed.
See Minimal Cost-Complexity Pruning for details. See Post pruning
decision trees with cost complexity pruning for an example of such pruning.
""",
    )
    monotonic_cst: list[int] | None = Field(
        default=None,
        description="""
Indicates the monotonicity constraint to enforce on each feature.
- 1: monotonic increase

- 0: no constraint

- -1: monotonic decrease

If monotonic_cst is None, no constraints are applied.

Monotonicity constraints are not supported for:
- multioutput regressions (i.e. when n_outputs_ > 1),

- regressions trained on data with missing values.

Read more in the User Guide.
""",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "criterion": "squared_error",
                    "splitter": "best",
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "min_weight_fraction_leaf": 0.0,
                    "max_features": None,
                    "random_state": None,
                    "max_leaf_nodes": None,
                    "min_impurity_decrease": 0.0,
                    "ccp_alpha": 0.0,
                    "monotonic_cst": None,
                }
            ]
        }
    }
