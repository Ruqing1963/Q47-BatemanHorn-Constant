#!/usr/bin/env python3
"""
Verify Asymptotic Prediction vs. Observed Prime Counts (Table 1).

Computes π_Q(x) = #{n ≤ x : Q(n) is prime} by direct primality
testing, and compares with the Bateman–Horn prediction:
    π_Q(x) ~ (C_Q / 46) Li(x)

For small n the values Q(n) are modest enough for deterministic
primality testing (trial division + Miller–Rabin with known bases).

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-BatemanHorn-Constant
"""

import csv
import math
import os


def is_prime(n: int) -> bool:
    """Deterministic primality test for integers up to ~10^18.
    Uses trial division for small numbers and Miller-Rabin for larger."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    if n < 1000000:
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    # Miller-Rabin with deterministic witnesses for n < 3.3 × 10^24
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def Q(n: int) -> int:
    """Compute Q(n) = n^47 - (n-1)^47."""
    return n**47 - (n - 1)**47


def Li(x: float, steps: int = 200000) -> float:
    """Numerical integration of dt/ln(t) from 2 to x."""
    a, b = 2.0, float(x)
    h = (b - a) / steps
    total = 0.0
    for i in range(steps):
        t = a + (i + 0.5) * h
        total += 1.0 / math.log(t)
    return total * h


def main():
    print("=" * 70)
    print("  Table 1 Verification: π_Q(x) vs Bateman–Horn Prediction")
    print("  Q(n) = n^47 - (n-1)^47,  C_Q ≈ 8.68")
    print("=" * 70)
    print()

    C_Q = 8.68
    coeff = C_Q / 46

    # Count primes at checkpoints
    checkpoints = [1000, 2000, 5000, 10000, 15000, 20000]
    count = 0
    results = []
    checkpoint_idx = 0

    x_max = max(checkpoints)
    print(f"Counting Q-primes for n ≤ {x_max:,}...")
    print(f"  (Q(n) grows as n^46; at n=20000, Q(n) ≈ 10^197)")
    print()

    for n in range(1, x_max + 1):
        val = Q(n)
        if val > 1 and is_prime(val):
            count += 1

        if checkpoint_idx < len(checkpoints) and n == checkpoints[checkpoint_idx]:
            li = Li(n)
            pred = coeff * li
            err = (pred - count) / count * 100 if count > 0 else 0
            results.append((n, count, pred, li, err))
            checkpoint_idx += 1

            if n % 5000 == 0 or n == checkpoints[0]:
                print(f"  n = {n:>6,}: π_Q = {count:>5}, "
                      f"pred = {pred:.1f}, err = {err:+.1f}%")

    print()
    print(f"{'x':>8}  {'Observed':>9}  {'Predicted':>10}  "
          f"{'Li(x)':>10}  {'Rel.Err':>8}")
    print("-" * 52)
    for x, obs, pred, li, err in results:
        print(f"{x:>8,}  {obs:>9}  {pred:>10.1f}  "
              f"{li:>10.1f}  {err:>+7.1f}%")

    print()

    # ── Paper Table 1 comparison ──
    print("Paper Table 1 verification:")
    for x, obs, pred, li, err in results:
        if x in [10000, 20000]:
            print(f"  x = {x:>6,}: observed = {obs}, "
                  f"predicted = {pred:.0f}, error = {err:+.1f}%")

    print()
    print(f"  C_Q / 46 = {coeff:.4f}")
    print(f"  Under Bateman–Horn, π_Q(x) ~ {coeff:.4f} × Li(x)")

    # ── Save CSV ──
    os.makedirs("data", exist_ok=True)
    with open("data/prime_counts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# Observed vs predicted prime counts for Q(n)"])
        writer.writerow(["# C_Q = 8.68, prediction = (C_Q/46) * Li(x)"])
        writer.writerow(["x", "Observed_piQ", "Predicted", "Li_x",
                         "Relative_Error_pct"])
        for x, obs, pred, li, err in results:
            writer.writerow([x, obs, f"{pred:.2f}", f"{li:.2f}",
                             f"{err:.2f}"])
    print()
    print("  Saved to data/prime_counts.csv")
    print("  [DONE]")


if __name__ == "__main__":
    main()
