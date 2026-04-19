# =============================================================================
# Positivity
# =============================================================================

def signal_ebit_positive(ebit_ttm: float | None) -> bool:
    """
    Calculate EBIT TTM Positivity Signal.

    EBIT_TTM > 0
    """
    if ebit_ttm is None:
        return False
    return ebit_ttm > 0


# =============================================================================
# Growth
# =============================================================================

def signal_ebit_growth_positive(ebit_growth: float | None) -> bool:
    """
    Calculate EBIT YoY Growth Signal.

    EBIT_Growth > 0
    """
    if ebit_growth is None:
        return False
    return ebit_growth > 0


# =============================================================================
# EV/EBIT Cycle
# =============================================================================

def signal_ev_ebit_cycle(ev_ebit_current: float | None, ev_ebit_q1: float | None) -> bool:
    """
    Calculate EV/EBIT Cycle Signal.

    EV_EBIT < Q_1
    """
    if ev_ebit_current is None or ev_ebit_q1 is None or ev_ebit_current <= 0:
        return False
    return ev_ebit_current < ev_ebit_q1
