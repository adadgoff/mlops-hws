"""
Логистическая регрессия.
"""

from typing import Literal

from pydantic import BaseModel, Field
from sklearn.linear_model import LogisticRegression  # noqa.


class LogisticRegressionParameters(BaseModel):
    C: float = Field(
        default=1.0,
        gt=0.0,
        description="""
Inverse of regularization strength; must be a positive float.
Like in support vector machines, smaller values specify stronger
regularization. C=np.inf results in unpenalized logistic regression.
For a visual example on the effect of tuning the C parameter with an
L1 penalty, see: Regularization path of L1- Logistic Regression.
""",
    )
    l1_ratio: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="""
The Elastic-Net mixing parameter, with 0 <= l1_ratio <= 1.
Setting l1_ratio=1 gives a pure L1-penalty, setting l1_ratio=0
a pure L2-penalty. Any value between 0 and 1 gives an Elastic-Net
penalty of the form l1_ratio * L1 + (1 - l1_ratio) * L2.
""",
    )
    dual: bool = Field(
        default=False,
        description="""
Dual (constrained) or primal (regularized, see also this equation)
formulation. Dual formulation is only implemented for l2 penalty
with liblinear solver. Prefer dual=False when n_samples > n_features.
""",
    )
    tol: float = Field(
        default=0.0001,
        gt=0.0,
        description="""
Tolerance for stopping criteria.
""",
    )
    fit_intercept: bool = Field(
        default=True,
        description="""
Specifies if a constant (a.k.a. bias or intercept) should be added
to the decision function.
""",
    )
    intercept_scaling: float = Field(
        default=1,
        gt=0.0,
        description="""
Useful only when the solver liblinear is used and self.fit_intercept
is set to True. In this case, x becomes [x, self.intercept_scaling],
i.e. a “synthetic” feature with constant value equal to intercept_scaling
is appended to the instance vector. The intercept becomes
intercept_scaling * synthetic_feature_weight.

Note

The synthetic feature weight is subject to L1 or L2 regularization as all
other features. To lessen the effect of regularization on synthetic feature
weight (and therefore on the intercept) intercept_scaling has to be increased.
""",
    )
    class_weight: dict | Literal["balanced"] | None = Field(
        default=None,
        description="""
Weights associated with classes in the form {class_label: weight}.
If not given, all classes are supposed to have weight one.

The “balanced” mode uses the values of y to automatically adjust
weights inversely proportional to class frequencies in the input
data as n_samples / (n_classes * np.bincount(y)).

Note that these weights will be multiplied with sample_weight (passed
through the fit method) if sample_weight is specified.
""",
    )
    random_state: int | None = Field(
        default=None,
        description="""
Used when solver == ‘sag’, ‘saga’ or ‘liblinear’ to shuffle the data.
See Glossary for details.
""",
    )
    solver: Literal[
        "lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga"
    ] = Field(
        default="lbfgs",
        description="""
Algorithm to use in the optimization problem. Default is ‘lbfgs’.
To choose a solver, you might want to consider the following aspects:

- ‘lbfgs’ is a good default solver because it works reasonably well
for a wide class of problems.

- For multiclass problems (n_classes >= 3), all solvers except ‘liblinear’
minimize the full multinomial loss, ‘liblinear’ will raise an error.

- ‘newton-cholesky’ is a good choice for n_samples >> n_features * n_classes,
especially with one-hot encoded categorical features with rare categories.
Be aware that the memory usage of this solver has a quadratic dependency on
n_features * n_classes because it explicitly computes the full Hessian matrix.

- For small datasets, ‘liblinear’ is a good choice, whereas ‘sag’ and ‘saga’
are faster for large ones;

- ‘liblinear’ can only handle binary classification by default. To apply a
one-versus-rest scheme for the multiclass setting one can wrap it with the
OneVsRestClassifier.

Note

‘sag’ and ‘saga’ fast convergence is only guaranteed on features with
approximately the same scale. You can preprocess the data with a scaler
from sklearn.preprocessing.

See also

Refer to the User Guide for more information regarding LogisticRegression
and more specifically the Table summarizing solver/penalty supports.
""",
    )
    max_iter: int = Field(
        default=100,
        gt=0,
        description="""
Maximum number of iterations taken for the solvers to converge.
""",
    )
    verbose: int = Field(
        default=0,
        ge=0,
        description="""
For the liblinear and lbfgs solvers set verbose to any positive
number for verbosity.
""",
    )
    warm_start: bool = Field(
        default=False,
        description="""
When set to True, reuse the solution of the previous call to fit
as initialization, otherwise, just erase the previous solution.
Useless for liblinear solver. See the Glossary.
""",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "C": 1.0,
                    "l1_ratio": 0.0,
                    "dual": False,
                    "tol": 0.0001,
                    "fit_intercept": True,
                    "intercept_scaling": 1,
                    "class_weight": None,
                    "random_state": None,
                    "solver": "lbfgs",
                    "max_iter": 100,
                    "verbose": 0,
                    "warm_start": False,
                }
            ]
        }
    }
