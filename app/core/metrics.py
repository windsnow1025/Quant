# =============================================================================
# P/E (NTM)
# =============================================================================

def calc_eps_ntm_quarterly(
        weight: float,
        eps_est_q: float,
        eps_est_q1: float,
        eps_est_q2: float,
        eps_est_q3: float,
        eps_est_q4: float,
) -> float:
    """
    Calculate EPS NTM (Earnings Per Share Next Twelve Months) Quarterly.

    EPS_NTM_t = w_t * EPS_est_q + Σ(i=1 to 3) EPS_est_{q+i} + (1 - w_t) * EPS_est_{q+4}
    """
    return weight * eps_est_q + eps_est_q1 + eps_est_q2 + eps_est_q3 + (1 - weight) * eps_est_q4


def calc_eps_ntm_fiscal_year(
        days_remaining_fy1: int,
        eps_est_fy1: float | None,
        eps_est_fy2: float | None,
) -> float | None:
    """
    Calculate EPS NTM (Earnings Per Share Next Twelve Months) Fiscal Year.

    EPS_NTM_t = (d_t / 365) * EPS_est_FY1 + ((365 - d_t) / 365) * EPS_est_FY2
    """
    if eps_est_fy1 is None or eps_est_fy2 is None:
        return None
    return (days_remaining_fy1 / 365) * eps_est_fy1 + ((365 - days_remaining_fy1) / 365) * eps_est_fy2


def calc_pe_ntm(price: float | None, eps_ntm: float | None) -> float | None:
    """
    Calculate P/E NTM (Price-to-Earnings Next Twelve Months).

    PE_NTM_t = Price_t / EPS_NTM_t
    """
    if price is None or price <= 0 or eps_ntm is None or eps_ntm == 0:
        return None
    return price / eps_ntm


def calc_pe_ntm_percentile(pe_ntm_values: list[float], percentile: float) -> float | None:
    """
    Calculate P/E NTM Percentile (25th percentile = Q1).

    Q_p = PE_NTM[⌊i⌋] * (1 - f) + PE_NTM[⌈i⌉] * f
    where i = (p/100) * (n-1), f = i - ⌊i⌋
    """
    if len(pe_ntm_values) == 0:
        return None
    sorted_values = sorted(pe_ntm_values)
    n = len(sorted_values)
    index = (percentile / 100) * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return sorted_values[-1]
    fraction = index - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


# =============================================================================
# NNI CAGR (1Y TTM)
# =============================================================================

def calc_ni_ttm(quarterly_net_incomes: list[float | None]) -> float | None:
    """
    Calculate NI TTM (Net Income Trailing Twelve Months).

    NI_TTM_q = Σ(i=0 to 3) NI_{q-i}
    """
    if len(quarterly_net_incomes) != 4:
        return None
    if any(ni is None for ni in quarterly_net_incomes):
        return None
    return sum(quarterly_net_incomes)


def calc_nni_ttm(ni_ttm: float | None, shares_outstanding: float | None) -> float | None:
    """
    Calculate NNI TTM (Normalized Net Income Trailing Twelve Months).

    NNI_TTM_q = NI_TTM_q / Shares_Outstanding_q
    """
    if ni_ttm is None or shares_outstanding is None or shares_outstanding == 0:
        return None
    return ni_ttm / shares_outstanding


def calc_nni_cagr(nni_ttm_current: float | None, nni_ttm_prior_year: float | None) -> float | None:
    """
    Calculate NNI CAGR (Normalized Net Income Compound Annual Growth Rate).

    NNI_CAGR = NNI_TTM_q / NNI_TTM_{q-4} - 1
    """
    if nni_ttm_current is None or nni_ttm_prior_year is None or nni_ttm_prior_year == 0:
        return None
    return (nni_ttm_current / nni_ttm_prior_year) - 1


# =============================================================================
# NNI Margin (LTM)
# =============================================================================

def calc_revenue_ltm(quarterly_revenues: list[float | None]) -> float | None:
    """
    Calculate Revenue LTM (Revenue Last Twelve Months).

    Revenue_LTM = Σ(i=0 to 3) Revenue_{q-i}
    """
    if len(quarterly_revenues) != 4:
        return None
    if any(revenue is None for revenue in quarterly_revenues):
        return None
    return sum(quarterly_revenues)


def calc_nni_margin(ni_ttm: float | None, revenue_ltm: float | None) -> float | None:
    """
    Calculate NNI Margin (Normalized Net Income Margin).

    NNI_Margin = NNI_TTM / Revenue_Per_Share = NI_TTM / Revenue_LTM
    """
    if ni_ttm is None or revenue_ltm is None or revenue_ltm == 0:
        return None
    return ni_ttm / revenue_ltm
