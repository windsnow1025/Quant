from dataclasses import dataclass
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
    name: str
    category: StockCategory


@dataclass(frozen=True)
class StockCurrentData:
    """Current/real-time stock data."""
    price: float
    eps_ntm: float
    shares_outstanding: float


@dataclass(frozen=True)
class StockDailyData:
    """Historical daily stock data (for P/E NTM history)."""
    date: str
    price: float
    eps_ntm: float


@dataclass(frozen=True)
class StockQuarterlyData:
    """Quarterly financial data."""
    quarter: str
    net_income: float
    revenue: float
    shares_outstanding: float


@dataclass
class Stock:
    """Complete stock data structure."""
    info: StockInfo
    current: StockCurrentData
    daily_history: list[StockDailyData]
    quarterly_history: list[StockQuarterlyData]


# ============================================================================
# Analysis Result Data Classes
# ============================================================================

@dataclass
class StockMetrics:
    """Calculated metrics for a stock."""
    pe_ntm: float | None = None
    pe_ntm_mean_10y: float | None = None
    pe_ntm_std_10y: float | None = None
    pe_ntm_mean_1y: float | None = None
    pe_ntm_std_1y: float | None = None
    nni_cagr: float | None = None
    nni_margin: float | None = None


@dataclass
class StockSignals:
    """Buy signals for a stock."""
    pe_ntm_10y_cycle: bool = False
    pe_ntm_1y_cycle: bool = False
    nni_cagr_positive: bool = False
    nni_margin_positive: bool = False

    @property
    def all_signals_pass(self) -> bool:
        """Returns True if all signals are positive."""
        return (
            self.pe_ntm_10y_cycle
            and self.pe_ntm_1y_cycle
            and self.nni_cagr_positive
            and self.nni_margin_positive
        )

    @property
    def signal_count(self) -> int:
        """Returns count of positive signals."""
        return sum([
            self.pe_ntm_10y_cycle,
            self.pe_ntm_1y_cycle,
            self.nni_cagr_positive,
            self.nni_margin_positive,
        ])


@dataclass
class StockAnalysis:
    """Complete analysis result for a stock."""
    info: StockInfo
    metrics: StockMetrics
    signals: StockSignals
    error: str | None = None
