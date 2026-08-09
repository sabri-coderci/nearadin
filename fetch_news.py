import urllib.request
import xml.etree.ElementTree as ET
import datetime
import html
import re
import urllib.parse

# Çeşitli haber kaynaklarının RSS akışları
RSS_SOURCES = [
    "https://www.sozcu.com.tr/rss/tum-haberler.xml",
    "https://www.haberturk.com/rss/kategori/gundem.xml",
    "https://www.ntv.com.tr/gundem.rss",
    "https://www.trthaber.com/gundem_articles.rss",
    "https://www.cumhuriyet.com.tr/rss/son_dakika.xml",
    "https://www.aksam.com.tr/rss/gundem.xml"
]

def clean_summary(raw_html, max_chars=180):
    if not raw_html:
        return ""
    text = re.sub(r'<script.*?>.*?</script>', '', raw_html, flags=re.DOTALL)
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text)
    text = html.unescape(text).strip()
    text = re.sub(r'\s+', ' ', text)
    if ' font' in text:
        text = text.split(' font')[0]
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + "..."
    return text

def generate_sitemap():
    now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://nearadin.net/</loc>
    <lastmod>{now_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

def generate_robots_txt():
    robots_content = """User-agent: *
Allow: /

Sitemap: https://nearadin.net/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)

def fetch_and_generate():
    all_items = []

    for rss_url in RSS_SOURCES:
        try:
            req = urllib.request.Request(
                rss_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            response = urllib.request.urlopen(req, timeout=5)
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = root.findall('./channel/item')
            all_items.extend(items[:5]) # Her kaynaktan son 5 haberi çek
        except Exception:
            continue

    news_html_cards = ""
    
    for item in all_items[:30]:
        title = item.find('title').text if item.find('title') is not None else 'Başlıksız Haber'
        link = item.find('link').text if item.find('link') is not None else '#'
        description = item.find('description').text if item.find('description') is not None else ''
        
        clean_title = html.unescape(title).rsplit(' - ', 1)[0]
        summary = clean_summary(description, max_chars=180)
        
        if not summary or len(summary) < 15:
            summary = "Gündemdeki son gelişmeler, sıcak başlıklar ve detaylar nearadin.net farkıyla anında yayında."

        encoded_link = urllib.parse.quote(link.strip(), safe='')
        custom_redirect_url = f"https://nearadin.net/url/?q={encoded_link}"

        news_html_cards += f'''
        <div class="card">
            <span class="badge">SON DAKİKA</span>
            <h2>{clean_title}</h2>
            <p>{summary}</p>

            <div class="card-footer">
                <a href="{custom_redirect_url}" target="_blank" rel="noopener">Habere Git →</a>
                <span>Canlı Akış</span>
            </div>
        </div>
        '''

    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    html_content = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <title>nearadin.net - SON DAKİKA</title>
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
    <link rel="canonical" href="https://nearadin.net/" />
    
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; margin: 0; padding: 0; }}
        header {{ background: #0056b3; color: white; text-align: center; padding: 20px 10px; font-size: 24px; font-weight: bold; }}
        .container {{ max-width: 800px; margin: 20px auto; padding: 0 15px; }}
        .info-box {{ background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); display: flex; justify-content: space-between; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .badge {{ background: #ffebee; color: #c62828; font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }}
        .card h2 {{ margin: 0 0 10px 0; font-size: 18px; color: #111; line-height: 1.4; }}
        .card p {{ color: #555; font-size: 14px; margin-bottom: 15px; line-height: 1.5; }}
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #eee; padding-top: 10px; font-size: 13px; color: #888; }}
        .card-footer a {{ color: #0056b3; text-decoration: none; font-weight: bold; }}
        .widget-box {{ text-align: center; margin: 20px 0; }}
    </style>
</head>
<body>
    <!-- Admatic AUTO ads START -->
    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    <!-- Admatic AUTO ads END -->

    <header>nearadin.net - SON DAKİKA</header>
    <div class="container">
        <div class="info-box">
            <div><strong>Kaynak:</strong> Canlı Haber Akışı</div>
            <div><strong>Son Güncelleme:</strong> {now}</div>
        </div>
        {news_html_cards}
    </div>

    <!-- Whos.Amung.Us Ziyaretçi Sayacı -->
    <div class="widget-box">
        <script id="_wauc41">var _wau = _wau || []; _wau.push(["dynamic", "0bq3jkzwyz", "c41", "c4302bffffff", "small"]);</script>
        <script async src="//waust.at/d.js"></script>
    </div>
</body>
</html>
'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    generate_sitemap()
    generate_robots_txt()

if __name__ == "__main__":
    fetch_and_generate()
