from app.core.models import StockAnalysis


def print_stock_analysis(analysis: StockAnalysis) -> None:
    print(f"{'=' * 50}")
    print(f"{analysis.info.ticker} ({analysis.info.name}) - {analysis.info.category.value}")
    print(f"{'=' * 50}")

    if analysis.error:
        print(f"  ERROR: {analysis.error}")
        return

    metrics = analysis.metrics
    signals = analysis.signals

    # Current EV/EBIT
    print(f"  📊 Current Metrics:")
    if metrics.ev_ebit is not None:
        print(f"    EV/EBIT:           {metrics.ev_ebit:.2f}")

    # EV/EBIT 5Y Cycle
    print(f"  📈 EV/EBIT 5Y Cycle:")
    if metrics.ev_ebit_q1_5y is not None:
        days_info = f" ({metrics.ev_ebit_days_5y}/1250)" if metrics.ev_ebit_days_5y < 1250 else ""
        print(f"    Q1 (25%):          {metrics.ev_ebit_q1_5y:.2f}{days_info}")
        if metrics.ev_ebit is not None:
            signal_5y = "✅" if signals.ev_ebit_5y_cycle else "❌"
            print(f"    Signal (EV/EBIT < Q1): {signal_5y}")
    else:
        print(f"    (No data)")

    # EV/EBIT 1Y Cycle
    print(f"  📈 EV/EBIT 1Y Cycle:")
    if metrics.ev_ebit_q1_1y is not None:
        days_info = f" ({metrics.ev_ebit_days_1y}/250)" if metrics.ev_ebit_days_1y < 250 else ""
        print(f"    Q1 (25%):          {metrics.ev_ebit_q1_1y:.2f}{days_info}")
        if metrics.ev_ebit is not None:
            signal_1y = "✅" if signals.ev_ebit_1y_cycle else "❌"
            print(f"    Signal (EV/EBIT < Q1): {signal_1y}")
    else:
        print(f"    (No data)")

    # EBIT TTM (Positivity)
    print(f"  📈 EBIT TTM:")
    if metrics.ebit_ttm is not None:
        signal_positive = "✅" if signals.ebit_positive else "❌"
        print(f"    Value:             {metrics.ebit_ttm / 1e6:,.0f}M")
        print(f"    Signal (> 0):      {signal_positive}")
    else:
        print(f"    (Insufficient data)")

    # EBIT YoY Growth
    print(f"  📈 EBIT YoY Growth:")
    if metrics.ebit_growth is not None:
        signal_growth = "✅" if signals.ebit_growth_positive else "❌"
        print(f"    Value:             {metrics.ebit_growth:.2%}")
        print(f"    Signal (> 0):      {signal_growth}")
    else:
        print(f"    (Insufficient data)")

    # Summary
    print(f"  {'─' * 40}")
    print(f"  📋 Signal Summary: {signals.signal_count}/4 passed")
    if signals.all_signals_pass:
        print(f"  🎯 RECOMMENDATION: STRONG BUY")
    elif signals.signal_count >= 3:
        print(f"  🎯 RECOMMENDATION: BUY")
    elif signals.signal_count >= 2:
        print(f"  🎯 RECOMMENDATION: HOLD")
    else:
        print(f"  🎯 RECOMMENDATION: AVOID")


def print_summary_report(analyses: list[StockAnalysis]) -> None:
    print(f"\n\n{'=' * 70}")
    print(f"{'SUMMARY REPORT':^70}")
    print(f"{'=' * 70}")

    strong_buy = []
    buy = []
    hold = []
    avoid = []
    errors = []

    for analysis in analyses:
        if analysis.error:
            errors.append(analysis)
        elif analysis.signals.all_signals_pass:
            strong_buy.append(analysis)
        elif analysis.signals.signal_count >= 3:
            buy.append(analysis)
        elif analysis.signals.signal_count >= 2:
            hold.append(analysis)
        else:
            avoid.append(analysis)

    def print_category(label: str, analyses: list[StockAnalysis]) -> None:
        if len(analyses) == 0:
            return

        print(f"\n{label} ({len(analyses)}):")
        for analysis in analyses:
            metrics = analysis.metrics
            ev_ebit = f"{metrics.ev_ebit:6.1f}" if metrics.ev_ebit is not None else "   N/A"
            ebit_ttm = f"{metrics.ebit_ttm / 1e6:8,.0f}M" if metrics.ebit_ttm is not None else "      N/A"
            growth = f"{metrics.ebit_growth:+7.1%}" if metrics.ebit_growth is not None else "    N/A"
            print(f"  {analysis.info.ticker:6} | EV/EBIT:{ev_ebit} | EBIT TTM:{ebit_ttm} | Growth:{growth} | Signals: {analysis.signals.signal_count}/4")

    print_category("🎯 STRONG BUY", strong_buy)
    print_category("✅ BUY", buy)
    print_category("⏸️ HOLD", hold)
    print_category("❌ AVOID", avoid)

    if errors:
        print(f"\n⚠️ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  {error.info.ticker:6} | {error.error}")

    print(f"\n{'=' * 70}")
    print(f"Total: {len(analyses)} stocks analyzed")
    print(f"{'=' * 70}")
