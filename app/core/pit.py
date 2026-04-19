from datetime import date
from itertools import pairwise

from app.core.metrics import calc_ebit_ttm, calc_ev, calc_ev_ebit
from app.core.models import StockQuarterlyData


def compute_pit_ev_ebit(
        day: date,
        price: float,
        quarterly_records: list[tuple[date, StockQuarterlyData]],
) -> float | None:
    assert all(a[0] <= b[0] for a, b in pairwise(quarterly_records))

    latest_idx = -1
    for i in range(len(quarterly_records) - 1, -1, -1):
        quarter_data = quarterly_records[i][1]
        if quarter_data.filing_date is not None and quarter_data.filing_date <= day:
            latest_idx = i
            break

    if latest_idx < 3:
        return None

    ebits = [quarterly_records[latest_idx - i][1].ebit for i in range(4)]
    ebit_ttm = calc_ebit_ttm(ebits)

    latest_quarter = quarterly_records[latest_idx][1]
    if latest_quarter.shares_outstanding is None:
        return None
    market_cap = price * latest_quarter.shares_outstanding
    ev = calc_ev(market_cap, latest_quarter.total_debt, latest_quarter.cash)
    return calc_ev_ebit(ev, ebit_ttm)
