# Engine Performance Analyzer

Bu proje, uçak motorlarına ait temel performans ve sağlık parametrelerini
analiz etmek amacıyla geliştirilen bir mühendislik analiz altyapısıdır.

Amaç; sensör verilerinden (ör. EGT, N1/N2, yakıt akışı) türetilen basit
hesaplamalar ile motor davranışını izlemek, trendleri analiz etmek ve
olası performans bozulmalarına erken aşamada işaret edebilmektir.

## Proje Kapsamı

- Motor performansına yönelik basit matematiksel modeller
- EGT margin, trend ve türev tabanlı sağlık göstergeleri
- Kural tabanlı ön arıza (fault) tespit mekanizmaları
- Python tabanlı analiz altyapısı
- MATLAB üzerinde destekleyici model ve görselleştirme fonksiyonları

## Proje Yapısı

- `python/`  
  Performans hesaplamaları, sağlık analizleri ve fault tespit mantıkları

- `matlab/`  
  Motor modelleri ve temel performans haritaları için yardımcı fonksiyonlar

Bu depo, projenin erken geliştirme aşamasını temsil etmektedir.
İlerleyen sürümlerde modellerin detaylandırılması, trend analizlerinin
genişletilmesi ve raporlama kabiliyetlerinin eklenmesi planlanmaktadır.
