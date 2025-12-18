"""
Basit dusuk geciren (low-pass) filtre.
Ustel yumusatma ile y[n] = alpha * x[n] + (1 - alpha) * y[n-1].
"""

from typing import Iterable, List, Union

Number = Union[int, float]


def low_pass_filter(values: Union[Iterable[Number], None], alpha: float = 0.2) -> List[float]:
    """
    Ustel yumusatma tabanli dusuk geciren filtre uygula.

    Parametreler:
        values: Giris sinyali (liste veya numpy array benzeri).
        alpha: Ustel agirlik katsayisi (0-1).

    Doner:
        Filtrelenmis yeni liste.
    """
    if values is None:
        return []

    output: List[float] = []
    prev: float | None = None
    a = float(alpha)

    for v in values:
        try:
            x = float(v)
        except (TypeError, ValueError):
            # Gecersiz degerleri atla
            continue

        if prev is None:
            prev = x
        else:
            prev = a * x + (1 - a) * prev

        output.append(prev)

    return output


def normalize_values(values: Union[Iterable[Number], None]) -> List[float]:
    """
    Degerleri [0, 1] araligina olce.

    Parametreler:
        values: Liste veya numpy array benzeri sayi dizisi.

    Doner:
        Normalize edilmis yeni liste.
    """
    if values is None:
        return []

    nums: List[float] = []
    for v in values:
        try:
            nums.append(float(v))
        except (TypeError, ValueError):
            # Sayiya donmeyenleri atla
            continue

    if not nums:
        return []

    v_min = min(nums)
    v_max = max(nums)
    if v_max == v_min:
        # Tum degerler ayniysa sifirla
        return [0.0 for _ in nums]

    scale = v_max - v_min
    return [(n - v_min) / scale for n in nums]


def moving_window(values: Union[Iterable[Number], None], window_size: int) -> Iterable[List[float]]:
    """
    Kaydirilan pencereler halinde dilim dondurur.

    Parametreler:
        values: Girdi dizisi.
        window_size: Pencere uzunlugu.

    Doner:
        Pencere listeleri ureten bir generator.
    """
    if values is None:
        return []

    window = max(int(window_size), 1)
    buffer: List[float] = []
    for v in values:
        try:
            num = float(v)
        except (TypeError, ValueError):
            continue
        buffer.append(num)
        if len(buffer) == window:
            yield list(buffer)
            buffer.pop(0)


def linear_interpolate(values: Union[List[Union[Number, None]], None]) -> List[float]:
    """
    None degerlerini basit dogrusal interpolasyon ile doldurur.

    Parametreler:
        values: None icerebilen sayi listesi.

    Doner:
        Interpole edilmis yeni liste.
    """
    if values is None:
        return []

    # Girdiyi float listesine cevirirken None'lari koru
    nums: List[Union[float, None]] = []
    for v in values:
        if v is None:
            nums.append(None)
        else:
            try:
                nums.append(float(v))
            except (TypeError, ValueError):
                nums.append(None)

    if not nums:
        return []

    # Ilk gecerli degeri bul ve basta doldur
    first_valid = next((x for x in nums if x is not None), None)
    if first_valid is None:
        return [0.0 for _ in nums]
    for i, x in enumerate(nums):
        if x is None:
            nums[i] = first_valid
        else:
            break

    # Orta ve son None'lari doldur
    last_valid = nums[0]
    for i in range(1, len(nums)):
        if nums[i] is None:
            # Sonraki gecerliyi ara
            j = i + 1
            next_valid = None
            while j < len(nums):
                if nums[j] is not None:
                    next_valid = nums[j]
                    break
                j += 1
            if next_valid is None:
                nums[i] = last_valid
            else:
                step = (next_valid - last_valid) / (j - i + 1)
                nums[i] = last_valid + step
        else:
            last_valid = nums[i]

    return [float(x) for x in nums]


def basic_stats(values: Union[Iterable[Number], None]) -> tuple[float, float, float]:
    """
    Sayisal dizinin ortalama, min ve max degerlerini dondurur.

    Parametreler:
        values: Liste veya numpy array benzeri sayilar.

    Doner:
        (ortalama, min, max) seklinde tuple.
    """
    if values is None:
        return (0.0, 0.0, 0.0)

    nums: List[float] = []
    for v in values:
        try:
            nums.append(float(v))
        except (TypeError, ValueError):
            continue

    if not nums:
        return (0.0, 0.0, 0.0)

    total = sum(nums)
    return (total / len(nums), min(nums), max(nums))


def resample_timeseries(values: Union[Iterable[Number], None], step: int = 2) -> List[float]:
    """
    Zaman serisinden her n'inci ornegi tutarak yeniden ornekler.

    Parametreler:
        values: Giris zaman serisi.
        step: Alinacak adim araligi (varsayilan 2).

    Doner:
        Azaltilmis ornek listesi.
    """
    if values is None:
        return []

    stride = max(int(step), 1)
    sampled: List[float] = []
    for idx, v in enumerate(values):
        if idx % stride != 0:
            continue
        try:
            sampled.append(float(v))
        except (TypeError, ValueError):
            continue

    return sampled
