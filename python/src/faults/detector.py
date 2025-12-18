"""
Ariza tespiti icin yer tutucu fonksiyonlar.
EGT marji, yakit akis sapmalari ve rpm anomali kontrolleri icin basit uyarilar verir.
"""

from typing import Iterable, Optional, Union

Number = Union[int, float]


def check_egt_margin(egt_margin: Number, threshold: Number = 50.0) -> Optional[str]:
    """
    EGT marji esigin altindaysa uyari dondurur.

    Parametreler:
        egt_margin: Hesaplanmis EGT marji (C).
        threshold: Kabul edilen minimum marj (C).

    Doner:
        Uyari metni veya None.
    """
    # Esik altinda ise uyari ver, degilse None dondur
    if float(egt_margin) < float(threshold):
        return "EGT margin below threshold"
    return None


def check_fuel_flow_deviation(
    fuel_flow: Number, nominal: Number, threshold: Number = 0.1
) -> Optional[str]:
    """
    Yakit akis nominal degerinden yuzdesel olarak saptiysa uyari dondurur.

    Parametreler:
        fuel_flow: Olculen yakit akis miktari.
        nominal: Beklenen nominal yakit akis degeri.
        threshold: Izin verilen yuzdesel sapma (0-1 arasi).

    Doner:
        Uyari metni veya None.
    """
    # Sapma mutlak fark > nominal * esik ise uyar
    if abs(float(fuel_flow) - float(nominal)) > float(nominal) * float(threshold):
        return "Fuel flow deviation above threshold"
    return None


def detect_sensor_drift(values: Union[Iterable[Number], None], drift_threshold: Number = 0.01) -> Optional[str]:
    """
    Sirali veride tutarli artis/azalis varsa (drift) uyari dondurur.

    Parametreler:
        values: Zaman sirali sayi listesi.
        drift_threshold: Her adimda aranacak minimum degisim miktari.

    Doner:
        Uyari metni veya None.
    """
    if values is None:
        return None

    diffs = []
    prev = None
    for v in values:
        try:
            num = float(v)
        except (TypeError, ValueError):
            continue
        if prev is not None:
            diffs.append(num - prev)
        prev = num

    if not diffs:
        return None

    # Drift, tum farklarin ayni yone ve esigin ustunde olmasi ile sinirli basit kontrol
    first_sign = 1 if diffs[0] > 0 else -1
    for d in diffs:
        if d == 0:
            continue
        if (d > 0) != (first_sign > 0):
            return None
        if abs(d) < float(drift_threshold):
            return None

    return "Sensor drift detected"


def aggregate_faults(*warnings: Optional[str]) -> list[str]:
    """
    Birden fazla uyaridan None olmayanlari toplayip liste dondurur.

    Parametreler:
        warnings: Uyari metinleri veya None.

    Doner:
        Aktif hatalar listesi.
    """
    return [w for w in warnings if w is not None]


def check_fuel_flow_stability(values: Union[Iterable[Number], None], delta: Number = 0.05) -> Optional[str]:
    """
    Ardisik yakit akis degisimleri delta esigini asiyorsa uyari dondurur.

    Parametreler:
        values: Zaman sirali yakit akis degerleri.
        delta: Kabul edilen maksimum adim farki.

    Doner:
        Uyari metni veya None.
    """
    if values is None:
        return None

    prev = None
    for v in values:
        try:
            num = float(v)
        except (TypeError, ValueError):
            continue
        if prev is not None and abs(num - prev) > float(delta):
            return "Fuel flow instability detected"
        prev = num

    return None


def detect_rpm_anomaly(
    n1_values: Union[Iterable[Number], None],
    n2_values: Union[Iterable[Number], None],
    threshold: Number = 5.0,
) -> Optional[str]:
    """
    N1 veya N2 degerleri ardarda esigi asan artis/azalis yaparsa uyari dondurur.

    Parametreler:
        n1_values: N1 zaman serisi.
        n2_values: N2 zaman serisi.
        threshold: Kabul edilen maksimum adim farki.

    Doner:
        Uyari metni veya None.
    """
    def has_jump(seq: Union[Iterable[Number], None]) -> bool:
        if seq is None:
            return False
        prev = None
        for v in seq:
            try:
                num = float(v)
            except (TypeError, ValueError):
                continue
            if prev is not None and abs(num - prev) > float(threshold):
                return True
            prev = num
        return False

    if has_jump(n1_values) or has_jump(n2_values):
        return "RPM anomaly detected"
    return None


def evaluate_fault_conditions(**conditions: bool) -> dict[str, bool]:
    """
    Boolean sartlardan aktif olanlari sozluk olarak dondurur.

    Parametreler:
        conditions: fault_adi=True/False seklinde sartlar.

    Doner:
        Sadece True olan sartlari iceren sozluk.
    """
    return {name: True for name, flag in conditions.items() if flag}


def combined_performance_fault(
    rpm_slope: Number, ff_slope: Number, rpm_threshold: Number = 0.0, ff_threshold: Number = 0.0
) -> Optional[str]:
    """
    RPM ve yakit akisi egimleri esikleri astiginda uyari dondurur.

    Parametreler:
        rpm_slope: RPM trend egimi.
        ff_slope: Yakit akis trend egimi.
        rpm_threshold: RPM icin minimum mutlak esik.
        ff_threshold: Yakit akis icin minimum mutlak esik.

    Doner:
        Uyari metni veya None.
    """
    if abs(float(rpm_slope)) > float(rpm_threshold) and abs(float(ff_slope)) > float(ff_threshold):
        return "Combined performance fault detected"
    return None


def weight_fault_signals(faults: dict[str, bool]) -> float:
    """
    Hata sozlugundeki True degerleri icin agirlikli bir siddet skoru dondurur.

    Parametreler:
        faults: {fault_adi: True/False} seklinde sozluk.

    Doner:
        Agirlikli toplam skor.
    """
    if not faults:
        return 0.0

    score = 0.0
    for name, active in faults.items():
        if not active:
            continue
        # Basit agirlik: kritik kelimesi geciyorsa daha yuksek ekle
        weight = 2.0 if "critical" in name.lower() else 1.0
        score += weight

    return score


def detect_compressor_efficiency_drop(
    n1: Number, n2: Number, expected_ratio: Number, threshold: Number = 0.05
) -> Optional[str]:
    """
    Beklenen N1/N2 orani ile olculen deger arasindaki sapmayi kontrol eder.

    Parametreler:
        n1: Olculen N1 degeri.
        n2: Olculen N2 degeri.
        expected_ratio: Beklenen N2/N1 orani.
        threshold: Kabul edilen yuzdesel sapma (0-1 arasi).

    Doner:
        Uyari metni veya None.
    """
    if float(n1) == 0:
        return None

    actual_ratio = float(n2) / float(n1)
    deviation = abs(actual_ratio - float(expected_ratio))
    if deviation > float(expected_ratio) * float(threshold):
        return "Compressor efficiency drop detected"
    return None
