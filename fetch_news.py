import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import os
import html
import json
import tweepy
from email.utils import parsedate_to_datetime

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


def share_on_twitter(news_list):
    """X (Twitter) Üzerinde Otomatik Paylaşım Yapan Fonksiyon"""
    API_KEY = os.getenv("X_API_KEY")
    API_SECRET = os.getenv("X_API_SECRET")
    ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("X API anahtarları eksik veya bulunamadı, X paylaşımı atlanıyor.")
        return

    TWEETED_FILE = "tweeted_news.json"

    tweeted_urls = set()
    if os.path.exists(TWEETED_FILE):
        try:
            with open(TWEETED_FILE, "r", encoding="utf-8") as f:
                tweeted_urls = set(json.load(f))
        except Exception as e:
            print(f"Tweet geçmişi okunamadı: {e}")

    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        for news in reversed(news_list):
            if news['full_url'] not in tweeted_urls:
                title = news['title']
                url = news['full_url']
                
                max_title_len = 280 - len(url) - 30
                if len(title) > max_title_len:
                    title = title[:max_title_len - 3] + "..."

                tweet_text = f"🔴 SON DAKİKA ({news['category_name'].upper()})\n\n{title}\n\nDetaylar 🔗 {url}\n\n#sondakika #{news['category_slug']} #nearadin"

                client.create_tweet(text=tweet_text)
                print(f"X üzerinde paylaşıldı: {news['title']}")

                tweeted_urls.add(news['full_url'])
                break 

        with open(TWEETED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(tweeted_urls), f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"X (Twitter) paylaşım hatası: {e}")


def get_header_html(title_text="nearadin.net - SON DAKİKA"):
    """Tüm Sayfalarda Ortak Kullanılan, Kategoriler Eklenmiş Hamburger Menülü Header Yapısı"""
    return f'''
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
        <button id="hamburgerBtn" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 5px; outline: none;">☰</button>
        
        <nav id="dropdownNav" style="display: none; position: absolute; top: 100%; right: 0; background: white; width: 230px; max-height: 80vh; overflow-y: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 0 0 8px 8px; border: 1px solid #e4e6eb;">
            <ul style="list-style: none; margin: 0; padding: 0;">
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">🏠 Anasayfa</a></li>
                
                <!-- KATEGORİLER -->
                <li style="background-color: #f7f8fa; padding: 8px 16px; font-size: 11px; font-weight: bold; color: #65676b; text-transform: uppercase; border-bottom: 1px solid #f0f2f5;">📰 Haber Kategorileri</li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/gundem/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">📌 Gündem</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/spor/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">⚽ Spor</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/ekonomi/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">📈 Ekonomi</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/teknoloji/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">💻 Teknoloji</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/dunya/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🌍 Dünya</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/saglik/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🏥 Sağlık</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/bilim/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🔬 Bilim</a></li>

                <!-- SERVİSLER VE ARAÇLAR -->
                <li style="background-color: #f7f8fa; padding: 8px 16px; font-size: 11px; font-weight: bold; color: #65676b; text-transform: uppercase; border-bottom: 1px solid #f0f2f5;">🛠️ Servisler ve Araçlar</li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/canli-mac-sonuclari/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">⚽ Canlı Maç Sonuçları</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/arsiv/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">📅 Günlük Arşiv</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/nobetci-eczane/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🏥 Nöbetçi Eczane</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/son-depremler/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🔴 Son Depremler</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/namaz-vakitleri/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🕌 Namaz Vakitleri</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/kripto-para/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">🪙 Kripto Piyasası</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/hava-durumu/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">☀️ Hava Durumu</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/film-izle/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">📺 Film İzle</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/iletisim/" style="display: block; padding: 10px 16px; color: #1c1e21; text-decoration: none; font-size: 14px;">📨 İletişim</a></li>
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
                        <li style="margin-bottom: 5px;"><a href="/gundem/" style="color: #617085; text-decoration: none;">Gündem</a></li>
                        <li style="margin-bottom: 5px;"><a href="/spor/" style="color: #617085; text-decoration: none;">Spor</a></li>
                        <li style="margin-bottom: 5px;"><a href="/ekonomi/" style="color: #617085; text-decoration: none;">Ekonomi</a></li>
                        <li style="margin-bottom: 5px;"><a href="/teknoloji/" style="color: #617085; text-decoration: none;">Teknoloji</a></li>
                        <li style="margin-bottom: 5px;"><a href="/arsiv/" style="color: #617085; text-decoration: none;">📅 Günlük Arşiv</a></li>
                        <li style="margin-bottom: 5px;"><a href="/sitemap.xml" style="color: #617085; text-decoration: none;">🔗Sitemap</a></li>
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

        .city-select-box {{ margin-bottom: 20px; }}
        .city-select-box label {{ display: block; font-weight: bold; font-size: 14px; margin-bottom: 6px; color: #333; }}
        .city-select-box select {{ width: 100%; max-width: 300px; padding: 10px; border-radius: 6px; border: 1px solid #ccd0d5; font-size: 14px; background: #fff; outline: none; cursor: pointer; }}

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
    
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>

    {admatic_code}
    {header_html}

    <div class="container">
        <div class="card">
            <h1>☀️ 7 Günlük Hava Durumu</h1>
            <p>İlini seçerek önümüzdeki 7 günlük sıcaklık ve hava tahmin raporunu hemen incele.</p>
            
            <div class="city-select-box">
                <label for="citySelect">İl Seçiniz:</label>
                <select id="citySelect" onchange="getWeatherData()">
                    <option value="34|41.0082|28.9784" selected>34 - İstanbul</option>
                    <option value="1|37.0000|35.3213">01 - Adana</option>
                    <option value="6|39.9208|32.8541">06 - Ankara</option>
                    <option value="7|36.8969|30.7133">07 - Antalya</option>
                    <option value="16|40.1826|29.0665">16 - Bursa</option>
                    <option value="35|38.4192|27.1287">35 - İzmir</option>
                    <option value="61|41.0015|39.7178">61 - Trabzon</option>
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

                    for (let i = 0; i < 7; i++) {{
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
    CATEGORIES = {
        "gundem": {"name": "Gündem", "url": "https://news.google.com/rss/headlines/section/topic/NATION?hl=tr&gl=TR&ceid=TR:tr"},
        "dunya": {"name": "Dünya", "url": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=tr&gl=TR&ceid=TR:tr"},
        "ekonomi": {"name": "Ekonomi", "url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=tr&gl=TR&ceid=TR:tr"},
        "teknoloji": {"name": "Teknoloji", "url": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=tr&gl=TR&ceid=TR:tr"},
        "spor": {"name": "Spor", "url": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=tr&gl=TR&ceid=TR:tr"},
        "saglik": {"name": "Sağlık", "url": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=tr&gl=TR&ceid=TR:tr"},
        "bilim": {"name": "Bilim", "url": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=tr&gl=TR&ceid=TR:tr"}
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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

    generate_weather_page(
        header_html=get_header_html("nearadin.net - Hava Durumu"),
        footer_html=footer_html,
        whos_amung_us_code=whos_amung_us_code,
        admatic_code=admatic_code
    )

    parsed_items = []
    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(datetime.timezone.utc)
    
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")
    last_update_iso = datetime.datetime.now(tz_tr).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    for cat_slug, cat_info in CATEGORIES.items():
        try:
            req = urllib.request.Request(cat_info["url"], headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            xml_data = response.read()

            root = ET.fromstring(xml_data)
            raw_items = root.findall('./channel/item')

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
                        'pub_date_raw': pub_date_raw,
                        'category_slug': cat_slug,
                        'category_name': cat_info["name"]
                    })
        except Exception as e:
            print(f"{cat_info['name']} kategorisi çekilirken hata oluştu: {e}")
            continue

    parsed_items.sort(key=lambda x: x['pub_datetime'], reverse=True)
    parsed_items = parsed_items[:500]

    news_list = []
    daily_news_grouped = {}

    for idx, entry in enumerate(parsed_items):
        item = entry['item']
        pub_datetime = entry['pub_datetime']
        cat_slug = entry['category_slug']
        cat_name = entry['category_name']

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
        
        os.makedirs(f"{cat_slug}/{date_folder}", exist_ok=True)

        slug = slugify(clean_title[:60])
        page_name = f"{slug}.html"
        internal_link = f"/{cat_slug}/{date_folder}/{page_name}"
        category_link = f"/{cat_slug}/{date_folder}/"
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
            "category_link": category_link,
            "full_url": full_url,
            "iso_date": dt_tr.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "category_slug": cat_slug,
            "category_name": cat_name
        }

        news_list.append(news_data)

        group_key = f"{cat_slug}/{date_folder}"
        if group_key not in daily_news_grouped:
            daily_news_grouped[group_key] = {
                "date_str": date_str,
                "cat_slug": cat_slug,
                "cat_name": cat_name,
                "folder_path": f"{cat_slug}/{date_folder}",
                "news_items": []
            }
        daily_news_grouped[group_key]["news_items"].append(news_data)

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
                    <span style="font-size: 11px; color: #65676b;">{other_news['category_name']} - {other_news['source']} - {other_news['time']}</span>
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
        .meta-info {{ display: flex; gap: 10px; font-size: 13px; color: #65676b; margin-bottom: 12px; align-items: center; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; text-transform: uppercase; text-decoration: none; display: inline-block; }}
        .badge:hover {{ background: #ffd0cc; }}
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

    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    
    {admatic_code}
    {header_html}

    <div class="container">
        <article class="article-card">
            <div class="meta-info">
                <!-- TIKLANABİLİR KIRMIZI KATEGORİ ROZETİ -->
                <a href="{news['category_link']}" class="badge">{news['category_name']}</a>
                <span>Tarih: <strong>{news['date_str']} - {news['time']}</strong></span>
                <span>Kaynak: <strong>{news['source']}</strong></span>
            </div>
            <h1>{news['title']}</h1>
            <p>{news['desc']}</p>
            
            <div class="actions">
                <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku ↗</a>
                <a href="{news['category_link']}" class="btn btn-secondary">← {news['category_name']} ({news['date_str']}) Haberlerine Dön</a>
            </div>

            <div id="disqus_thread" style="width: 100%;"></div>
            <script>
                var disqus_config = function () {{
                    this.page.url = '{news['full_url']}';
                    this.page.identifier = '{news['internal_link']}';
                }};
                (function() {{
                    var d = document, s = d.createElement('script');
                    s.src = 'https://nearadin.disqus.com/embed.js';
                    s.setAttribute('data-timestamp', +new Date());
                    (d.head || d.body).appendChild(s);
                }})();
            </script>

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

        file_path = f"{news['category_slug']}/{news['date_folder']}/{news['page_name']}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(detail_html)

        # Kart Üzerinde Tıklanabilir Rozet
        news_cards_html += f'''
        <article class="news-card">
            <div class="card-header">
                <a href="{news['category_link']}" title="{news['category_name']} Haberleri" class="badge">{news['category_name']}</a>
                <span title="{news['source']}" class="source">{news['source']}</span>
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

    # --- KATEGORİ VEYA GÜN BAZLI ÖZEL İNDEKS SAYFALARI ---
    for group_key, group_data in daily_news_grouped.items():
        folder_path = group_data["folder_path"]
        json_path = f"{folder_path}/news.json"
        accumulated_news = []

        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as jf:
                    accumulated_news = json.load(jf)
            except Exception:
                accumulated_news = []

        existing_urls = {item['full_url'] for item in accumulated_news}
        for new_item in group_data["news_items"]:
            if new_item['full_url'] not in existing_urls:
                accumulated_news.append(new_item)
                existing_urls.add(new_item['full_url'])

        accumulated_news.sort(key=lambda x: x['time'], reverse=True)

        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(accumulated_news, jf, ensure_ascii=False, indent=2)

        day_cards_html = ""
        for idx, d_news in enumerate(accumulated_news):
            day_cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <a href="/{d_news['category_slug']}/{d_news['date_folder']}/" class="badge">{d_news['category_name']}</a>
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
    <title>{group_data['cat_name']} - {group_data['date_str']} Haberleri - nearadin.net</title>
    <meta name="description" content="{group_data['cat_name']} kategorisinde {group_data['date_str']} gününe ait tüm son dakika haberleri." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 12px 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold; color: #0056b3; border: 1px solid #e4e6eb; display: flex; justify-content: space-between; align-items: center; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; text-transform: uppercase; text-decoration: none; }}
        .badge:hover {{ background: #ffd0cc; }}
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
            <span>📅 {group_data['cat_name']} - {group_data['date_str']} ({len(accumulated_news)} Haber)</span>
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
        with open(f"{folder_path}/index.html", "w", encoding="utf-8") as f:
            f.write(daily_index_html)

    # --- ANA KATEGORİ SAYFALARINI OLUŞTUR (/spor/, /teknoloji/ VB.) ---
    for cat_slug, cat_info in CATEGORIES.items():
        cat_news = [n for n in news_list if n['category_slug'] == cat_slug]
        cat_cards = ""
        for d_news in cat_news:
            cat_cards += f'''
            <article class="news-card">
                <div class="card-header">
                    <a href="/{d_news['category_slug']}/{d_news['date_folder']}/" class="badge">{d_news['category_name']}</a>
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

        cat_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_info['name']} Haberleri - nearadin.net</title>
    <meta name="description" content="En son {cat_info['name']} haberleri ve canlı gelişmeler." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 12px 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold; color: #0056b3; border: 1px solid #e4e6eb; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; text-transform: uppercase; text-decoration: none; }}
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
        <div class="status-bar">
            📌 {cat_info['name']} Haberleri
        </div>
        <main>
            {cat_cards if cat_cards else '<p style="padding: 20px; background: white; border-radius: 8px;">Bu kategoride henüz güncel haber bulunmamaktadır.</p>'}
        </main>
        {whos_amung_us_code}
    </div>
    {footer_html}
</body>
</html>'''
        os.makedirs(cat_slug, exist_ok=True)
        with open(f"{cat_slug}/index.html", "w", encoding="utf-8") as f:
            f.write(cat_page_html)

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
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; text-transform: uppercase; text-decoration: none; }}
        .badge:hover {{ background: #ffd0cc; }}
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

    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>

    {header_html}

    <div class="container">
        <div class="status-bar">
            <span>Kaynak: <strong>Tüm Kategoriler Akışı</strong></span>
            <span><script id="_wauelp">var _wau = _wau || []; _wau.push(["dynamic", "tgui40zwet", "elp", "c4302bffffff", "small"]);</script><script async src="//waust.at/d.js"></script></span>
            
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
    <loc>https://nearadin.net/canli-mac-sonuclari/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nearadin.net/arsiv/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://nearadin.net/hava-durumu/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>\n'''

    for cat_slug in CATEGORIES.keys():
        sitemap_items += f'''  <url>
    <loc>https://nearadin.net/{cat_slug}/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>0.9</priority>
  </url>\n'''

    # --- ARŞİV SAYFASI OLUŞTURMA (KATEGORİ BAZLI GRUPLANDIRMA VE ACCORDION YAPISI) ---
    category_archives = {cat_slug: {} for cat_slug in CATEGORIES.keys()}

    for cat_slug in CATEGORIES.keys():
        if os.path.exists(cat_slug):
            for root_dir, dirs, files in os.walk(cat_slug):
                for file_name in files:
                    if file_name.endswith(".html"):
                        rel_path = os.path.relpath(os.path.join(root_dir, file_name), cat_slug)
                        clean_rel_path = rel_path.replace("\\", "/")
                        
                        if file_name == "index.html":
                            continue
                            
                        page_url = f"https://nearadin.net/{cat_slug}/{clean_rel_path}"
                        
                        sitemap_items += f'''  <url>
    <loc>{page_url}</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>\n'''
                        
                        path_parts = clean_rel_path.split('/')
                        if len(path_parts) >= 3:
                            year, month, day = path_parts[0], path_parts[1], path_parts[2]
                            sort_key = f"{year}/{month}/{day}"
                            d_str = f"{day}.{month}.{year}"
                            folder_link = f"/{cat_slug}/{year}/{month}/{day}/"
                            
                            category_archives[cat_slug][sort_key] = (d_str, folder_link)

    archive_blocks_html = ""
    for cat_slug, cat_info in CATEGORIES.items():
        dates_dict = category_archives.get(cat_slug, {})
        if not dates_dict:
            continue

        date_items_html = ""
        for sort_key in sorted(dates_dict.keys(), reverse=True):
            d_str, folder_link = dates_dict[sort_key]
            date_items_html += f'''
            <li style="border-bottom: 1px solid #f0f2f5; padding: 10px 15px;">
                <a href="{folder_link}" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: #1c1e21; font-size: 14px;">
                    <span>📅 {d_str} {cat_info['name']} Haberleri</span>
                    <span style="font-size: 12px; color: #1877f2; font-weight: bold;">Arşivi İncele →</span>
                </a>
            </li>'''

        archive_blocks_html += f'''
        <div id="{cat_slug}" class="archive-card" style="background: white; border-radius: 10px; border: 1px solid #e4e6eb; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); overflow: hidden;">
            <div class="archive-header" onclick="toggleArchive('{cat_slug}')" style="background-color: #f7f8fa; padding: 14px 16px; border-bottom: 1px solid #e4e6eb; font-weight: bold; font-size: 16px; color: #0056b3; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none;">
                <span style="display: flex; align-items: center; gap: 8px;">
                    📌 {cat_info['name']} Arşivi 
                    <span class="toggle-icon" id="icon-{cat_slug}" style="font-size: 12px; color: #65676b;">▼</span>
                </span>
                <a href="/{cat_slug}/" onclick="event.stopPropagation();" style="font-size: 12px; color: #1877f2; text-decoration: none; font-weight: normal;">Kategoriye Git →</a>
            </div>
            <ul id="list-{cat_slug}" class="archive-list" style="list-style: none; margin: 0; padding: 0; display: none;">
                {date_items_html}
            </ul>
        </div>'''

    archive_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haber Arşivi - nearadin.net</title>
    <meta name="description" content="nearadin.net kategorilere göre tarihlendirilmiş güncel haber arşivleri." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; scroll-behavior: smooth; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        h1 {{ font-size: 20px; margin-bottom: 15px; color: #0056b3; }}
        .archive-header:hover {{ background-color: #eef2f7 !important; }}
        .ad-container {{ margin-bottom: 12px; text-align: center; width: 100%; overflow: hidden; }}
        .ad-container:empty {{ display: none !important; }}
    </style>
</head>
<body>

    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>

    {header_html}
    <div class="container">
        <h1>📁 Kategorilere Göre Günlük Arşiv</h1>
        {archive_blocks_html if archive_blocks_html else '<p style="background: white; padding: 15px; border-radius: 8px;">Henüz arşivlenmiş gün bulunmuyor.</p>'}
    </div>

    <script>
        function toggleArchive(slug) {{
            const list = document.getElementById('list-' + slug);
            const icon = document.getElementById('icon-' + slug);
            const card = document.getElementById(slug);

            if (list.style.display === 'none' || list.style.display === '') {{
                list.style.display = 'block';
                icon.innerText = '▲';
                setTimeout(() => {{
                    card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}, 100);
            }} else {{
                list.style.display = 'none';
                icon.innerText = '▼';
            }}
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            const hash = window.location.hash.replace('#', '');
            if (hash) {{
                toggleArchive(hash);
            }}
        }});
    </script>

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

    # --- GOOGLE NEWS SITEMAP ---
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

    # --- X (TWITTER) OTOMATİK PAYLAŞIM ---
    share_on_twitter(news_list)

    print("İşlem tamamlandı. Kategoriye özel arşivler başarıyla güncellendi.")

if __name__ == "__main__":
    fetch_and_generate()
