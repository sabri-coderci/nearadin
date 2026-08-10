import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re

def resolve_google_link(google_url):
    """
    Google News'in şifrelenmiş linklerini pure Python (HTTP) ile çözer.
    Ek kütüphane veya tarayıcı sürücüsü gerektirmez.
    """
    try:
        req = urllib.request.Request(
            google_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            final_url = response.geturl()
            if "news.google.com" not in final_url:
                return final_url
            
            # HTML içinden hedef URL'i regex ile yakalama (Fallback)
            html_content = response.read().decode('utf-8', errors='ignore')
            urls = re.findall(r'data-n-head-a2a="true" href="(.*?)"', html_content)
            if urls:
                return urls[0]
            urls_c = re.findall(r'c-wiz url="(.*?)"', html_content)
            if urls_c:
                return urls_c[0]
    except Exception as e:
        print(f"Link çözme uyarısı ({google_url[:30]}...): {e}")
    
    return google_url

def fetch_google_search_news():
    rss_url = "https://news.google.com/rss/search?q=haberler&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(rss_url, headers=headers)
    
    try:
        response = urllib.request.urlopen(req, timeout=15)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')

        cards_html = ""
        for item in items[:15]:
            title = item.find('title').text if item.find('title') is not None else 'Başlıksız'
            google_link = item.find('link').text if item.find('link') is not None else '#'

            # Orijinal habere çözme
            real_link = resolve_google_link(google_link)

            # Kaynak ve Başlık Ayıklama
            source_name = "Haber Akışı"
            clean_title = title
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                clean_title = parts[0]
                source_name = parts[1]

            # Link yönlendirmesi
            if "news.google.com" in real_link:
                redirect_link = real_link
            else:
                redirect_link = f"https://nearadin.net/url/?q={urllib.parse.quote(real_link)}"

            cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <span class="badge">SON DAKİKA</span>
                    <span class="source">{source_name}</span>
                </div>
                <h2 class="news-title">
                    <a href="{redirect_link}">{clean_title}</a>
                </h2>
                <div class="card-footer">
                    <a href="{redirect_link}" class="read-btn">Habere Git →</a>
                </div>
            </article>
            '''
        return cards_html

    except Exception as e:
        print(f"Veri Çekme Hatası: {e}")
        return "<p style='text-align:center; padding:20px;'>Haber akışı şu anda güncellenemiyor.</p>"

def generate_site():
    news_html = fetch_google_search_news()

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

    full_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nearadin.net - Son Dakika Haberleri</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.5; padding-bottom: 30px; }}
        header {{ background-color: #0056b3; color: white; padding: 15px 20px; text-align: center; font-size: 20px; font-weight: bold; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .container {{ max-width: 680px; margin: 0 auto; padding: 12px; }}
        .widgets-nav {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px; scrollbar-width: none; }}
        .widgets-nav::-webkit-scrollbar {{ display: none; }}
        .widget-btn {{ background: white; padding: 8px 14px; border-radius: 20px; text-decoration: none; color: #333; font-weight: 600; font-size: 13px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; align-items: center; gap: 5px; white-space: nowrap; border: 1px solid #e4e6eb; }}
        .widget-btn:hover {{ background: #e7f3ff; color: #1877f2; border-color: #1877f2; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 10px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-title a:hover {{ color: #1877f2; }}
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
    </style>
</head>
<body>
    <header>nearadin.net - SON DAKİKA</header>
    <div class="container">
        <div class="widgets-nav">
            <a href="/son-depremler/" class="widget-btn">🔴 Son Depremler</a>
            <a href="/kripto-para/" class="widget-btn">🪙 Kripto Piyasası</a>
            <a href="/hava-durumu/" class="widget-btn">☀️ Hava Durumu</a>
        </div>
        <div class="status-bar">
            <span>Kaynak: <strong>Canlı Arama Akışı</strong></span>
            <span>Son Güncelleme: <strong>{last_update}</strong></span>
        </div>
        <main>
            {news_html}
        </main>
    </div>
</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    generate_site()
