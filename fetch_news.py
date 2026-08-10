import urllib.request
import urllib.parse
import json
import datetime
import os

def fetch_and_generate():
    # Google Özel Arama API Bilgileri
    api_key = os.environ.get("G_API_KEY", "AIzaSyDMEJ6_O7vYVwYJqmHYu9U_qr3UDO0DJow")
    cx_id = os.environ.get("G_CX", "a33464712b4234607")
    query = "haberler"
    
    # Custom Search API Endpoint
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx_id}&q={urllib.parse.quote(query)}&hl=tr"
    
    news_cards_html = ""
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read().decode('utf-8'))
        
        items = data.get('items', [])
        
        for item in items:
            title = item.get('title', 'Başlıksız')
            original_link = item.get('link', '#')
            snippet = item.get('snippet', '')
            
            # Yayıncı kaynak adını alma (Örn: haberturk.com)
            source_name = item.get('displayLink', 'Google Arama').replace('www.', '')

            # /url/?q= yönlendirme yapısı
            redirect_link = f"https://nearadin.net/url/?q={urllib.parse.quote(original_link)}"

            news_cards_html += f'''
            <article class="news-card">
                <div class="card-header">
                    <span class="badge">SON DAKİKA</span>
                    <span class="source">{source_name}</span>
                </div>
                <h2 class="news-title">
                    <a href="{redirect_link}">{title}</a>
                </h2>
                <p class="news-snippet">{snippet}</p>
                <div class="card-footer">
                    <a href="{redirect_link}" class="read-btn">Habere Git →</a>
                </div>
            </article>
            '''

    except Exception as e:
        print(f"Google Custom Search Hatası: {e}")
        news_cards_html = "<p style='text-align:center; padding:20px;'>Haber akışı şu anda yüklenemiyor.</p>"

    # Türkiye Saati (UTC+3)
    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

    # Ana Sayfa HTML Tasarımı
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

        /* Servis Butonları Paneli */
        .widgets-nav {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; padding-bottom: 5px; scrollbar-width: none; }}
        .widgets-nav::-webkit-scrollbar {{ display: none; }}
        .widget-btn {{ background: white; padding: 8px 14px; border-radius: 20px; text-decoration: none; color: #333; font-weight: 600; font-size: 13px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; align-items: center; gap: 5px; white-space: nowrap; border: 1px solid #e4e6eb; }}
        .widget-btn:hover {{ background: #e7f3ff; color: #1877f2; border-color: #1877f2; }}

        /* Güncelleme Bilgisi Bandı */
        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        
        /* Haber Kartları */
        .news-card {{ background: white; border-radius: 10px; padding: 16px; margin-bottom: 12px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: transform 0.1s ease; }}
        .news-card:active {{ transform: scale(0.99); }}
        
        .card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 6px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-title a:hover {{ color: #1877f2; }}

        .news-snippet {{ font-size: 13px; color: #4b4f56; margin-bottom: 10px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
        
        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
    </style>
</head>
<body>

    <header>
        nearadin.net - SON DAKİKA
    </header>

    <div class="container">
        
        <!-- Hızlı Servisler -->
        <div class="widgets-nav">
            <a href="/son-depremler/" class="widget-btn">🔴 Son Depremler</a>
            <a href="/kripto-para/" class="widget-btn">🪙 Kripto Piyasası</a>
            <a href="/hava-durumu/" class="widget-btn">☀️ Hava Durumu</a>
        </div>

        <!-- Güncelleme Zamanı -->
        <div class="status-bar">
            <span>Kaynak: <strong>Google Özel Arama</strong></span>
            <span>Son Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <!-- Haber Listesi -->
        <main>
            {news_cards_html}
        </main>

    </div>

</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("index.html Google Özel Arama verileriyle başarıyla yenilendi.")

if __name__ == "__main__":
    fetch_and_generate()
