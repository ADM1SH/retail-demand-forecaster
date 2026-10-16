from pathlib import Path
from typing import List
import pandas as pd
from pydantic import BaseModel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MATRIX_PATH = DATA_DIR / "hygr_indexed_matrix.csv"
MACRO_PATH = DATA_DIR / "table_3_5_private_consumption.csv"

HYGR_CHANNELS: List[str] = [
    "Shopee MY",
    "Shopee SG",
    "TikTok MY",
    "TikTok SG",
]

class HYGRChannelMetric(BaseModel):
    period: str
    platform_region: str
    sales_index: float
    orders_index: float
    visitors_index: float
    basket_size_rm: float
    conversion_rate_pct: float
    macro_predicted_index: float

def load_indexed_matrix() -> pd.DataFrame:
    return pd.read_csv(MATRIX_PATH)

def load_macro_consumption_indicators() -> pd.DataFrame:
    return pd.read_csv(MACRO_PATH)

def forecast_hygr_retail_demand(
    private_consumption_growth_pct: float = 4.8,
    cpi_inflation_pct: float = 2.3,
    employment_growth_pct: float = 2.0,
) -> List[HYGRChannelMetric]:
    df = load_indexed_matrix()
    cons_delta = private_consumption_growth_pct - 4.8
    cpi_delta = cpi_inflation_pct - 2.3
    emp_delta = employment_growth_pct - 2.0
    scenario_multiplier = 1.0 + (0.018 * cons_delta) - (0.009 * cpi_delta) + (0.015 * emp_delta)

    results: List[HYGRChannelMetric] = []
    for _, row in df.iterrows():
        adj_pred = float(row["macro_predicted_index"]) * (
            scenario_multiplier if "Fcst" in str(row["period"]) else 1.0
        )
        results.append(
            HYGRChannelMetric(
                period=str(row["period"]),
                platform_region=str(row["platform_region"]),
                sales_index=float(row["sales_index"]),
                orders_index=float(row["orders_index"]),
                visitors_index=float(row["visitors_index"]),
                basket_size_rm=float(row["basket_size_rm"]),
                conversion_rate_pct=float(row["conversion_rate_pct"]),
                macro_predicted_index=round(adj_pred, 2),
            )
        )
    return results
