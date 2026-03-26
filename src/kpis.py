"""
kpis.py
Cálculo de KPIs principales del negocio.
"""

import pandas as pd


# ── Resumen global ────────────────────────────────────────────────────────────

def summary_kpis(df: pd.DataFrame) -> dict:
    """Retorna un dict con los KPIs de alto nivel."""
    total_sales = df["sales"].sum()
    total_expenses = df["expenses"].sum()
    total_profit = df["profit"].sum()
    total_units = df["units_sold"].sum()
    roi = (total_profit / total_expenses * 100) if total_expenses else 0
    margin = (total_profit / total_sales * 100) if total_sales else 0
    return {
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "total_units": total_units,
        "roi": roi,
        "margin": margin,
    }


# ── Series temporales ─────────────────────────────────────────────────────────

def sales_by_period(df: pd.DataFrame, period: str = "month") -> pd.DataFrame:
    """
    Agrupa ventas, gastos y utilidad por período.
    period: 'month' (year_month) | 'year'
    """
    group_col = "year_month" if period == "month" else "year"
    agg = (
        df.groupby(group_col, sort=True)
        .agg(sales=("sales", "sum"), expenses=("expenses", "sum"), profit=("profit", "sum"))
        .reset_index()
        .rename(columns={group_col: "period"})
    )
    agg["roi"] = (agg["profit"] / agg["expenses"] * 100).round(2)
    return agg


def sales_by_month_name(df: pd.DataFrame) -> pd.DataFrame:
    """Ventas totales por nombre de mes (todos los años combinados), respetando orden."""
    agg = (
        df.groupby("month_cat", observed=True)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"), units=("units_sold", "sum"))
        .reset_index()
        .rename(columns={"month_cat": "month"})
    )
    return agg


# ── Productos ─────────────────────────────────────────────────────────────────

def top_products_by_sales(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top N productos por ventas totales."""
    return (
        df.groupby("product")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
            expenses=("expenses", "sum"),
            units=("units_sold", "sum"),
        )
        .assign(roi=lambda x: (x["profit"] / x["expenses"] * 100).round(2))
        .sort_values("sales", ascending=False)
        .head(n)
        .reset_index()
    )


def roi_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """ROI (%) por producto."""
    return (
        df.groupby("product")
        .agg(expenses=("expenses", "sum"), profit=("profit", "sum"))
        .assign(roi=lambda x: (x["profit"] / x["expenses"] * 100).round(2))
        .sort_values("roi", ascending=False)
        .reset_index()
    )


def product_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Ventas mensuales por producto (para análisis de tendencia)."""
    return (
        df.groupby(["year_month", "product"])
        .agg(sales=("sales", "sum"))
        .reset_index()
    )
