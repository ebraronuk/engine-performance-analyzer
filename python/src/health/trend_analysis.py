"""
Trend verisini basitce temizlemek icin yer tutucu.
None ve negatif ani dususleri ayiklar.
"""

from typing import Iterable, List, Optional, Tuple, Union

Number = Union[int, float]


def prepare_trend(values: Union[Iterable[Number], None]) -> List[float]:
    """
    Trend hesaplari icin temel veri temizleme.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        None ve negatif degerlerden arindirilmis yeni liste.
    """
    if values is None:
        return []

    cleaned: List[float] = []
    for v in values:
        # Sadece sayisal ve negatif olmayan degerleri tut
        if v is None:
            continue
        try:
            num = float(v)
        except (TypeError, ValueError):
            continue
        if num < 0:
            continue
        cleaned.append(num)

    return cleaned


def apply_moving_average(values: Union[Iterable[Number], None], window_size: int = 3) -> List[float]:
    """
    Basit hareketli ortalama uygula.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.
        window_size: Ortalama alinacak pencere boyutu.

    Doner:
        Hareketli ortalama ile yumusatilmis yeni liste.
    """
    cleaned = prepare_trend(values)
    if not cleaned:
        return []

    window = max(int(window_size), 1)
    smoothed: List[float] = []
    for i in range(len(cleaned) - window + 1):
        # Pencere icindeki degerlerin ortalamasini al
        window_slice = cleaned[i : i + window]
        smoothed.append(sum(window_slice) / window)

    return smoothed


def compute_rolling_variance(values: Union[Iterable[Number], None], window_size: int = 5) -> List[float]:
    """
    Kaydirilan pencereler icin varyans hesaplar.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.
        window_size: Varyans alinacak pencere boyutu.

    Doner:
        Pencere bazli varyans listesi.
    """
    cleaned = prepare_trend(values)
    window = max(int(window_size), 1)
    if len(cleaned) < window:
        return []

    variances: List[float] = []
    for i in range(len(cleaned) - window + 1):
        window_slice = cleaned[i : i + window]
        mean = sum(window_slice) / window
        variance = sum((x - mean) ** 2 for x in window_slice) / window
        variances.append(variance)

    return variances


def compute_slope(values: Union[Iterable[Number], None]) -> float:
    """
    Ilk ve son gecerli nokta arasindaki egimi hesapla.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        (son - ilk) / veri_sayisi degeri.
    """
    cleaned = prepare_trend(values)
    if not cleaned:
        return 0.0

    first = cleaned[0]
    last = cleaned[-1]
    length = len(cleaned)

    # Basit egim: (last - first) / N
    return (last - first) / length


def compute_derivative(values: Union[Iterable[Number], None]) -> List[float]:
    """
    Ardısık degerler arasindaki ilk farki (turev yaklasimi) hesaplar.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        v[i+1] - v[i] seklinde fark listesi.
    """
    cleaned = prepare_trend(values)
    if len(cleaned) < 2:
        return []

    diffs: List[float] = []
    for i in range(len(cleaned) - 1):
        diffs.append(cleaned[i + 1] - cleaned[i])

    return diffs


def detect_outliers(values: Union[Iterable[Number], None]) -> List[bool]:
    """
    Ortalamadan 2 standart sapmadan fazla sapanlari isaretler.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        Outlier icin True/False listesi (cleaned uzunlugunda).
    """
    cleaned = prepare_trend(values)
    if not cleaned:
        return []

    mean = sum(cleaned) / len(cleaned)
    variance = sum((x - mean) ** 2 for x in cleaned) / len(cleaned)
    std = variance ** 0.5

    if std == 0:
        return [False for _ in cleaned]

    threshold = 2 * std
    return [abs(x - mean) > threshold for x in cleaned]


def generate_operational_summary(slope: Number, derivative: List[float], outlier_count: int) -> str:
    """
    Egim, turev ve aykiri sayisini kullanarak kisa bir operasyon ozeti uretir.

    Parametreler:
        slope: Trend egimi.
        derivative: Ardil farklar listesi.
        outlier_count: Tespit edilen aykiri deger sayisi.

    Doner:
        Kisa Turkce ozet metni.
    """
    avg_derivative = 0.0
    if derivative:
        avg_derivative = sum(derivative) / len(derivative)

    return (
        f"Egim: {float(slope):.3f}, "
        f"Ortalama turev: {avg_derivative:.3f}, "
        f"Aykiri sayisi: {int(outlier_count)}"
    )


def detect_degradation(slope: Number, rolling_variances: List[float]) -> str:
    """
    Negatif egim ve artan rolling varyans ile degradasyonu kontrol eder.

    Parametreler:
        slope: Trend egimi.
        rolling_variances: Kaydirilan pencere varyanslari listesi.

    Doner:
        Kisa aciklama metni.
    """
    s = float(slope)
    if s < 0 and rolling_variances:
        variance_trend = rolling_variances[-1] - rolling_variances[0]
        if variance_trend > 0:
            return "Degradasyon sinyali: negatif egim ve artan varyans"
    return "Belirgin degradasyon yok"


def compute_percentile_threshold(values: Union[Iterable[Number], None]) -> Tuple[float, float]:
    """
    5. ve 95. persentil degerlerini hesaplar.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        (p5, p95) tuple degerleri.
    """
    cleaned = prepare_trend(values)
    if not cleaned:
        return (0.0, 0.0)

    sorted_vals = sorted(cleaned)
    n = len(sorted_vals)

    def percentile(p: float) -> float:
        # Basit lineer interpolasyonlu persentil
        if n == 1:
            return sorted_vals[0]
        k = (n - 1) * p
        lower = int(k)
        upper = min(lower + 1, n - 1)
        frac = k - lower
        return sorted_vals[lower] + (sorted_vals[upper] - sorted_vals[lower]) * frac

    return (percentile(0.05), percentile(0.95))


def detect_slow_drift(
    slopes: Union[Iterable[Number], None], threshold: Number = -0.01, min_length: int = 3
) -> Optional[str]:
    """
    Ardisik egimlerin uzun sureli hafif negatif kalip kalmadigini kontrol eder.

    Parametreler:
        slopes: Zamanla hesaplanmis egim listesi.
        threshold: Negatif kabul edilen maksimum deger (ornegin -0.01).
        min_length: Kesintisiz kac adimda bu kosulun saglanmasi gerektigi.

    Doner:
        "slow drift detected" veya None.
    """
    if slopes is None:
        return None

    run_required = max(int(min_length), 1)
    run = 0
    limit = float(threshold)

    for s in slopes:
        try:
            val = float(s)
        except (TypeError, ValueError):
            continue

        if val <= limit:
            run += 1
            if run >= run_required:
                return "slow drift detected"
        else:
            run = 0

    return None


def generate_extended_summary(
    slope: Number,
    variance: Number,
    drift_flag: Optional[str],
    outlier_count: int,
) -> str:
    """
    Egim, varyans, drift durumu ve aykiri sayisini toplayip cok satirli ozet dondurur.

    Parametreler:
        slope: Trend egimi.
        variance: Ortalama veya son varyans degeri.
        drift_flag: Drift tespit etiketi (None veya metin).
        outlier_count: Tespit edilen aykiri sayisi.

    Doner:
        Turkce cok satirli ozet metni.
    """
    drift_text = drift_flag if drift_flag else "Drift yok"
    return (
        f"Egim: {float(slope):.3f}\n"
        f"Varyans: {float(variance):.3f}\n"
        f"Drift: {drift_text}\n"
        f"Aykiri sayisi: {int(outlier_count)}"
    )
