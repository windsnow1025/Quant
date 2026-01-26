import pickle
from pathlib import Path

from app.core.models import StockHistoricalData

historical_data_file_path = Path(__file__).parent.parent.parent.resolve() / "data" / "historical_data.pkl"


def save_historical_data(data: dict[str, StockHistoricalData]) -> None:
    historical_data_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(historical_data_file_path, "wb") as f:
        pickle.dump(data, f)


def load_historical_data() -> dict[str, StockHistoricalData]:
    if not historical_data_file_path.exists():
        return {}
    with open(historical_data_file_path, "rb") as f:
        return pickle.load(f)
