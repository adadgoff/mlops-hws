from abc import abstractmethod

from sklearn.base import BaseEstimator


class MLBaseModel(BaseEstimator):
    @abstractmethod
    def __name__() -> str:
        pass

    @abstractmethod
    def fit(
        *args,
        **kwargs,
    ) -> None:
        pass

    @abstractmethod
    def predict(
        *args,
        **kwargs,
    ) -> list[float]:
        pass
