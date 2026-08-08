import urllib.request
import xml.etree.ElementTree as ET
import datetime
import html
import re

# Google News Türkiye RSS Akışı
RSS_URL = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"

def clean_summary(raw_html, max_chars=200):
    if not raw_html:
        return ""
    
    # 1. HTML etiketlerini ve Script/Style içeriklerini temizle
    text = re.sub(r'<script.*?>.*?</script>', '', raw_html, flags=re.DOTALL)
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text)
    
    # 2. HTML karakter kodlarını çöz (&nbsp;, &amp; vs.)
    text = html.unescape(text).strip()
    
    # 3. Fazla boşlukları ve yeni satırları temizle
    text = re.sub(r'\s+', ' ', text)
    
    # 4. Google News RSS özetinin sonundaki kaynak listesini temizle (örn: Hürriyet, Milliyet vb.)
    if ' font' in text:
        text = text.split(' font')[0]
        
    # 5. Belirlenen karakter sınırına göre kes
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + "..."
        
    return text

def fetch_and_generate():
    req = urllib.request.Request(
        RSS_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    response = urllib.request.urlopen(req)
    xml_data = response.read()
    
    root = ET.fromstring(xml_data)
    items = root.findall('./channel/item')
    
    news_html_cards = ""
    
    # 20 Adet haber işleniyor
    for item in items[:30]:
        title = item.find('title').text if item.find('title') is not None else 'Başlıksız Haber'
        link = item.find('link').text if item.find('link') is not None else '#'
        description = item.find('description').text if item.find('description') is not None else ''
        
        # Google News başlıklarındaki kaynak isimlerini temizleme
        clean_title = title.rsplit(' - ', 1)[0]
        
        # Türkçe haber özetini temizleme (Max 180 Karakter)
        summary = clean_summary(description, max_chars=180)
        
        # Eğer özet çekilemezse yedek Türkçe metin koy
        if not summary or len(summary) < 15:
            summary = "Gündemdeki son gelişmeler, sıcak başlıklar ve detaylar nearadin.net farkıyla anında yayında."
        
        news_html_cards += f'''
        <div class="card">
            <span class="badge">SON DAKİKA</span>
            <h2>{clean_title}</h2>
            <p>{summary}</p>
            <div class="card-footer">
                <a href="{link}" target="_blank" rel="noopener">Habere Git →</a>
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
<ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492"   class="adm-ads-area"></ins>
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

if __name__ == "__main__":
    fetch_and_generate()
