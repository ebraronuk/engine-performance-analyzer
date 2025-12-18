"""
EGT marji hesaplama ve yorumlama.
Olculen deger ile limit arasindaki farki dondurur ve basit durum etiketi verir.
"""

from typing import Union

Number = Union[int, float]


def compute_egt_margin(egt_measured: Number, egt_limit: Number) -> float:
    """
    EGT marjini hesapla.

    Parametreler:
        egt_measured: Olculen EGT (C).
        egt_limit: Izin verilen EGT limiti (C).

    Doner:
        egt_limit - egt_measured degeri.
    """
    # Pozitif deger limitin altinda oldugunu gosterir
    return float(egt_limit) - float(egt_measured)


def interpret_margin_trend(margin: Number) -> str:
    """
    EGT marji icin basit durum yorumu.

    Parametreler:
        margin: Hesaplanmis EGT marji (C).

    Doner:
        "critical", "caution" veya "normal".
    """
    m = float(margin)
    # Ornek esikler: <20 critical, <50 caution, digerleri normal
    if m < 20.0:
        return "critical"
    if m < 50.0:
        return "caution"
    return "normal"


def generate_health_summary(margin: Number, slope: Number) -> str:
    """
    Marj ve egim bilgilerini birlestirip kisa bir ozet metni dondurur.

    Parametreler:
        margin: Hesaplanmis EGT marji (C).
        slope: Trend egimi (C/adim).

    Doner:
        Durum ve egim iceren kisa metin.
    """
    status = interpret_margin_trend(margin)
    return f"Status: {status}, Margin: {float(margin):.1f} C, Slope: {float(slope):.3f} C/step"


def classify_egt_level(egt_measured: Number) -> str:
    """
    Olculen EGT degerine gore basit seviye sinifi dondurur.

    Parametreler:
        egt_measured: Olculen EGT (C).

    Doner:
        "low", "medium" veya "high".
    """
    value = float(egt_measured)
    # Ornek esikler: <600 low, <800 medium, digerleri high
    if value < 600.0:
        return "low"
    if value < 800.0:
        return "medium"
    return "high"


def calculate_operational_rating(margin: Number, slope: Number, variance: Number) -> float:
    """
    Marj, egim ve varyansa dayali basit bir skor (0-100) uretir.

    Parametreler:
        margin: EGT marji (C).
        slope: Trend egimi (C/adim).
        variance: Degisim varyansi (C^2).

    Doner:
        0-100 araliginda operasyon skoru.
    """
    m = float(margin)
    s = abs(float(slope))
    v = float(variance)

    # Baslangic skoru: marji -50 ile 50 arasina kirp ve 50 ekle
    margin_adjust = max(min(m, 50.0), -50.0)
    score = 50.0 + margin_adjust

    # Daha buyuk egim ve varyans icin basit cezalar
    score -= min(s * 10.0, 20.0)
    score -= min(v * 5.0, 30.0)

    # 0-100 araligina kirp
    return max(0.0, min(100.0, score))


def explain_operational_rating(score: Number) -> str:
    """
    Hesaplanan operasyon skorunu aciklayan Turkce metin dondurur.

    Parametreler:
        score: 0-100 araliginda sayisal skor.

    Doner:
        Durumu aciklayan kisa metin.
    """
    value = float(score)
    if value >= 70.0:
        return "Motor durumu iyi"
    if value >= 40.0:
        return "Dikkat"
    return "Kritik seviyeye yakin"
