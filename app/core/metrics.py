import numpy as np


# =============================================================================
# EBIT TTM
# =============================================================================

def calc_ebit_ttm(quarterly_ebits: list[float | None]) -> float | None:
    """
    Calculate EBIT TTM (Earnings Before Interest and Taxes, Trailing Twelve Months).

    EBIT_TTM_q = Σ(i=0 to 3) EBIT_{q-i}
    """
    if len(quarterly_ebits) != 4:
        return None
    if any(ebit is None for ebit in quarterly_ebits):
        return None
    return sum(quarterly_ebits)


# =============================================================================
# Enterprise Value
# =============================================================================

def calc_ev(
        market_cap: float | None,
        total_debt: float | None,
        cash: float | None,
) -> float | None:
    """
    Calculate EV (Enterprise Value).

    EV_t = Market_Cap_t + Total_Debt_{q(t)} - Cash_and_Equivalents_{q(t)}
    """
    if market_cap is None or total_debt is None or cash is None:
        return None
    return market_cap + total_debt - cash


# =============================================================================
# EV/EBIT
# =============================================================================

def calc_ev_ebit(ev: float | None, ebit_ttm: float | None) -> float | None:
    """
    Calculate EV/EBIT.

    EV_EBIT_t = EV_t / EBIT_TTM_{q(t)}
    """
    if ev is None or ev <= 0 or ebit_ttm is None or ebit_ttm <= 0:
        return None
    return ev / ebit_ttm


def calc_ev_ebit_percentile(ev_ebit_values: list[float], percentile: float) -> float | None:
    """
    Calculate EV/EBIT Percentile.

    Q_p = p-th percentile of {EV_EBIT_t}_{t=1}^{n}
    """
    if len(ev_ebit_values) == 0:
        return None
    return float(np.percentile(ev_ebit_values, percentile))


# =============================================================================
# EBIT Growth
# =============================================================================

def calc_ebit_growth(
        ebit_ttm_current: float | None,
        ebit_ttm_prior: float | None,
) -> float | None:
    """
    Calculate EBIT YoY Growth.

    EBIT_Growth_q = EBIT_TTM_q / EBIT_TTM_{q-4} - 1
    """
    if ebit_ttm_current is None or ebit_ttm_prior is None or ebit_ttm_prior == 0:
        return None
    return (ebit_ttm_current / ebit_ttm_prior) - 1
