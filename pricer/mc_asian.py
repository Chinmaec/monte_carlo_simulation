# Asian Monte Carlo (plain and antithetic methods)

import numpy as np
from pricer.core import payoff_vanilla
from pricer.core import mc_stats

def _simulate_asian_terminal_matrix(S0, T, r, sigma, n_steps, Z):
    dt = T / n_steps
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * np.sqrt(dt)
    log_paths = np.cumsum(drift + vol * Z, axis=1)
    return S0 * np.exp(log_paths)


def _asian_average(S, averaging):
    if averaging == "arithmetic":
        return S.mean(axis=1)
    if averaging == "geometric":
        return np.exp(np.log(S).mean(axis=1))
    raise ValueError("averaging must be 'arithmetic' or 'geometric'")


def mc_asian(
    S0, K, T, r, sigma,
    n_steps=252,
    n_samples=20_000,
    option_type="call",
    averaging="arithmetic",
    include_S0=False,
    method="plain",   # "plain" or "antithetic"
    seed=42,
):
    rng = np.random.default_rng(seed)

    if method == "plain":
        Z = rng.standard_normal((n_samples, n_steps))
        S = _simulate_asian_terminal_matrix(S0, T, r, sigma, n_steps, Z)

        if include_S0:
            S = np.concatenate([np.full((n_samples, 1), S0), S], axis=1)

        A = _asian_average(S, averaging)
        payoff = payoff_vanilla(A, K, option_type)
        disc = np.exp(-r * T) * payoff
        return mc_stats(disc)

    if method == "antithetic":
        if n_samples % 2 != 0:
            raise ValueError("For method='antithetic', n_samples must be even.")
        n_pairs = n_samples // 2

        Z = rng.standard_normal((n_pairs, n_steps))
        S_plus = _simulate_asian_terminal_matrix(S0, T, r, sigma, n_steps, Z)
        S_minus = _simulate_asian_terminal_matrix(S0, T, r, sigma, n_steps, -Z)

        if include_S0:
            S_plus = np.concatenate([np.full((n_pairs, 1), S0), S_plus], axis=1)
            S_minus = np.concatenate([np.full((n_pairs, 1), S0), S_minus], axis=1)

        A_plus = _asian_average(S_plus, averaging)
        A_minus = _asian_average(S_minus, averaging)

        pay_plus = payoff_vanilla(A_plus, K, option_type)
        pay_minus = payoff_vanilla(A_minus, K, option_type)
        disc_pair = np.exp(-r * T) * 0.5 * (pay_plus + pay_minus)
        return mc_stats(disc_pair)

    raise ValueError("method must be 'plain' or 'antithetic'")
