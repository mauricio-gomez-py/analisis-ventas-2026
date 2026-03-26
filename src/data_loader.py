"""
data_loader.py
Carga y validación inicial del dataset de ventas.
"""

import csv
import pandas as pd
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "dataset_ventas.csv"

COLUMN_NAMES = [
    "date", "month", "year", "product",
    "quantity", "expenses", "selling_price",
    "units_sold", "sales", "profit",
]


def load_data(path: Path = DATASET_PATH) -> pd.DataFrame:
    """
    Lee el CSV donde cada fila está envuelta en comillas dobles, p. ej.:
        "DATE;MONTH;YEAR;..."
    csv.reader (con delimitador coma) trata cada línea como un único campo
    y elimina las comillas; luego se parte por ';'.
    """
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f):          # quotechar='"', delimiter=',' (default)
            if row:
                rows.append(row[0].split(";"))

    # La primera fila es el encabezado original; se descarta
    df = pd.DataFrame(rows[1:], columns=COLUMN_NAMES)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    for col in ["quantity", "expenses", "selling_price", "units_sold", "sales", "profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["year"] = df["year"].astype(int)
    return df
