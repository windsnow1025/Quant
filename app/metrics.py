import math


# =============================================================================
# P/E (NTM)
# =============================================================================

def calc_pe_ntm(price: float, eps_ntm: float) -> float:
    """
    Calculate P/E NTM (Price-to-Earnings Next Twelve Months).

    PE_NTM_t = Price_t / EPS_NTM_t
    """
    return price / eps_ntm


def calc_pe_ntm_mean(pe_ntm_values: list[float]) -> float:
    """
    Calculate P/E NTM Mean (Price-to-Earnings Next Twelve Months Mean).

    μ = (1/n) * Σ PE_NTM_t
    """
    n = len(pe_ntm_values)
    return sum(pe_ntm_values) / n


def calc_pe_ntm_std(pe_ntm_values: list[float]) -> float:
    """
    Calculate P/E NTM Std (Price-to-Earnings Next Twelve Months Standard Deviation).

    σ = sqrt((1/(n-1)) * Σ(PE_NTM_t - μ)^2)
    """
    n = len(pe_ntm_values)
    mean = calc_pe_ntm_mean(pe_ntm_values)
    variance = sum((x - mean) ** 2 for x in pe_ntm_values) / (n - 1)
    return math.sqrt(variance)


# =============================================================================
# NNI CAGR (1Y TTM)
# =============================================================================

def calc_ni_ttm(quarterly_net_incomes: list[float]) -> float:
    """
    Calculate NI TTM (Net Income Trailing Twelve Months).

    NI_TTM_q = Σ(i=0 to 3) NI_{q-i}
    """
    if len(quarterly_net_incomes) != 4:
        raise ValueError("Exactly 4 quarterly net income values are required")
    return sum(quarterly_net_incomes)


def calc_nni_ttm(ni_ttm: float, shares_outstanding: float) -> float:
    """
    Calculate NNI TTM (Normalized Net Income Trailing Twelve Months).

    NNI_TTM_q = NI_TTM_q / Shares_Outstanding_q
    """
    return ni_ttm / shares_outstanding


def calc_nni_cagr(nni_ttm_current: float, nni_ttm_prior_year: float) -> float:
    """
    Calculate NNI CAGR (Normalized Net Income Compound Annual Growth Rate).

    NNI_CAGR = NNI_TTM_q / NNI_TTM_{q-4} - 1
    """
    return (nni_ttm_current / nni_ttm_prior_year) - 1


# =============================================================================
# NNI Margin (LTM)
# =============================================================================

def calc_revenue_ltm(quarterly_revenues: list[float]) -> float:
    """
    Calculate Revenue LTM (Revenue Last Twelve Months).

    Revenue_LTM = Σ(i=0 to 3) Revenue_{q-i}
    """
    if len(quarterly_revenues) != 4:
        raise ValueError("Exactly 4 quarterly revenue values are required")
    return sum(quarterly_revenues)


def calc_nni_margin(ni_ttm: float, revenue_ltm: float) -> float:
    """
    Calculate NNI Margin (Normalized Net Income Margin).

    NNI_Margin = NNI_TTM / Revenue_Per_Share = NI_TTM / Revenue_LTM
    """
    return ni_ttm / revenue_ltm
