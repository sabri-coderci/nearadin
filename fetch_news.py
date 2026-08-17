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
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: spac[...]
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
        <button id="hamburgerBtn" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 5px; outline: none;">☰</button>
        
        <nav id="dropdownNav" style="display: none; position: absolute; top: 100%; right: 0; background: white; width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 0 0 8px 8px; b[...]
            <ul style="list-style: none; margin: 0; padding: 0;">
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏠[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/canli-mac-sonuclari/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; fo[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/arsiv/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/nobetci-eczane/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-si[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/son-depremler/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-siz[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/kripto-para/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size:[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/hava-durumu/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size:[...]
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/film-izle/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 1[...]
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
                <p style="margin-bottom: 8px;">Takip Edin: <a href="https://x.com/nearadin2026" target="_blank" rel="nofollow" style="color: #1877f2; text-decoration: none; font-weight: bold;">@n[...]
                <p>© 2026 nearadin.net - Tüm Hakları Saklıdır.</p>
            </div>
        </div>
    </footer>
    '''


def ensure_daily_indexes_from_files(header_html, footer_html, whos_amung_us_code, admatic_code):
    """
    Tarayıcı (filesystem) tabanlı günlük indexler oluşturur.
    Haber klasöründeki her `haber/YYYY/MM/DD/` dizini için eğer `index.html`
    yoksa basit bir günlük liste sayfası oluşturur. Bu, arsiv/index.html
    içindeki tarihlere tıklandığında 404/eksik sayfa oluşmasını engeller.
    """
    import os
    import re
    import datetime

    base = "haber"
    if not os.path.exists(base):
        return

    for root_dir, dirs, files in os.walk(base):
        rel = os.path.relpath(root_dir, base)
        if rel == ".":
            continue
        rel = rel.replace("\\", "/")
        parts = rel.split("/")
        if len(parts) < 3:
            continue
        year, month, day = parts[0], parts[1], parts[2]

        # Haber HTML dosyaları (index.html hariç)
        articles = [f for f in files if f.endswith(".html") and f.lower() != "index.html"]
        if not articles:
            continue

        index_path = os.path.join(root_dir, "index.html")
        # Eğer varolan index'i korumak istersen bu continue satırını tut;
        # her çalıştırmada yeniden oluşturmak istersen bu satırı kaldır.
        if os.path.exists(index_path):
            continue

        # Haberleri dosya zamanına göre tersine sırala (yeni ilk)
        articles.sort(key=lambda a: os.path.getmtime(os.path.join(root_dir, a)), reverse=True)

        day_cards_html = ""
        for a in articles:
            path = os.path.join(root_dir, a)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    content = fh.read(4096)
                m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
                title = m.group(1).split(" - nearadin.net")[0].strip() if m else a
            except Exception:
                title = a
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%H:%M")
            except Exception:
                mtime = ""
            internal_link = f"/{base}/{year}/{month}/{day}/{a}"
            day_cards_html += f'''\
                <article class="news-card">\n\
                    <div class="card-header">\n\
                        <span class="badge">SON DAKİKA</span>\n\
                        <span class="source">nearadin.net</span>\n\
                        <span class="time">{mtime}</span>\n\
                    </div>\n\
                    <h2 class="news-title">\n\
                        <a href="{internal_link}">{title}</a>\n\
                    </h2>\n\
                </article>\n'''

        daily_index_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{day}.{month}.{year} Tarihli Son Dakika Haberleri - nearadin.net</title>
  <meta name="description" content="{day}.{month}.{year} tarihli haberler." />
</head>
<body>
{header_html}
<div class="container">
    <div class="status-bar">📅 {day}.{month}.{year} Tarihli Haber Listesi</div>
    <main>{day_cards_html}</main>
    {whos_amung_us_code}
</div>
{footer_html}
</body>
</html>'''
        try:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(daily_index_html)
            print(f"Oluşturuldu/yenilendi: {index_path}")
        except Exception as e:
            print(f"index yazılamadı: {index_path} -> {e}")

import os

def generate_live_scores_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """
    fetch_news.py tarafından çalıştırılarak canli-mac-sonuclari/index.html 
    sayfasını otomatik oluşturan fonksiyon.
    """
    os.makedirs("canli-mac-sonuclari", exist_ok=True)

    scores_html = f'''<!DOCTYPE html>
 <html lang="tr">
 <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Canlı Maç Sonuçları ve Anlık Skor Takibi - nearadin.net</title>
     <meta name="description" content="Süper Lig, UEFA Şampiyonlar Ligi, Avrupa ligleri ve dünya genelindeki tüm futbol maçlarının canlı skorları, anlık sonuçları ve maç takvimi neara[...]
     <link rel="canonical" href="https://nearadin.net/canli-mac-sonuclari/" />
     <style>
         * {{ box-sizing: border-box; margin: 0; padding: 0; }}
         body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
         .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 75vh; }}
         
         .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 20px; }}
         h1 {{ font-size: 20px; margin-bottom: 10px; color: #0056b3; font-weight: 700; }}
         p {{ color: #65676b; font-size: 14px; margin-bottom: 15px; }}

         /* Yüksekliği Uzun Tutulmuş Widget Alanı */
         .hb-widget-content {{ 
             width: 100%; 
             min-height: 1200px; 
             border-radius: 8px; 
             overflow: hidden; 
             background: #0b1220;
         }}

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
             <h1>⚽ Canlı Maç Sonuçları ve Anlık Skorlar</h1>
             <p>Süper Lig, UEFA Şampiyonlar Ligi, Avrupa ligleri ve dünyadan anlık canlı maç sonuçları, futbol karşılaşmaları ve güncel maç programı.</p>
             
             <!-- ProScores Doğru Widget Yapısı -->
             <div class="hb-widget-content">
                 <script type="text/javascript" src="https://widgets.proscores.app/njs/tr/prolivewidget.js" async></script>
                 <a href="https://www.macsonuclari1.net/" data-w="" title="iddaa sonuçları" style="display:block; text-align:center; padding:10px; font-size:10px; color:#ccc; text-decoration:non[...]
             </div>
         </div>

         {whos_amung_us_code}
     </div>

     {footer_html}
 </body>
 </html>'''

    with open("canli-mac-sonuclari/index.html", "w", encoding="utf-8") as f:
        f.write(scores_html)
        
    print("✅ Canlı maç sonuçları sayfası güncellendi (Yükseklik: 1200px, ProScores Anchor eklendi).")

import os

def generate_turksat_frequency_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """
    turksat-frekans-listesi/index.html sayfasını tüm TV kanallarının 
    frekans tablosu ile SEO uyumlu olarak oluşturur.
    """
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
         .info-box strong {{ color: #0056b3; }}

         /* Mobil Uyumlu Tablo Tasarımı */
         .table-responsive {{ overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 20px 0; }}
         .freq-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; color: #333; }}
         .freq-table th {{ background-color: #0056b3; color: #ffffff; padding: 10px 12px; font-weight: 600; white-space: nowrap; }}
         .freq-table td {{ padding: 10px 12px; border-bottom: 1px solid #e4e6eb; white-space: nowrap; }}
         .freq-table tr:nth-child(even) {{ background-color: #f8f9fa; }}
         .freq-table tr:hover {{ background-color: #eef5ff; }}
         .badge-hd {{ background: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
         .badge-sd {{ background: #6c757d; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }}

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
             <h1>📡 Güncel Türksat Frekans Listesi ve Tüm TV Kanalları</h1>
             <p>Türksat 4A ve Türksat 5B uyduları üzerinden yayın yapan ulusal ve yerel televizyon kanallarının güncel frekans bilgileri aşağıda listelenmiştir. Uydu alıcınızda kana[...]
             
             <h2>Tüm TV Kanallarının Güncel Frekans Tablosu</h2>
             
             <div class="table-responsive">
                 <table class="freq-table">
                     <thead>
                         <tr>
                             <th>Kanal / Paket Adı</th>
                             <th>Yayın</th>
                             <th>Frekans</th>
                             <th>Sembol (SR)</th>
                             <th>Polarizasyon</th>
                             <th>FEC</th>
                         </tr>
                     </thead>
                     <tbody>
                         <tr>
                             <td><strong>TRT 1, TRT Haber, TRT Spor, TRT Çocuk</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>11054</td>
                             <td>30000</td>
                             <td>Dikey (V)</td>
                             <td>3/4</td>
                         </tr>
                         <tr>
                             <td><strong>ATV, A Haber, A Spor, A2, A News</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12053</td>
                             <td>27500</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>Kanal D, CNN Türk, Teve2</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12245</td>
                             <td>27500</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>Show TV, Habertürk, Bloomberg HT</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12209</td>
                             <td>10000</td>
                             <td>Yatay (H)</td>
                             <td>3/4</td>
                         </tr>
                         <tr>
                             <td><strong>Star TV, NTV, Kral POP TV</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12015</td>
                             <td>27500</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>TV8, TV8.5</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12356</td>
                             <td>7100</td>
                             <td>Yatay (H)</td>
                             <td>2/3</td>
                         </tr>
                         <tr>
                             <td><strong>NOW TV (FOX)</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12329</td>
                             <td>6666</td>
                             <td>Yatay (H)</td>
                             <td>2/3</td>
                         </tr>
                         <tr>
                             <td><strong>Kanal 7, Ülke TV</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12095</td>
                             <td>4800</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>Sözcü TV (SZC), Halk TV, Tele1, Ekol TV</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12034</td>
                             <td>27500</td>
                             <td>Dikey (V)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>Beyaz TV, TVNET</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12380</td>
                             <td>27500</td>
                             <td>Dikey (V)</td>
                             <td>3/4</td>
                         </tr>
                         <tr>
                             <td><strong>TGRT Haber, TGRT EU</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12015</td>
                             <td>27500</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                         <tr>
                             <td><strong>Flash Haber</strong></td>
                             <td><span class="badge-hd">HD</span></td>
                             <td>12685</td>
                             <td>30000</td>
                             <td>Dikey (V)</td>
                             <td>2/3</td>
                         </tr>
                         <tr>
                             <td><strong>A Spor, A Haber, Minika Çocuk</strong></td>
                             <td><span class="badge-sd">SD</span></td>
                             <td>12053</td>
                             <td>27500</td>
                             <td>Yatay (H)</td>
                             <td>5/6</td>
                         </tr>
                     </tbody>
                 </table>
             </div>

             <h2>Türksat Otomatik Kanal Arama Frekansı</h2>
             <p>Tüm kanalları tek tek girmek yerine otomatik tarama yapmak isterseniz aşağıdaki şebeke arama frekansını kullanabilirsiniz:</p>
             
             <div class="info-box">
                 <ul>
                     <li><strong>Frekans:</strong> 12380 MHz</li>
                     <li><strong>Sembol Rate:</strong> 27500</li>
                     <li><strong>Polarizasyon:</strong> Dikey (V - Vertical)</li>
                     <li><strong>Şebeke Arama (Network Search):</strong> Açık</li>
                 </ul>
             </div>

             <h2>Televizyon Kanal Frekansları Nasıl Yüklenir?</h2>
             <ul>
                 <li>Kumandanızın <strong>Menü</strong> veya <strong>Home</strong> tuşuna basın.</li>
                 <li><strong>Kurulum / Kanal Ayarları / Uydu Ayarları</strong> menüsüne gidin.</li>
                 <li><strong>Manuel Tarama</strong> veya <strong>TP Ekle</strong> seçeneğini bulun.</li>
                 <li>Yukarıdaki tabloda yer alan frekans, sembol rate ve polarizasyon değerlerini girin.</li>
                 <li>Aramayı başlatın ve bulunan kanalları kaydedin.</li>
             </ul>
         </div>

         {whos_amung_us_code}
     </div>

     {footer_html}
 </body>
 </html>'''

    with open("turksat-frekans-listesi/index.html", "w", encoding="utf-8") as f:
        f.write(turksat_html)
        
    print("✅ Türksat Frekans Listesi (Tüm kanallar tablosuyla) başarıyla güncellendi.")



def generate_search_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """search.html Sayfasını Otomatik Oluşturur"""
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
         .search-input:focus {{ border-color: #0056b3; box-shadow: 0 0 0 2px rgba(0,86,179,0.15); }}
         .search-button {{ padding: 10px 18px; background-color: #0056b3; color: white; border: none; border-radius: 6px; font-weight: bold; font-size: 14px; cursor: pointer; }}
         .search-button:hover {{ background-color: #004085; }}

         .results-header {{ font-size: 15px; font-weight: 600; border-bottom: 2px solid #e4e6eb; padding-bottom: 8px; margin-bottom: 15px; color: #333; }}
         
         .results-list {{ list-style: none; padding: 0; margin: 0; }}
         .result-item {{ background: #fff; border: 1px solid #e4e6eb; border-radius: 8px; padding: 14px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }}
         .result-item a {{ color: #0056b3; text-decoration: none; font-size: 15px; font-weight: bold; display: block; margin-bottom: 4px; line-height: 1.3; }}
         .result-item a:hover {{ text-decoration: underline; }}
         .result-item .url {{ color: #28a745; font-size: 12px; margin-bottom: 6px; word-break: break-all; }}
         .result-item p {{ color: #4b4f56; font-size: 13px; line-height: 1.5; margin: 0; }}
         
         .status-message {{ text-align: center; color: #65676b; padding: 20px 0; font-style: italic; font-size: 14px; }}
         .error-box {{ background: #fff8f7; border: 1px solid #f5c6cb; color: #721c24; padding: 18px; border-radius: 8px; text-align: center; font-size: 14px; margin-top: 10px; }}
         .fallback-btn {{ display: inline-block; margin-top: 12px; background: #1877f2; color: white; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1[...]
         .fallback-btn:hover {{ background: #0056b3; }}

         .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
         .ad-container:empty {{ display: none !important; }}
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

     <script>
         const urlParams = new URLSearchParams(window.location.search);
         const query = urlParams.get('q');

         const API_KEY = "AIzaSyDrJkl3V_vW3b0vmI_hlJbmJM2bhFCYQek";
         const SEARCH_ENGINE_ID = "a33464712b4234607";

         function escapeHtml(str) {{
             if (!str) return '';
             return str.replace(/[&<>'"]/g, 
                 tag => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }}[tag] || tag)
             );
         }}

         function sanitizeUrl(url) {{
             try {{
                 const parsed = new URL(url);
                 if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {{
                     return parsed.href;
                 }}
             }} catch (e) {{}}
             return '#';
         }}

         if (query) {{
             document.getElementById('search-input').value = query;
             document.getElementById('search-keyword').innerText = query;
             
             const container = document.getElementById('results-results-container');
             container.innerText = "Arama sonuçları getiriliyor...";

             const apiUrl = 'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' + SEARCH_ENGINE_ID + '&q=' + encodeURIComponent(query);

             fetch(apiUrl)
                 .then(response => {{
                     if (!response.ok) throw new Error('API kotası veya bağlantı hatası.');
                     return response.json();
                 }})
                 .then(data => {{
                     if (!data.items || data.items.length === 0) {{
                         container.className = "status-message";
                         container.innerHTML = "Aradığınız kriterlere uygun haber veya içerik bulunamadı.";
                         return;
                     }}

                     let html = '<ul class="results-list">';
                     data.items.forEach(function(item) {{
                         var safeLink = sanitizeUrl(item.link);
                         var title = escapeHtml(item.title);
                         var snippet = escapeHtml(item.snippet || '');
                         html += '<li class="result-item">' +
                                     '<a href="' + safeLink + '" target="_blank" rel="noopener noreferrer">' + title + '</a>' +
                                     '<div class="url">' + safeLink + '</div>' +
                                     '<p>' + snippet + '</p>' +
                                 '</li>';
                     }});
                     html += '</ul>';
                     
                     container.className = "";
                     container.innerHTML = html;
                 }})
                 .catch(err => {{
                     console.error(err);
                     var googleFallbackUrl = 'https://www.google.com/search?q=site:nearadin.net+' + encodeURIComponent(query);
                     
                     container.className = "";
                     container.innerHTML = '<div class="error-box">' +
                         '<p><strong>Arama servisinde geçici bir yoğunluk oluştu.</strong></p>' +
                         '<p style="font-size:12px; margin-top:6px; color:#65676b;">Google API günlük ücretsiz sorgu limitine ulaşılmış olabilir.</p>' +
                         '<a href="' + googleFallbackUrl + '" target="_blank" class="fallback-btn">Google Üzerinden nearadin.net&#39;te Ara ↗</a>' +
                     '</div>';
                 }});
         }}
     </script>
 </body>
 </html>'''

   # with open("search.html", "w", encoding="utf-8") as f:
        #f.write(search_html)


def generate_weather_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """hava-durumu/index.html Sayfasını Otomatik Oluşturur"""
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

         /* İl Seçim Alanı */
         .city-select-box {{ margin-bottom: 20px; }}
         .city-select-box label {{ display: block; font-weight: bold; font-size: 14px; margin-bottom: 6px; color: #333; }}
         .city-select-box select {{ width: 100%; max-width: 300px; padding: 10px; border-radius: 6px; border: 1px solid #ccd0d5; font-size: 14px; background: #fff; outline: none; cursor: pointer; [...]

         /* Hava Durumu Liste Stilleri */
         .weather-list {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
         .weather-item {{ background: #f9f9f9; border: 1px solid #e4e6eb; padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
         .weather-date {{ font-weight: bold; color: #333; font-size: 14px; }}
         .weather-desc {{ font-size: 13px; color: #65676b; }}
         .weather-temp {{ font-weight: bold; font-size: 15px; color: #0056b3; }}

         .loading {{ text-align: center; color: #65676b; padding: 20px; font-style: italic; }}
         .btn-home {{ display: inline-block; background: #1877f2; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 20px;[...]
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
             <h1>☀️ 5 Günlük Hava Durumu</h1>
             <p>İlini seçerek önümüzdeki 5 günlük sıcaklık ve hava tahmin raporunu hemen incele.</p>
             
             <!-- İl Seçim Menüsü -->
             <div class="city-select-box">
                 <label for="citySelect">İl Seçiniz:</label>
                 <select id="citySelect" onchange="getWeatherData()">
                     <option value="34|41.0082|28.9784" selected>34 - İstanbul</option>
                     <option value="1|37.0000|35.3213">01 - Adana</option>
[...]
''',