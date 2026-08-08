import urllib.request
import xml.etree.ElementTree as ET
import datetime

# Google News Türkiye RSS Akışı
RSS_URL = "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"

def fetch_and_generate():
    req = urllib.request.Request(
        RSS_URL, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    response = urllib.request.urlopen(req)
    xml_data = response.read()
    
    root = ET.fromstring(xml_data)
    items = root.findall('./channel/item')
    
    news_html_cards = ""
    
    # 20 Adet haber çekiliyor
    for item in items[:20]:
        title = item.find('title').text if item.find('title') is not None else 'Başlıksız Haber'
        link = item.find('link').text if item.find('link') is not None else '#'
        
        # Google News başlıklarındaki kaynak isimlerini temizleme
        clean_title = title.rsplit(' - ', 1)[0]
        
        # 'Habere Git' butonu JavaScript modal fonksiyonuna bağlandı
        news_html_cards += f'''
        <div class="card">
            <span class="badge">SON DAKİKA</span>
            <h2>{clean_title}</h2>
            <p>Gündemdeki son gelişmeler, sıcak başlıklar ve detaylar nearadin.net farkıyla anında yayında.</p>
            <div class="card-footer">
                <button class="read-btn" onclick="openNews('{link}', '{clean_title}')">Haberi Sitede Oku →</button>
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
        .card h2 {{ margin: 0 0 10px 0; font-size: 18px; color: #111; }}
        .card p {{ color: #666; font-size: 14px; margin-bottom: 15px; line-height: 1.5; }}
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #eee; padding-top: 10px; font-size: 13px; color: #888; }}
        .read-btn {{ background: #0056b3; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; font-size: 13px; font-weight: bold; }}
        .read-btn:hover {{ background: #004085; }}
        .widget-box {{ text-align: center; margin: 25px 0; }}

        /* Modal (Açılır Pencere) Stilleri */
        .modal-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center; }}
        .modal-content {{ background: white; width: 92%; max-width: 900px; height: 85vh; border-radius: 10px; display: flex; flex-direction: column; overflow: hidden; position: relative; }}
        .modal-header {{ background: #0056b3; color: white; padding: 12px 15px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; }}
        .modal-header h3 {{ margin: 0; font-size: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 65%; }}
        .modal-actions a {{ color: white; text-decoration: underline; margin-right: 12px; font-size: 13px; }}
        .close-btn {{ background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold; }}
        .modal-body {{ flex: 1; border: none; width: 100%; height: 100%; }}
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
        <script id="_wauvgw">var _wau = _wau || []; _wau.push(["dynamic", "7jdp69gi36", "vgw", "c4302bffffff", "small"]);</script>
        <script async src="//waust.at/d.js"></script>
    </div>

    <!-- Sitede Oku Açılır Penceresi (Modal) -->
    <div id="newsModal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Haber Detayı</h3>
                <div class="modal-actions">
                    <a id="externalLink" href="#" target="_blank">Orijinal Sayfada Aç ↗</a>
                    <button class="close-btn" onclick="closeNews()">Kapat ✖</button>
                </div>
            </div>
            <iframe id="newsFrame" class="modal-body" src=""></iframe>
        </div>
    </div>

    <script>
        function openNews(url, title) {{
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('newsFrame').src = url;
            document.getElementById('externalLink').href = url;
            document.getElementById('newsModal').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}

        function closeNews() {{
            document.getElementById('newsModal').style.display = 'none';
            document.getElementById('newsFrame').src = '';
            document.body.style.overflow = 'auto';
        }}
    </script>
</body>
</html>
'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    fetch_and_generate()
