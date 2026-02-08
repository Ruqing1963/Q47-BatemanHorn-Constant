#!/usr/bin/env python3
"""
Compute the Bateman–Horn constant C_Q for Q(n) = n^47 - (n-1)^47.

The constant is the Euler product:
    C_Q = prod_p (1 - omega_Q(p)/p) / (1 - 1/p)

where omega_Q(p) = 0 for p < 283 or p ≢ 1 (mod 47),
      omega_Q(p) = 46 for p ≡ 1 (mod 47), p ≥ 283.

For p with omega_Q(p) = 0:  factor = p/(p-1) > 1   (boost)
For p with omega_Q(p) = 46: factor = (1-46/p)/(1-1/p) < 1 (suppression)

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-BatemanHorn-Constant
"""

import csv
import math
import os


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def omega_Q(p: int) -> int:
    """Local root count for Q(n) mod p."""
    if p < 283:
        return 0
    if (p - 1) % 47 == 0:
        return 46
    return 0


def local_factor(p: int) -> float:
    """Compute (1 - omega/p) / (1 - 1/p) for a single prime."""
    w = omega_Q(p)
    return (1 - w / p) / (1 - 1 / p)


def main():
    print("=" * 65)
    print("  Bateman–Horn Constant C_Q")
    print("  Q(n) = n^47 - (n-1)^47")
    print("=" * 65)
    print()

    # ── Part 1: Small primes product ──
    P_MAX = 10_000_000
    primes = sieve_primes(P_MAX)

    small_primes = [p for p in primes if p < 283]
    print(f"Small primes (p < 283): {len(small_primes)} primes")

    P_small = 1.0
    for p in small_primes:
        P_small *= p / (p - 1)
    print(f"  P_small = prod(p/(p-1)) = {P_small:.4f}")

    # Mertens' theorem check: e^gamma * ln(283) ≈ 10.05
    mertens_approx = math.exp(0.5772156649) * math.log(283)
    print(f"  Mertens approx e^gamma * ln(283) = {mertens_approx:.2f}")
    print()

    # ── Part 2: Convergence of total product ──
    checkpoints = [10**3, 10**4, 10**5, 10**6, 10**7]
    convergence = []

    print(f"{'Truncation X':>14}  {'C_Q(X)':>10}  {'# splitting':>12}")
    print("-" * 42)

    for X in checkpoints:
        C = 1.0
        n_splitting = 0
        for p in primes:
            if p > X:
                break
            f = local_factor(p)
            C *= f
            if omega_Q(p) == 46:
                n_splitting += 1
        print(f"{X:>14,}  {C:>10.4f}  {n_splitting:>12}")
        convergence.append((X, C, n_splitting))

    print()
    C_Q = convergence[-1][1]
    print(f"  Best estimate: C_Q ≈ {C_Q:.2f}")
    print(f"  C_Q / 46 ≈ {C_Q / 46:.4f}")
    print()

    # ── Part 3: Breakdown of large primes product ──
    P_large = 1.0
    splitting_factors = []
    for p in primes:
        if p < 283:
            continue
        if (p - 1) % 47 == 0:
            f = local_factor(p)
            P_large *= f
            splitting_factors.append((p, f))

    print(f"Large primes product (splitting primes only):")
    print(f"  # splitting primes ≤ {P_MAX:,}: {len(splitting_factors)}")
    print(f"  P_large = {P_large:.6f}")
    print(f"  P_small × P_large = {P_small * P_large:.4f}")
    print()

    # Show first 10 splitting primes
    print("First 10 splitting primes and their local factors:")
    print(f"  {'p':>6}  {'ω(p)':>5}  {'factor':>10}")
    for p, f in splitting_factors[:10]:
        print(f"  {p:>6}  {46:>5}  {f:>10.6f}")

    # ── Part 4: Inert primes contribute nothing beyond p/(p-1) ──
    # Actually for inert p ≥ 283, factor = p/(p-1), but these are
    # already captured by the full product. Let's verify the split.
    print()
    print("Verification: P_small × P_large(splitting) × P_large(inert)")
    P_inert = 1.0
    for p in primes:
        if p < 283:
            continue
        if (p - 1) % 47 != 0:
            P_inert *= p / (p - 1)
    # P_inert diverges (Mertens), so C_Q = P_small × P_splitting_suppression
    # where P_splitting_suppression absorbs the convergent part
    print(f"  Note: the product over ALL p of p/(p-1) diverges.")
    print(f"  C_Q converges because splitting primes contribute")
    print(f"  (1-46/p)/(1-1/p) = (p-46)/(p-1) instead of p/(p-1).")

    print()
    print(f"  [DONE] C_Q ≈ {C_Q:.2f}")

    # ── Save CSVs ──
    os.makedirs("data", exist_ok=True)

    with open("data/convergence.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# Convergence of C_Q with truncation limit X"])
        writer.writerow(["Truncation_X", "C_Q", "Num_splitting_primes"])
        for X, C, ns in convergence:
            writer.writerow([X, f"{C:.6f}", ns])
    print("  Saved to data/convergence.csv")

    with open("data/local_factors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# Local Euler factors for Q(n) = n^47 - (n-1)^47"])
        writer.writerow(["Prime_p", "omega_Q", "Factor", "Type"])
        # Small primes
        for p in small_primes:
            writer.writerow([p, 0, f"{p/(p-1):.8f}", "shielded"])
        # First 50 splitting primes
        for p, f in splitting_factors[:50]:
            writer.writerow([p, 46, f"{f:.8f}", "splitting"])
    print("  Saved to data/local_factors.csv")


if __name__ == "__main__":
    main()
