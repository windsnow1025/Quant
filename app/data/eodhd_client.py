import os
from datetime import date
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class EODHDClient:
    """Base client for EODHD API with shared functionality."""

    BASE_URL = "https://eodhd.com/api"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found. Set it in .env or pass directly.")

    def _make_request(self, endpoint: str, params: dict | None = None) -> dict | list:
        """Make a request to EODHD API."""
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {"api_token": self.api_key, "fmt": "json"}
        if params:
            request_params.update(params)

        response = requests.get(url, params=request_params)
        response.raise_for_status()
        return response.json()

    def get_fundamentals(self, ticker: str, exchange: str = "US") -> dict[str, Any]:
        """Get fundamental data for a stock."""
        return self._make_request(f"fundamentals/{ticker}.{exchange}")

    # =========================================================================
    # Fiscal Year Helpers
    # =========================================================================

    def get_fiscal_year_end_month(self, fiscal_year_end: str) -> int:
        """Convert fiscal year end month name to month number."""
        months = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        return months.get(fiscal_year_end, 12)

    def get_last_day_of_month(self, year: int, month: int) -> int:
        """Get the last day of a given month."""
        import calendar
        return calendar.monthrange(year, month)[1]

    def build_fy_estimates_from_trend(self, earnings_trend: dict) -> dict[str, float]:
        """
        Build fiscal year estimates map from Earnings.Trend.

        Returns dict mapping fiscal year end date (YYYY-MM-DD) to earningsEstimateAvg.
        Only includes entries with period = '0y' or '+1y'.
        """
        fy_estimates: dict[str, float] = {}
        for fy_date, fy_data in earnings_trend.items():
            period = fy_data.get("period")
            if period in ["0y", "+1y"]:
                eps_avg = fy_data.get("earningsEstimateAvg")
                if eps_avg is not None:
                    fy_estimates[fy_date] = float(eps_avg)
        return fy_estimates

    def get_fy_for_date(
            self,
            target_date: date,
            fiscal_year_end_month: int,
            fy_estimates: dict[str, float],
    ) -> tuple[float | None, float | None]:
        """
        Get FY1 and FY2 estimates for a specific date from Trend data.

        If FY2 is not available, uses FY1 value for both.
        Returns (fy1_estimate, fy2_estimate) or (None, None) if FY1 not found.
        """
        if target_date.month > fiscal_year_end_month:
            fy1_year = target_date.year + 1
        else:
            fy1_year = target_date.year
        fy2_year = fy1_year + 1

        fy1_last_day = self.get_last_day_of_month(fy1_year, fiscal_year_end_month)
        fy2_last_day = self.get_last_day_of_month(fy2_year, fiscal_year_end_month)
        fy1_str = f"{fy1_year}-{fiscal_year_end_month:02d}-{fy1_last_day:02d}"
        fy2_str = f"{fy2_year}-{fiscal_year_end_month:02d}-{fy2_last_day:02d}"

        fy1_est = fy_estimates.get(fy1_str)
        fy2_est = fy_estimates.get(fy2_str)

        if fy1_est is not None and fy2_est is None:
            fy2_est = fy1_est

        return fy1_est, fy2_est

    # =========================================================================
    # Quarter Helpers
    # =========================================================================

    def get_quarter_end_for_date(self, target_date: date) -> date:
        """Get the quarter end date that contains the target date."""
        month = target_date.month
        if month <= 3:
            return date(target_date.year, 3, 31)
        elif month <= 6:
            return date(target_date.year, 6, 30)
        elif month <= 9:
            return date(target_date.year, 9, 30)
        else:
            return date(target_date.year, 12, 31)

    def get_next_quarter_end(self, quarter_end: date) -> date:
        """Get the next quarter end date."""
        if quarter_end.month == 3:
            return date(quarter_end.year, 6, 30)
        elif quarter_end.month == 6:
            return date(quarter_end.year, 9, 30)
        elif quarter_end.month == 9:
            return date(quarter_end.year, 12, 31)
        else:
            return date(quarter_end.year + 1, 3, 31)

    def get_quarter_estimates_for_date(
            self,
            target_date: date,
            quarterly_estimates: dict[str, float],
    ) -> tuple[float, ...] | None:
        """
        Get 5 consecutive quarter epsEstimates (Q, Q+1, Q+2, Q+3, Q+4) for a date.

        Returns tuple of 5 floats if all available, None otherwise.
        """
        q_end = self.get_quarter_end_for_date(target_date)
        estimates = []

        current_q = q_end
        for _ in range(5):
            q_str = current_q.strftime("%Y-%m-%d")
            if q_str not in quarterly_estimates:
                return None
            estimates.append(quarterly_estimates[q_str])
            current_q = self.get_next_quarter_end(current_q)

        return tuple(estimates)

    def calculate_quarter_weight(self, target_date: date) -> float:
        """
        Calculate w_t = fraction of current quarter remaining from target_date.

        Used in: EPS_NTM = w * EPS_q + EPS_{q+1} + EPS_{q+2} + EPS_{q+3} + (1-w) * EPS_{q+4}
        """
        q_end = self.get_quarter_end_for_date(target_date)

        if q_end.month == 3:
            q_start = date(q_end.year, 1, 1)
        elif q_end.month == 6:
            q_start = date(q_end.year, 4, 1)
        elif q_end.month == 9:
            q_start = date(q_end.year, 7, 1)
        else:
            q_start = date(q_end.year, 10, 1)

        total_days = (q_end - q_start).days + 1
        days_remaining = (q_end - target_date).days + 1
        return max(0.0, min(1.0, days_remaining / total_days))

    def calculate_days_remaining_fy1(self, fiscal_year_end_month: int) -> int:
        """
        Calculate days remaining from today to the end of current fiscal year.
        """
        today = date.today()
        current_year = today.year

        last_day = self.get_last_day_of_month(current_year, fiscal_year_end_month)
        fy_end = date(current_year, fiscal_year_end_month, last_day)

        if today > fy_end:
            fy_end = date(
                current_year + 1,
                fiscal_year_end_month,
                self.get_last_day_of_month(current_year + 1, fiscal_year_end_month)
            )

        days_remaining = (fy_end - today).days
        return max(0, min(365, days_remaining))

    def calculate_days_remaining_for_date(self, target_date: date, fiscal_year_end_month: int) -> int:
        """
        Calculate days remaining from a specific date to the end of its fiscal year.
        """
        current_year = target_date.year
        last_day = self.get_last_day_of_month(current_year, fiscal_year_end_month)
        fy_end = date(current_year, fiscal_year_end_month, last_day)

        if target_date > fy_end:
            last_day = self.get_last_day_of_month(current_year + 1, fiscal_year_end_month)
            fy_end = date(current_year + 1, fiscal_year_end_month, last_day)

        days_remaining = (fy_end - target_date).days
        return max(0, min(365, days_remaining))

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def parse_float(self, value: Any) -> float | None:
        """Safely parse a value to float, returns None if invalid."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
