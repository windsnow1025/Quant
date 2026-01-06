from app.core.analyzer import analyze_stock
from app.core.models import StockAnalysis, StockMetrics, StockSignals
from app.data.historical_data_storage import load_historical_data
from app.data.watchlist import WATCHLIST
from app.live.live import fetch_stock
from app.live.report import print_stock_analysis, print_summary_report


def main():
    historical_data = load_historical_data()
    analyses: list[StockAnalysis] = []

    for i, stock_info in enumerate(WATCHLIST, 1):
        print(f"\n[{i}/{len(WATCHLIST)}]")
        try:
            stock = fetch_stock(stock_info, historical_data)
            analysis = analyze_stock(stock)
            analyses.append(analysis)
            print_stock_analysis(analysis)
        except Exception as e:
            print(f"  ERROR: {e}")
            analyses.append(StockAnalysis(
                info=stock_info,
                metrics=StockMetrics(),
                signals=StockSignals(),
                error=str(e),
            ))

    print_summary_report(analyses)


if __name__ == "__main__":
    main()
