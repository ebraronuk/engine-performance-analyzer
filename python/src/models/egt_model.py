"""
Basit EGT (egzoz gaz sicakligi) tahmini.
Lineer bir iliski kullanarak yakit akisina dayali hizli hesaplama yapar.
"""

from typing import Union

Number = Union[int, float]


def estimate_egt(fuel_flow: Number, ambient_temp: Number, slope: Number = 2.5) -> float:
    """
    EGT'yi lineer bir modelle tahmin et.

    Parametreler:
        fuel_flow: Yakıt akış miktarı (kg/s veya tutarlı birim).
        ambient_temp: Ortam sıcaklığı (°C).
        slope: Yakıt akışının EGT üzerindeki katsayısı.

    Döndürür:
        Tahmini EGT değeri (°C).
    """
    # Basit model: EGT = ortam sicakligi + slope * yakit akisi
    return float(ambient_temp) + float(slope) * float(fuel_flow)
