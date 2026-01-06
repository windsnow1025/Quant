from dataclasses import dataclass
from datetime import date
from enum import Enum


# ============================================================================
# Stock Data Classes
# ============================================================================

class StockCategory(Enum):
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
    eps_ntm: float | None
    shares_outstanding: float | None


@dataclass(frozen=True)
class StockDailyData:
    price: float | None
    eps_ntm: float | None


@dataclass(frozen=True)
class StockQuarterlyData:
    net_income: float | None
    revenue: float | None
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
    pe_ntm: float | None = None
    pe_ntm_q1_5y: float | None = None
    pe_ntm_q1_1y: float | None = None
    pe_ntm_days_5y: int = 0
    pe_ntm_days_1y: int = 0
    nni_cagr: float | None = None
    nni_margin: float | None = None


@dataclass
class StockSignals:
    pe_ntm_10y_cycle: bool = False
    pe_ntm_1y_cycle: bool = False
    nni_cagr_positive: bool = False
    nni_margin_positive: bool = False

    @property
    def all_signals_pass(self) -> bool:
        return (
                self.pe_ntm_10y_cycle
                and self.pe_ntm_1y_cycle
                and self.nni_cagr_positive
                and self.nni_margin_positive
        )

    @property
    def signal_count(self) -> int:
        return sum([
            self.pe_ntm_10y_cycle,
            self.pe_ntm_1y_cycle,
            self.nni_cagr_positive,
            self.nni_margin_positive,
        ])


@dataclass
class StockAnalysis:
    info: StockInfo
    metrics: StockMetrics
    signals: StockSignals
    error: str | None = None
