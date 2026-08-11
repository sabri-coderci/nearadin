import urllib.request
import re
import datetime
from bs4 import BeautifulSoup  # pip install bs4 beautifulsoup4 (Gerekirse workflow'a ekleyin)

def fetch_koeri_earthquakes():
    url = "http://www.koeri.boun.edu.tr/scripts/lst2.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    # Admatic Auto Ads Kodu
    admatic_code = '''
    <div style="margin: 20px 0; text-align: center; min-height: 100px;">
        <!-- Admatic AUTO ads START -->
        <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
        <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
        <!-- Admatic AUTO ads END -->
    </div>
    '''

    # Online Ziyaretçi Sayacı (Who's Amung Us)
    whos_amung_us_code = '''
    <div style="text-align: center; margin: 25px 0;">
        <script id="_wauelp">var _wau = _wau || []; _wau.push(["dynamic", "tgui40zwet", "elp", "c4302bffffff", "small"]);</script><script async src="//waust.at/d.js"></script>
    </div>
    '''

    try:
        req = urllib.request.Request(url, headers=headers)
        # Kandilli ISO-8859-9 (Türkçe) karakter seti kullanır
        response = urllib.request.urlopen(req, timeout=15)
        html_content = response.read().decode('iso-8859-9')

        # <pre> etiketleri arasındaki ham metni çek
        soup = BeautifulSoup(html_content, 'html.parser')
        pre_tag = soup.find('pre')

        if not pre_tag:
            print("Kandilli veri formatı okunamadı.")
            return

        lines = pre_tag.text.split('\n')
        earthquakes = []

        # Başlık satırlarını atlayıp verileri işle
        for line in lines[5:]:
            line = line.strip()
            if not line or line.startswith('--------------'):
                continue
            
            parts = re.split(r'\s+', line)
            if len(parts) >= 9:
                date = parts[0]
                time = parts[1][:5]  # HH:MM
                
                # Büyüklük tespiti (MD, ML, Mw kolonları içerisinden en doğru ML/Mw seçimi)
                try:
                    mag_val = float(parts[6])  # Genelde ML büyüklüğü
                except ValueError:
                    continue

                # SADECE 4.0 VE ÜZERİ DEPREMLERİ FİLTRELE
                if mag_val >= 4.0:
                    # Yer adı parçalarını birleştir (İl/İlçe parantezlerini düzgün alması için)
                    location = " ".join(parts[8:-1]) 
                    depth = parts[4]

                    earthquakes.append({
                        "date": date,
                        "time": time,
                        "mag": f"{mag_val:.1f}",
                        "depth": depth,
                        "location": location
                    })

        # Tablo HTML Satırlarını Oluştur
        rows_html = ""
        if earthquakes:
            for eq in earthquakes:
                rows_html += f'''
                <tr>
                    <td><strong>{eq['time']}</strong> <small style="color:#666;">({eq['date']})</small></td>
                    <td><span class="mag mag-high">{eq['mag']}</span></td>
                    <td><strong>{eq['location']}</strong></td>
                    <td>{eq['depth']} km</td>
                </tr>
                '''
        else:
            rows_html = '<tr><td colspan="4" style="text-align:center; padding: 20px; color: #666;">Son saatlerde 4.0 ve üzeri büyüklükte deprem kaydedilmedi.</td></tr>'

        # SEO Uyumlu Tam HTML Çıktısı
        tz_tr = datetime.timezone(datetime.timedelta(hours=3))
        now_str = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

        full_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son Depremler (4.0+ Üzeri) - Canlı Kandilli Rasathanesi Listesi - nearadin.net</title>
    <meta name="description" content="Türkiye ve yakın çevresinde meydana gelen 4.0 ve üzeri büyüklükteki son dakika canlı deprem listesi. Kandilli Rasathanesi anlık verileri." />
    <link rel="canonical" href="https://nearadin.net/son-depremler/" />
    
    <!-- Open Graph / Social Media -->
    <meta property="og:title" content="Son Depremler (4.0 ve Üzeri) - nearadin.net" />
    <meta property="og:description" content="Kandilli Rasathanesi verileriyle Türkiye'deki 4.0 üzeri son depremler." />
    <meta property="og:image" content="https://nearadin.net/P5xJ5K5J_400x400.jpg" />

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background: #f4f6f9; color: #1c1e21; padding-bottom: 40px; }}
        header {{ background-color: #0056b3; color: white; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; }}
        header a {{ color: white; text-decoration: none; }}
        .container {{ max-width: 800px; margin: 20px auto; padding: 0 12px; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .info-box {{ background: #fff3cd; color: #856404; padding: 12px; border-radius: 6px; font-size: 13px; margin-bottom: 15px; border: 1px solid #ffeeba; }}
        .back-btn {{ display: inline-block; margin-bottom: 15px; color: #0056b3; text-decoration: none; font-weight: 600; font-size: 14px; }}
        h1 {{ font-size: 20px; color: #111; margin-bottom: 15px; }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
        th, td {{ padding: 12px 10px; border-bottom: 1px solid #eee; }}
        th {{ background: #0056b3; color: white; font-weight: 600; }}
        
        .mag {{ font-weight: bold; padding: 4px 8px; border-radius: 4px; color: white; display: inline-block; }}
        .mag-high {{ background: #d93025; }} /* 4.0 ve üzeri Kırmızı */

        .status-footer {{ margin-top: 15px; font-size: 12px; color: #65676b; text-align: right; }}
    </style>
</head>
<body>

    <header>
        <a href="/">nearadin.net - Son Dakika</a>
    </header>

    <div class="container">
        <a href="/" class="back-btn">← Ana Sayfaya Dön</a>
        
        <div class="card">
            <h1>🚨 Son Depremler (Canlı Akış)</h1>
            
            <div class="info-box">
                📌 <strong>Not:</strong> Sayfamızda arama motoru standartları ve kullanıcı deneyimi gereği <strong>sadece 4.0 ve üzeri büyüklükteki</strong> hissettiren depremler anlık olarak listelenmektedir. Veriler Kandilli Rasathanesi kaynaklıdır.
            </div>

            {admatic_code}

            <div style="overflow-x:auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Saat / Tarih</th>
                            <th>Büyüklük</th>
                            <th>Yer</th>
                            <th>Derinlik</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>

            <div class="status-footer">
                Son Güncelleme: <strong>{now_str}</strong>
            </div>

            {whos_amung_us_code}
        </div>
    </div>

</body>
</html>'''

        # Klasör ve Dosya Oluşturma (`/son-depremler/index.html`)
        import os
        os.makedirs("son-depremler", exist_ok=True)
        with open("son-depremler/index.html", "w", encoding="utf-8") as f:
            f.write(full_page_html)

        print("Son Depremler sayfası (4.0+ filtreli) başarıyla oluşturuldu.")

    except Exception as e:
        print(f"Deprem verisi çekilirken hata: {e}")

if __name__ == "__main__":
    fetch_koeri_earthquakes()
