"""
Basit N1-N2 iliskisi.
Lineer bir katsayi ile N2 hizini tahmin eder.
"""

from typing import Union

Number = Union[int, float]


def estimate_n2(n1: Number, ratio: Number = 0.98) -> float:
    """
    N1 degerinden N2'yi tahmin et.

    Parametreler:
        n1: Fan devri (N1).
        ratio: N2/N1 oranini temsil eden katsayi.

    Döndürür:
        Tahmini N2 degeri.
    """
    # N2 = N1 * oran
    return float(n1) * float(ratio)
