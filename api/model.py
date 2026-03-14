import sys

import joblib
import pandas as pd

MODEL_PATH = "model/model_random_forest_adresowo_lodz.pkl"

_model = None


# Stub required to unpickle the LGBM pipeline
class LocalityTargetEncoder:
    def __init__(self, smoothing: int = 10) -> None:
        self.smoothing = smoothing
        self.mean_map_: dict = {}
        self.median_map_: dict = {}
        self.std_map_: dict = {}
        self.global_mean_: float = 0.0
        self.global_median_: float = 0.0
        self.global_std_: float = 0.0

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X

    def fit_transform(self, X, y=None):
        return self.transform(X)


sys.modules[__name__].LocalityTargetEncoder = LocalityTargetEncoder  # type: ignore


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_price(area_m2: float, rooms: int, photos: int, locality: str,
                  owner_direct: bool, date_posted: str, street: str | None) -> float:
    model = get_model()
    X = pd.DataFrame(
        [[area_m2, rooms, photos, locality, owner_direct, date_posted, street]],
        columns=["area_m2", "rooms", "photos", "locality", "owner_direct", "date_posted", "street"],
    )
    return float(model.predict(X)[0])
