from datetime import date, timedelta

from app.core.metrics import (
    calc_ebit_ttm,
    calc_ev_ebit_percentile,
    calc_ebit_growth,
)
from app.core.models import Stock, StockMetrics, StockSignals, StockAnalysis
from app.core.signals import (
    signal_ev_ebit_cycle,
    signal_ebit_positive,
    signal_ebit_growth_positive,
)


def analyze_stock(stock: Stock, target_date: date | None = None) -> StockAnalysis:
    try:
        metrics = _calculate_metrics(stock, target_date)
        signals = StockSignals(
            ev_ebit_5y_cycle=signal_ev_ebit_cycle(metrics.ev_ebit, metrics.ev_ebit_q1_5y),
            ev_ebit_1y_cycle=signal_ev_ebit_cycle(metrics.ev_ebit, metrics.ev_ebit_q1_1y),
            ebit_positive=signal_ebit_positive(metrics.ebit_ttm),
            ebit_growth_positive=signal_ebit_growth_positive(metrics.ebit_growth),
        )

        return StockAnalysis(
            info=stock.info,
            metrics=metrics,
            signals=signals,
        )
    except Exception as e:
        return StockAnalysis(
            info=stock.info,
            metrics=StockMetrics(),
            signals=StockSignals(),
            error=str(e),
        )


def _calculate_metrics(stock: Stock, target_date: date | None = None) -> StockMetrics:
    analysis_date = target_date if target_date else date.today()

    sorted_daily_dates = sorted(
        (day for day in stock.history.daily.keys() if day <= analysis_date),
        reverse=True,
    )
    filed_quarters = sorted(
        (
            quarter for quarter, data in stock.history.quarterly.items()
            if data.filing_date is not None and data.filing_date <= analysis_date
        ),
        reverse=True,
    )

    # EV/EBIT (current)
    if target_date is None:
        assert stock.live
        current_ev_ebit = stock.live.ev_ebit
    else:
        if not sorted_daily_dates:
            current_ev_ebit = None
        else:
            current_ev_ebit = stock.history.daily[sorted_daily_dates[0]].ev_ebit

    # EV/EBIT (historical cycle)
    daily_ev_ebit: dict[date, float] = {}
    for day in sorted_daily_dates:
        stock_daily_data = stock.history.daily[day]
        if stock_daily_data.ev_ebit is not None and stock_daily_data.ev_ebit > 0:
            daily_ev_ebit[day] = stock_daily_data.ev_ebit

    def calc_ev_ebit_cycle(
            ev_ebit_data: dict[date, float],
            years: int,
            end_date: date,
    ) -> tuple[float | None, int]:
        date_ago = end_date - timedelta(days=365 * years)
        values = [value for day, value in ev_ebit_data.items() if day >= date_ago]
        return calc_ev_ebit_percentile(values, 25), len(values)

    ev_ebit_q1_5y, ev_ebit_days_5y = calc_ev_ebit_cycle(daily_ev_ebit, 5, analysis_date)
    ev_ebit_q1_1y, ev_ebit_days_1y = calc_ev_ebit_cycle(daily_ev_ebit, 1, analysis_date)

    # EBIT TTM & EBIT YoY Growth
    ebit_ttm_current = None
    if len(filed_quarters) >= 4:
        current_quarters = [stock.history.quarterly[quarter] for quarter in filed_quarters[:4]]
        ebit_ttm_current = calc_ebit_ttm([quarter.ebit for quarter in current_quarters])

    ebit_growth = None
    if len(filed_quarters) >= 8:
        prior_quarters = [stock.history.quarterly[quarter] for quarter in filed_quarters[4:8]]
        ebit_ttm_prior = calc_ebit_ttm([quarter.ebit for quarter in prior_quarters])
        ebit_growth = calc_ebit_growth(ebit_ttm_current, ebit_ttm_prior)

    return StockMetrics(
        ev_ebit=current_ev_ebit,
        ev_ebit_q1_5y=ev_ebit_q1_5y,
        ev_ebit_q1_1y=ev_ebit_q1_1y,
        ev_ebit_days_5y=ev_ebit_days_5y,
        ev_ebit_days_1y=ev_ebit_days_1y,
        ebit_ttm=ebit_ttm_current,
        ebit_growth=ebit_growth,
    )
