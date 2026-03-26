# Dashboard de Análisis de Ventas 2025–2026

Dashboard interactivo construido con **Python + Dash + Plotly** para el análisis de ventas de productos de snacks y frutos secos, con datos del período enero 2025 – marzo 2026.

---

## Características

- **6 KPI cards** en tiempo real: Ventas totales, Gastos, Utilidad neta, Unidades vendidas, ROI y Margen neto
- **Filtros interactivos** por año y producto
- **7 visualizaciones:**
  - Evolución de ventas mensual (línea)
  - Ventas por mes del año — estacionalidad (barras)
  - Top productos por ventas vs. utilidad (barras agrupadas)
  - ROI por producto en % (barras horizontales)
  - Ventas / Gastos / Utilidad mensual comparados
  - Tendencia de ventas por producto a lo largo del tiempo

---

## Tecnologías

| Librería | Uso |
|---|---|
| `pandas` | Carga, limpieza y transformación de datos |
| `plotly` | Gráficos interactivos |
| `dash` | Servidor web del dashboard |
| `dash-bootstrap-components` | Tema y layout responsivo |

---

## Estructura del proyecto

```
├── app.py                  # Dashboard principal (entry point)
├── dataset_ventas.csv      # Dataset de ventas
├── requirements.txt        # Dependencias
├── assets/
│   └── custom.css          # Estilos personalizados
└── src/
    ├── __init__.py
    ├── data_loader.py      # Carga y parsing del CSV
    ├── preprocessing.py    # Enriquecimiento del dataset
    └── kpis.py             # Cálculo de métricas de negocio
```

---

Abrir en el navegador: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## Dataset

El archivo `dataset_ventas.csv` contiene 120 registros con las siguientes columnas:

| Columna | Descripción |
|---|---|
| `DATE` | Fecha de la transacción |
| `MONTH` | Mes en español |
| `YEAR` | Año |
| `ID PRODUCT` | Nombre del producto |
| `QUANTITY` | Cantidad de paquetes comprados |
| `EXPENSES` | Costo total (CLP) |
| `SELLING PRICE` | Precio de venta unitario (CLP) |
| `UNITS SOLD` | Unidades vendidas |
| `SALES` | Ingresos totales (CLP) |
| `PROFIT` | Utilidad neta (CLP) |

---

## KPIs globales del dataset

| Métrica | Valor |
|---|---|
| Ventas totales | $11.4M CLP |
| Gastos totales | $4.8M CLP |
| Utilidad neta | $6.6M CLP |
| ROI | 138% |
| Margen neto | 58% |
