"""
preprocessing.py
Transformaciones y enriquecimiento del dataset.
"""

import pandas as pd

MONTH_ORDER = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

MONTH_NUMBER = {m: i + 1 for i, m in enumerate(MONTH_ORDER)}


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas calculadas útiles para el análisis."""
    df = df.copy()
    df["month_num"] = df["month"].str.lower().map(MONTH_NUMBER)
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    df["margin_pct"] = (df["profit"] / df["sales"] * 100).round(2)
    df["roi"] = (df["profit"] / df["expenses"] * 100).round(2)
    df["month_cat"] = pd.Categorical(
        df["month"].str.lower(), categories=MONTH_ORDER, ordered=True
    )
    return df.dropna(subset=["date", "sales", "profit", "expenses"])
