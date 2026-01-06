from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DailySnapshot:
    date: date
    equity: float
    positions: dict[str, float]  # ticker -> shares


@dataclass(frozen=True)
class BacktestMetrics:
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
