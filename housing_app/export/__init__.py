from housing_app.export.csv_export import save_csv
from housing_app.export.xlsx_export import save_xlsx

DEFAULT_FIELDNAMES = ["id", "url", "locality", "rooms", "area_m2", "price_total_zl", "price_per_m2_zl"]
NUMERIC_FIELDS = {"rooms", "area_m2", "price_total_zl", "price_per_m2_zl"}

__all__ = ["save_csv", "save_xlsx", "DEFAULT_FIELDNAMES", "NUMERIC_FIELDS"]
