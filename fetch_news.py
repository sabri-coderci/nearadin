import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Google Haberler - Son Dakika RSS Akışı
RSS_URL = "https://news.google.com/rss/search?q=sondakika&hl=tr&gl=TR&ceid=TR:tr"

def get_news():
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    xml_data = urllib.request.urlopen(req).read()
    root = ET.fromstring(xml_data)
    
    articles = []
    # En güncel 8 haberi çek
    for item in root.findall('./channel/item')[:20]:
        title = item.find('title').text if item.find('title') is not None else ""
        link = item.find('link').text if item.find('link') is not None else "#"
        
        # Başlık temizleme (örn: "Haber Başlığı - Gazete Adı" kısmından kaynak adını ayırma)
        source_name = "nearadin.net / Gündem"
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            title = parts[0]
            source_name = f"nearadin.net ({parts[1]})"

        articles.append({
            'title': title,
            'link': link,
            'source': source_name
        })
    return articles

def generate_html(articles):
    cards_html = ""
    for article in articles:
        cards_html += f"""
            <article class="news-card">
                <span class="news-tag">Son Dakika</span>
                <h3 class="news-title"><a href="{article['link']}" target="_blank" rel="noopener noreferrer">{article['title']}</a></h3>
                <p class="news-excerpt">Gündemdeki son gelişmeler, sıcak başlıklar ve detaylar nearadin.net farkıyla anında yayında.</p>
                <div class="news-footer">
                    <span class="news-source">{article['source']}</span> • Canlı Akış
                </div>
            </article>
        """

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

    html_template = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son Dakika Haberleri - nearadin.net</title>
    <meta name="description" content="nearadin.net ile en son dakika haberleri, Türkiye ve dünyadan sıcak gelişmeleri anında takip edin.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://nearadin.net/">
    <style>
        :root {{ --primary: #0056b3; --bg: #f4f6f9; --card-bg: #ffffff; --border: #e2e8f0; --text: #212529; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; line-height: 1.6; }}
        .header {{ background: var(--primary); color: #fff; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .container {{ max-width: 900px; margin: 20px auto; padding: 0 15px; }}
        .meta-bar {{ background: #fff; padding: 10px 15px; border-radius: 6px; border: 1px solid var(--border); margin-bottom: 20px; font-size: 14px; display: flex; justify-content: space-between; }}
        .news-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 18px; margin-bottom: 15px; }}
        .news-tag {{ background: #e9ecef; color: #d9534f; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }}
        .news-title {{ margin: 10px 0; font-size: 18px; }}
        .news-title a {{ color: var(--text); text-decoration: none; }}
        .news-title a:hover {{ color: var(--primary); }}
        .news-excerpt {{ font-size: 14px; color: #495057; }}
        .news-footer {{ font-size: 12px; color: #6c757d; border-top: 1px solid #f1f3f5; padding-top: 8px; margin-top: 10px; }}
        .news-source {{ font-weight: 600; color: var(--primary); }}
        .footer {{ text-align: center; padding: 20px; font-size: 13px; color: #6c757d; border-top: 1px solid var(--border); margin-top: 30px; }}
    </style>
</head>
<body>
    <header class="header">
        <h1>nearadin.net - SON DAKİKA</h1>
    </header>
    <div class="container">
        <div class="meta-bar">
            <span><strong>Kaynak:</strong> Canlı Haber Akışı</span>
            <span><strong>Son Güncelleme:</strong> {current_time}</span>
        </div>
        <div class="news-grid">
            {cards_html}
        </div>
        <footer class="footer">
            <p>&copy; 2026 nearadin.net - Tüm Hakları Saklıdır.</p>
        </footer>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    news_data = get_news()
    generate_html(news_data)
