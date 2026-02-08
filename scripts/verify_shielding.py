#!/usr/bin/env python3
"""
Verify the Shielding Property of Q(n) = n^47 - (n-1)^47.

For every prime p < 283, checks that Q(n) ≡ 0 (mod p) has NO solutions,
confirming omega_Q(p) = 0.  This means no value Q(n) is ever divisible
by any prime less than 283.

Also verifies the three rigid primes (p ∈ {2,3,47}) where Q(n) ≡ 1,
and confirms that p = 283 is the smallest splitting prime where
omega_Q(283) = 46.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-BatemanHorn-Constant
"""


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def Q_mod(n: int, p: int) -> int:
    """Compute Q(n) = n^47 - (n-1)^47 mod p."""
    return (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p


def omega(p: int) -> int:
    """Count solutions of Q(n) ≡ 0 (mod p) by exhaustive search."""
    return sum(1 for n in range(p) if Q_mod(n, p) == 0)


def main():
    print("=" * 60)
    print("  Shielding Property Verification")
    print("  Q(n) = n^47 - (n-1)^47")
    print("=" * 60)
    print()

    primes = sieve_primes(6300)

    # ── Part 1: Verify ω(p) = 0 for all p < 283 ──
    small_primes = [p for p in primes if p < 283]
    print(f"Primes p < 283: {len(small_primes)} primes")
    print()

    all_shielded = True
    rigid = []
    for p in small_primes:
        w = omega(p)
        if w != 0:
            print(f"  FAIL: ω({p}) = {w} (expected 0)")
            all_shielded = False
        # Check if Q(n) ≡ 1 for all n (rigid prime)
        vals = set(Q_mod(n, p) for n in range(p))
        if vals == {1}:
            rigid.append(p)

    print(f"  All ω(p) = 0 for p < 283: "
          f"{'PASS' if all_shielded else 'FAIL'}")
    print(f"  Rigid primes (Q(n) ≡ 1 for all n): {rigid}")
    print()

    # ── Part 2: Verify why each prime is shielded ──
    print("Classification of small primes by mechanism:")
    fermat_primes = [p for p in small_primes if 46 % (p - 1) == 0]
    inert_primes = [p for p in small_primes
                    if p not in fermat_primes and (p - 1) % 47 != 0]

    print(f"  Fermat rigidity ((p-1)|46): {fermat_primes}")
    print(f"  Inert (p ≢ 1 mod 47):      {len(inert_primes)} primes "
          f"(all others < 283)")
    print()

    # ── Part 3: First splitting prime ──
    print("First splitting prime (p ≡ 1 mod 47):")
    first_splitting = None
    for p in primes:
        if (p - 1) % 47 == 0:
            w = omega(p)
            first_splitting = p
            print(f"  p = {p}: ω(p) = {w}")
            if w == 46:
                print(f"  CONFIRMED: smallest splitting prime is {p}")
            break

    print()

    # ── Part 4: Verify all splitting primes up to 6299 ──
    print("All splitting primes p ≤ 6299:")
    print(f"  {'p':>6}  {'ω(p)':>5}  {'p ≡ 1 (47)?':>12}")
    print("  " + "-" * 28)

    splitting_ok = True
    for p in primes:
        if (p - 1) % 47 == 0:
            w = omega(p)
            cong = (p - 1) % 47 == 0
            ok = w == 46
            if not ok:
                splitting_ok = False
            print(f"  {p:>6}  {w:>5}  {'yes':>12}  "
                  f"{'OK' if ok else 'FAIL'}")

    print()
    print(f"  All splitting primes have ω(p) = 46: "
          f"{'PASS' if splitting_ok else 'FAIL'}")

    # ── Summary ──
    print()
    print("=" * 60)
    status = "ALL PASS" if (all_shielded and splitting_ok) else "FAILED"
    print(f"  [{status}] Shielding property verified:")
    print(f"    • ω(p) = 0  for all {len(small_primes)} primes p < 283")
    print(f"    • ω(p) = 46 for all splitting primes p ≡ 1 (mod 47)")
    print(f"    • Smallest splitting prime: {first_splitting}")
    print("=" * 60)


if __name__ == "__main__":
    main()
