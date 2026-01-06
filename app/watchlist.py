from app.models import StockCategory, StockInfo

WATCHLIST: list[StockInfo] = [
    # Online
    StockInfo("GOOGL", "Alphabet Inc-Cl A", StockCategory.Online),
    StockInfo("MSFT", "Microsoft Corp", StockCategory.Online),
    StockInfo("META", "Meta Platforms Inc-Class A", StockCategory.Online),
    StockInfo("NET", "Cloudflare Inc - Class A", StockCategory.Online),
    StockInfo("ADBE", "Adobe Inc", StockCategory.Online),
    StockInfo("U", "Unity Software Inc", StockCategory.Online),
    StockInfo("RDDT", "Reddit Inc-Cl A", StockCategory.Online),
    StockInfo("SPOT", "Spotify Technology SA", StockCategory.Online),
    StockInfo("DUOL", "Duolingo", StockCategory.Online),
    # Offline
    StockInfo("DOCU", "Docusign Inc", StockCategory.Offline),
    StockInfo("SHOP", "Shopify Inc - Class A", StockCategory.Offline),
    StockInfo("CART", "Maplebear Inc", StockCategory.Offline),
    StockInfo("UBER", "Uber Technologies Inc", StockCategory.Offline),
    StockInfo("BKNG", "Booking Holdings Inc", StockCategory.Offline),
    StockInfo("EB", "Eventbrite Inc-Class A", StockCategory.Offline),
    StockInfo("LYV", "Live Nation Entertainment In", StockCategory.Offline),
    # Hardware
    StockInfo("ASML", "ASML Holdings NV-NY REG Shs", StockCategory.Hardware),
    StockInfo("TSM", "Taiwan Semiconductor-SP ADR", StockCategory.Hardware),
    StockInfo("NVDA", "NVIDIA Corp", StockCategory.Hardware),
    StockInfo("INTC", "Intel Corp", StockCategory.Hardware),
    StockInfo("AMD", "Advanced Micro Devices", StockCategory.Hardware),
    StockInfo("ARM", "ARM Holdings PLC-ADR", StockCategory.Hardware),
    StockInfo("QCOM", "Qualcomm Inc", StockCategory.Hardware),
    StockInfo("AVGO", "Broadcom Inc", StockCategory.Hardware),
    StockInfo("MU", "Micron Technology Inc", StockCategory.Hardware),
    StockInfo("WDC", "Western Digital Corp", StockCategory.Hardware),
    StockInfo("SONY", "Sony Group Corp - SP ADR", StockCategory.Hardware),
    StockInfo("LOGI", "Logitech International-REG", StockCategory.Hardware),
    # Finance
    StockInfo("NDAQ", "Nasdaq Inc", StockCategory.Finance),
    StockInfo("ICE", "Intercontinental Exchange In", StockCategory.Finance),
    StockInfo("SPGI", "S&P Global Inc", StockCategory.Finance),
    StockInfo("CBOE", "Cboe Global Markets Inc", StockCategory.Finance),
    StockInfo("CME", "CME Group Inc", StockCategory.Finance),
    StockInfo("V", "Visa Inc-Class A Shares", StockCategory.Finance),
    StockInfo("MA", "Mastercard Inc - A", StockCategory.Finance),
    StockInfo("AXP", "American Express Co", StockCategory.Finance),
    StockInfo("JPM", "JPMorgan Chase & Co", StockCategory.Finance),
    StockInfo("C", "Citigroup Inc", StockCategory.Finance),
    StockInfo("SOFI", "SoFi Technologies Inc", StockCategory.Finance),
    StockInfo("BAC", "Bank of America Corp", StockCategory.Finance),
    StockInfo("IBKR", "Interactive Brokers Gro-Cl A", StockCategory.Finance),
    StockInfo("SCHW", "Schwab (Charles) Corp", StockCategory.Finance),
    StockInfo("PYPL", "PayPal Holdings Inc", StockCategory.Finance),
    StockInfo("NWSA", "News Corp - Class A", StockCategory.Finance),
    # Industrial
    StockInfo("FDX", "FedEx Corporation", StockCategory.Industrial),
    StockInfo("UPS", "United Parcel Service-Cl B", StockCategory.Industrial),
    StockInfo("BA", "Boeing Co/The", StockCategory.Industrial),
    StockInfo("GM", "General Motors Co", StockCategory.Industrial),
    StockInfo("MMM", "3M Co", StockCategory.Industrial),
    # Consumer
    StockInfo("TMUS", "T-Mobile US Inc", StockCategory.Consumer),
    StockInfo("VZ", "Verizon Communications Inc", StockCategory.Consumer),
    StockInfo("LMND", "Lemonade Inc", StockCategory.Consumer),
    StockInfo("CVS", "CVS Health Corp", StockCategory.Consumer),
    StockInfo("ED", "Consolidated Edison Inc", StockCategory.Consumer),
    StockInfo("MCD", "McDonald's Corp", StockCategory.Consumer),
]


def get_stocks_by_category(category: StockCategory) -> list[StockInfo]:
    return [stock for stock in WATCHLIST if stock.category == category]


def get_all_tickers() -> list[str]:
    return [stock.ticker for stock in WATCHLIST]
