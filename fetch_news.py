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
        'Ä±': 'i', 'ÄŸ': 'g', 'Ã¼': 'u', 'ÅŸ': 's', 'Ã¶': 'o', 'Ã§': 'c',
        'Ä°': 'i', 'Ä': 'g', 'Ãœ': 'u', 'Å': 's', 'Ã–': 'o', 'Ã‡': 'c'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def post_to_x(latest_news):
    """En son Ã§Ä±kan haberi X Ã¼zerinde paylaÅŸÄ±r."""
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("X API anahtarlarÄ± bulunamadÄ±. Tweet atma adÄ±mÄ± atlanÄ±yor.")
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
            f"ğŸš¨ SON DAKÄ°KA HABERÄ°\n\n"
            f"ğŸ“Œ {title}\n\n"
            f"ğŸ“ {desc_preview}\n\n"
            f"ğŸ”— Detaylar iÃ§in tÄ±klayÄ±n:\n{latest_news['full_url']}\n\n"
            f"#sondakika #haber #gundem"
        )
        
        response = client.create_tweet(text=tweet_text)
        print(f"X (Twitter) paylaÅŸÄ±mÄ± baÅŸarÄ±lÄ±! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"X (Twitter) paylaÅŸÄ±mÄ±nda hata oluÅŸtu: {e}")

def get_header_html(title_text="nearadin.net - SON DAKÄ°KA"):
    """TÃ¼m Sayfalarda Ortak KullanÄ±lan Hamburger MenÃ¼lÃ¼ Header YapÄ±sÄ±"""
    return f'''
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
        <button id="hamburgerBtn" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 5px; outline: none;">â˜°</button>
        
        <nav id="dropdownNav" style="display: none; position: absolute; top: 100%; right: 0; background: white; width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 0 0 8px 8px; border: 1px solid #e4e6eb; overflow: hidden;">
            <ul style="list-style: none; margin: 0; padding: 0;">
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸ  Anasayfa</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/arsiv/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸ“… GÃ¼nlÃ¼k ArÅŸiv</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/nobetci-eczane/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸ¥ NÃ¶betÃ§i Eczane</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/son-depremler/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸ”´ Son Depremler</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/kripto-para/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸª™ Kripto PiyasasÄ±</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/hava-durumu/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">â˜€ï¸ Hava Durumu</a></li>
                <li style="border-bottom: 1px solid #f0f2f5;"><a href="/film-izle/" style="display: block; padding: 12px 16px; color: #1c1e21; text-decoration: none; font-weight: 600; font-size: 14px;">ğŸ“º Film Ä°zle</a></li>
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
    """TÃ¼m Sayfalarda Ortak KullanÄ±lan Standart Footer BileÅŸeni"""
    return '''
    <footer style="background-color: #1c1e21; color: #90949c; padding: 30px 15px; margin-top: 40px; font-size: 13px; line-height: 1.6; clear: both;">
        <div style="max-width: 680px; margin: 0 auto;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 20px;">
                <div style="flex: 1; min-width: 200px;">
                    <h3 style="color: #fff; font-size: 16px; margin-bottom: 10px;">nearadin.net</h3>
                    <p>TÃ¼rkiye ve dÃ¼nyadan en gÃ¼ncel son dakika haberleri, anlÄ±k geliÅŸmeler ve canlÄ± servis haber akÄ±ÅŸ platformu.</p>
                </div>
                <div style="flex: 1; min-width: 140px;">
                    <h4 style="color: #fff; font-size: 14px; margin-bottom: 10px;">HÄ±zlÄ± MenÃ¼</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 5px;"><a href="/" style="color: #617085; text-decoration: none;">Anasayfa</a></li>
                        <li style="margin-bottom: 5px;"><a href="/arsiv/" style="color: #617085; text-decoration: none;">ğŸ“… GÃ¼nlÃ¼k ArÅŸiv</a></li>
                        <li style="margin-bottom: 5px;"><a href="/nobetci-eczane/" style="color: #617085; text-decoration: none;">ğŸ¥ NÃ¶betÃ§i Eczane</a></li>
                        <li style="margin-bottom: 5px;"><a href="/son-depremler/" style="color: #617085; text-decoration: none;">ğŸ”´ Son Depremler</a></li>
                        <li style="margin-bottom: 5px;"><a href="/kripto-para/" style="color: #617085; text-decoration: none;">ğŸª™ Kripto PiyasasÄ±</a></li>
                        <li style="margin-bottom: 5px;"><a href="/hava-durumu/" style="color: #617085; text-decoration: none;">â˜€ï¸ Hava Durumu</a></li>
                        <li style="margin-bottom: 5px;"><a href="/film-izle/" style="color: #617085; text-decoration: none;">ğŸ“º Film Ä°zle</a></li>
                        <li style="margin-bottom: 5px;"><a href="/sitemap.xml" style="color: #617085; text-decoration: none;">Sitemap</a></li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; font-size: 12px; color: #65676b;">
                <p style="margin-bottom: 8px;">Takip Edin: <a href="https://x.com/nearadin2026" target="_blank" rel="nofollow" style="color: #1877f2; text-decoration: none; font-weight: bold;">@nearadin2026 (X / Twitter)</a></p>
                <p>Â© 2026 nearadin.net - TÃ¼m HaklarÄ± SaklÄ±dÄ±r.</p>
            </div>
        </div>
    </footer>
    '''

def generate_weather_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """hava-durumu/index.html SayfasÄ±nÄ± Otomatik OluÅŸturur"""
    os.makedirs("hava-durumu", exist_ok=True)

    weather_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5 GÃ¼nlÃ¼k Hava Durumu Tahmini - nearadin.net</title>
    <meta name="description" content="TÃ¼rkiye'nin 81 ili iÃ§in gÃ¼ncel 5 gÃ¼nlÃ¼k detaylÄ± hava durumu tahminleri." />
    <link rel="canonical" href="https://nearadin.net/hava-durumu/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        h1 {{ font-size: 20px; margin-bottom: 10px; color: #0056b3; }}
        p {{ color: #65676b; font-size: 14px; margin-bottom: 15px; }}

        /* Ä°l SeÃ§im AlanÄ± */
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
            <h1>â˜€ï¸ 5 GÃ¼nlÃ¼k Hava Durumu</h1>
            <p>Ä°lini seÃ§erek Ã¶nÃ¼mÃ¼zdeki 5 gÃ¼nlÃ¼k sÄ±caklÄ±k ve hava tahmin raporunu hemen incele.</p>
            
            <!-- Ä°l SeÃ§im MenÃ¼sÃ¼ -->
            <div class="city-select-box">
                <label for="citySelect">Ä°l SeÃ§iniz:</label>
                <select id="citySelect" onchange="getWeatherData()">
                    <option value="34|41.0082|28.9784" selected>34 - Ä°stanbul</option>
                    <option value="1|37.0000|35.3213">01 - Adana</option>
                    <option value="2|37.7648|38.2786">02 - AdÄ±yaman</option>
                    <option value="3|38.7507|30.5567">03 - Afyonkarahisar</option>
                    <option value="4|39.7191|43.0503">04 - AÄŸrÄ±</option>
                    <option value="5|40.6547|35.8356">05 - Amasya</option>
                    <option value="6|39.9208|32.8541">06 - Ankara</option>
                    <option value="7|36.8969|30.7133">07 - Antalya</option>
                    <option value="8|41.1828|41.8183">08 - Artvin</option>
                    <option value="9|37.8481|27.8446">09 - AydÄ±n</option>
                    <option value="10|39.6484|27.8826">10 - BalÄ±kesir</option>
                    <option value="11|40.1418|30.0609">11 - Bilecik</option>
                    <option value="12|38.8856|40.4980">12 - BingÃ¶l</option>
                    <option value="13|38.4004|42.1095">13 - Bitlis</option>
                    <option value="14|40.7359|31.6061">14 - Bolu</option>
                    <option value="15|37.7214|30.2874">15 - Burdur</option>
                    <option value="16|40.1826|29.0665">16 - Bursa</option>
                    <option value="17|40.1553|26.4142">17 - Ã‡anakkale</option>
                    <option value="18|40.6013|33.6134">18 - Ã‡ankÄ±rÄ±</option>
                    <option value="19|40.5506|34.9556">19 - Ã‡orum</option>
                    <option value="20|37.7765|29.0864">20 - Denizli</option>
                    <option value="21|37.9144|40.2306">21 - DiyarbakÄ±r</option>
                    <option value="22|41.6771|26.5557">22 - Edirne</option>
                    <option value="23|38.6810|39.2264">23 - ElazÄ±ÄŸ</option>
                    <option value="24|39.7500|39.5000">24 - Erzincan</option>
                    <option value="25|39.9043|41.2679">25 - Erzurum</option>
                    <option value="26|39.7767|30.5206">26 - EskiÅŸehir</option>
                    <option value="27|37.0662|37.3833">27 - Gaziantep</option>
                    <option value="28|40.9128|38.3895">28 - Giresun</option>
                    <option value="29|40.4386|39.5086">29 - GÃ¼mÃ¼ÅŸhane</option>
                    <option value="30|37.5833|43.7333">30 - Hakkari</option>
                    <option value="31|36.2023|36.1606">31 - Hatay</option>
                    <option value="32|37.7648|30.5566">32 - Isparta</option>
                    <option value="33|36.8000|34.6333">33 - Mersin</option>
                    <option value="35|38.4192|27.1287">35 - Ä°zmir</option>
                    <option value="36|40.6017|43.0975">36 - Kars</option>
                    <option value="37|41.3887|33.7827">37 - Kastamonu</option>
                    <option value="38|38.7312|35.4787">38 - Kayseri</option>
                    <option value="39|41.7333|27.2167">39 - KÄ±rklareli</option>
                    <option value="40|39.1425|34.1709">40 - KÄ±rÅŸehir</option>
                    <option value="41|40.7654|29.9408">41 - Kocaeli</option>
                    <option value="42|37.8667|32.4833">42 - Konya</option>
                    <option value="43|39.4167|29.9833">43 - KÃ¼tahya</option>
                    <option value="44|38.3552|38.3095">44 - Malatya</option>
                    <option value="45|38.6191|27.4289">45 - Manisa</option>
                    <option value="46|37.5858|36.9371">46 - KahramanmaraÅŸ</option>
                    <option value="47|37.3211|40.7245">47 - Mardin</option>
                    <option value="48|37.2153|28.3636">48 - MuÄŸla</option>
                    <option value="49|38.7437|41.5064">49 - MuÅŸ</option>
                    <option value="50|38.6244|34.7231">50 - NevÅŸehir</option>
                    <option value="51|37.9659|34.6850">51 - NiÄŸde</option>
                    <option value="52|40.9839|37.8764">52 - Ordu</option>
                    <option value="53|41.0201|40.5234">53 - Rize</option>
                    <option value="54|40.7569|30.3783">54 - Sakarya</option>
                    <option value="55|41.2867|36.3300">55 - Samsun</option>
                    <option value="56|37.9333|41.9500">56 - Siirt</option>
                    <option value="57|42.0231|35.1531">57 - Sinop</option>
                    <option value="58|39.7477|37.0179">58 - Sivas</option>
                    <option value="59|40.9833|27.5167">59 - TekirdaÄŸ</option>
                    <option value="60|40.3167|36.5500">60 - Tokat</option>
                    <option value="61|41.0015|39.7178">61 - Trabzon</option>
                    <option value="62|39.1079|39.5401">62 - Tunceli</option>
                    <option value="63|37.1591|38.7969">63 - ÅanlÄ±urfa</option>
                    <option value="64|38.4122|29.4077">64 - UÅŸak</option>
                    <option value="65|38.5028|43.3730">65 - Van</option>
                    <option value="66|39.8181|34.8147">66 - Yozgat</option>
                    <option value="67|41.4564|31.7987">67 - Zonguldak</option>
                    <option value="68|38.3687|34.0370">68 - Aksaray</option>
                    <option value="69|40.2551|40.2249">69 - Bayburt</option>
                    <option value="70|37.1759|33.2287">70 - Karaman</option>
                    <option value="71|41.8486|33.7753">71 - KÄ±rÄ±kkale</option>
                    <option value="72|37.8812|41.1285">72 - Batman</option>
                    <option value="73|37.5205|42.4598">73 - ÅÄ±rnak</option>
                    <option value="74|41.6344|32.3375">74 - BartÄ±n</option>
                    <option value="75|41.1126|42.7020">75 - Ardahan</option>
                    <option value="76|39.9167|44.0500">76 - IÄŸdÄ±r</option>
                    <option value="77|40.6500|29.4000">77 - Yalova</option>
                    <option value="78|41.2061|32.6204">78 - KarabÃ¼k</option>
                    <option value="79|36.7184|37.1212">79 - Kilis</option>
                    <option value="80|37.0742|36.1753">80 - Osmaniye</option>
                    <option value="81|40.8438|31.1565">81 - DÃ¼zce</option>
                </select>
            </div>

            <div id="loading" class="loading">Hava durumu verileri yÃ¼kleniyor...</div>
            <div id="weatherList" class="weather-list"></div>

            <a href="/" class="btn-home">â† Anasayfaya DÃ¶n</a>
        </div>

        {whos_amung_us_code}
    </div>

    <script>
        function getWeatherDescription(code) {{
            const descriptions = {{
                0: "ğŸŒ AÃ§Ä±k / GÃ¼neÅŸli",
                1: "ğŸŒ¤ï¸ Ã‡oÄŸunlukla AÃ§Ä±k",
                2: "â›… ParÃ§alÄ± Bulutlu",
                3: "â˜ï¸ Ã‡ok Bulutlu",
                45: "ğŸŒ«ï¸ Sisli",
                48: "ğŸŒ«ï¸ KÄ±raÄŸÄ±lÄ± Sis",
                51: "ğŸŒ§ï¸ Hafif Ã‡isenti",
                53: "ğŸŒ§ï¸ Ã‡isenti",
                55: "ğŸŒ§ï¸ YoÄŸun Ã‡isenti",
                61: "ğŸŒ§ï¸ Hafif YaÄŸmurlu",
                63: "ğŸŒ§ï¸ YaÄŸmurlu",
                65: "ğŸŒ§ï¸ Åiddetli YaÄŸmur",
                71: "â„ï¸ Hafif KarlÄ±",
                73: "â„ï¸ KarlÄ±",
                75: "â„ï¸ YoÄŸun Kar YaÄŸÄ±ÅŸlÄ±",
                95: "âš¡ GÃ¶k GÃ¼rÃ¼ltÃ¼lÃ¼ FÄ±rtÄ±na"
            }};
            return descriptions[code] || "ğŸŒ¤ï¸ ParÃ§alÄ± Bulutlu";
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

                    for (let i = 0; i < 5; i++) {{
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
                            <div class="weather-temp">${{maxT}}Â°C / <span style="color:#65676b; font-weight:normal;">${{minT}}Â°C</span></div>
                        `;
                        listEl.appendChild(item);
                    }}
                }} else {{
                    loadingEl.style.display = 'block';
                    loadingEl.innerText = 'Hava durumu bilgisi alÄ±namadÄ±.';
                }}
            }} catch (error) {{
                loadingEl.style.display = 'block';
                loadingEl.innerText = 'BaÄŸlantÄ± hatasÄ± oluÅŸtu.';
            }}
        }}

        getWeatherData();
    </script>

    {footer_html}

</body>
</html>'''

    with open("hava-durumu/index.html", "w", encoding="utf-8") as f:
        f.write(weather_html)

def generate_film_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    """film-izle/index.html SayfasÄ±nÄ± Otomatik OluÅŸturur"""
    os.makedirs("film-izle", exist_ok=True)
    
    film_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TÃ¼rkÃ§e Dublaj HD Film Ä°zle - nearadin.net</title>
    <meta name="description" content="nearadin.net Ã¶zel sinema portalÄ±. En gÃ¼ncel TÃ¼rkÃ§e dublaj yabancÄ± filmler, aksiyon ve macera filmlerini kesintisiz izleyin." />
    <link rel="canonical" href="https://nearadin.net/film-izle/" />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        :root {{ --sinema-ana: #e74c3c; --sinema-koyu: #121212; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; }}
        
        .film-container {{ max-width: 680px; margin: 0 auto; padding: 12px; min-height: 80vh; }}

        #sinema-kontrol-merkezi {{
            position: sticky; top: 50px; z-index: 999;
            background: var(--sinema-koyu); color: #fff;
            padding: 10px 14px; border-bottom: 3px solid var(--sinema-ana); width: 100%;
            border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .sinema-wrapper {{ display: flex; align-items: center; justify-content: space-between; }}
        #izlenen-bilgi {{ flex: 1; min-width: 0; margin-right: 10px; }}
        .canli-etiket {{ font-size: 9px; color: var(--sinema-ana); font-weight: bold; letter-spacing: 1px; display: block; }}
        #film-adi-aktif {{ display: block; font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

        #film-kapat-btn {{
            background: var(--sinema-ana); color: white; border: none;
            padding: 6px 12px; border-radius: 4px; cursor: pointer;
            font-weight: bold; font-size: 11px; flex-shrink: 0; display: none;
        }}

        #video-oynatici-alan {{ margin-top: 10px; display: none; width: 100%; }}
        .video-kapsayici {{ 
            position: relative; padding-bottom: 56.25%; height: 0; 
            overflow: hidden; border-radius: 8px; background: #000; 
        }}
        .video-kapsayici iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}

        .film-kart-ozel {{
            display: flex; align-items: center; padding: 10px; background: #fff;
            border: 1px solid #e4e6eb; border-radius: 8px; margin-bottom: 10px;
            cursor: pointer; transition: transform 0.1s ease, background 0.2s; width: 100%;
        }}
        .film-kart-ozel:hover {{ background: #fff8f7; }}
        .film-kart-ozel.aktif {{ border-left: 5px solid var(--sinema-ana); background: #fef5f4; }}
        
        .film-resim {{ width: 95px; height: 58px; border-radius: 6px; margin-right: 12px; object-fit: cover; flex-shrink: 0; }}
        .film-metin {{ 
            font-weight: 600; font-size: 14px; color: #1c1e21; flex: 1; min-width: 0; margin: 0;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis;
        }}
        .oynat-simge {{ color: var(--sinema-ana); font-size: 18px; margin-left: 8px; flex-shrink: 0; }}
        
        .durum-alani {{ text-align: center; padding: 15px 0; }}
        .daha-fazla-btn {{
            background: #0056b3; color: white; border: none;
            padding: 10px 22px; border-radius: 20px; font-weight: bold;
            font-size: 13px; cursor: pointer; transition: 0.2s;
        }}
        .daha-fazla-btn:hover {{ background: #004085; }}
        .son-yazi {{ color: #888; font-size: 12px; font-style: italic; display: none; }}
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

    <div class="film-container">
        <div id="sinema-kontrol-merkezi">
            <div class="sinema-wrapper">
                <div id="izlenen-bilgi">
                    <span class="canli-etiket">ÅU AN Ä°ZLENÄ°YOR</span>
                    <span id="film-adi-aktif">AÅŸaÄŸÄ±dan bir film seÃ§in...</span>
                </div>
                <button id="film-kapat-btn" onclick="filmDurdur()">KAPAT âœ•</button>
            </div>
            
            <div id="video-oynatici-alan">
                <div class="video-kapsayici">
                    <iframe id="film-iframe" src="" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                </div>
            </div>
        </div>

        <main id="canli-sonuc-listesi"></main>

        <div class="durum-alani">
            <button id="yukle-btn" class="daha-fazla-btn" onclick="sonrakiPartiYukle()">Daha Fazla Film YÃ¼kle â•</button>
            <div id="son-yazi" class="son-yazi">TÃ¼m filmler listelendi.</div>
        </div>

        {whos_amung_us_code}
    </div>

    {footer_html}

<script>
    const tumFilmler = [
        {{ id: 'aYbUTg-bfUU', baslik: 'Yeni Film 2026 - TÃ¼rkÃ§e Dublaj Aksiyon Dolu YabancÄ± Film Full HD' }},
        {{ id: 'vcMqEy6udI8', baslik: 'SÃ¼rÃ¼kleyici Gerilim & Macera Filmleri - TÃ¼rkÃ§e Dublaj Tek ParÃ§a' }},
        {{ id: 'U_uL_kFVdMU', baslik: 'YÃ¼ksek Tempolu YabancÄ± Sinema KuÅŸaÄŸÄ± - TÃ¼rkÃ§e Dublaj Ä°zle' }},
        {{ id: 'F-VEUnkkrPQ', baslik: 'YENÄ° FÄ°LM En Ä°yi Aksiyon Filmi Tek ParÃ§a HD - TÃ¼rkÃ§e Dublaj' }},
        {{ id: 'F5DEmClsMNA', baslik: 'Hayatta Kalmak Ä°Ã§in 80 Dakikan Var - Aksiyon Filmi TÃ¼rkÃ§e Dublaj' }},
        {{ id: 'U06i7AO53mM', baslik: 'Bilinmeyen Bir Adada UyanÄ±r - Macera ve Hayatta Kalma Filmi' }},
        {{ id: '30j_VWvOWX8', baslik: 'Ä°NFAZCI | En Tehlikeli ParalÄ± Asker - Aksiyon Filmi TÃ¼rkÃ§e Dublaj' }},
        {{ id: 'ZF6sfeS8H8M', baslik: 'Efsane Macera SinemasÄ± - TÃ¼rkÃ§e Dublaj Full Ä°zle' }}
    ];

    const SAYFA_BASINA = 4;
    let mevcutIndex = 0;

    function sonrakiPartiYukle() {{
        const container = document.getElementById('canli-sonuc-listesi');
        const yukleBtn = document.getElementById('yukle-btn');
        const sonYazi = document.getElementById('son-yazi');

        const dilim = tumFilmler.slice(mevcutIndex, mevcutIndex + SAYFA_BASINA);

        dilim.forEach(film => {{
            const card = document.createElement('article');
            card.className = 'film-kart-ozel';
            card.onclick = () => startMovie(film.id, film.baslik, card);
            card.innerHTML = `
                <img src="https://img.youtube.com/vi/${{film.id}}/hqdefault.jpg" class="film-resim" alt="${{film.baslik}}">
                <h3 class="film-metin">${{film.baslik}}</h3>
                <div class="oynat-simge">â–¶</div>
            `;
            container.appendChild(card);
        }});

        mevcutIndex += SAYFA_BASINA;

        if (mevcutIndex >= tumFilmler.length) {{
            yukleBtn.style.display = 'none';
            sonYazi.style.display = 'block';
        }}
    }}

    function startMovie(id, title, el) {{
        const frame = document.getElementById('film-iframe');
        const container = document.getElementById('video-oynatici-alan');
        const btn = document.getElementById('film-kapat-btn');
        const baslik = document.getElementById('film-adi-aktif');
        
        frame.src = `https://www.youtube.com/embed/${{id}}?autoplay=1&rel=0`;
        container.style.display = 'block';
        btn.style.display = 'block';
        baslik.innerText = title;
        
        document.querySelectorAll('.film-kart-ozel').forEach(k => k.classList.remove('aktif'));
        el.classList.add('aktif');
        
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function filmDurdur() {{
        const frame = document.getElementById('film-iframe');
        frame.src = '';
        document.getElementById('video-oynatici-alan').style.display = 'none';
        document.getElementById('film-kapat-btn').style.display = 'none';
        document.getElementById('film-adi-aktif').innerText = 'AÅŸaÄŸÄ±dan bir film seÃ§in...';
        document.querySelectorAll('.film-kart-ozel').forEach(k => k.classList.remove('aktif'));
    }}

    document.addEventListener('DOMContentLoaded', sonrakiPartiYukle);
</script>

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
    header_html = get_header_html("nearadin.net - SON DAKÄ°KA")
    
    admatic_code = '''
   <div class="ad-container">
      <!-- Admatic AUTO ads START -->
       <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
        <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
       <!-- Admatic AUTO ads END -->
   </div>
    '''

    # Film Ä°zle sayfasÄ±nÄ± dinamik olarak oluÅŸtur
    generate_film_page(
        header_html=get_header_html("nearadin.net - Film Ä°zle"),
        footer_html=footer_html,
        whos_amung_us_code=whos_amung_us_code,
        admatic_code=admatic_code
    )

    # Hava Durumu sayfasÄ±nÄ± dinamik olarak oluÅŸtur
    generate_weather_page(
        header_html=get_header_html("nearadin.net - Hava Durumu"),
        footer_html=footer_html,
        whos_amung_us_code=whos_amung_us_code,
        admatic_code=admatic_code
    )

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

            title = item.find('title').text if item.find('title') is not None else 'BaÅŸlÄ±ksÄ±z'
            original_link = item.find('link').text if item.find('link') is not None else '#'
            
            raw_desc = item.find('description').text if item.find('description') is not None else ''
            clean_desc = re.sub('<[^<]+?>', '', raw_desc)
            clean_desc = html.unescape(clean_desc)
            clean_title = html.unescape(title)

            source_name = "CanlÄ± Haber AkÄ±ÅŸÄ±"
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
                            â€¢ {other_news['title']}
                        </a>
                        <span style="font-size: 11px; color: #65676b;">{other_news['source']} - {other_news['time']}</span>
                    </li>'''
                    other_count += 1

            # Haber Detay SayfasÄ±
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
                <span class="badge">SON DAKÄ°KA</span>
                <span>Tarih: <strong>{news['date_str']} - {news['time']}</strong></span>
                <span>Kaynak: <strong>{news['source']}</strong></span>
            </div>
            <h1>{news['title']}</h1>
            <p>{news['desc']}</p>
            
            <div class="actions">
                <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku â†—</a>
                <a href="/haber/{news['date_folder']}/" class="btn btn-secondary">â† {news['date_str']} Tarihli TÃ¼m Haberlere DÃ¶n</a>
            </div>

            <div class="related-news">
                <div class="related-title">ğŸ”¥ DiÄŸer Son Dakika GeliÅŸmeleri</div>
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
                    <span class="badge">SON DAKÄ°KA</span>
                    <span class="source">{news['source']}</span>
                    <span class="time">{news['time']}</span>
                </div>
                <h2 class="news-title">
                    <a href="{news['internal_link']}">{news['title']}</a>
                </h2>
                <p class="news-summary">{news['desc']}</p>
                <div class="card-footer">
                    <a href="{news['internal_link']}" class="read-btn">DetayÄ± Oku â†’</a>
                </div>
            </article>
            '''

            if news["idx"] == 1:
                news_cards_html += admatic_code

        # --- HER GÃœN Ä°Ã‡Ä°N Ã–ZEL GÃœNLÃœK Ä°NDEKS SAYFASI ---
        for folder_path, group_data in daily_news_grouped.items():
            day_cards_html = ""
            for idx, d_news in enumerate(group_data["news_items"]):
                day_cards_html += f'''
                <article class="news-card">
                    <div class="card-header">
                        <span class="badge">SON DAKÄ°KA</span>
                        <span class="source">{d_news['source']}</span>
                        <span class="time">{d_news['time']}</span>
                    </div>
                    <h2 class="news-title">
                        <a href="{d_news['internal_link']}">{d_news['title']}</a>
                    </h2>
                    <p class="news-summary">{d_news['desc']}</p>
                    <div class="card-footer">
                        <a href="{d_news['internal_link']}" class="read-btn">DetayÄ± Oku â†’</a>
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
    <meta name="description" content="{group_data['date_str']} gÃ¼nÃ¼ne ait tÃ¼m son dakika haberleri ve geliÅŸmeleri akÄ±ÅŸÄ±." />
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

    <!-- Admatic AUTO ads START -->
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    <!-- Admatic AUTO ads END -->

    {header_html}
    <div class="container">
        <div class="status-bar">
            <span>ğŸ“… {group_data['date_str']} Tarihli Haber Listesi</span>
            <a href="/arsiv/" style="color: #1877f2; text-decoration: none; font-size: 12px;">â† TÃ¼m ArÅŸiv</a>
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
    <title>nearadin.net - Son Dakika Haberleri ve CanlÄ± AkÄ±ÅŸ</title>
    <meta name="description" content="TÃ¼rkiye ve dÃ¼nyadan son dakika haberleri, gÃ¼ncel geliÅŸmeler ve canlÄ± haber akÄ±ÅŸÄ±." />
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
            <span>Kaynak: <strong>Google CanlÄ± AkÄ±ÅŸ</strong></span>
            <span>Son GÃ¼ncelleme: <strong>{last_update}</strong></span>
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

        # XML Sitemap & ArÅŸiv YapÄ±sÄ±
        sitemap_items = f'''  <url>
    <loc>https://nearadin.net/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>1.0</priority>
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

        archive_dates_dict = {}

        if os.path.exists("haber"):
            for root_dir, dirs, files in os.walk("haber"):
                for file_name in files:
                    if file_name.endswith(".html"):
                        rel_path = os.path.relpath(os.path.join(root_dir, file_name), "haber")
                        clean_rel_path = rel_path.replace("\\", "/")
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
                            d_str = f"{day}.{month}.{year}"
                            folder_link = f"/haber/{year}/{month}/{day}/"
                            archive_dates_dict[d_str] = folder_link

        # Ana ArÅŸiv SayfasÄ± (arsiv/index.html)
        archive_list_html = ""
        for date_item in sorted(list(archive_dates_dict.keys()), reverse=True):
            folder_link = archive_dates_dict[date_item]
            archive_list_html += f'''
            <li style="background: white; padding: 14px 16px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                <a href="{folder_link}" style="display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: inherit;">
                    <span style="font-weight: 600; color: #333; font-size: 15px;">ğŸ“… {date_item} Tarihli TÃ¼m Haberler</span>
                    <span style="font-size: 13px; color: #1877f2; font-weight: bold;">TÃ¼m Liste â†’</span>
                </a>
            </li>'''

        archive_page_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haber ArÅŸivi - nearadin.net</title>
    <meta name="description" content="nearadin.net gÃ¼n bazlÄ± geÃ§miÅŸ son dakika haber arÅŸivleri." />
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
        <h1>GÃ¼n BazlÄ± Haber ArÅŸivi</h1>
        <ul>
            {archive_list_html if archive_list_html else '<p>HenÃ¼z arÅŸivlenmiÅŸ gÃ¼n bulunmuyor.</p>'}
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

        print("Betik baÅŸarÄ±yla Ã§alÄ±ÅŸtÄ±. Hava Durumu, Film-izle ve tÃ¼m servis sayfalarÄ± gÃ¼ncellendi.")

        if news_list:
            post_to_x(news_list[0])

    except Exception as e:
        print(f"Hata oluÅŸtu: {e}")

if __name__ == "__main__":
    fetch_and_generate()
