"""
app.py
Dashboard de Análisis de Ventas 2025-2026
Ejecutar: python app.py
Abrir en: http://127.0.0.1:8050
"""

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output

from src.data_loader import load_data
from src.preprocessing import enrich
from src.kpis import (
    summary_kpis,
    sales_by_period,
    sales_by_month_name,
    top_products_by_sales,
    roi_by_product,
    product_monthly_trend,
)

# ── Paleta corporativa ────────────────────────────────────────────────────────
PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
WARNING = "#D97706"
DANGER  = "#DC2626"
BG_CARD = "#1E293B"
BG_PAGE = "#0F172A"
TEXT    = "#F1F5F9"
SUBTLE  = "#94A3B8"
GRID    = "#1E293B"

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Inter, sans-serif"),
        xaxis=dict(gridcolor=GRID, linecolor=GRID),
        yaxis=dict(gridcolor=GRID, linecolor=GRID),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
)

CARD_STYLE = {
    "backgroundColor": BG_CARD,
    "borderRadius": "12px",
    "padding": "20px",
    "border": f"1px solid #334155",
}

# ── Carga y preparación de datos ──────────────────────────────────────────────
df_raw = load_data()
df = enrich(df_raw)

kpis     = summary_kpis(df)
years    = sorted(df["year"].unique().tolist())
products = sorted(df["product"].unique().tolist())


# ── Helpers de formato ────────────────────────────────────────────────────────

def fmt_clp(value: float) -> str:
    """Formatea como pesos chilenos abreviados."""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.0f}K"
    return f"${value:.0f}"


def kpi_card(title: str, value: str, delta: str = "", color: str = PRIMARY) -> dbc.Col:
    return dbc.Col(
        html.Div(
            [
                html.P(title, style={"color": SUBTLE, "fontSize": "13px", "marginBottom": "4px"}),
                html.H3(value, style={"color": TEXT, "fontWeight": "700", "margin": "0"}),
                html.P(delta, style={"color": color, "fontSize": "12px", "marginTop": "4px"}),
            ],
            style=CARD_STYLE,
        ),
        xs=12, sm=6, md=4, lg=2,
    )


# ── Layout ────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="Dashboard de Ventas",
)

app.layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": BG_PAGE, "minHeight": "100vh", "padding": "24px"},
    children=[
        # Header
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Dashboard de Ventas", style={"color": TEXT, "fontWeight": "800", "margin": "0"}),
                        html.P("Análisis integral 2025 – 2026", style={"color": SUBTLE, "margin": "0"}),
                    ]
                ),
                style={"marginBottom": "24px"},
            )
        ),

        # Filtros
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Año", style={"color": SUBTLE, "fontSize": "13px"}),
                            dcc.Dropdown(
                                id="filter-year",
                                options=[{"label": "Todos", "value": "all"}]
                                + [{"label": str(y), "value": y} for y in years],
                                value="all",
                                clearable=False,
                                style={"backgroundColor": BG_CARD},
                            ),
                        ]
                    ),
                    md=3,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Producto", style={"color": SUBTLE, "fontSize": "13px"}),
                            dcc.Dropdown(
                                id="filter-product",
                                options=[{"label": "Todos", "value": "all"}]
                                + [{"label": p, "value": p} for p in products],
                                value="all",
                                clearable=False,
                                style={"backgroundColor": BG_CARD},
                            ),
                        ]
                    ),
                    md=4,
                ),
            ],
            style={"marginBottom": "24px"},
        ),

        # KPI Cards
        dbc.Row(id="kpi-row", style={"marginBottom": "24px"}),

        # Fila 1: evolución temporal + meses con más ventas
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Evolución de Ventas Mensual", style={"color": TEXT}),
                            dcc.Graph(id="chart-evolution", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=8,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Ventas por Mes del Año", style={"color": TEXT}),
                            dcc.Graph(id="chart-monthly", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=4,
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Fila 2: top productos + ROI por producto
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Top Productos por Ventas", style={"color": TEXT}),
                            dcc.Graph(id="chart-top-products", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H6("ROI por Producto (%)", style={"color": TEXT}),
                            dcc.Graph(id="chart-roi", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Fila 3: ventas vs gastos vs utilidad + tendencia por producto
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Ventas / Gastos / Utilidad Mensual", style={"color": TEXT}),
                            dcc.Graph(id="chart-waterfall", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=5,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Tendencia de Ventas por Producto", style={"color": TEXT}),
                            dcc.Graph(id="chart-product-trend", config={"displayModeBar": False}),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=7,
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Footer
        dbc.Row(
            dbc.Col(
                html.P(
                    f"Dataset: {len(df)} registros · Período: {df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}",
                    style={"color": SUBTLE, "fontSize": "12px", "textAlign": "center"},
                )
            )
        ),
    ],
)


# ── Callbacks ─────────────────────────────────────────────────────────────────

def filter_df(year, product):
    dff = df.copy()
    if year != "all":
        dff = dff[dff["year"] == year]
    if product != "all":
        dff = dff[dff["product"] == product]
    return dff


@app.callback(
    Output("kpi-row", "children"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_kpis(year, product):
    dff = filter_df(year, product)
    k = summary_kpis(dff)
    return [
        kpi_card("Ventas Totales",   fmt_clp(k["total_sales"]),    color=PRIMARY),
        kpi_card("Gastos Totales",   fmt_clp(k["total_expenses"]), color=WARNING),
        kpi_card("Utilidad Neta",    fmt_clp(k["total_profit"]),   color=SUCCESS),
        kpi_card("Unidades Vendidas",f"{k['total_units']:,.0f}",    color=PRIMARY),
        kpi_card("ROI",              f"{k['roi']:.1f}%",            color=SUCCESS if k["roi"] > 0 else DANGER),
        kpi_card("Margen Neto",      f"{k['margin']:.1f}%",         color=SUCCESS if k["margin"] > 0 else DANGER),
    ]


@app.callback(
    Output("chart-evolution", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_evolution(year, product):
    dff = filter_df(year, product)
    agg = sales_by_period(dff, "month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=agg["period"], y=agg["sales"],
        name="Ventas", mode="lines+markers",
        line=dict(color=PRIMARY, width=2.5),
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=agg["period"], y=agg["profit"],
        name="Utilidad", mode="lines+markers",
        line=dict(color=SUCCESS, width=2, dash="dot"),
        marker=dict(size=5),
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=280)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


@app.callback(
    Output("chart-monthly", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_monthly(year, product):
    dff = filter_df(year, product)
    agg = sales_by_month_name(dff)
    fig = px.bar(
        agg, x="sales", y="month",
        orientation="h",
        color="sales",
        color_continuous_scale=[[0, "#1E40AF"], [1, "#60A5FA"]],
        labels={"sales": "Ventas", "month": ""},
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=280)
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    return fig


@app.callback(
    Output("chart-top-products", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_top_products(year, product):
    dff = filter_df(year, product)
    top = top_products_by_sales(dff, n=7)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Ventas", x=top["product"], y=top["sales"],
        marker_color=PRIMARY, opacity=0.9,
    ))
    fig.add_trace(go.Bar(
        name="Utilidad", x=top["product"], y=top["profit"],
        marker_color=SUCCESS, opacity=0.9,
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], barmode="group", height=300)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig.update_xaxes(tickangle=-20)
    return fig


@app.callback(
    Output("chart-roi", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_roi(year, product):
    dff = filter_df(year, product)
    roi = roi_by_product(dff)
    colors = [SUCCESS if v > 0 else DANGER for v in roi["roi"]]
    fig = go.Figure(go.Bar(
        x=roi["roi"], y=roi["product"],
        orientation="h",
        marker_color=colors,
        text=roi["roi"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=300)
    fig.update_xaxes(ticksuffix="%")
    return fig


@app.callback(
    Output("chart-waterfall", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_waterfall(year, product):
    dff = filter_df(year, product)
    agg = sales_by_period(dff, "month")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Ventas", x=agg["period"], y=agg["sales"],
        marker_color=PRIMARY, opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        name="Gastos", x=agg["period"], y=agg["expenses"],
        marker_color=WARNING, opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        name="Utilidad", x=agg["period"], y=agg["profit"],
        marker_color=SUCCESS, opacity=0.85,
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], barmode="group", height=280)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig.update_xaxes(tickangle=-30)
    return fig


@app.callback(
    Output("chart-product-trend", "figure"),
    Input("filter-year", "value"),
    Input("filter-product", "value"),
)
def update_product_trend(year, product):
    dff = filter_df(year, product)
    trend = product_monthly_trend(dff)
    fig = px.line(
        trend, x="year_month", y="sales", color="product",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Plotly,
        labels={"year_month": "", "sales": "Ventas", "product": "Producto"},
    )
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=280)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig.update_xaxes(tickangle=-30)
    return fig


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
