from pricer.mc_euro import mc_european, black_scholes_price
from pricer.mc_asian import mc_asian
from pricer.mc_greeks import mc_delta, mc_gamma

S0, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.20
option_type = "call"


# European demo
bs = black_scholes_price(S0, K, T, r, sigma, option_type)
price, se, ci = mc_european(S0, K, T, r, sigma, 200_000, option_type, seed=42, method= "antithetic")

d_eur = mc_delta(mc_european, S0, K, T, r, sigma, option_type=option_type, n_samples=200_000, seed=42)
g_eur = mc_gamma(mc_european, S0, K, T, r, sigma, option_type=option_type, n_samples=200_000, seed=42)

print(f"BS price: {bs:.2f}")
print(f"European MC: {price:.2f}")
print(f"SE: {se:.2f}")
print(f"CI95: ({ci[0]:.2f}, {ci[1]:.2f})")
print(f"European Delta MC: {d_eur:.2f}")
print(f"European Gamma MC: {g_eur:.2f}")


# Asian Demo 
price, se, ci = mc_asian(
    S0, K, T, r, sigma, n_steps=252, n_samples=40_000, method= "antithetic",
    option_type="call", averaging="arithmetic", include_S0=False, seed=42)

d_as = mc_delta(
    mc_asian, S0, K, T, r, sigma, bump_rel=1e-2, seed=42,
    n_steps=252, n_samples=40_000, option_type="call", averaging="arithmetic", include_S0=False)

g_as = mc_gamma(
    mc_asian, S0, K, T, r, sigma, bump_rel=1e-2, seed=42,
    n_steps=252, n_samples=40_000, option_type="call", averaging="arithmetic", include_S0=False)

print(f"Asian MC: {price:.2f}")
print(f"SE: {se:.2f}")
print(f"CI95: ({ci[0]:.2f}, {ci[1]:.2f})")
print(f"Asian Delta MC: {d_as:.2f}")
print(f"Asian Gamma MC: {g_as:.2f}")

