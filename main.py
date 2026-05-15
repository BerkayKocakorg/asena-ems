import time
import random
import math
import requests

# ================= AYARLAR =================
# Berkay'ın Spring Boot sunucu adresi
API_URL = "http://10.24.0.56:8080/api/telemetry"

# Enkaz altındaki kazazedenin SABİT konumu (Gerçek hayatta bilinmez, biz simülasyon için sabitliyoruz)
VICTIM_LAT = 39.920770
VICTIM_LON = 32.854110
VICTIM_MAC = "AA:BB:CC:DD:EE:FF"

# Sensörü taşıyan kişinin/drone'un BAŞLANGIÇ konumu
sensor_lat = 39.920800
sensor_lon = 32.854200
# ============================================

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine formülü ile iki koordinat arası kuş uçuşu mesafeyi (metre) bulur.
    """
    R = 6371000  # Dünya yarıçapı (metre)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_rssi(distance):
    """Mesafe ve beton yoğunluğuna göre anlık gürültülü sinyal gücünü (RSSI) hesaplar."""
    if distance < 1: distance = 1  # 0'a bölme hatasını önle
    n = 4.5  # Beton sönümleme katsayısı
    rssi_0 = -40  # 1 metredeki referans sinyal gücü
    noise = random.gauss(0, 4)  # Multipath fading (çoklu yansıma) için rastgele gürültü

    rssi = rssi_0 - 10 * n * math.log10(distance) + noise
    return round(rssi, 2)

print("📡 Sensör Simülasyonu Başlatıldı! Sahadan veriler akıyor...")
print(f"Hedef Sunucu: {API_URL}\n")

while True:
    try:
        # 1. Sensörü titret (Kurtarma ekibinin enkaz üstündeki yürüyüşü / sarsıntı)
        sensor_lat += random.uniform(-0.00001, 0.00001)
        sensor_lon += random.uniform(-0.00001, 0.00001)

        # 2. Mesafeyi ve buna bağlı RSSI'ı hesapla
        distance = calculate_distance(sensor_lat, sensor_lon, VICTIM_LAT, VICTIM_LON)
        rssi = get_rssi(distance)

        # 3. Berkay'ın istediği JSON Paketini Hazırla
        payload = {
            "sensorLat": round(sensor_lat, 6),  # sensor_lat DEĞİL sensorLat
            "sensorLon": round(sensor_lon, 6),  # sensor_lon DEĞİL sensorLon
            "mac": VICTIM_MAC,
            "rssi": rssi,
            "timestamp": int(time.time() * 1000)
        }

        # 4. Veriyi Berkay'ın Sunucusuna Ateşle (POST Request)
        response = requests.post(API_URL, json=payload, timeout=2)

        # 5. Konsola başarılı logu bas
        print(f"[OK] Gönderildi -> Mesafe: {distance:.1f}m | RSSI: {rssi}dBm | HTTP Status: {response.status_code} | Timestamp: {payload['timestamp']}")

    except requests.exceptions.RequestException as e:
        # Berkay sunucusunu kapatırsa veya çökerse, kod hata verip kapanmaz.
        print(f"[HATA] Sunucuya ulaşılamıyor (Berkay API'yi güncelliyor olabilir). Üretilen RSSI: {rssi}dBm")

    # 6. Döngüyü 1 saniye beklet
    time.sleep(1)