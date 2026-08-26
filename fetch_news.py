import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import os
import html
import json
import time
import tweepy
from email.utils import parsedate_to_datetime

# Kategori Yapılandırması ve Otomatik Kelime Eşleme Mantığı
CATEGORIES = {
    "gundem": {
        "name": "Gündem Haberleri",
        "slug": "gundem",
        "query": "son+dakika",
        "keywords": ["sondakika", "gündem", "bakan", "cumhurbaşkanı", "açıklama", "polisi", "asayiş"]
    },
    "teknoloji": {
        "name": "Teknoloji Haberleri",
        "slug": "teknoloji",
        "query": "teknoloji",
        "keywords": ["teknoloji", "yapay zeka", "ai", "google", "apple", "samsung", "iphone", "android", "yazılım", "siber", "uzay", "nasa", "chip", "mikroçip", "togg", "sosyal medya", "instagram", "whatsapp"]
    },
    "spor": {
        "name": "Spor Haberleri",
        "slug": "spor",
        "query": "spor",
        "keywords": ["spor", "futbol", "basketbol", "voleybol", "maç", "transfer", "lig", "fenerbahçe", "galatasaray", "beşiktaş", "trabzonspor", "uefa", "fifa", "gol", "şampiyon", "skor", "hakem", "derbi"]
    },
    "kultur": {
        "name": "Kültür Haberleri",
        "slug": "kultur-sanat",
        "query": "kultur+sanat",
        "keywords": ["kültür", "sanat", "sinema", "film", "tiyatro", "konser", "müzik", "sergi", "kitap", "yazar", "festival", "oyuncu", "dizi", "vizyon"]
    },
    "ekonomi": {
        "name": "Ekonomi Haberleri",
        "slug": "ekonomi",
        "query": "ekonomi",
        "keywords": ["ekonomi", "dolar", "euro", "borsa", "faiz", "enflasyon", "merkez bankası", "altın", "mevduat", "zam", "maaş", "emekli", "asgari ücret", "piyasa", "hisse", "vergi"]
    },
    "saglik": {
        "name": "Sağlık Haberleri",
        "slug": "saglik",
        "query": "saglik",
        "keywords": ["sağlık haberleri"]
    }
}

def slugify(text):
    text = text.lower()
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c',
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def detect_category(title, desc):
    """Haber başlığı ve özetine göre kategori tespiti yapar."""
    text = f"{title} {desc}".lower()
    for cat_key, cat_info in CATEGORIES.items():
        if cat_key == "gundem":
            continue
        for kw in cat_info["keywords"]:
            if kw in text:
                return cat_info["name"], cat_info["slug"]
    return CATEGORIES["gundem"]["name"], CATEGORIES["gundem"]["slug"]

def post_to_x(latest_news):
    """En son çıkan haberi X üzerinde paylaşır."""
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("❌ X API anahtarları bulunamadı. GitHub Secrets kontrol edin.")
        return

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )

        title = latest_news['title']
        url = latest_news['full_url']
        
        if len(title) > 170:
            title = title[:167] + "..."

        tweet_text = (
            f"🚨 SON DAKİKA ({latest_news['cat_name']})\n\n"
            f"📌 {title}\n\n"
            f"🔗 Detaylar:\n{url}\n\n"
            f"#{latest_news['cat_slug']} #sondakika #haber"
        )
        
        response = client.create_tweet(text=tweet_text)
        print(f"✅ X paylaşımı başarılı! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ X (Twitter) paylaşımında hata oluştu: {e}")

def get_header_html(title_text="nearadin.net - SON DAKİKA"):
    category_menu_items = ""
    for cat_key, cat in CATEGORIES.items():
        category_menu_items += f'<li style="border-bottom: 1px solid #f0f2f5;"><a href="/kategori/{cat["slug"]}/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏷️ {cat["name"]}</a></li>'

    return f'''
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
        <button id="hamburgerBtn" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 5px; outline: none;">☰</button>
        
        <nav id="dropdownNav" style="display: none; position: absolute; top: 100%; right: 0; background: white; width: 240px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 0 0 8px 8px; border: 1px solid #e4e6eb; overflow: hidden; max-height: 80vh; overflow-y: auto;">
            <ul style="list-style: none; margin: 0; padding: 0;">
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏠 Anasayfa</a></li>
                {category_menu_items}
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
    return '''
    <footer style="background-color: #1c1e21; color: #90949c; padding: 30px 15px; margin-top: 40px; font-size: 13px; line-height: 1.6; clear: both;">
        <div style="max-width: 680px; margin: 0 auto;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 20px;">
                <div style="flex: 1; min-width: 200px;">
                    <h3 style="color: #fff; font-size: 16px; margin-bottom: 10px;">nearadin.net</h3>
                    <p>Türkiye ve dünyadan en güncel son dakika haberleri, teknoloji, spor ve kültür-sanat haberleri akış platformu.</p>
                </div>
                <div style="flex: 1; min-width: 140px;">
                    <h4 style="color: #fff; font-size: 14px; margin-bottom: 10px;">Kategoriler</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 5px;"><a href="/kategori/gundem/" style="color: #617085; text-decoration: none;">Gündem</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kategori/teknoloji/" style="color: #617085; text-decoration: none;">Teknoloji</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kategori/spor/" style="color: #617085; text-decoration: none;">Spor</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kategori/kultur-sanat/" style="color: #617085; text-decoration: none;">Kültür-Sanat</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kategori/ekonomi/" style="color: #617085; text-decoration: none;">Ekonomi</a></li>
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

def fetch_and_generate():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    os.makedirs("haber", exist_ok=True)
    os.makedirs("arsiv", exist_ok=True)
    os.makedirs("kategori", exist_ok=True)

    whos_amung_us_code = '''
    <div style="text-align: center; margin: 20px 0;">
        <script id="_wauelp">var _wau = _wau || []; _wau.push(["dynamic", "tgui40zwet", "elp", "c4302bffffff", "small"]);</script><script async src="//waust.at/d.js"></script>
    </div>
    '''

    footer_html = get_footer_html()
    header_html = get_header_html("nearadin.net - Haberler")
    
    admatic_code = '''
   <div class="ad-container">
       <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
        <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
   </div>
    '''

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(datetime.timezone.utc)
    
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")
    last_update_iso = datetime.datetime.now(tz_tr).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    all_parsed_items = []
    seen_urls = set()

    # 1. Öncelik: Ana Son Dakika Akışını Çek (Anasayfa Garanti)
    main_rss_url = "https://news.google.com/rss/search?q=son+dakika&hl=tr&gl=TR&ceid=TR:tr"
    try:
        req = urllib.request.Request(main_rss_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=12)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall('./channel/item'):
            link = item.find('link').text if item.find('link') is not None else ''
            if link and link not in seen_urls:
                seen_urls.add(link)
                pub_date_raw = item.find('pubDate').text if item.find('pubDate') is not None else ''
                try:
                    pub_datetime = parsedate_to_datetime(pub_date_raw)
                except Exception:
                    pub_datetime = now
                
                all_parsed_items.append({
                    'item': item,
                    'pub_datetime': pub_datetime,
                    'forced_cat': None
                })
    except Exception as e:
        print(f"Ana RSS çekme hatası: {e}")

    # 2. Öncelik: Özel Kategori RSS'lerini Çek
    for cat_key, cat in CATEGORIES.items():
        if cat_key == "gundem": continue
        rss_url = f"https://news.google.com/rss/search?q={cat['query']}&hl=tr&gl=TR&ceid=TR:tr"
        try:
            time.sleep(0.5)
            req = urllib.request.Request(rss_url, headers=headers)
            response = urllib.request.urlopen(req, timeout=8)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            for item in root.findall('./channel/item'):
                link = item.find('link').text if item.find('link') is not None else ''
                if link and link not in seen_urls:
                    seen_urls.add(link)
                    pub_date_raw = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    try:
                        pub_datetime = parsedate_to_datetime(pub_date_raw)
                    except Exception:
                        pub_datetime = now

                    all_parsed_items.append({
                        'item': item,
                        'pub_datetime': pub_datetime,
                        'forced_cat': (cat['name'], cat['slug'])
                    })
        except Exception as e:
            print(f"Kategori RSS hatası ({cat_key}): {e}")

    all_parsed_items.sort(key=lambda x: x['pub_datetime'], reverse=True)

    news_list = []
    daily_news_grouped = {}
    category_news_grouped = {cat['slug']: [] for cat in CATEGORIES.values()}

    for idx, entry in enumerate(all_parsed_items):
        item = entry['item']
        pub_datetime = entry['pub_datetime']

        title = item.find('title').text if item.find('title') is not None else 'Başlıksız'
        original_link = item.find('link').text if item.find('link') is not None else '#'
        
        raw_desc = item.find('description').text if item.find('description') is not None else ''
        clean_desc = html.unescape(re.sub('<[^<]+?>', '', raw_desc))
        clean_title = html.unescape(title)

        source_name = "Canlı Haber Akışı"
        if " - " in clean_title:
            parts = clean_title.rsplit(" - ", 1)
            clean_title = parts[0]
            source_name = parts[1]

        # Kategori Tespiti
        if entry['forced_cat']:
            cat_name, cat_slug = entry['forced_cat']
        else:
            cat_name, cat_slug = detect_category(clean_title, clean_desc)

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
            "iso_date": dt_tr.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "cat_name": cat_name,
            "cat_slug": cat_slug
        }

        news_list.append(news_data)

        if date_folder not in daily_news_grouped:
            daily_news_grouped[date_folder] = {"date_str": date_str, "news_items": []}
        daily_news_grouped[date_folder]["news_items"].append(news_data)

        if cat_slug in category_news_grouped:
            category_news_grouped[cat_slug].append(news_data)

    # Detay Sayfalarını Üret
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
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto 0 auto; padding: 0 12px; }}
        .article-card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .meta-info {{ display: flex; gap: 10px; font-size: 13px; color: #65676b; margin-bottom: 12px; align-items: center; flex-wrap: wrap; }}
        .cat-badge {{ background: #e7f3ff; color: #1877f2; font-weight: bold; padding: 3px 8px; border-radius: 4px; font-size: 12px; text-decoration: none; }}
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
                <a href="/kategori/{news['cat_slug']}/" class="cat-badge">🏷️ {news['cat_name']}</a>
                <span>Tarih: <strong>{news['date_str']} - {news['time']}</strong></span>
                <span>Kaynak: <strong>{news['source']}</strong></span>
            </div>
            <h1>{news['title']}</h1>
            <p>{news['desc']}</p>
            
            <div class="actions">
                <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku ↗</a>
                <a href="/kategori/{news['cat_slug']}/" class="btn btn-secondary">← {news['cat_name']} Kategorisine Dön</a>
            </div>

            <div class="related-news">
                <div class="related-title">🔥 Diğer Gelişmeler</div>
                <ul class="related-list">{other_news_html}</ul>
            </div>
            {whos_amung_us_code}
        </article>
    </div>
    {footer_html}
</body>
</html>'''

        with open(f"haber/{news['date_folder']}/{news['page_name']}", "w", encoding="utf-8") as f:
            f.write(detail_html)

    # Kategori Sayfalarını Oluştur (/kategori/[slug]/index.html)
    for cat_key, cat in CATEGORIES.items():
        cat_slug = cat['slug']
        cat_dir = f"kategori/{cat_slug}"
        os.makedirs(cat_dir, exist_ok=True)

        cat_items = category_news_grouped.get(cat_slug, [])
        cat_cards_html = ""

        for idx, news in enumerate(cat_items):
            cat_cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <a href="/kategori/{news['cat_slug']}/" class="cat-link">🏷️ {news['cat_name']}</a>
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
            if idx == 1:
                cat_cards_html += admatic_code

        cat_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat['name']} - nearadin.net</title>
    <meta name="description" content="En son {cat['name'].lower()} ve güncel gelişmeler." />
    <link rel="canonical" href="https://nearadin.net/kategori/{cat_slug}/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}
        .category-header {{ background: white; border-radius: 8px; padding: 16px; margin-bottom: 15px; border: 1px solid #e4e6eb; text-align: center; }}
        .category-header h1 {{ font-size: 20px; color: #0056b3; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .cat-link {{ color: #1877f2; font-weight: bold; text-decoration: none; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        .time {{ color: #8d949e; margin-left: auto; }}
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 8px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-summary {{ font-size: 13px; color: #4b4f56; line-height: 1.4; margin-bottom: 12px; }}
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
    </style>
</head>
<body>
    {header_html}
    <div class="container">
        <div class="category-header">
            <h1>📌 {cat['name']}</h1>
            <p>Son Dakika {cat['name']} ve Öne Çıkan Gelişmeler</p>
        </div>
        <main>
            {cat_cards_html if cat_cards_html else '<p style="text-align:center; padding:20px;">Bu kategoride henüz haber bulunmuyor.</p>'}
        </main>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

        with open(f"{cat_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(cat_page_html)

    # Anasayfa (index.html) Hazırlığı
    news_cards_html = ""
    for idx, news in enumerate(news_list):
        news_cards_html += f'''
        <article class="news-card">
            <div class="card-header">
                <a href="/kategori/{news['cat_slug']}/" class="cat-link">🏷️ {news['cat_name']}</a>
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
        if idx == 1:
            news_cards_html += admatic_code

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
        .category-bar {{ display: flex; gap: 8px; overflow-x: auto; padding: 10px 0; margin-bottom: 12px; scrollbar-width: none; }}
        .category-bar::-webkit-scrollbar {{ display: none; }}
        .cat-chip {{ background: white; border: 1px solid #ccd0d5; border-radius: 20px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: #0056b3; text-decoration: none; white-space: nowrap; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }}
        .cat-chip:hover {{ background: #0056b3; color: white; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .cat-link {{ color: #1877f2; font-weight: bold; text-decoration: none; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        .time {{ color: #8d949e; margin-left: auto; }}
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 8px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-summary {{ font-size: 13px; color: #4b4f56; line-height: 1.4; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
    </style>
</head>
<body>
    {header_html}

    <div class="container">
        <!-- Yatay Kategori Çubuğu -->
        <div class="category-bar">
            <a href="/kategori/gundem/" class="cat-chip">🔴 Gündem</a>
            <a href="/kategori/teknoloji/" class="cat-chip">💻 Teknoloji</a>
            <a href="/kategori/spor/" class="cat-chip">⚽ Spor</a>
            <a href="/kategori/kultur-sanat/" class="cat-chip">🎭 Kültür-Sanat</a>
            <a href="/kategori/ekonomi/" class="cat-chip">📈 Ekonomi</a>
            <a href="/kategori/saglik/" class="cat-chip">🌡️Sağlık</a>
        </div>

        <div class="status-bar">
            <span>Kaynak: <strong>Google Canlı Akış</strong></span>
            <span>Son Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <main>{news_cards_html}</main>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # Sitemap Güncellemesi
    sitemap_items = f'''  <url><loc>https://nearadin.net/</loc><lastmod>{last_update_iso}</lastmod><priority>1.0</priority></url>\n'''
    for cat in CATEGORIES.values():
        sitemap_items += f'''  <url><loc>https://nearadin.net/kategori/{cat['slug']}/</loc><lastmod>{last_update_iso}</lastmod><priority>0.8</priority></url>\n'''

    for news in news_list:
        sitemap_items += f'''  <url><loc>{news['full_url']}</loc><lastmod>{last_update_iso}</lastmod><priority>0.6</priority></url>\n'''

    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}</urlset>'''

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print("✅ Anasayfa haber akışı ve kategori eşleşmeleri düzeltildi.")

    if news_list:
        post_to_x(news_list[0])

if __name__ == "__main__":
    fetch_and_generate()
