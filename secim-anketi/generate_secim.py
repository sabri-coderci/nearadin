import os
import sys
import datetime

# Üst dizindeki (ana projedeki) modüllere ve fonksiyonlara erişebilmek için parent dizini ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def generate_secim_anketi_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """Bulunduğu klasördeki (secim-anketi) anket_verileri.txt dosyasını okuyarak index.html oluşturur."""
    
    # Betiğin çalıştığı klasörün tam yolunu belirleme
    current_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(current_dir, "anket_verileri.txt")
    output_html_path = os.path.join(current_dir, "index.html")

    poll_results = []
    total_votes = 0

    # 1. Aynı klasördeki TXT dosyasından verileri okuma
    if os.path.exists(txt_path):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("|")
                        if len(parts) == 5:
                            code, name, percent, votes, color = parts
                            votes_int = int(votes)
                            total_votes += votes_int
                            poll_results.append({
                                "code": code.strip(),
                                "name": name.strip(),
                                "percent": float(percent.strip()),
                                "votes": votes_int,
                                "color": color.strip()
                            })
        except Exception as e:
            print(f"⚠️ Anket TXT dosyası okunurken hata oluştu: {e}")
    else:
        print(f"⚠️ Hata: {txt_path} dosyası bulunamadı! 'anket_verileri.txt' dosyasını bu klasöre ekleyin.")

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")
    last_update_iso = datetime.datetime.now(tz_tr).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    # 2. Oy oranları grafik bileşenleri
    poll_bars_html = ""
    for party in poll_results:
        poll_bars_html += f'''
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; margin-bottom: 4px;">
                <span>{party['name']} ({party['code']})</span>
                <span style="color: {party['color']};">%{party['percent']}</span>
            </div>
            <div style="background: #e4e6eb; height: 18px; border-radius: 9px; overflow: hidden; position: relative;">
                <div style="background: {party['color']}; width: {party['percent']}%; height: 100%; border-radius: 9px; transition: width 0.5s ease;"></div>
            </div>
            <div style="font-size: 11px; color: #65676b; text-align: right; margin-top: 2px;">Oy Sayısı: {party['votes']:,}</div>
        </div>
        '''

    # 3. HTML Şablonu
    poll_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son Seçim Anketi Sonuçları - Oy Oranları ve Anket Verileri - nearadin.net</title>
    <meta name="description" content="En son yapılan genel seçim anketi sonuçları, partilerin oy oranları, oy dağılımı ve kararsızların oranı. Güncel seçim anketi verileri canlı akış." />
    <link rel="canonical" href="https://nearadin.net/secim-anketi/" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Son Seçim Anketi Sonuçları & Oy Dağılımı" />
    <meta name="twitter:description" content="Türkiye geneli en son seçim anketi oy oranları ve parti bazlı canlı anket verileri." />
    <meta name="twitter:site" content="@nearadin2026" />
    <meta name="twitter:image" content="https://nearadin.net/1786394487303.png" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="Güncel Seçim Anketi Sonuçları ve Oy Oranları" />
    <meta property="og:description" content="Partilerin son oy oranları, seçim anketi analizleri ve detaylı istatistikler." />
    <meta property="og:url" content="https://nearadin.net/secim-anketi/" />
    <meta property="og:image" content="https://nearadin.net/1786394487303.png" />

    <!-- Schema.org Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Dataset",
      "name": "Türkiye Genel Seçim Anketi Sonuçları",
      "description": "Güncel seçim anketi oy oranları veriseti.",
      "dateModified": "{last_update_iso}",
      "publisher": {{
        "@type": "Organization",
        "name": "nearadin.net"
      }}
    }}
    </script>

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 15px; }}
        
        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin-bottom: 10px; }}
        
        h1 {{ font-size: 22px; margin-bottom: 12px; color: #050505; line-height: 1.3; }}
        h2 {{ font-size: 17px; margin: 18px 0 10px 0; color: #0056b3; border-bottom: 2px solid #e4e6eb; padding-bottom: 5px; }}
        p {{ font-size: 14px; color: #333; margin-bottom: 12px; line-height: 1.6; }}
        
        .total-box {{ background: #f7f8fa; border-left: 4px solid #1877f2; padding: 12px 15px; border-radius: 0 8px 8px 0; margin: 15px 0; font-size: 13px; color: #4b4f56; }}
        
        .btn-home {{ display: inline-block; background: #1877f2; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 15px; text-align: center; }}
        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>
    
    <!-- Admatic AUTO ads START -->
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    <!-- Admatic AUTO ads END -->

    {admatic_code}
    {header_html}

    <div class="container">
        <div class="status-bar">
            <span>Veri Kaynağı: <strong>Yerel Anket Veritabanı</strong></span>
            <span>Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <article class="card">
            <span class="badge">🔴 CANLI ANKET SONUÇLARI</span>
            <h1>Son Seçim Anketi Sonuçları ve Partilerin Oy Oranları</h1>
            
            <p>Türkiye genelinde gerçekleştirilen son <strong>seçim anketi</strong> verilerine göre siyasi partilerin güncel oy oranları ve seçmen tercihleri belirlendi. Kamuoyu araştırmalarından elde edilen verilere göre oy dağılımı grafikteki gibi şekillenmiştir.</p>

            <div class="total-box">
                📊 <strong>Toplam Örneklem:</strong> Bu anket çalışmasında toplam <strong>{total_votes:,}</strong> seçmenin oy tercihi değerlendirilmiştir.
            </div>

            <h2>🗳️ Parti Bazlı Oy Dağılım Grafiği</h2>
            
            {poll_bars_html if poll_bars_html else '<p>Anket verileri yüklenemedi.</p>'}

            {admatic_code}

            <h2>📈 Seçim Anketi Analizi ve Değerlendirme</h2>
            <p>Son yapılan <strong>seçim anketi sonuçları</strong> incelendiğinde, kararsız seçmenlerin oranı ve oy geçişleri seçimin kaderini belirleyecek en kritik unsur olarak öne çıkmaktadır. Siyasi partilerin saha çalışmaları, ekonomi politikaları ve vaatleri seçmen eğilimleri üzerinde doğrudan etkili olmaktadır.</p>

            <a href="/" class="btn-home">← Anasayfaya Dön</a>
        </article>

        {whos_amung_us_code}
    </div>

    {footer_html}

</body>
</html>'''

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(poll_html)
    print("✅ /secim-anketi/index.html başarıyla oluşturuldu.")

# Doğrudan klasör içinden çalıştırma bloğu
if __name__ == "__main__":
    try:
        from main import get_header_html, footer_html, whos_amung_us_code, admatic_code
        generate_secim_anketi_page(
            header_html=get_header_html("nearadin.net - Seçim Anketi"),
            footer_html=footer_html,
            whos_amung_us_code=whos_amung_us_code,
            admatic_code=admatic_code
        )
    except ImportError:
        print("⚠️ Ana dizindeki 'main.py' bileşenleri içe aktarılamadı. Lütfen üst dizinde 'main.py' dosyasının bulunduğundan emin olun.")
