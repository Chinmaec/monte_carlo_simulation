# Monte Carlo Option Pricer

## Overview
Monte Carlo pricing engine for derivative valuation under risk-neutral Geometric Brownian Motioon, integrated variance reduction and Greeks estimation.  

Implements European and Asian options, reports statistical uncertainty, and validates European outputs against Black–Scholes.

## Methodology
- Simulate under $\mathbb{Q}$:

$$
S_{t+\Delta t}=S_t\exp\left((r-\frac{1}{2}\sigma^2)\Delta t+\sigma\sqrt{\Delta t}\,Z\right),\quad Z\sim\mathcal{N}(0,1)
$$
- Price estimator:

$$
\hat V_0=e^{-rT}\frac{1}{N}\sum_{i=1}^N \mathrm{Payoff}\!\left(S^{(i)}\right)
$$
- Variance reduction via antithetic variates (\(Z,-Z\)) on shared path construction.
- Inference metrics: Monte Carlo standard error and two-sided 95% confidence interval.
- Estimates Greeks (Delta, Gamma) via central finite differences with common random numbers (CRN).
- Benchmarks European options against closed-form Black–Scholes for validation.

## Features
- European and Asian option pricing (arithmetic & geometric averaging).
- Variance-reduced Monte Carlo estimators.
- Fully vectorized simulation/payoff pipeline for high-throughput path evaluation.
- Integrated diagnostics: price, SE, CI95, Delta, Gamma.
- Deterministic reproducibility via controlled seeding and CRN-consistent Greek estimation.

## Results (sample run, seed=42)
| Contract | Price | SE | CI95 | Delta | Gamma |
|---|---:|---:|---|---:|---:|
| European Call (MC, antithetic) | 10.47 | 0.02 | (10.44, 10.50) | 0.64 | 0.02 |
| European Call (Black-Scholes) | 10.45 | - | - | - | - |
| Asian Call (MC, arithmetic, antithetic) | 5.82 | 0.03 | (5.76, 5.87) | 0.59 | 0.03 |

## Usage
cd monte_carlo_simulation
pip install -r requirements.txt
python test.py


