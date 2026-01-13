from datetime import date

import yfinance as yf

from app.core.metrics import calc_eps_ntm_fiscal_year, calc_eps_ntm_quarterly
from app.core.models import StockLiveData
from app.data.eodhd_client import EODHDClient


class LiveDataFetcher(EODHDClient):
    def fetch(self, ticker: str) -> StockLiveData:
        fundamentals = self.get_fundamentals(ticker)

        general = fundamentals.get("General", {})
        fiscal_year_end_month = self.get_fiscal_year_end_month(
            general.get("FiscalYearEnd", "December")
        )

        earnings_history = fundamentals.get("Earnings", {}).get("History", {})
        earnings_trend = fundamentals.get("Earnings", {}).get("Trend", {})
        fy_estimates = self.build_fy_estimates_from_trend(earnings_trend)

        shares_stats = fundamentals.get("SharesStats", {})
        today = date.today()

        # Build quarterly estimates map from Earnings.History (past quarters)
        quarterly_estimates: dict[str, float] = {}
        for q_date, q_data in earnings_history.items():
            eps_est = q_data.get("epsEstimate")
            if eps_est is not None:
                quarterly_estimates[q_date] = float(eps_est)

        # Supplement with Earnings.Trend for current/future quarters
        for q_date, q_data in earnings_trend.items():
            if q_date not in quarterly_estimates:
                eps_avg = q_data.get("earningsEstimateAvg")
                if eps_avg is not None:
                    quarterly_estimates[q_date] = float(eps_avg)

        # Try quarterly interpolation (Method 1)
        q_estimates = self.get_quarter_estimates_for_date(today, quarterly_estimates)
        if q_estimates:
            weight = self.calculate_quarter_weight(today)
            eps_ntm = calc_eps_ntm_quarterly(weight, *q_estimates)
        else:
            # Fallback to fiscal year interpolation (Method 2)
            eps_est_fy1, eps_est_fy2 = self.get_fy_for_date(
                today, fiscal_year_end_month, fy_estimates
            )
            days_remaining = self.calculate_days_remaining_fy1(fiscal_year_end_month)
            eps_ntm = calc_eps_ntm_fiscal_year(days_remaining, eps_est_fy1, eps_est_fy2)

        # Get real-time price from yfinance
        price = self._get_current_price(ticker)
        shares_outstanding = shares_stats.get("SharesOutstanding")

        return StockLiveData(
            price=price,
            eps_ntm=eps_ntm,
            shares_outstanding=shares_outstanding,
        )

    def get_company_name(self, ticker: str) -> str:
        """Get company name for a ticker."""
        fundamentals = self.get_fundamentals(ticker)
        return fundamentals.get("General", {}).get("Name", ticker)

    def _get_current_price(self, ticker: str) -> float | None:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            return float(price) if price else None
        except Exception:
            return None
