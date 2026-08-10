import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import os

def slugify(text):
    """Haber başlığından SEO uyumlu URL yapısı oluşturur."""
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

def fetch_and_generate():
    rss_url = "https://news.google.com/rss/search?q=son+dakika&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Haber sayfalarının kaydedileceği klasör
    os.makedirs("haber", exist_ok=True)

    try:
        req = urllib.request.Request(rss_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')

        news_cards_html = ""
        sitemap_urls = []

        # --- ADMATİC AUTO ADS REKLAM KODU ---
        admatic_code = '''
        <div class="ad-container">
            <!-- Admatic AUTO ads START -->
            <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
            <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
            <!-- Admatic AUTO ads END -->
        </div>
        '''

        tz_tr = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(tz_tr)
        last_update = now.strftime("%d.%m.%Y %H:%M")
        last_update_iso = now.strftime("%Y-%m-%dT%H:%M:%S+03:00")

        for idx, item in enumerate(items[:25]):
            title = item.find('title').text if item.find('title') is not None else 'Başlıksız'
            original_link = item.find('link').text if item.find('link') is not None else '#'
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            raw_desc = item.find('description').text if item.find('description') is not None else ''
            clean_desc = re.sub('<[^<]+?>', '', raw_desc)

            source_name = "Canlı Haber Akışı"
            clean_title = title
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                clean_title = parts[0]
                source_name = parts[1]

            time_str = pub_date[17:22] if len(pub_date) >= 22 else ""

            # SEO Uyumlu İç Link Yapısı
            slug = slugify(clean_title[:60])
            internal_page_name = f"{slug}-{idx+1}.html"
            internal_link = f"/haber/{internal_page_name}"
            full_internal_url = f"https://nearadin.net{internal_link}"

            sitemap_urls.append(full_internal_url)

            # -------------------------------------------------------------
            # 1. TEKİL HABER DETAY SAYFASINI ÜRET (/haber/haber-basligi.html)
            # -------------------------------------------------------------
            detail_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{clean_title} - nearadin.net Haber</title>
    <meta name="description" content="{clean_desc[:150]}..." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; padding-bottom: 40px; }}
        header {{ background-color: #0056b3; color: white; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; }}
        header a {{ color: white; text-decoration: none; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; }}
        .article-card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .meta-info {{ display: flex; gap: 10px; font-size: 13px; color: #65676b; margin-bottom: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        h1 {{ font-size: 22px; margin-bottom: 15px; color: #050505; line-height: 1.3; }}
        p {{ font-size: 15px; color: #333; margin-bottom: 20px; line-height: 1.6; }}
        .actions {{ display: flex; flex-direction: column; gap: 10px; margin-top: 25px; }}
        .btn {{ display: block; text-align: center; padding: 12px; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 14px; }}
        .btn-primary {{ background: #1877f2; color: white; }}
        .btn-secondary {{ background: #e4e6eb; color: #050505; }}
        .ad-container {{ margin: 20px 0; text-align: center; min-height: 100px; }}
    </style>
</head>
<body>
    <header>
        <a href="/">nearadin.net - Son Dakika</a>
    </header>
    <div class="container">
        <article class="article-card">
            <div class="meta-info">
                <span class="badge">SON DAKİKA</span>
                <span>Kaynak: <strong>{source_name}</strong></span>
                <span>Saat: <strong>{time_str}</strong></span>
            </div>
            <h1>{clean_title}</h1>
            <p>{clean_desc}</p>
            
            {admatic_code}

            <div class="actions">
                <a href="{original_link}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku ↗</a>
                <a href="/" class="btn btn-secondary">← Tüm Son Dakika Haberlerine Dön</a>
            </div>
        </article>
    </div>
</body>
</html>'''

            with open(f"haber/{internal_page_name}", "w", encoding="utf-8") as f:
                f.write(detail_html)

            # -------------------------------------------------------------
            # 2. ANASAYFA KARTINI OLUŞTUR (Sitenin İçi Linkiyle)
            # -------------------------------------------------------------
            news_cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <span class="badge">SON DAKİKA</span>
                    <span class="source">{source_name}</span>
                    <span class="time">{time_str}</span>
                </div>
                <h2 class="news-title">
                    <a href="{internal_link}">{clean_title}</a>
                </h2>
                <p class="news-summary">{clean_desc}</p>
                <div class="card-footer">
                    <a href="{internal_link}" class="read-btn">Detayı Oku →</a>
                </div>
            </article>
            '''

            if idx == 1:
                news_cards_html += admatic_code

        # -------------------------------------------------------------
        # 3. ANASAYFA (index.html) OLUŞTUR
        # -------------------------------------------------------------
        full_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nearadin.net - Son Dakika Haberleri ve Canlı Akış</title>
    <meta name="description" content="Türkiye ve dünyadan son dakika haberleri, güncel gelişmeler ve canlı haber akışı." />
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; padding-bottom: 30px; }}
        
        header {{ background-color: #0056b3; color: white; padding: 15px 20px; text-align: center; font-size: 20px; font-weight: bold; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; }}

        .widgets-nav {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px; scrollbar-width: none; }}
        .widgets-nav::-webkit-scrollbar {{ display: none; }}
        .widget-btn {{ background: white; padding: 8px 14px; border-radius: 20px; text-decoration: none; color: #333; font-weight: 600; font-size: 13px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; align-items: center; gap: 5px; white-space: nowrap; border: 1px solid #e4e6eb; }}
        .widget-btn:hover {{ background: #e7f3ff; color: #1877f2; border-color: #1877f2; }}

        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        
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

        .ad-container {{ background: white; border-radius: 10px; padding: 10px; margin-bottom: 12px; text-align: center; min-height: 100px; overflow: hidden; }}
    </style>
</head>
<body>

    <header>
        nearadin.net - SON DAKİKA
    </header>

    <div class="container">
        
        <div class="widgets-nav">
            <a href="/son-depremler/" class="widget-btn">🔴 Son Depremler</a>
            <a href="/kripto-para/" class="widget-btn">🪙 Kripto Piyasası</a>
            <a href="/hava-durumu/" class="widget-btn">☀️ Hava Durumu</a>
        </div>

        <div class="status-bar">
            <span>Kaynak: <strong>Google Canlı Akış</strong></span>
            <span>Son Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <main>
            {news_cards_html}
        </main>

    </div>

</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)

        # -------------------------------------------------------------
        # 4. SITEMAP.XML OLUŞTUR (Detay Sayfalarını İçerir)
        # -------------------------------------------------------------
        sitemap_items = f'''  <url>
    <loc>https://nearadin.net/</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>always</changefreq>
    <priority>1.0</priority>
  </url>\n'''

        for url in sitemap_urls:
            sitemap_items += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{last_update_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>\n'''

        sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}</urlset>'''

        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap_content)
            
        print("index.html, haber detay sayfaları ve sitemap.xml başarıyla oluşturuldu.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    fetch_and_generate()
