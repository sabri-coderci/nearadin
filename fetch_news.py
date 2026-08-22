import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import os
import html
import tweepy
from email.utils import parsedate_to_datetime

def slugify(text):
    text = text.lower()
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def post_to_x(latest_news):
    """En son çıkan haberi X üzerinde paylaşır."""
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("X API anahtarları bulunamadı. Tweet atma adımı atlanıyor.")
        return

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )

        title = latest_news['title']
        desc_preview = latest_news['desc'][:100] + "..." if len(latest_news['desc']) > 100 else latest_news['desc']

        tweet_text = (
            f"🚨 SON DAKİKA HABERİ\n\n"
            f"📌 {title}\n\n"
            f"📝 {desc_preview}\n\n"
            f"🔗 Detaylar için tıklayın:\n{latest_news['full_url']}\n\n"
            f"#sondakika #haber #gundem"
        )
        
        response = client.create_tweet(text=tweet_text)
        print(f"X (Twitter) paylaşımı başarılı! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"X (Twitter) paylaşımında hata oluştu: {e}")

def get_header_html(title_text="nearadin.net - SON DAKİKA"):
    """Tüm Sayfalarda Ortak Kullanılan Hamburger Menülü Header Yapısı"""
    return f'''
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
        <button id="hamburgerBtn" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 5px; outline: none;">☰</button>
        
        <nav id="dropdownNav" style="display: none; position: absolute; top: 100%; right: 0; background: white; width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 0 0 8px 8px; border: 1px solid #e4e6eb; overflow: hidden;">
            <ul style="list-style: none; margin: 0; padding: 0;">
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏠 Anasayfa</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/canli-mac-sonuclari/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">⚽ Canlı Maç Sonuçları</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/arsiv/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">📅 Günlük Arşiv</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/nobetci-eczane/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏥 Nöbetçi Eczane</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/son-depremler/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🔴 Son Depremler</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/kripto-para/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🪙 Kripto Piyasası</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/hava-durumu/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">☀️ Hava Durumu</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/film-izle/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">📺 Film İzle</a></li>
                 <li style="border-bottom: 1px solid #f0f2f5;"><a href="/iletisim/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">📨 İletişim</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/namaz-vakitleri/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🕌 Namaz Vakitleri</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/backlink/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">♻️ Geri Bağlantı/Backlink</a></li>

                
            </ul>
        </nav>
    </header>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const btn = document.getElementById('hamburgerBtn');
            const nav = document.getElementById('dropdownNav');
            if (btn && nav) {{
                btn.addEventListener('click', function(e) {{
                    e.stopPropagation();
                    nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
                }});
                document.addEventListener('click', function(e) {{
                    if (!nav.contains(e.target) && e.target !== btn) {{
                        nav.style.display = 'none';
                    }}
                }});
            }}
        }});
    </script>
    '''

def get_footer_html():
    """Tüm Sayfalarda Ortak Kullanılan Standart Footer Bileşeni"""
    return '''
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
                        <li style="margin-bottom: 5px;"><a href="/canli-mac-sonuclari/" style="color: #617085; text-decoration: none;">⚽ Canlı Maç Sonuçları</a></li>
                        <li style="margin-bottom: 5px;"><a href="/arsiv/" style="color: #617085; text-decoration: none;">📅 Günlük Arşiv</a></li>
                        <li style="margin-bottom: 5px;"><a href="/nobetci-eczane/" style="color: #617085; text-decoration: none;">🏥 Nöbetçi Eczane</a></li>
                        <li style="margin-bottom: 5px;"><a href="/son-depremler/" style="color: #617085; text-decoration: none;">🔴 Son Depremler</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kripto-para/" style="color: #617085; text-decoration: none;">🪙 Kripto Piyasası</a></li>
                        <li style="margin-bottom: 5px;"><a href="/hava-durumu/" style="color: #617085; text-decoration: none;">☀️ Hava Durumu</a></li>
                        <li style="margin-bottom: 5px;"><a href="/film-izle/" style="color: #617085; text-decoration: none;">📺 Film İzle</a></li>
                        <li style="margin-bottom: 5px;"><a href="/sitemap.xml" style="color: #617085; text-decoration: none;">🔗Sitemap</a></li>
                        <li style="margin-bottom: 5px;"><a href="/llms.txt" style="color: #617085; text-decoration: none;">⚙️LLMs.txt</a></li>
                        <li style="margin-bottom: 5px;"><a href="/backlink" style="color: #617085; text-decoration: none;">♻️ Backlink</a></li>                    

                    </ul>
                </div>
            </div>
            <div style="text-align: center; font-size: 12px; color: #65676b;">
                <p style="margin-bottom: 8px;">Takip Edin: <a href="https://x.com/nearadin2026" target="_blank" rel="nofollow" style="color: #1877f2; text-decoration: none; font-weight: bold;">@nearadin2026 (X / Twitter)</a></p>
                <p>© 2026 nearadin.net - Tüm Hakları Saklıdır.</p>
            </div>
        </div>
    </footer>
    '''

import urllib.request
import os

# Sisteme başvuran/eklenen sitelerin listesi
BACKLINK_SITES = [
    {"name": "Teknoloji Blogu", "url": "https://ornek-site1.com"},
    {"name": "Haber Portalı", "url": "https://ornek-site2.com"}
]

def verify_and_generate_backlinks(header_html, footer_html):
    """Karşı sitede nearadin.net linki var mı kontrol eder, varsa backlink.html sayfasına ekler."""
    os.makedirs("backlink", exist_ok=True)
    verified_links_html = ""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for site in BACKLINK_SITES:
        try:
            # Karşı sitenin kodunu çek
            req = urllib.request.Request(site["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                page_html = response.read().decode('utf-8', errors='ignore')
                
                # Sitede nearadin.net adresi geçiyor mu kontrol et
                if "nearadin.net" in page_html:
                    verified_links_html += f'''
                    <li style="background: white; padding: 12px 16px; margin-bottom: 10px; border-radius: 6px; border: 1px solid #e4e6eb; display: flex; justify-content: space-between; align-items: center;">
                        <a href="{site['url']}" target="_blank" rel="nofollow sponsored" style="font-weight: bold; color: #0056b3; text-decoration: none;">🔗 {site['name']}</a>
                        <span style="color: #28a745; font-size: 12px; font-weight: bold;">✅ Doğrulandı</span>
                    </li>'''
        except Exception as e:
            print(f"{site['url']} kontrol edilirken hata oluştu: {e}")

    if not verified_links_html:
        verified_links_html = "<p style='color: #65676b;'>Henüz doğrulanmış bir backlink ortaklığı bulunmuyor.</p>"

    # backlink/index.html sayfa yapısı
    backlink_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backlink Ortakları - nearadin.net</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; border: 1px solid #e4e6eb; margin-bottom: 20px; }}
        h1 {{ font-size: 20px; color: #0056b3; margin-bottom: 10px; }}
        code {{ background: #f0f2f5; padding: 8px; display: block; border-radius: 4px; font-size: 12px; margin: 10px 0; word-break: break-all; }}
        ul {{ list-style: none; padding: 0; }}
    </style>
</head>
<body>
    {header_html}
    <div class="container">
        <div class="card">
            <h1>🤝 Otomatik Backlink Ağı</h1>
            <p style="font-size: 14px; color: #65676b;">Sitenize aşağıdaki kodu ekleyin, sistemimiz otomatik doğruladıktan sonra siteniz bu listede yer alsın:</p>
            <code>&lt;a href="https://nearadin.net" target="_blank"&gt;nearadin.net - Son Dakika Haberler&lt;/a&gt;</code>
        </div>

        <h2 style="font-size: 16px; margin-bottom: 12px;">Destekleyen Siteler</h2>
        <ul>
            {verified_links_html}
        </ul>
    </div>
    {footer_html}
</body>
</html>'''
  
    with open("backlink/index.html", "w", encoding="utf-8") as f:
        f.write(backlink_page_html)


def generate_weather_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """hava-durumu/index.html Sayfasını Otomatik Oluşturur"""
    os.makedirs("hava-durumu", exist_ok=True)

    weather_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7 Günlük Hava Durumu Tahmini - nearadin.net</title>
    <meta name="description" content="Türkiye'nin 81 ili için güncel 7 günlük detaylı hava durumu tahminleri." />
    <link rel="canonical" href="https://nearadin.net/hava-durumu/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 20px; margin-bottom: 10px; color: #0056b3; }}
        p {{ color: #65676b; font-size: 14px; margin-bottom: 15px; }}

        /* İl Seçim Alanı */
        .city-select-box {{ margin-bottom: 20px; }}
        .city-select-box label {{ display: block; font-weight: bold; font-size: 14px; margin-bottom: 6px; color: #333; }}
        .city-select-box select {{ width: 100%; max-width: 300px; padding: 10px; border-radius: 6px; border: 1px solid #ccd0d5; font-size: 14px; background: #fff; outline: none; cursor: pointer; }}

        /* Hava Durumu Liste Stilleri */
        .weather-list {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .weather-item {{ background: #f9f9f9; border: 1px solid #e4e6eb; padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
        .weather-date {{ font-weight: bold; color: #333; font-size: 14px; }}
        .weather-desc {{ font-size: 13px; color: #65676b; }}
        .weather-temp {{ font-weight: bold; font-size: 15px; color: #0056b3; }}

        .loading {{ text-align: center; color: #65676b; padding: 20px; font-style: italic; }}
        .btn-home {{ display: inline-block; background: #1877f2; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 20px; }}
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
        <div class="card">
            <h1>☀️ 7 Günlük Hava Durumu</h1>
            <p>İlini seçerek önümüzdeki 7 günlük sıcaklık ve hava tahmin raporunu hemen incele.</p>
            
            <!-- İl Seçim Menüsü -->
            <div class="city-select-box">
                <label for="citySelect">İl Seçiniz:</label>
                <select id="citySelect" onchange="getWeatherData()">
                    <option value="34|41.0082|28.9784" selected>34 - İstanbul</option>
                    <option value="1|37.0000|35.3213">01 - Adana</option>
                    <option value="2|37.7648|38.2786">02 - Adıyaman</option>
                    <option value="3|38.7507|30.5567">03 - Afyonkarahisar</option>
                    <option value="4|39.7191|43.0503">04 - Ağrı</option>
                    <option value="5|40.6547|35.8356">05 - Amasya</option>
                    <option value="6|39.9208|32.8541">06 - Ankara</option>
                    <option value="7|36.8969|30.7133">07 - Antalya</option>
                    <option value="8|41.1828|41.8183">08 - Artvin</option>
                    <option value="9|37.8481|27.8446">09 - Aydın</option>
                    <option value="10|39.6484|27.8826">10 - Balıkesir</option>
                    <option value="11|40.1418|30.0609">11 - Bilecik</option>
                    <option value="12|38.8856|40.4980">12 - Bingöl</option>
                    <option value="13|38.4004|42.1095">13 - Bitlis</option>
                    <option value="14|40.7359|31.6061">14 - Bolu</option>
                    <option value="15|37.7214|30.2874">15 - Burdur</option>
                    <option value="16|40.1826|29.0665">16 - Bursa</option>
                    <option value="17|40.1553|26.4142">17 - Çanakkale</option>
                    <option value="18|40.6013|33.6134">18 - Çankırı</option>
                    <option value="19|40.5506|34.9556">19 - Çorum</option>
                    <option value="20|37.7765|29.0864">20 - Denizli</option>
                    <option value="21|37.9144|40.2306">21 - Diyarbakır</option>
                    <option value="22|41.6771|26.5557">22 - Edirne</option>
                    <option value="23|38.6810|39.2264">23 - Elazığ</option>
                    <option value="24|39.7500|39.5000">24 - Erzincan</option>
                    <option value="25|39.9043|41.2679">25 - Erzurum</option>
                    <option value="26|39.7767|30.5206">26 - Eskişehir</option>
                    <option value="27|37.0662|37.3833">27 - Gaziantep</option>
                    <option value="28|40.9128|38.3895">28 - Giresun</option>
                    <option value="29|40.4386|39.5086">29 - Gümüşhane</option>
                    <option value="30|37.5833|43.7333">30 - Hakkari</option>
                    <option value="31|36.2023|36.1606">31 - Hatay</option>
                    <option value="32|37.7648|30.5566">32 - Isparta</option>
                    <option value="33|36.8000|34.6333">33 - Mersin</option>
                    <option value="35|38.4192|27.1287">35 - İzmir</option>
                    <option value="36|40.6017|43.0975">36 - Kars</option>
                    <option value="37|41.3887|33.7827">37 - Kastamonu</option>
                    <option value="38|38.7312|35.4787">38 - Kayseri</option>
                    <option value="39|41.7333|27.2167">39 - Kırklareli</option>
                    <option value="40|39.1425|34.1709">40 - Kırşehir</option>
                    <option value="41|40.7654|29.9408">41 - Kocaeli</option>
                    <option value="42|37.8667|32.4833">42 - Konya</option>
                    <option value="43|39.4167|29.9833">43 - Kütahya</option>
                    <option value="44|38.3552|38.3095">44 - Malatya</option>
                    <option value="45|38.6191|27.4289">45 - Manisa</option>
                    <option value="46|37.5858|36.9371">46 - Kahramanmaraş</option>
                    <option value="47|37.3211|40.7245">47 - Mardin</option>
                    <option value="48|37.2153|28.3636">48 - Muğla</option>
                    <option value="49|38.7437|41.5064">49 - Muş</option>
                    <option value="50|38.6244|34.7231">50 - Nevşehir</option>
                    <option value="51|37.9659|34.6850">51 - Niğde</option>
                    <option value="52|40.9839|37.8764">52 - Ordu</option>
                    <option value="53|41.0201|40.5234">53 - Rize</option>
                    <option value="54|40.7569|30.3783">54 - Sakarya</option>
                    <option value="55|41.2867|36.3300">55 - Samsun</option>
                    <option value="56|37.9333|41.9500">56 - Siirt</option>
                    <option value="57|42.0231|35.1531">57 - Sinop</option>
                    <option value="58|39.7477|37.0179">58 - Sivas</option>
                    <option value="59|40.9833|27.5167">59 - Tekirdağ</option>
                    <option value="60|40.3167|36.5500">60 - Tokat</option>
                    <option value="61|41.0015|39.7178">61 - Trabzon</option>
                    <option value="62|39.1079|39.5401">62 - Tunceli</option>
                    <option value="63|37.1591|38.7969">63 - Şanlıurfa</option>
                    <option value="64|38.4122|29.4077">64 - Uşak</option>
                    <option value="65|38.5028|43.3730">65 - Van</option>
                    <option value="66|39.8181|34.8147">66 - Yozgat</option>
                    <option value="67|41.4564|31.7987">67 - Zonguldak</option>
                    <option value="68|38.3687|34.0370">68 - Aksaray</option>
                    <option value="69|40.2551|40.2249">69 - Bayburt</option>
                    <option value="70|37.1759|33.2287">70 - Karaman</option>
                    <option value="71|41.8486|33.7753">71 - Kırıkkale</option>
                    <option value="72|37.8812|41.1285">72 - Batman</option>
                    <option value="73|37.5205|42.4598">73 - Şırnak</option>
                    <option value="74|41.6344|32.3375">74 - Bartın</option>
                    <option value="75|41.1126|42.7020">75 - Ardahan</option>
                    <option value="76|39.9167|44.0500">76 - Iğdır</option>
                    <option value="77|40.6500|29.4000">77 - Yalova</option>
                    <option value="78|41.2061|32.6204">78 - Karabük</option>
                    <option value="79|36.7184|37.1212">79 - Kilis</option>
                    <option value="80|37.0742|36.1753">80 - Osmaniye</option>
                    <option value="81|40.8438|31.1565">81 - Düzce</option>
                </select>
            </div>

            <div id="loading" class="loading">Hava durumu verileri yükleniyor...</div>
            <div id="weatherList" class="weather-list"></div>

            <a href="/" class="btn-home">← Anasayfaya Dön</a>
        </div>

        {whos_amung_us_code}
    </div>

    <script>
        function getWeatherDescription(code) {{
            const descriptions = {{
                0: "🌞 Açık / Güneşli",
                1: "🌤️ Çoğunlukla Açık",
                2: "⛅ Parçalı Bulutlu",
                3: "☁️ Çok Bulutlu",
                45: "🌫️ Sisli",
                48: "🌫️ Kırağılı Sis",
                51: "🌧️ Hafif Çisenti",
                53: "🌧️ Çisenti",
                55: "🌧️ Yoğun Çisenti",
                61: "🌧️ Hafif Yağmurlu",
                63: "🌧️ Yağmurlu",
                65: "🌧️ Şiddetli Yağmur",
                71: "❄️ Hafif Karlı",
                73: "❄️ Karlı",
                75: "❄️ Yoğun Kar Yağışlı",
                95: "⚡ Gök Gürültülü Fırtına"
            }};
            return descriptions[code] || "🌤️ Parçalı Bulutlu";
        }}

        async function getWeatherData() {{
            const selectEl = document.getElementById('citySelect');
            const val = selectEl.value.split('|');
            const lat = val[1];
            const lon = val[2];

            const loadingEl = document.getElementById('loading');
            const listEl = document.getElementById('weatherList');
            
            loadingEl.style.display = 'block';
            listEl.innerHTML = '';

            try {{
                const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto`);
                const data = await response.json();

                loadingEl.style.display = 'none';

                if (data && data.daily) {{
                    const times = data.daily.time;
                    const maxTemps = data.daily.temperature_2m_max;
                    const minTemps = data.daily.temperature_2m_min;
                    const weatherCodes = data.daily.weathercode;

                    for (let i = 0; i < 10; i++) {{
                        const dateObj = new Date(times[i]);
                        const options = {{ weekday: 'long', day: 'numeric', month: 'long' }};
                        const formattedDate = dateObj.toLocaleDateString('tr-TR', options);
                        
                        const desc = getWeatherDescription(weatherCodes[i]);
                        const maxT = Math.round(maxTemps[i]);
                        const minT = Math.round(minTemps[i]);

                        const item = document.createElement('div');
                        item.className = 'weather-item';
                        item.innerHTML = `
                            <div>
                                <div class="weather-date">${{formattedDate}}</div>
                                <div class="weather-desc">${{desc}}</div>
                            </div>
                            <div class="weather-temp">${{maxT}}°C / <span style="color:#65676b; font-weight:normal;">${{minT}}°C</span></div>
                        `;
                        listEl.appendChild(item);
                    }}
                }} else {{
                    loadingEl.style.display = 'block';
                    loadingEl.innerText = 'Hava durumu bilgisi alınamadı.';
                }}
            }} catch (error) {{
                loadingEl.style.display = 'block';
                loadingEl.innerText = 'Bağlantı hatası oluştu.';
            }}
        }}

        getWeatherData();
    </script>

    {footer_html}

</body>
</html>'''

    with open("hava-durumu/index.html", "w", encoding="utf-8") as f:
        f.write(weather_html)


def fetch_and_generate():
    rss_url = "https://news.google.com/rss/search?q=son+dakika&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    os.makedirs("haber", exist_ok=True)
    os.makedirs("arsiv", exist_ok=True)

    whos_amung_us_code = '''
    <div style="text-align: center; margin: 20px 0;">
        <script id="_wauelp">var _wau = _wau || []; _wau.push(["dynamic", "tgui40zwet", "elp", "c4302bffffff", "small"]);</script><script async src="//waust.at/d.js"></script>
    </div>
    '''

    footer_html = get_footer_html()
    header_html = get_header_html("nearadin.net - SON DAKİKA")
    
    admatic_code = '''
   <div class="ad-container">
      <!-- Admatic AUTO ads START -->
       <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
        <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
       <!-- Admatic AUTO ads END -->
   </div>
    '''

    # Hava Durumu sayfasını dinamik olarak oluştur
    generate_weather_page(
        header_html=get_header_html("nearadin.net - Hava Durumu"),
        footer_html=footer_html,
        whos_amung_us_code=whos_amung_us_code,
        admatic_code=admatic_code
    )

    
    # Backlink sayfasını oluştur (YENİ EKLENEN SATIR)
    verify_and_generate_backlinks(
        header_html, footer_html)

    try:
        req = urllib.request.Request(rss_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        raw_items = root.findall('./channel/item')

        tz_tr = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")
        last_update_iso = datetime.datetime.now(tz_tr).strftime("%Y-%m-%dT%H:%M:%S+03:00")

        parsed_items = []

        for item in raw_items:
            pub_date_raw = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            pub_datetime = None
            if pub_date_raw:
                try:
                    pub_datetime = parsedate_to_datetime(pub_date_raw)
                except Exception:
                    pub_datetime = now

            if pub_datetime and (now - pub_datetime.astimezone(datetime.timezone.utc)).total_seconds() <= 86400:
                parsed_items.append({
                    'item': item,
                    'pub_datetime': pub_datetime,
                    'pub_date_raw': pub_date_raw
                })

        parsed_items.sort(key=lambda x: x['pub_datetime'], reverse=True)
        parsed_items = parsed_items[:500]

        news_list = []
        daily_news_grouped = {}

        for idx, entry in enumerate(parsed_items):
            item = entry['item']
            pub_datetime = entry['pub_datetime']

            title = item.find('title').text if item.find('title') is not None else 'Başlıksız'
            original_link = item.find('link').text if item.find('link') is not None else '#'
            
            raw_desc = item.find('description').text if item.find('description') is not None else ''
            clean_desc = re.sub('<[^<]+?>', '', raw_desc)
            clean_desc = html.unescape(clean_desc)
            clean_title = html.unescape(title)

            source_name = "Canlı Haber Akışı"
            if " - " in clean_title:
                parts = clean_title.rsplit(" - ", 1)
                clean_title = parts[0]
                source_name = parts[1]

            dt_tr = pub_datetime.astimezone(tz_tr)
            time_str = dt_tr.strftime("%H:%M")
            date_folder = dt_tr.strftime("%Y/%m/%d")
            date_str = dt_tr.strftime("%d.%m.%Y")
            
            os.makedirs(f"haber/{date_folder}", exist_ok=True)

            slug = slugify(clean_title[:60])
            page_name = f"{slug}.html"
            internal_link = f"/haber/{date_folder}/{page_name}"
            full_url = f"https://nearadin.net{internal_link}"

            news_data = {
                "idx": idx,
                "title": clean_title,
                "original_link": original_link,
                "desc": clean_desc,
                "source": source_name,
                "time": time_str,
                "date_str": date_str,
                "date_folder": date_folder,
                "page_name": page_name,
                "internal_link": internal_link,
                "full_url": full_url,
                "iso_date": dt_tr.strftime("%Y-%m-%dT%H:%M:%S+03:00")
            }

            news_list.append(news_data)

            if date_folder not in daily_news_grouped:
                daily_news_grouped[date_folder] = {
                    "date_str": date_str,
                    "news_items": []
                }
            daily_news_grouped[date_folder]["news_items"].append(news_data)

        news_cards_html = ""

        for news in news_list:
            other_news_html = ""
            other_count = 0
            for other_news in news_list:
                if other_news["idx"] != news["idx"] and other_count < 5:
                    other_news_html += f'''
                    <li style="margin-bottom: 10px;">
                        <a href="{other_news['internal_link']}" style="color: #050505; text-decoration: none; font-weight: 600; font-size: 14px; display: block; line-height: 1.3;">
                            • {other_news['title']}
                        </a>
                        <span style="font-size: 11px; color: #65676b;">{other_news['source']} - {other_news['time']}</span>
                    </li>'''
                    other_count += 1

            # Haber Detay Sayfası
            detail_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{news['title']} - nearadin.net</title>
    <meta name="description" content="{news['desc'][:150]}..." />
    <link rel="canonical" href="{news['full_url']}" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{news['title']}" />
    <meta name="twitter:description" content="{news['desc'][:150]}..." />
    <meta name="twitter:site" content="@nearadin2026" />
    <meta name="twitter:image" content="https://nearadin.net/P5xJ5K5J_400x400.jpg" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{news['title']}" />
    <meta property="og:description" content="{news['desc'][:150]}..." />
    <meta property="og:url" content="{news['full_url']}" />
    <meta property="og:image" content="https://nearadin.net/1786394487303.png" />

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": "{news['title']}",
      "description": "{news['desc'][:150]}...",
      "datePublished": "{news['iso_date']}",
      "dateModified": "{news['iso_date']}",
      "mainEntityOfPage": "{news['full_url']}",
      "author": {{
        "@type": "Organization",
        "name": "{news['source']}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "nearadin.net",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://nearadin.net/1786394487303.png"
        }}
      }}
    }}
    </script>

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto 0 auto; padding: 0 12px; }}
        .article-card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .meta-info {{ display: flex; gap: 10px; font-size: 13px; color: #65676b; margin-bottom: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        h1 {{ font-size: 22px; margin-bottom: 15px; color: #050505; line-height: 1.3; }}
        p {{ font-size: 15px; color: #333; margin-bottom: 20px; line-height: 1.6; }}
        .actions {{ display: flex; flex-direction: column; gap: 10px; margin-top: 25px; margin-bottom: 25px; }}
        .btn {{ display: block; text-align: center; padding: 12px; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 14px; }}
        .btn-primary {{ background: #1877f2; color: white; }}
        .btn-secondary {{ background: #e4e6eb; color: #050505; }}
        .ad-container {{ margin: 0 0 12px 0; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
        .related-news {{ background: #f7f8fa; border-radius: 8px; padding: 15px; border: 1px solid #e4e6eb; margin-top: 20px; }}
        .related-title {{ font-size: 16px; font-weight: 700; margin-bottom: 12px; color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 5px; }}
        .related-list {{ list-style: none; }}
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
        <article class="article-card">
            <div class="meta-info">
                <span class="badge">SON DAKİKA</span>
                <span>Tarih: <strong>{news['date_str']} - {news['time']}</strong></span>
                <span>Kaynak: <strong>{news['source']}</strong></span>
            </div>
            <h1>{news['title']}</h1>
            <p>{news['desc']}</p>
            
            <div class="actions">
                <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku ↗</a>
                <a href="/haber/{news['date_folder']}/" class="btn btn-secondary">← {news['date_str']} Tarihli Tüm Haberlere Dön</a>
            </div>

            <div class="related-news">
                <div class="related-title">🔥 Diğer Son Dakika Gelişmeleri</div>
                <ul class="related-list">
                    {other_news_html}
                </ul>
            </div>

            {whos_amung_us_code}
        </article>
    </div>

    {footer_html}
</body>
</html>'''

            file_path = f"haber/{news['date_folder']}/{news['page_name']}"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(detail_html)

            news_cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <span class="badge">SON DAKİKA</span>
                    <span class="source">{news['source']}</span>
                    <span class="time">{news['time']}</span>
                </div>
                <h2 class="news-title">
                    <a href="{news['internal_link']}">{news['title']}</a>
                </h2>
                <p class="news-summary">{news['desc']}</p>
                <div class="card-footer">
                    <a href="{news['internal_link']}" class="read-btn">Detayı Oku →</a>
                </div>
            </article>
            '''

            if news["idx"] == 1:
                news_cards_html += admatic_code

        # --- HER GÜN İÇİN ÖZEL GÜNLÜK İNDEKS SAYFASI (BİRİKMİŞ VERİ YAPISI) ---
        import json

        for folder_path, group_data in daily_news_grouped.items():
            json_path = f"haber/{folder_path}/news.json"
            accumulated_news = []

            # 1. O güne ait önceden birikmiş haberler varsa JSON'dan oku
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as jf:
                        accumulated_news = json.load(jf)
                except Exception:
                    accumulated_news = []

            # 2. RSS'ten yeni gelen haberleri mükerrer olmayacak şekilde listeye ekle
            existing_urls = {item['full_url'] for item in accumulated_news}
            for new_item in group_data["news_items"]:
                if new_item['full_url'] not in existing_urls:
                    accumulated_news.append(new_item)
                    existing_urls.add(new_item['full_url'])

            # 3. Haberleri saat sırasına göre diz (en yeni en üstte)
            accumulated_news.sort(key=lambda x: x['time'], reverse=True)

            # 4. Güncellenmiş birikmiş haber listesini JSON olarak sakla
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(accumulated_news, jf, ensure_ascii=False, indent=2)

            # 5. İndeks HTML sayfasını o gün biriken TÜM haberlerle oluştur
            day_cards_html = ""
            for idx, d_news in enumerate(accumulated_news):
                day_cards_html += f'''
                <article class="news-card">
                    <div class="card-header">
                        <span class="badge">SON DAKİKA</span>
                        <span class="source">{d_news['source']}</span>
                        <span class="time">{d_news['time']}</span>
                    </div>
                    <h2 class="news-title">
                        <a href="{d_news['internal_link']}">{d_news['title']}</a>
                    </h2>
                    <p class="news-summary">{d_news['desc']}</p>
                    <div class="card-footer">
                        <a href="{d_news['internal_link']}" class="read-btn">Detayı Oku →</a>
                    </div>
                </article>
                '''
                if idx == 1:
                    day_cards_html += admatic_code

            daily_index_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{group_data['date_str']} Tarihli Son Dakika Haberleri - nearadin.net</title>
    <meta name="description" content="{group_data['date_str']} gününe ait tüm son dakika haberleri ve gelişmeleri akışı." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 12px 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold; color: #0056b3; border: 1px solid #e4e6eb; display: flex; justify-content: space-between; align-items: center; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        .time {{ color: #8d949e; margin-left: auto; }}
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 8px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-summary {{ font-size: 13px; color: #4b4f56; line-height: 1.4; margin-bottom: 12px; }}
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>
    {header_html}
    <div class="container">
        <div class="status-bar">
            <span>📅 {group_data['date_str']} Tarihli Haber Listesi ({len(accumulated_news)} Haber)</span>
            <a href="/arsiv/" style="color: #1877f2; text-decoration: none; font-size: 12px;">← Tüm Arşiv</a>
        </div>
        <main>
            {day_cards_html}
        </main>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''
            with open(f"haber/{folder_path}/index.html", "w", encoding="utf-8") as f:
                f.write(daily_index_html)


        # Anasayfa (index.html)
        full_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nearadin.net - Son Dakika Haberleri ve Canlı Akış</title>
    <meta name="description" content="Türkiye ve dünyadan son dakika haberleri, güncel gelişmeler ve canlı haber akışı." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}

        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; margin-top: 10px; }}
        
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: transform 0.1s ease; }}
        .news-card:active {{ transform: scale(0.99); }}
        
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        .time {{ color: #8d949e; margin-left: auto; }}
        
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 8px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-title a:hover {{ color: #1877f2; }}

        .news-summary {{ font-size: 13px; color: #4b4f56; line-height: 1.4; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}

        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>

    <!-- Admatic AUTO ads START -->
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    <!-- Admatic AUTO ads END -->

    {header_html}

    <div class="container">
        <div class="status-bar">
            <span>Kaynak: <strong>Google Canlı Akış</strong></span>
            <span>Son Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <main>
            {news_cards_html}
        </main>

        {whos_amung_us_code}
    </div>

    {footer_html}

</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)

        # XML Sitemap & Arşiv Yapısı
        sitemap_items = f'''  <url>
    <loc>https://nearadin.net/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>1.0</priority>
  </url>
      <url>
    <loc>https://nearadin.net/llms.txt</loc>
    <changefreq>daily</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>https://nearadin.net/canli-mac-sonuclari/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nearadin.net/search.html</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://nearadin.net/arsiv/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nearadin.net/film-izle/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nearadin.net/hava-durumu/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>\n'''

                # XML Sitemap & Arşiv Yapısı
        archive_dates_dict = {}

        if os.path.exists("haber"):
            for root_dir, dirs, files in os.walk("haber"):
                for file_name in files:
                    if file_name.endswith(".html"):
                        rel_path = os.path.relpath(os.path.join(root_dir, file_name), "haber")
                        clean_rel_path = rel_path.replace("\\", "/")
                        
                        # 1. Günlük index.html sayfalarını haber URL'i olarak ekleme
                        if file_name == "index.html":
                            continue
                            
                        page_url = f"https://nearadin.net/haber/{clean_rel_path}"
                        
                        sitemap_items += f'''  <url>
    <loc>{page_url}</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>\n'''
                        
                        path_parts = clean_rel_path.split('/')
                        if len(path_parts) >= 3:
                            year, month, day = path_parts[0], path_parts[1], path_parts[2]
                            
                            # 2. Doğru sıralama için key: YYYY/MM/DD, value: (GG.AA.YYYY, Link)
                            sort_key = f"{year}/{month}/{day}"
                            d_str = f"{day}.{month}.{year}"
                            folder_link = f"/haber/{year}/{month}/{day}/"
                            
                            archive_dates_dict[sort_key] = (d_str, folder_link)

        # Ana Arşiv Sayfası (arsiv/index.html) - YYYY/MM/DD formatına göre doğru sıralama
        archive_list_html = ""
        for sort_key in sorted(archive_dates_dict.keys(), reverse=True):
            d_str, folder_link = archive_dates_dict[sort_key]
            archive_list_html += f'''
            <li style="background: white; padding: 14px 16px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                <a href="{folder_link}" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: inherit;">
                    <span style="font-weight: 600; color: #333; font-size: 15px;">📅 {d_str} Tarihli Tüm Haberler</span>
                    <span style="font-size: 13px; color: #1877f2; font-weight: bold;">Tüm Liste →</span>
                </a>
            </li>'''


        archive_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haber Arşivi - nearadin.net</title>
    <meta name="description" content="nearadin.net gün bazlı geçmiş son dakika haber arşivleri." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        h1 {{ font-size: 20px; margin-bottom: 15px; color: #0056b3; }}
        ul {{ list-style: none; }}
    </style>
</head>
<body>

    <!-- Admatic AUTO ads START -->
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    <!-- Admatic AUTO ads END -->

    {header_html}
    <div class="container">
        <h1>Gün Bazlı Haber Arşivi</h1>
        <ul>
            {archive_list_html if archive_list_html else '<p>Henüz arşivlenmiş gün bulunmuyor.</p>'}
        </ul>
    </div>
    {footer_html}
</body>
</html>'''

        with open("arsiv/index.html", "w", encoding="utf-8") as f:
            f.write(archive_page_html)

        sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}</urlset>'''

        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap_content)

        # --- GOOGLE NEWS SITEMAP (news-sitemap.xml) ---
        news_sitemap_items = ""
        for news in news_list:
            safe_title = html.escape(news['title'])
            news_sitemap_items += f'''  <url>
    <loc>{news['full_url']}</loc>
    <news:news>
      <news:publication>
        <news:name>nearadin.net</news:name>
        <news:language>tr</news:language>
      </news:publication>
      <news:publication_date>{news['iso_date']}</news:publication_date>
      <news:title>{safe_title}</news:title>
    </news:news>
  </url>\n'''

        news_sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{news_sitemap_items}</urlset>'''

        with open("news-sitemap.xml", "w", encoding="utf-8") as f:
            f.write(news_sitemap_content)

        print("Betik başarıyla çalıştı. Canlı Maç Sonuçları, Hava Durumu, Film-izle, Arama (search.html), sitemap.xml ve news-sitemap.xml güncellendi.")

        if news_list:
            post_to_x(news_list[0])

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    fetch_and_generate()
