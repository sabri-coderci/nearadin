import urllib.request
import re
import os
from bs4 import BeautifulSoup

def generate_earthquakes_html():
    url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    earthquakes = []

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        html_content = response.read().decode('iso-8859-9')

        soup = BeautifulSoup(html_content, 'html.parser')
        pre_tag = soup.find('pre')

        if pre_tag:
            lines = pre_tag.text.split('\n')
            for line in lines[5:]:
                line = line.strip()
                if not line or line.startswith('--------------'):
                    continue
                
                parts = re.split(r'\s+', line)
                if len(parts) >= 9:
                    date = parts[0]
                    time = parts[1][:5]
                    depth = parts[4]

                    try:
                        mag_val = float(parts[6])  # ML Büyüklüğü
                    except ValueError:
                        continue

                    # SADECE 4.0 VE ÜZERİ DEPREMLERİ AL
                    if mag_val >= 4.0:
                        raw_location = " ".join(parts[8:])
                        location = re.sub(r'\s+(İlksel|REVISE\d*).*$', '', raw_location, flags=re.IGNORECASE)
                        
                        earthquakes.append({
                            "date": date,
                            "time": time,
                            "mag": f"{mag_val:.1f}",
                            "depth": depth,
                            "location": location.strip()
                        })
    except Exception as e:
        print(f"Deprem verisi çekilirken hata: {e}")

    # Deprem Kartları HTML Yapısını Oluşturma
    cards_html = ""
    if earthquakes:
        for eq in earthquakes:
            mag = float(eq['mag'])
            badge_class = 'bg-high' if mag >= 5.0 else 'bg-medium'
            cards_html += f'''
            <div class="eq-item">
                <div class="eq-left">
                    <div class="eq-location">📍 {eq['location']}</div>
                    <div class="eq-meta">📅 {eq['date']} - {eq['time']} | 🔽 Derinlik: {eq['depth']} km</div>
                </div>
                <div class="eq-badge {badge_class}">{eq['mag']}</div>
            </div>
            '''
    else:
        cards_html = '<div class="loading">Son kaydedilen 4.0 veya üzeri deprem bulunmamaktadır.</div>'

    # HTML Şablonu
    full_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son Depremler - nearadin.net</title>
    <meta name="description" content="Kandilli ve AFAD verileriyle son dakika anlık deprem listesi." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        header {{ background-color: #0056b3; color: white; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; position: sticky; top: 0; z-index: 100; }}
        header a {{ color: white; text-decoration: none; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        h1 {{ font-size: 20px; margin-bottom: 8px; color: #0056b3; text-align: center; }}
        p.subtitle {{ color: #65676b; font-size: 13px; text-align: center; margin-bottom: 20px; }}

        .eq-list {{ display: flex; flex-direction: column; gap: 12px; }}
        .eq-item {{ display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1px solid #e4e6eb; border-radius: 8px; padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }}
        
        .eq-left {{ display: flex; flex-direction: column; gap: 4px; text-align: left; }}
        .eq-location {{ font-size: 15px; font-weight: bold; color: #1c1e21; }}
        .eq-meta {{ font-size: 12px; color: #65676b; }}
        
        .eq-badge {{ min-width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px; color: white; flex-shrink: 0; margin-left: 10px; }}
        
        .bg-medium {{ background-color: #f57c00; }}
        .bg-high {{ background-color: #d32f2f; }}

        .loading {{ text-align: center; padding: 30px 0; color: #65676b; font-size: 14px; }}
        .btn-home {{ display: block; text-align: center; background: #e4e6eb; color: #050505; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 20px; }}
    </style>
</head>
<body>
    <header><a href="/">nearadin.net - Son Depremler</a></header>
    
    <div class="container">
        <div class="card">
            <h1>🔴 Son Depremler (4.0+)</h1>
            <p class="subtitle">Kandilli Rasathanesi verileriyle Türkiye ve yakın çevresinde meydana gelen 4.0 ve üzeri depremler.</p>
            
            <div class="eq-list">
                {cards_html}
            </div>

            <a href="/" class="btn-home">← Anasayfaya Dön</a>
        </div>
    </div>

    <footer style="background-color: #1c1e21; color: #90949c; padding: 30px 15px; margin-top: 40px; font-size: 13px; line-height: 1.6; clear: both;">
        <div style="max-width: 680px; margin: 0 auto;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 20px;">
                <div style="flex: 1; min-width: 200px;">
                    <h3 style="color: #fff; font-size: 16px; margin-bottom: 10px;">nearadin.net</h3>
                    <p>Türkiye ve dünyadan en güncel son dakika haberleri, anlık gelişmeler ve canlı servis haber akış platformu.</p>
                </div>
                <div style="flex: 1; min-width: 140px;">
                    <h4 style="color: #fff; font-size: 14px; margin-bottom: 10px;">Hızlı Menü</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 5px;"><a href="/" style="color: #617085; text-decoration: none;">Anasayfa</a></li>
                        <li style="margin-bottom: 5px;"><a href="/arsiv/" style="color: #617085; text-decoration: none;">📅 Günlük Arşiv</a></li>
                        <li style="margin-bottom: 5px;"><a href="/nobetci-eczane/" style="color: #617085; text-decoration: none;">🏥 Nöbetçi Eczane</a></li>
                        <li style="margin-bottom: 5px;"><a href="/son-depremler/" style="color: #617085; text-decoration: none;">🔴 Son Depremler</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kripto-para/" style="color: #617085; text-decoration: none;">🪙 Kripto Piyasası</a></li>
                        <li style="margin-bottom: 5px;"><a href="/hava-durumu/" style="color: #617085; text-decoration: none;">☀️ Hava Durumu</a></li>
                        <li style="margin-bottom: 5px;"><a href="/sitemap.xml" style="color: #617085; text-decoration: none;">Sitemap</a></li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; font-size: 12px; color: #65676b;">
                <p style="margin-bottom: 8px;">Takip Edin: <a href="https://x.com/nearadin2026" target="_blank" rel="nofollow" style="color: #1877f2; text-decoration: none; font-weight: bold;">@nearadin2026 (X / Twitter)</a></p>
                <p>© 2026 nearadin.net - Tüm Hakları Saklıdır.</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''

    # Dosyayı kaydet
    os.makedirs("son-depremler", exist_ok=True)
    with open("son-depremler/index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"son-depremler/index.html başarıyla güncellendi. Toplam 4.0+ deprem sayısı: {len(earthquakes)}")

if __name__ == "__main__":
    generate_earthquakes_html()
