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

    # Current P/E NTM
    print(f"  📊 Current Metrics:")
    if metrics.pe_ntm is not None:
        print(f"    P/E NTM:           {metrics.pe_ntm:.2f}")

    # P/E NTM 5Y Cycle
    print(f"  📈 P/E NTM 5Y Cycle:")
    if metrics.pe_ntm_q1_5y is not None:
        days_info = f" ({metrics.pe_ntm_days_5y}/1250)" if metrics.pe_ntm_days_5y < 1250 else ""
        print(f"    Q1 (25%):          {metrics.pe_ntm_q1_5y:.2f}{days_info}")
        if metrics.pe_ntm is not None:
            signal_5y = "✅" if signals.pe_ntm_10y_cycle else "❌"
            print(f"    Signal (P/E < Q1): {signal_5y}")
    else:
        print(f"    (No data)")

    # P/E NTM 1Y Cycle
    print(f"  📈 P/E NTM 1Y Cycle:")
    if metrics.pe_ntm_q1_1y is not None:
        days_info = f" ({metrics.pe_ntm_days_1y}/250)" if metrics.pe_ntm_days_1y < 250 else ""
        print(f"    Q1 (25%):          {metrics.pe_ntm_q1_1y:.2f}{days_info}")
        if metrics.pe_ntm is not None:
            signal_1y = "✅" if signals.pe_ntm_1y_cycle else "❌"
            print(f"    Signal (P/E < Q1): {signal_1y}")
    else:
        print(f"    (No data)")

    # NNI CAGR
    print(f"  📈 NNI CAGR (1Y TTM):")
    if metrics.nni_cagr is not None:
        signal_cagr = "✅" if signals.nni_cagr_positive else "❌"
        print(f"    Value:             {metrics.nni_cagr:.2%}")
        print(f"    Signal (> 0):      {signal_cagr}")
    else:
        print(f"    (Insufficient data)")

    # NNI Margin
    print(f"  📈 NNI Margin (LTM):")
    if metrics.nni_margin is not None:
        signal_margin = "✅" if signals.nni_margin_positive else "❌"
        print(f"    Value:             {metrics.nni_margin:.2%}")
        print(f"    Signal (> 0):      {signal_margin}")
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
            m = analysis.metrics
            pe = f"{m.pe_ntm:6.1f}" if m.pe_ntm else "   N/A"
            cagr = f"{m.nni_cagr:+7.1%}" if m.nni_cagr else "    N/A"
            margin = f"{m.nni_margin:6.1%}" if m.nni_margin else "   N/A"
            print(
                f"  {analysis.info.ticker:6} | P/E:{pe} | CAGR:{cagr} | Margin:{margin} | Signals: {analysis.signals.signal_count}/4")

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
