from datetime import date, timedelta

from app.core.metrics import (
    calc_pe_ntm,
    calc_pe_ntm_percentile,
    calc_ni_ttm,
    calc_nni_ttm,
    calc_nni_cagr,
    calc_revenue_ltm,
    calc_nni_margin,
)
from app.core.models import Stock, StockMetrics, StockSignals, StockAnalysis
from app.core.signals import signal_pe_ntm_cycle, signal_nni_cagr, signal_nni_margin


def analyze_stock(stock: Stock, target_date: date | None = None) -> StockAnalysis:
    try:
        metrics = _calculate_metrics(stock, target_date)
        signals = StockSignals(
            pe_ntm_10y_cycle=signal_pe_ntm_cycle(metrics.pe_ntm, metrics.pe_ntm_q1_5y),
            pe_ntm_1y_cycle=signal_pe_ntm_cycle(metrics.pe_ntm, metrics.pe_ntm_q1_1y),
            nni_cagr_positive=signal_nni_cagr(metrics.nni_cagr),
            nni_margin_positive=signal_nni_margin(metrics.nni_margin),
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
        reverse=True
    )
    sorted_quarterly_dates = sorted(
        (quarter for quarter in stock.history.quarterly.keys() if quarter <= analysis_date),
        reverse=True
    )

    # P/E NTM (current)
    if target_date is None:
        if stock.live is None:
            raise ValueError("Live data required when target_date is None")
        current_price = stock.live.price
        current_eps_ntm = stock.live.eps_ntm
    else:
        if not sorted_daily_dates:
            current_price = None
            current_eps_ntm = None
        else:
            current_daily_stock_data = stock.history.daily[sorted_daily_dates[0]]
            current_price = current_daily_stock_data.price
            current_eps_ntm = current_daily_stock_data.eps_ntm

    pe_ntm = calc_pe_ntm(current_price, current_eps_ntm)

    # P/E NTM (historical)
    daily_pe_ntm: dict[date, float] = {}
    for day in sorted_daily_dates:
        stock_daily_data = stock.history.daily[day]
        if stock_daily_data.price and stock_daily_data.price > 0 and stock_daily_data.eps_ntm and stock_daily_data.eps_ntm > 0:
            daily_pe_ntm[day] = calc_pe_ntm(stock_daily_data.price, stock_daily_data.eps_ntm)

    def calc_pe_ntm_cycle(
            pe_ntm_data: dict[date, float],
            years: int,
            end_date: date,
    ) -> tuple[float | None, int]:
        date_ago = end_date - timedelta(days=365 * years)
        pe_data = [pe for day, pe in pe_ntm_data.items() if day >= date_ago]
        return calc_pe_ntm_percentile(pe_data, 25), len(pe_data)

    pe_ntm_q1_5y, pe_ntm_days_5y = calc_pe_ntm_cycle(daily_pe_ntm, 5, analysis_date)
    pe_ntm_q1_1y, pe_ntm_days_1y = calc_pe_ntm_cycle(daily_pe_ntm, 1, analysis_date)

    # NNI CAGR
    def calc_nni_ttm_from_quarters(quarter_dates: list[date]) -> float | None:
        quarters = [stock.history.quarterly[day] for day in quarter_dates]
        ni_ttm = calc_ni_ttm([quarter.net_income for quarter in quarters])
        shares = quarters[0].shares_outstanding
        return calc_nni_ttm(ni_ttm, shares) if shares else None

    nni_cagr = None
    if len(sorted_quarterly_dates) >= 8:
        nni_ttm_current = calc_nni_ttm_from_quarters(sorted_quarterly_dates[:4])
        nni_ttm_prior = calc_nni_ttm_from_quarters(sorted_quarterly_dates[4:8])
        nni_cagr = calc_nni_cagr(nni_ttm_current, nni_ttm_prior)

    # NNI Margin
    nni_margin = None
    if len(sorted_quarterly_dates) >= 4:
        current_quarters = [stock.history.quarterly[day] for day in sorted_quarterly_dates[:4]]
        ni_ttm = calc_ni_ttm([quarter.net_income for quarter in current_quarters])
        revenue_ltm = calc_revenue_ltm([quarter.revenue for quarter in current_quarters])
        nni_margin = calc_nni_margin(ni_ttm, revenue_ltm)

    return StockMetrics(
        pe_ntm=pe_ntm,
        pe_ntm_q1_5y=pe_ntm_q1_5y,
        pe_ntm_q1_1y=pe_ntm_q1_1y,
        pe_ntm_days_5y=pe_ntm_days_5y,
        pe_ntm_days_1y=pe_ntm_days_1y,
        nni_cagr=nni_cagr,
        nni_margin=nni_margin,
    )
