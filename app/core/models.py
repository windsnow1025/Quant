from dataclasses import dataclass
from datetime import date
from enum import Enum


# ============================================================================
# Stock Data Classes
# ============================================================================

class StockCategory(Enum):
    SoftwareDevelop = "Software Develop"
    Online = "Online"
    Offline = "Offline"
    Hardware = "Hardware"
    Finance = "Finance"
    Industrial = "Industrial"
    Consumer = "Consumer"


@dataclass(frozen=True)
class StockInfo:
    ticker: str
    category: StockCategory
    name: str | None = None


@dataclass(frozen=True)
class StockLiveData:
    price: float | None
    ev_ebit: float | None


@dataclass(frozen=True)
class StockDailyData:
    price: float | None
    ev_ebit: float | None


@dataclass(frozen=True)
class StockQuarterlyData:
    filing_date: date | None
    ebit: float | None
    total_debt: float | None
    cash: float | None
    shares_outstanding: float | None


@dataclass
class StockHistoricalData:
    daily: dict[date, StockDailyData]
    quarterly: dict[date, StockQuarterlyData]


@dataclass
class Stock:
    info: StockInfo
    history: StockHistoricalData
    live: StockLiveData | None = None


# ============================================================================
# Analysis Result Data Classes
# ============================================================================

@dataclass
class StockMetrics:
    ev_ebit: float | None = None
    ev_ebit_q1_5y: float | None = None
    ev_ebit_q1_1y: float | None = None
    ev_ebit_days_5y: int = 0
    ev_ebit_days_1y: int = 0
    ebit_ttm: float | None = None
    ebit_growth: float | None = None


@dataclass
class StockSignals:
    ev_ebit_5y_cycle: bool = False
    ev_ebit_1y_cycle: bool = False
    ebit_positive: bool = False
    ebit_growth_positive: bool = False

    @property
    def all_signals_pass(self) -> bool:
        return (
                self.ev_ebit_5y_cycle
                and self.ev_ebit_1y_cycle
                and self.ebit_positive
                and self.ebit_growth_positive
        )

    @property
    def signal_count(self) -> int:
        return sum([
            self.ev_ebit_5y_cycle,
            self.ev_ebit_1y_cycle,
            self.ebit_positive,
            self.ebit_growth_positive,
        ])


@dataclass
class StockAnalysis:
    info: StockInfo
    metrics: StockMetrics
    signals: StockSignals
    error: str | None = None
