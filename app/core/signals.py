# =============================================================================
# P/E (NTM)
# =============================================================================

def signal_pe_ntm_cycle(pe_ntm_current: float | None, pe_ntm_q1: float | None) -> bool:
    """
    Calculate P/E NTM (Price-to-Earnings Next Twelve Months) Cycle Signal.

    PE_NTM < Q1 (25th percentile)
    """
    if pe_ntm_current is None or pe_ntm_q1 is None or pe_ntm_current <= 0:
        return False
    return pe_ntm_current < pe_ntm_q1


# =============================================================================
# NNI CAGR (1Y TTM)
# =============================================================================

def signal_nni_cagr(nni_cagr: float | None) -> bool:
    """
    Calculate NNI CAGR (Normalized Net Income Compound Annual Growth Rate) Signal.

    NNI_CAGR > 0
    """
    if nni_cagr is None:
        return False
    return nni_cagr > 0


def signal_eps_cagr_ntm(eps_cagr_ntm: float | None) -> bool:
    """
    Calculate EPS CAGR NTM (EPS Compound Annual Growth Rate NTM) Signal.

    EPS_CAGR_NTM > 0
    """
    if eps_cagr_ntm is None:
        return False
    return eps_cagr_ntm > 0


# =============================================================================
# NNI Margin (LTM)
# =============================================================================

def signal_nni_margin(nni_margin: float | None) -> bool:
    """
    Calculate NNI Margin (Normalized Net Income Margin) Signal.

    NNI_Margin > 0
    """
    if nni_margin is None:
        return False
    return nni_margin > 0
