# Q47-BatemanHorn-Constant

**Quantitative Heuristics for Prime Values of the Titan Polynomial: The Bateman–Horn Constant and Asymptotic Density**

**Author:** Ruqing Chen, GUT Geoservice Inc., Montreal, Canada

---

## Overview

This repository contains the paper, data, and verification scripts for computing the Bateman–Horn constant $C_Q$ for the Titan polynomial:

$$Q(n) = n^{47} - (n-1)^{47}$$

The key result: $C_Q \approx 8.68$, meaning that under the Bateman–Horn heuristic, prime values of $Q(n)$ occur with a frequency approximately **8.7 times** that predicted for a generic degree-46 polynomial.

## Main Results

| # | Result | Value |
|---|--------|-------|
| **§2** | Shielding Property: $\omega_Q(p) = 0$ for all $p < 283$ | 60 primes shielded |
| **§3.1** | Small primes product $P_{\mathrm{small}} = \prod_{p<283} p/(p-1)$ | ≈ 10.19 |
| **§3.2** | Large primes product (splitting primes $p \equiv 1 \pmod{47}$) | ≈ 0.852 |
| **§3** | Bateman–Horn constant $C_Q = P_{\mathrm{small}} \times P_{\mathrm{large}}$ | ≈ 8.68 |
| **§4** | Asymptotic prediction $\pi_Q(x) \sim (C_Q/46)\operatorname{Li}(x)$ | ≈ 0.1887 Li(x) |
| **Table 1** | Prediction vs observed at $x = 20{,}000$ | Error < 2% |

### Why is C_Q so large?

The Euler product for $C_Q$ has two competing effects:

- **60 shielded primes** ($p < 283$): each contributes $p/(p-1) > 1$ → combined boost ≈ 10.19
- **Splitting primes** ($p \equiv 1 \pmod{47}$, $p \geq 283$): each contributes $(1-46/p)/(1-1/p) < 1$ → combined suppression ≈ 0.852

The net effect is $10.19 \times 0.852 \approx 8.68$.

## Repository Structure

```
Q47-BatemanHorn-Constant/
├── README.md
├── LICENSE
├── .gitignore
├── paper/
│   ├── BatemanHorn_TitanPolynomial.tex     # LaTeX source (3 pages)
│   └── BatemanHorn_TitanPolynomial.pdf     # Compiled paper
├── data/
│   ├── local_factors.csv                   # Euler factors for 60 + 50 primes
│   ├── convergence.csv                     # C_Q convergence at truncation limits
│   └── prime_counts.csv                    # π_Q(x) observed vs predicted
└── scripts/
    ├── compute_bateman_horn.py             # Compute C_Q via Euler product
    ├── verify_shielding.py                 # ω(p)=0 for all p < 283
    └── verify_prediction.py               # Table 1: observed vs predicted
```

## Quick Start

### Compute the Bateman–Horn Constant
```bash
python scripts/compute_bateman_horn.py
```
Evaluates the Euler product up to $10^7$, showing convergence to $C_Q \approx 8.68$.

### Verify the Shielding Property
```bash
python scripts/verify_shielding.py
```
Confirms $\omega_Q(p) = 0$ for all 60 primes $p < 283$, and $\omega_Q(p) = 46$ for splitting primes.

### Verify Asymptotic Prediction (Table 1)
```bash
python scripts/verify_prediction.py
```
Counts $Q$-primes for $n \leq 20{,}000$ and compares with the Bateman–Horn prediction. ⚠️ This script takes a few minutes due to primality testing of large integers ($Q(n) \sim n^{46}$).

## Companion Papers

1. **Titan paper** (local root structure, bounded gap conjecture):
   R. Chen, *Prime Values of a Cyclotomic Norm Polynomial and a Conjectural Bounded Gap Phenomenon*, Preprint (2026),
   [Zenodo](https://zenodo.org/records/18521551)

2. **Null–Sparse Decomposition** (Bombieri–Vinogradov):
   R. Chen, *On the Distribution of the Cyclotomic Norm Form n⁴⁷−(n−1)⁴⁷ in Arithmetic Progressions*, Preprint (2026),
   [Zenodo](https://zenodo.org/records/18521778)

3. **Admissible Shifts** (fixed divisor analysis):
   R. Chen, *Algebraic Rigidity of the Titan Polynomial: Admissible Shifts and Absence of Fixed Divisors*, Preprint (2026),
   [GitHub](https://github.com/Ruqing1963/Q47-Admissible-Shifts)

4. **Landau–Siegel paper** (15.4M primes, spectral gap):
   R. Chen, *Experimental Constraints on Landau–Siegel Zeros: A 2-Billion Point Spectral Gap Analysis of Q₄₇*, Preprint (2026),
   [Zenodo](https://zenodo.org/records/18315796)

## Citation

```bibtex
@article{chen2026batemanhornQ47,
  title   = {Quantitative Heuristics for Prime Values of the Titan
             Polynomial: The {Bateman--Horn} Constant and Asymptotic
             Density},
  author  = {Chen, Ruqing},
  year    = {2026},
  note    = {Preprint, \url{https://github.com/Ruqing1963/Q47-BatemanHorn-Constant}}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
