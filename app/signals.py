from app.metrics import calc_pe_ntm_mean, calc_pe_ntm_std


# =============================================================================
# P/E (NTM)
# =============================================================================

def signal_pe_ntm_cycle(pe_ntm_current: float, pe_ntm_values: list[float]) -> bool:
    """
    Calculate P/E NTM Cycle Signal (Price-to-Earnings Next Twelve Months Cycle Signal).

    PE_NTM < μ - σ
    """
    mean = calc_pe_ntm_mean(pe_ntm_values)
    std = calc_pe_ntm_std(pe_ntm_values)
    return pe_ntm_current < mean - std


# =============================================================================
# NNI CAGR (1Y TTM)
# =============================================================================

def signal_nni_cagr(nni_cagr: float) -> bool:
    """
    Calculate NNI CAGR Signal (Normalized Net Income Compound Annual Growth Rate Signal).

    NNI_CAGR > 0
    """
    return nni_cagr > 0


# =============================================================================
# NNI Margin (LTM)
# =============================================================================

def signal_nni_margin(nni_margin: float) -> bool:
    """
    Calculate NNI Margin Signal (Normalized Net Income Margin Signal).

    NNI_Margin > 0
    """
    return nni_margin > 0
