import os
from datetime import date
from typing import Any

import requests
from dotenv import load_dotenv

from app.core.models import StockQuarterlyData

load_dotenv()


class EODHDClient:
    BASE_URL = "https://eodhd.com/api"

    def __init__(self):
        api_key = os.getenv("API_KEY")
        assert api_key
        self.api_key = api_key

    def _fetch_json(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {"api_token": self.api_key, "fmt": "json"}
        if params:
            request_params.update(params)

        response = requests.get(url, params=request_params)
        response.raise_for_status()
        return response.json()

    def fetch_fundamentals(self, ticker: str, exchange: str = "US") -> dict[str, Any]:
        result = self._fetch_json(f"fundamentals/{ticker}.{exchange}")
        assert isinstance(result, dict)
        return result

    def fetch_company_name(self, ticker: str) -> str:
        fundamentals = self.fetch_fundamentals(ticker)
        return fundamentals.get("General", {}).get("Name", ticker)

    # =========================================================================
    # Domain Mapping
    # =========================================================================

    def get_total_debt(self, balance_sheet_quarter: dict[str, Any]) -> float | None:
        total = self.parse_float(balance_sheet_quarter.get("shortLongTermDebtTotal"))
        if total is not None:
            return total

        long_term = self.parse_float(balance_sheet_quarter.get("longTermDebt"))
        short_term = self.parse_float(balance_sheet_quarter.get("shortTermDebt"))
        if long_term is None and short_term is None:
            return None
        return (long_term or 0.0) + (short_term or 0.0)

    def extract_quarterly_history(self, fundamentals: dict[str, Any]) -> dict[date, StockQuarterlyData]:
        financials = fundamentals.get("Financials", {})
        income_statement = financials.get("Income_Statement", {}).get("quarterly", {})
        balance_sheet = financials.get("Balance_Sheet", {}).get("quarterly", {})

        quarterly_data: dict[date, StockQuarterlyData] = {}
        for quarter, bs_data in balance_sheet.items():
            income_data = income_statement.get(quarter, {})

            filing_str = bs_data.get("filing_date")
            filing_date = date.fromisoformat(filing_str) if filing_str else None

            quarter_date = date.fromisoformat(quarter)
            quarterly_data[quarter_date] = StockQuarterlyData(
                filing_date=filing_date,
                ebit=self.parse_float(income_data.get("operatingIncome")),
                total_debt=self.get_total_debt(bs_data),
                cash=self.parse_float(bs_data.get("cashAndShortTermInvestments")),
                shares_outstanding=self.parse_float(bs_data.get("commonStockSharesOutstanding")),
            )

        return quarterly_data

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def parse_float(self, value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
