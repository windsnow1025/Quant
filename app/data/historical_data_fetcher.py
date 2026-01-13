from datetime import date

import yfinance as yf

from app.core.metrics import calc_eps_ntm_fiscal_year, calc_eps_ntm_quarterly
from app.core.models import StockDailyData, StockQuarterlyData, StockHistoricalData
from app.data.eodhd_client import EODHDClient


class HistoryDataFetcher(EODHDClient):
    def fetch(self, ticker: str) -> StockHistoricalData:
        fundamentals = self.get_fundamentals(ticker)

        general = fundamentals.get("General", {})
        fiscal_year_end_month = self.get_fiscal_year_end_month(
            general.get("FiscalYearEnd", "December")
        )

        earnings_history = fundamentals.get("Earnings", {}).get("History", {})
        earnings_trend = fundamentals.get("Earnings", {}).get("Trend", {})
        fy_estimates = self.build_fy_estimates_from_trend(earnings_trend)

        daily_history = self._fetch_historical_daily_data(
            ticker,
            fiscal_year_end_month,
            earnings_history,
            fy_estimates,
        )

        quarterly_history = self._extract_quarterly_history(fundamentals)

        return StockHistoricalData(
            daily=daily_history,
            quarterly=quarterly_history,
        )

    def _fetch_historical_daily_data(
            self,
            ticker: str,
            fiscal_year_end_month: int,
            earnings_history: dict,
            fy_estimates: dict[str, float],
    ) -> dict[date, StockDailyData]:
        """
        Fetch historical daily price data and calculate P/E NTM for each day.

        Uses quarterly interpolation (Method 1) as primary.
        Falls back to fiscal year interpolation (Method 2) using Trend 0y/+1y data.
        Uses yfinance for historical price data.
        """
        if not earnings_history:
            return {}

        try:
            # Build a map of quarter_end_date -> epsEstimate
            quarterly_estimates: dict[str, float] = {}
            for q_date, q_data in earnings_history.items():
                eps_est = q_data.get("epsEstimate")
                if eps_est is not None:
                    quarterly_estimates[q_date] = float(eps_est)

            if not quarterly_estimates:
                return {}

            # Get all available historical daily price data from yfinance
            stock = yf.Ticker(ticker)
            hist = stock.history(period="max")

            if hist.empty:
                return {}

            daily_data: dict[date, StockDailyData] = {}
            for date_idx in hist.index:
                price = float(hist.loc[date_idx, 'Close'])
                date_obj = date_idx.date()

                # Try quarterly interpolation (Method 1)
                q_estimates = self.get_quarter_estimates_for_date(date_obj, quarterly_estimates)
                if q_estimates:
                    weight = self.calculate_quarter_weight(date_obj)
                    eps_ntm = calc_eps_ntm_quarterly(weight, *q_estimates)
                else:
                    # Fallback to fiscal year interpolation (Method 2)
                    eps_fy1, eps_fy2 = self.get_fy_for_date(
                        date_obj, fiscal_year_end_month, fy_estimates
                    )
                    days_remaining = self.calculate_days_remaining_for_date(
                        date_obj, fiscal_year_end_month
                    )
                    eps_ntm = calc_eps_ntm_fiscal_year(days_remaining, eps_fy1, eps_fy2)

                daily_data[date_obj] = StockDailyData(
                    price=price,
                    eps_ntm=eps_ntm,
                )

            return daily_data
        except Exception:
            return {}

    def _extract_quarterly_history(self, fundamentals: dict) -> dict[date, StockQuarterlyData]:
        """Extract quarterly financial data from fundamentals.

        Uses Non-GAAP Net Income derived from epsActual (Earnings.History) * shares_outstanding,
        as specified in the paper (all metrics based on Non-GAAP figures).
        """
        financials = fundamentals.get("Financials", {})
        income_statement = financials.get("Income_Statement", {})
        balance_sheet = financials.get("Balance_Sheet", {})
        earnings_history = fundamentals.get("Earnings", {}).get("History", {})

        quarterly_income = income_statement.get("quarterly", {})
        quarterly_balance = balance_sheet.get("quarterly", {})

        quarterly_data: dict[date, StockQuarterlyData] = {}

        quarters = sorted(quarterly_income.keys(), reverse=True)

        for quarter in quarters:
            income_data = quarterly_income.get(quarter, {})
            balance_data = quarterly_balance.get(quarter, {})

            shares = self.parse_float(balance_data.get("commonStockSharesOutstanding"))
            revenue = self.parse_float(income_data.get("totalRevenue"))

            # Use Non-GAAP Net Income: epsActual * shares_outstanding
            eps_actual = self._get_eps_actual_for_quarter(quarter, earnings_history)
            if eps_actual is not None and shares is not None and shares > 0:
                net_income = eps_actual * shares
            else:
                net_income = None

            quarter_date = date.fromisoformat(quarter)
            quarterly_data[quarter_date] = StockQuarterlyData(
                net_income=net_income,
                revenue=revenue,
                shares_outstanding=shares,
            )

        return quarterly_data

    def _get_eps_actual_for_quarter(self, quarter: str, earnings_history: dict) -> float | None:
        """Get epsActual (Non-GAAP EPS) for a specific quarter from Earnings.History."""
        if not earnings_history:
            return None

        if quarter in earnings_history:
            eps_actual = earnings_history[quarter].get("epsActual")
            if eps_actual is not None:
                return self.parse_float(eps_actual)

        return None
