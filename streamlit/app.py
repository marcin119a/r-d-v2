import sys
import types
import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ── LocalityTargetEncoder must be defined before unpickling the LGBM pipeline ──
class LocalityTargetEncoder:
    """Stub that mirrors the custom encoder stored in the LGBM pickle."""

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


# Make the class discoverable under __main__ (required by pickle)
_main = sys.modules["__main__"]
_main.LocalityTargetEncoder = LocalityTargetEncoder  # type: ignore[attr-defined]


# ── Model loading (cached across reruns) ────────────────────────────────────
MODEL_PATH = "model/model_random_forest_adresowo_lodz.pkl"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def predict_price(
    area_m2: float,
    rooms: int,
    photos: int,
    owner_direct: bool,
    locality: str,
    date_posted: datetime.date,
) -> float:
    model = load_model()
    date_str = date_posted.strftime("%Y-%m-%d")
    X_new = pd.DataFrame(
        [[area_m2, rooms, photos, locality, owner_direct, date_str, None]],
        columns=["area_m2", "rooms", "photos", "locality", "owner_direct", "date_posted", "street"],
    )
    return float(model.predict(X_new)[0])


# ── Streamlit UI ─────────────────────────────────────────────────────────────
def main() -> None:
    st.set_page_config(page_title="Predykcja ceny mieszkania", page_icon="🏠")
    st.title("Predykcja ceny mieszkania (Adresowo)")
    st.write("Podaj dane mieszkania, aby uzyskać szacowaną cenę:")

    area = st.number_input("Powierzchnia (m²)", min_value=10.0, max_value=300.0, value=50.0, step=1.0)
    rooms = st.slider("Liczba pokoi", 1, 6, 3)
    photos = st.number_input("Liczba zdjęć", min_value=0, max_value=50, value=10)
    owner_direct = st.checkbox("Oferta bezpośrednio od właściciela", value=True)
    locality = st.selectbox(
        "Dzielnica",
        ["Łódź Bałuty", "Łódź Górna", "Łódź Śródmieście", "Łódź Widzew", "Łódź Polesie"],
    )
    date_posted = st.date_input("Data ogłoszenia", value=datetime.date.today())

    if st.button("Szacuj cenę", type="primary"):
        with st.spinner("Trwa obliczanie..."):
            try:
                price = predict_price(
                    area_m2=area,
                    rooms=int(rooms),
                    photos=int(photos),
                    owner_direct=owner_direct,
                    locality=locality,
                    date_posted=date_posted,
                )
                st.success(f"### Szacowana cena: **{price:,.0f} zł**")
                col1, col2 = st.columns(2)
                col1.metric("Cena za m²", f"{price / area:,.0f} zł/m²")
                col2.metric("Łączna cena", f"{price:,.0f} zł")
            except Exception as exc:
                st.error(f"Błąd predykcji: {exc}")


if __name__ == "__main__":
    main()
