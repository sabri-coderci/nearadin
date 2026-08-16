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
    '''

def generate_live_scores_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    os.makedirs("canli-mac-sonuclari", exist_ok=True)
    scores_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canlı Maç Sonuçları ve Anlık Skor Takibi - nearadin.net</title>
    <meta name="description" content="Süper Lig, UEFA Şampiyonlar Ligi, Avrupa ligleri ve dünya genelindeki tüm futbol maçlarının canlı skorları, anlık sonuçları ve maç takvimi nearadin.net'te!" />
    <link rel="canonical" href="https://nearadin.net/canli-mac-sonuclari/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 75vh; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        h1 {{ font-size: 20px; margin-bottom: 10px; color: #0056b3; font-weight: 700; }}
        p {{ color: #65676b; font-size: 14px; margin-bottom: 15px; }}
        .hb-widget-content {{ width: 100%; min-height: 1200px; border-radius: 8px; overflow: hidden; background: #0b1220; }}
        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    {admatic_code}
    {header_html}
    <div class="container">
        <div class="card">
            <h1>⚽ Canlı Maç Sonuçları ve Anlık Skorlar</h1>
            <p>Süper Lig, UEFA Şampiyonlar Ligi, Avrupa ligleri ve dünyadan anlık canlı maç sonuçları, futbol karşılaşmaları ve güncel maç programı.</p>
            <div class="hb-widget-content">
                <script type="text/javascript" src="https://widgets.proscores.app/njs/tr/prolivewidget.js" async></script>
                <a href="https://www.macsonuclari1.net/" data-w="" title="iddaa sonuçları" style="display:block; text-align:center; padding:10px; font-size:10px; color:#ccc; text-decoration:none;">macsonuclari1.net</a>
            </div>
        </div>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

    with open("canli-mac-sonuclari/index.html", "w", encoding="utf-8") as f:
        f.write(scores_html)
    print("✅ Canlı maç sonuçları sayfası güncellendi.")

def generate_turksat_frequency_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    os.makedirs("turksat-frekans-listesi", exist_ok=True)
    turksat_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Güncel Türksat Frekans Listesi 2026 - Tüm TV Kanalları Frekans Ayarları - nearadin.net</title>
    <meta name="description" content="TRT, ATV, Kanal D, Show TV, Star TV, TV8, NOW TV ve tüm ulusal TV kanallarının güncel Türksat 4A/5B frekans listesi ve otomatik kanal arama rehberi." />
    <link rel="canonical" href="https://nearadin.net/turksat-frekans-listesi/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 850px; margin: 20px auto; padding: 0 12px; min-height: 75vh; }}
        .card {{ background: white; border-radius: 10px; padding: 25px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        h1 {{ font-size: 22px; margin-bottom: 12px; color: #0056b3; font-weight: 700; }}
        h2 {{ font-size: 18px; margin: 25px 0 12px 0; color: #1c1e21; font-weight: 600; border-bottom: 2px solid #e4e6eb; padding-bottom: 6px; }}
        p {{ color: #4b4f56; font-size: 15px; margin-bottom: 15px; line-height: 1.7; }}
        ul {{ margin: 10px 0 15px 20px; color: #4b4f56; }}
        li {{ margin-bottom: 8px; font-size: 15px; }}
        .info-box {{ background: #f0f7ff; border-left: 4px solid #0056b3; padding: 15px; border-radius: 4px; margin: 15px 0; }}
        .table-responsive {{ overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 20px 0; }}
        .freq-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; color: #333; }}
        .freq-table th {{ background-color: #0056b3; color: #ffffff; padding: 10px 12px; font-weight: 600; white-space: nowrap; }}
        .freq-table td {{ padding: 10px 12px; border-bottom: 1px solid #e4e6eb; white-space: nowrap; }}
        .freq-table tr:nth-child(even) {{ background-color: #f8f9fa; }}
        .badge-hd {{ background: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .badge-sd {{ background: #6c757d; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    {admatic_code}
    {header_html}
    <div class="container">
        <div class="card">
            <h1>📡 Güncel Türksat Frekans Listesi ve Tüm TV Kanalları</h1>
            <p>Türksat 4A ve Türksat 5B uyduları üzerinden yayın yapan ulusal ve yerel televizyon kanallarının güncel frekans bilgileri aşağıda listelenmiştir.</p>
            <h2>Tüm TV Kanallarının Güncel Frekans Tablosu</h2>
            <div class="table-responsive">
                <table class="freq-table">
                    <thead>
                        <tr><th>Kanal / Paket Adı</th><th>Yayın</th><th>Frekans</th><th>Sembol (SR)</th><th>Polarizasyon</th><th>FEC</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>TRT 1, TRT Haber, TRT Spor</strong></td><td><span class="badge-hd">HD</span></td><td>11054</td><td>30000</td><td>Dikey (V)</td><td>3/4</td></tr>
                        <tr><td><strong>ATV, A Haber, A Spor</strong></td><td><span class="badge-hd">HD</span></td><td>12053</td><td>27500</td><td>Yatay (H)</td><td>5/6</td></tr>
                        <tr><td><strong>Kanal D, CNN Türk</strong></td><td><span class="badge-hd">HD</span></td><td>12245</td><td>27500</td><td>Yatay (H)</td><td>5/6</td></tr>
                        <tr><td><strong>Show TV, Habertürk</strong></td><td><span class="badge-hd">HD</span></td><td>12209</td><td>10000</td><td>Yatay (H)</td><td>3/4</td></tr>
                        <tr><td><strong>Star TV, NTV</strong></td><td><span class="badge-hd">HD</span></td><td>12015</td><td>27500</td><td>Yatay (H)</td><td>5/6</td></tr>
                        <tr><td><strong>TV8, TV8.5</strong></td><td><span class="badge-hd">HD</span></td><td>12356</td><td>7100</td><td>Yatay (H)</td><td>2/3</td></tr>
                        <tr><td><strong>NOW TV (FOX)</strong></td><td><span class="badge-hd">HD</span></td><td>12329</td><td>6666</td><td>Yatay (H)</td><td>2/3</td></tr>
                    </tbody>
                </table>
            </div>
            <h2>Türksat Otomatik Kanal Arama Frekansı</h2>
            <div class="info-box">
                <ul>
                    <li><strong>Frekans:</strong> 12380 MHz</li>
                    <li><strong>Sembol Rate:</strong> 27500</li>
                    <li><strong>Polarizasyon:</strong> Dikey (V)</li>
                    <li><strong>Şebeke Arama:</strong> Açık</li>
                </ul>
            </div>
        </div>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

    with open("turksat-frekans-listesi/index.html", "w", encoding="utf-8") as f:
        f.write(turksat_html)
    print("✅ Türksat Frekans Listesi güncellendi.")

def generate_search_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    search_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arama Sonuçları - nearadin.net</title>
    <meta name="description" content="nearadin.net son dakika haberleri ve içerik arama sayfası." />
    <link rel="canonical" href="https://nearadin.net/search.html" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 75vh; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        h1 {{ font-size: 20px; margin-bottom: 15px; color: #0056b3; }}
        .search-form {{ display: flex; gap: 8px; margin-bottom: 20px; }}
        .search-input {{ flex: 1; padding: 10px 14px; font-size: 14px; border: 1px solid #ccd0d5; border-radius: 6px; outline: none; }}
        .search-button {{ padding: 10px 18px; background-color: #0056b3; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
        .results-header {{ font-size: 15px; font-weight: 600; border-bottom: 2px solid #e4e6eb; padding-bottom: 8px; margin-bottom: 15px; color: #333; }}
        .results-list {{ list-style: none; padding: 0; margin: 0; }}
        .result-item {{ background: #fff; border: 1px solid #e4e6eb; border-radius: 8px; padding: 14px; margin-bottom: 12px; }}
        .result-item a {{ color: #0056b3; text-decoration: none; font-size: 15px; font-weight: bold; display: block; margin-bottom: 4px; }}
        .status-message {{ text-align: center; color: #65676b; padding: 20px 0; font-style: italic; font-size: 14px; }}
    </style>
</head>
<body>
    {admatic_code}
    {header_html}
    <div class="container">
        <div class="card">
            <h1>🔍 Site İçi Arama</h1>
            <form class="search-form" method="GET" action="">
                <input type="text" name="q" id="search-input" class="search-input" placeholder="Aramak istediğiniz kelimeyi yazın..." required>
                <button type="submit" class="search-button">Ara</button>
            </form>
            <div class="results-header">Arama Sonuçları: <span id="search-keyword" style="color: #0056b3;">-</span></div>
            <div id="results-results-container" class="status-message">Lütfen yukarıdaki kutudan bir arama yapın.</div>
        </div>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''
    with open("search.html", "w", encoding="utf-8") as f:
        f.write(search_html)

def generate_weather_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    os.makedirs("hava-durumu", exist_ok=True)
    weather_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5 Günlük Hava Durumu Tahmini - nearadin.net</title>
    <meta name="description" content="Türkiye'nin 81 ili için güncel 5 günlük detaylı hava durumu tahminleri." />
    <link rel="canonical" href="https://nearadin.net/hava-durumu/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 20px; margin-bottom: 10px; color: #0056b3; }}
        p {{ color: #65676b; font-size: 14px; margin-bottom: 15px; }}
        .city-select-box select {{ width: 100%; max-width: 300px; padding: 10px; border-radius: 6px; border: 1px solid #ccd0d5; font-size: 14px; }}
        .weather-list {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .weather-item {{ background: #f9f9f9; border: 1px solid #e4e6eb; padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
    </style>
</head>
<body>
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    {admatic_code}
    {header_html}
    <div class="container">
        <div class="card">
            <h1>☀️ 5 Günlük Hava Durumu</h1>
            <p>İlini seçerek önümüzdeki 5 günlük sıcaklık ve hava tahmin raporunu hemen incele.</p>
            <div class="city-select-box">
                <select id="citySelect" onchange="getWeatherData()">
                    <option value="34|41.0082|28.9784" selected>34 - İstanbul</option>
                    <option value="6|39.9208|32.8541">06 - Ankara</option>
                    <option value="35|38.4192|27.1287">35 - İzmir</option>
                </select>
            </div>
            <div id="loading" style="text-align:center; padding:20px; color:#65676b;">Yükleniyor...</div>
            <div id="weatherList" class="weather-list"></div>
        </div>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''
    with open("hava-durumu/index.html", "w", encoding="utf-8") as f:
        f.write(weather_html)

def generate_film_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    os.makedirs("film-izle", exist_ok=True)
    film_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Türkçe Dublaj HD Film İzle - nearadin.net</title>
    <meta name="description" content="nearadin.net özel sinema portalı. En güncel Türkçe dublaj filmleri kesintisiz izleyin." />
    <link rel="canonical" href="https://nearadin.net/film-izle/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; }}
        .film-container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}
    </style>
</head>
<body>
    {admatic_code}
    {header_html}
    <div class="film-container">
        <h2>📺 Film Kuşağı</h2>
        <p>Gelişmiş sinema kataloğumuz güncelleniyor.</p>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''
    with open("film-izle/index.html", "w", encoding="utf-8") as f:
        f.write(film_html)

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
       <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
       <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
   </div>
    '''

    # Sayfaları oluştur
    generate_live_scores_page(get_header_html("nearadin.net - Canlı Maç Sonuçları"), footer_html, whos_amung_us_code, admatic_code)
    generate_film_page(get_header_html("nearadin.net - Film İzle"), footer_html, whos_amung_us_code, admatic_code)
    generate_weather_page(get_header_html("nearadin.net - Hava Durumu"), footer_html, whos_amung_us_code, admatic_code)
    generate_search_page(get_header_html("nearadin.net - Arama"), footer_html, whos_amung_us_code, admatic_code)
    generate_turksat_frequency_page(get_header_html("nearadin.net - Frekans Listesi"), footer_html, whos_amung_us_code, admatic_code)

    try:
        req = urllib.request.Request(rss_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        raw_items = root.findall('./channel/item')

        tz_tr = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")
        parsed_items = []

        for item in raw_items:
            pub_date_raw = item.find('pubDate').text if item.find('pubDate') is not None else ''
            pub_datetime = None
            if pub_date_raw:
                try:
                    pub_datetime = parsedate_to_datetime(pub_date_raw)
                except Exception:
                    pub_datetime = now

            if pub_datetime and (now - pub_datetime.astimezone(datetime.timezone.utc)).total_seconds() <= 43200:
                parsed_items.append({
                    'item': item,
                    'pub_datetime': pub_datetime,
                    'pub_date_raw': pub_date_raw
                })

        parsed_items.sort(key=lambda x: x['pub_datetime'], reverse=True)
        parsed_items = parsed_items[:50]

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

        # Haber Sayfalarını Oluşturma
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

            detail_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{news['title']} - nearadin.net</title>
    <meta name="description" content="{news['desc'][:150]}..." />
    <link rel="canonical" href="{news['full_url']}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{news['title']}" />
    <meta name="twitter:description" content="{news['desc'][:150]}..." />
    <meta name="twitter:site" content="@nearadin2026" />

    <meta property="og:type" content="article" />
    <meta property="og:title" content="{news['title']}" />
    <meta property="og:description" content="{news['desc'][:150]}..." />
    <meta property="og:url" content="{news['full_url']}" />

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
        .related-news {{ background: #f7f8fa; border-radius: 8px; padding: 15px; border: 1px solid #e4e6eb; margin-top: 20px; }}
        .related-title {{ font-size: 16px; font-weight: 700; margin-bottom: 12px; color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 5px; }}
        .related-list {{ list-style: none; }}
    </style>
</head>
<body>
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
        </article>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

            file_path = f"haber/{news['date_folder']}/{news['page_name']}"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(detail_html)

        # Anasayfa (index.html) oluşturma
        cards_html = ""
        for news in news_list:
            cards_html += f'''
            <article style="background: white; border-radius: 10px; padding: 16px; margin-bottom: 15px; border: 1px solid #e4e6eb;">
                <span style="color: #d93025; font-size: 12px; font-weight: bold;">{news['time']} - {news['source']}</span>
                <h2 style="font-size: 17px; margin: 6px 0;"><a href="{news['internal_link']}" style="color: #050505; text-decoration: none;">{news['title']}</a></h2>
                <p style="font-size: 14px; color: #4b4f56; line-height: 1.5;">{news['desc'][:120]}...</p>
            </article>'''

        index_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nearadin.net - Son Dakika Haberler</title>
    <meta name="description" content="Türkiye ve dünyadan anlık son dakika haberleri, güncel gelişmeler." />
    <link rel="canonical" href="https://nearadin.net/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; }}
    </style>
</head>
<body>
    {admatic_code}
    {header_html}
    <div class="container">
        <div style="margin-bottom: 15px; font-size: 12px; color: #65676b;">Son Güncelleme: {last_update}</div>
        {cards_html}
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_html)

        # En son haberi X üzerinde otomatik paylaş
        if news_list:
            post_to_x(news_list[0])

        print("✅ Haber akışı, tüm sayfalar ve yayınlama süreci tamamlandı.")

    except Exception as e:
        print(f"Haber çekme ve yayınlama sürecinde hata oluştu: {e}")

if __name__ == "__main__":
    fetch_and_generate()
