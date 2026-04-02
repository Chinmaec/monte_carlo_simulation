# MC Greeks (works for european and asian)

def _price_only(result):
    # result can be (price, se, ci95)
    return result[0] if isinstance(result, tuple) else result

def mc_delta(pricer, S0, K, T, r, sigma, bump_rel=1e-2, seed=42, **kwargs):
    h = bump_rel * S0
    p_up = _price_only(pricer(S0 + h, K, T, r, sigma, seed=seed, **kwargs))
    p_dn = _price_only(pricer(S0 - h, K, T, r, sigma, seed=seed, **kwargs))
    return (p_up - p_dn) / (2*h)

def mc_gamma(pricer, S0, K, T, r, sigma, bump_rel=1e-2, seed=42, **kwargs):
    h = bump_rel * S0
    p_up = _price_only(pricer(S0 + h, K, T, r, sigma, seed=seed, **kwargs))
    p_md = _price_only(pricer(S0,     K, T, r, sigma, seed=seed, **kwargs))
    p_dn = _price_only(pricer(S0 - h, K, T, r, sigma, seed=seed, **kwargs))
    return (p_up - 2*p_md + p_dn) / (h*h)
