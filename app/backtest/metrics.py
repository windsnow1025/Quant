import math


# =============================================================================
# Total Return
# =============================================================================

def calc_total_return(equity_curve: list[float]) -> float:
    """
    Calculate Total Return.

    Total_Return = (Equity_end - Equity_start) / Equity_start
    """
    if len(equity_curve) == 0 or equity_curve[0] == 0:
        return 0.0
    return (equity_curve[-1] - equity_curve[0]) / equity_curve[0]


# =============================================================================
# Annual Return
# =============================================================================

def calc_annual_return(total_return: float, trading_days: int) -> float:
    """
    Calculate Annual Return (annualized return).

    Annual_Return = (1 + Total_Return) ^ (1 / years) - 1
    where years = trading_days / 252
    """
    if trading_days == 0:
        return 0.0
    years = trading_days / 252
    return (1 + total_return) ** (1 / years) - 1


# =============================================================================
# Max Drawdown
# =============================================================================

def calc_max_drawdown(equity_curve: list[float]) -> float:
    """
    Calculate Max Drawdown (maximum peak-to-trough decline).

    Max_Drawdown = max((Peak_t - Equity_t) / Peak_t)
    """
    if len(equity_curve) == 0:
        return 0.0
    peak = equity_curve[0]
    max_drawdown = 0.0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak
        max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


# =============================================================================
# Sharpe Ratio
# =============================================================================

def calc_sharpe_ratio(equity_curve: list[float]) -> float:
    """
    Calculate Sharpe Ratio (annualized).

    Sharpe_Ratio = (mean(daily_returns) / std(daily_returns)) * sqrt(252)
    """
    if len(equity_curve) < 2:
        return 0.0

    daily_returns = [
        (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
        for i in range(1, len(equity_curve))
        if equity_curve[i - 1] > 0
    ]

    mean_return = sum(daily_returns) / len(daily_returns)
    variance = sum((r - mean_return) ** 2 for r in daily_returns) / len(daily_returns)
    std_return = math.sqrt(variance)

    if std_return == 0:
        return 0.0

    return (mean_return / std_return) * math.sqrt(252)
