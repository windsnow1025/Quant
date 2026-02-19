from app.core.models import StockCategory, StockInfo

WATCHLIST: list[StockInfo] = [
    # Online
    StockInfo("GOOGL", StockCategory.Online),
    StockInfo("MSFT", StockCategory.Online),
    StockInfo("META", StockCategory.Online),
    StockInfo("NET", StockCategory.Online),
    StockInfo("ADBE", StockCategory.Online),
    StockInfo("U", StockCategory.Online),
    StockInfo("RDDT", StockCategory.Online),
    StockInfo("SPOT", StockCategory.Online),
    StockInfo("DUOL", StockCategory.Online),
    # Offline
    StockInfo("AMZN", StockCategory.Offline),
    StockInfo("SHOP", StockCategory.Offline),
    StockInfo("CART", StockCategory.Offline),
    StockInfo("UBER", StockCategory.Offline),
    StockInfo("BKNG", StockCategory.Offline),
    StockInfo("EB", StockCategory.Offline),
    StockInfo("LYV", StockCategory.Offline),
    StockInfo("DOCU", StockCategory.Offline),
    StockInfo("WDAY", StockCategory.Offline),
    # Hardware
    StockInfo("ASML", StockCategory.Hardware),
    StockInfo("TSM", StockCategory.Hardware),
    StockInfo("NVDA", StockCategory.Hardware),
    StockInfo("INTC", StockCategory.Hardware),
    StockInfo("AMD", StockCategory.Hardware),
    StockInfo("ARM", StockCategory.Hardware),
    StockInfo("QCOM", StockCategory.Hardware),
    StockInfo("AVGO", StockCategory.Hardware),
    StockInfo("MU", StockCategory.Hardware),
    StockInfo("SNDK", StockCategory.Hardware),
    StockInfo("WDC", StockCategory.Hardware),
    StockInfo("SONY", StockCategory.Hardware),
    StockInfo("LOGI", StockCategory.Hardware),
    # Finance
    StockInfo("NDAQ", StockCategory.Finance),
    StockInfo("ICE", StockCategory.Finance),
    StockInfo("SPGI", StockCategory.Finance),
    StockInfo("CBOE", StockCategory.Finance),
    StockInfo("CME", StockCategory.Finance),
    StockInfo("V", StockCategory.Finance),
    StockInfo("MA", StockCategory.Finance),
    StockInfo("AXP", StockCategory.Finance),
    StockInfo("JPM", StockCategory.Finance),
    StockInfo("C", StockCategory.Finance),
    StockInfo("SOFI", StockCategory.Finance),
    StockInfo("BLK", StockCategory.Finance),
    StockInfo("BAC", StockCategory.Finance),
    StockInfo("IBKR", StockCategory.Finance),
    StockInfo("SCHW", StockCategory.Finance),
    StockInfo("PYPL", StockCategory.Finance),
    StockInfo("NWSA", StockCategory.Finance),
    # Industrial
    StockInfo("FDX", StockCategory.Industrial),
    StockInfo("UPS", StockCategory.Industrial),
    StockInfo("BA", StockCategory.Industrial),
    StockInfo("GM", StockCategory.Industrial),
    StockInfo("MMM", StockCategory.Industrial),
    # Consumer
    StockInfo("TMUS", StockCategory.Consumer),
    StockInfo("VZ", StockCategory.Consumer),
    StockInfo("COST", StockCategory.Consumer),
    StockInfo("LMND", StockCategory.Consumer),
    StockInfo("CVS", StockCategory.Consumer),
    StockInfo("ED", StockCategory.Consumer),
    StockInfo("MCD", StockCategory.Consumer),
]


def get_stocks_by_category(category: StockCategory) -> list[StockInfo]:
    return [stock for stock in WATCHLIST if stock.category == category]


def get_all_tickers() -> list[str]:
    return [stock.ticker for stock in WATCHLIST]
