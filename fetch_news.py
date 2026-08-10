import urllib.request
import urllib.parse
import json
import datetime

# --- GOOGLE CUSTOM SEARCH BİLGİLERİNİZ ---
# Buradaki tırnak içine kendi API Key ve CX değerinizi yapıştırın:
GOOGLE_API_KEY = "AIzaSyDMEJ6_O7vYVwYJqmHYu9U_qr3UDO0DJow" 
SEARCH_ENGINE_CX = "a33464712b4234607" 

def fetch_google_custom_search(query="haberler"):
    """
    Google Custom Search JSON API kullanarak q=haberler araması yapar.
    Doğrudan haber sitelerinin kendi (yalın) URL'lerini döndürür.
    """
    encoded_query = urllib.parse.quote(query)
    
    url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_CX}&hl=tr&gl=tr&num=10"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])

            cards_html = ""
            for item in items:
                clean_title = item.get('title', 'Başlıksız')
                real_link = item.get('link', '#')
                display_link = item.get('displayLink', 'Haber Kaynağı')

                # Link doğrudan sizin /url/?q= yönlendiricinize bağlanır.
                # Custom Search kullandığımız için real_link zaten doğrudan orijinal sitedir (sozcu, birgun vb.)
                redirect_link = f"https://nearadin.net/url/?q={urllib.parse.quote(real_link)}"

                cards_html += f'''
                <article class="news-card">
                    <div class="card-header">
                        <span class="badge">ARAMA SONUCU</span>
                        <span class="source">{display_link}</span>
                    </div>
                    <h2 class="news-title">
                        <a href="{redirect_link}">{clean_title}</a>
                    </h2>
                    <div class="card-footer">
                        <a href="{redirect_link}" class="read-btn">Sonuca Git →</a>
                    </div>
                </article>
                '''
            return cards_html if cards_html else "<p style='text-align:center; padding:20px;'>Sonuç bulunamadı.</p>"

    except Exception as e:
        print(f"API Arama Hatası: {e}")
        return f"<p style='text-align:center; padding:20px;'>Arama sonuçları yüklenemedi. (Hata: {e})</p>"

def generate_site():
    search_html = fetch_google_custom_search(query="haberler")

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

    full_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nearadin.net - Canlı Arama Sonuçları</title>
    <meta name="description" content="nearadin.net canlı arama sonuçları ve haber akışı." />
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
        .badge {{ background: #e7f3ff; color: #1877f2; font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .source {{ font-weight: 600; color: #4b4f56; }}
        
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.4; margin-bottom: 10px; }}
        .news-title a {{ color: #050505; text-decoration: none; }}
        .news-title a:hover {{ color: #1877f2; }}

        .card-footer {{ display: flex; justify-content: flex-end; }}
        .read-btn {{ color: #1877f2; font-weight: 600; text-decoration: none; font-size: 13px; }}
    </style>
</head>
<body>

    <header>nearadin.net - CANLI ARAMA</header>

    <div class="container">
        <div class="widgets-nav">
            <a href="/son-depremler/" class="widget-btn">🔴 Son Depremler</a>
            <a href="/kripto-para/" class="widget-btn">🪙 Kripto Piyasası</a>
            <a href="/hava-durumu/" class="widget-btn">☀️ Hava Durumu</a>
        </div>

        <div class="status-bar">
            <span>Sorgu: <strong>q=haberler</strong></span>
            <span>Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <main>
            {search_html}
        </main>
    </div>

</body>
</html>'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    generate_site()
