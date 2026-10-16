from src.forecaster import forecast_hygr_retail_demand, load_macro_consumption_indicators, HYGR_CHANNELS

def test_forecast_dimensions():
    metrics = forecast_hygr_retail_demand(4.8, 2.3, 2.0)
    assert len(metrics) == 40
    channels = {m.platform_region for m in metrics}
    assert channels == set(HYGR_CHANNELS)

def test_macro_indicators():
    df = load_macro_consumption_indicators()
    assert len(df) >= 8
