Motor performance analyzer scaffold initialized.
Python klasörü modeller, health, faults ve utils alt modülleriyle birlikte 
analiz tarafında kullanılacak temel yapıyı sağlar.

Matlab klasöründe egt_model.m ve n1_n2_map.m fonksiyonları 
simülasyon ve performans haritaları için başlangıç yer tutucuları olarak hazırlandı.

Bu sürüm yalnızca proje iskeletini ve ana modül yapı taşlarını içerir.
İlerleyen versiyonlarda motor parametre modelleri, trend analizi ve 
fault tespit mekanizmaları kademeli olarak eklenecektir.

Kisa notlar: python/tests altindaki pytest dosyalari temel kontrol saglar.
Matlab scriptlerini calistirirken motor parametrelerini baslangicta guncelleyebilirsiniz.
Yeni motor senaryolari icin python/src/models altinda genislettiginiz fonksiyonlari testlerle destekleyin.
