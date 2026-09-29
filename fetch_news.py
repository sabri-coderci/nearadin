# --- DİNAMİK HESAPLAMALAR ---
        # Kelime sayısına göre tahmini okuma süresi (dakika)
word_count = len(news['desc'].split())
        reading_time = max(1, round(word_count / 40))  # Özet metinler için minimum 1 dk

        # Sosyal Medya Paylaşım Linkleri
        encoded_url = urllib.parse.quote(news['full_url'])
        encoded_title = urllib.parse.quote(news['title'])
        whatsapp_share = f"https://api.whatsapp.com/send?text={encoded_title}%20{encoded_url}"
        twitter_share = f"https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}"
        facebook_share = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
        telegram_share = f"https://t.me/share/url?url={encoded_url}&text={encoded_title}"

        # Haber Detay Sayfası (Geliştirilmiş Dinamik Yapı)
        detail_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{news['title']} - nearadin.net</title>
    <meta name="description" content="{news['desc'][:150]}..." />
    <link rel="canonical" href="{news['full_url']}" />

    <!-- Open Graph / Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{news['title']}" />
    <meta name="twitter:description" content="{news['desc'][:150]}..." />
    <meta name="twitter:site" content="@nearadin2026" />
    <meta name="twitter:image" content="https://nearadin.net/1789249176325.png" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{news['title']}" />
    <meta property="og:description" content="{news['desc'][:150]}..." />
    <meta property="og:url" content="{news['full_url']}" />
    <meta property="og:image" content="https://nearadin.net/1789249176325.png" />

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
          "url": "https://nearadin.net/1789249176325.png"
        }}
      }}
    }}
    </script>

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        
        /* Okuma İlerleme Çubuğu */
        #progress-bar {{ position: fixed; top: 0; left: 0; height: 4px; background: #1877f2; width: 0%; z-index: 9999; transition: width 0.1s ease; }}
        
        .container {{ max-width: 680px; margin: 20px auto 0 auto; padding: 0 12px; }}
        .article-card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); position: relative; }}
        
        .meta-info {{ display: flex; flex-wrap: wrap; gap: 8px 12px; font-size: 13px; color: #65676b; margin-bottom: 15px; align-items: center; border-bottom: 1px solid #f0f2f5; padding-bottom: 10px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 3px 8px; border-radius: 4px; font-size: 11px; text-transform: uppercase; text-decoration: none; }}
        .badge:hover {{ background: #ffd0cc; }}
        
        h1 {{ font-size: 22px; margin-bottom: 15px; color: #050505; line-height: 1.3; font-weight: 700; }}
        
        /* Okuma Araç Barı (Font / Sesli Okuma) */
        .reader-tools {{ display: flex; justify-content: space-between; align-items: center; background: #f7f8fa; padding: 8px 12px; border-radius: 6px; margin-bottom: 15px; font-size: 13px; }}
        .tool-btn {{ background: white; border: 1px solid #ccd0d5; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600; color: #333; }}
        .tool-btn:hover {{ background: #e4e6eb; }}
        
        #article-body {{ font-size: 16px; color: #333; margin-bottom: 20px; line-height: 1.7; transition: font-size 0.2s ease; }}
        
        /* Sosyal Paylaşım Butonları */
        .share-bar {{ display: flex; gap: 8px; margin: 20px 0; flex-wrap: wrap; }}
        .share-btn {{ flex: 1; min-width: 90px; text-align: center; padding: 8px; border-radius: 6px; color: white; text-decoration: none; font-size: 12px; font-weight: bold; }}
        .share-whatsapp {{ background: #25D366; }}
        .share-x {{ background: #000000; }}
        .share-facebook {{ background: #1877F2; }}
        .share-telegram {{ background: #0088cc; }}
        
        .actions {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; margin-bottom: 25px; }}
        .btn {{ display: block; text-align: center; padding: 12px; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 14px; }}
        .btn-primary {{ background: #1877f2; color: white; }}
        .btn-secondary {{ background: #e4e6eb; color: #050505; }}
        
        .related-news {{ background: #f7f8fa; border-radius: 8px; padding: 15px; border: 1px solid #e4e6eb; margin-top: 25px; }}
        .related-title {{ font-size: 16px; font-weight: 700; margin-bottom: 12px; color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 5px; }}
        .related-list {{ list-style: none; }}
    </style>
</head>

<body>
    <!-- Okuma İlerleme Çubuğu -->
    <div id="progress-bar"></div>

    <ins data-publisher="adm-pub-342021502" data-ad-network="6938571fadda546eb28ca492" class="adm-ads-area"></ins>
    <script type="text/javascript" src="https://static.cdn.admatic.com.tr/showad/showad.min.js"></script>
    
    {admatic_code}
    {header_html}

    <div class="container">
        <article class="article-card">
            <div class="meta-info">
                <a href="{news['category_link']}" class="badge">{news['category_name']}</a>
                <span>🕒 <strong>{news['date_str']} - {news['time']}</strong></span>
                <span>📰 <strong>{news['source']}</strong></span>
                <span>⏱️ <strong>~{reading_time} dk okuma</strong></span>
            </div>

            <h1>{news['title']}</h1>

            <!-- Etkileşim Araç Barı -->
            <div class="reader-tools">
                <div>
                    <span>Metin Boyutu:</span>
                    <button class="tool-btn" onclick="changeFontSize(-1)">A-</button>
                    <button class="tool-btn" onclick="changeFontSize(1)">A+</button>
                </div>
                <button class="tool-btn" id="ttsBtn" onclick="toggleSpeech()">🔊 Sesli Dinle</button>
            </div>

            <p id="article-body">{news['desc']}</p>

            <!-- Sosyal Paylaşım -->
            <div class="share-bar">
                <a href="{whatsapp_share}" target="_blank" class="share-btn share-whatsapp">WhatsApp</a>
                <a href="{twitter_share}" target="_blank" class="share-btn share-x">X'te Paylaş</a>
                <a href="{facebook_share}" target="_blank" class="share-btn share-facebook">Facebook</a>
                <a href="{telegram_share}" target="_blank" class="share-btn share-telegram">Telegram</a>
            </div>

            <div class="actions">
                <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn btn-primary">Kaynaktan Orijinal Haberi Oku ↗</a>
                <a href="{news['category_link']}" class="btn btn-secondary">← {news['category_name']} ({news['date_str']}) Haberlerine Dön</a>
            </div>

            <!-- Disqus Yorum Alanı -->
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

    <!-- İstemci Tarafı Dinamik JS İşlevleri -->
    <script>
        // Sayfa İlerleme Çubuğu (Reading Progress)
        window.onscroll = function() {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("progress-bar").style.width = scrolled + "%";
        }};

        // Font Boyutu Değiştirme
        let currentFontSize = 16;
        function changeFontSize(delta) {{
            currentFontSize += delta;
            if (currentFontSize < 13) currentFontSize = 13;
            if (currentFontSize > 22) currentFontSize = 22;
            document.getElementById("article-body").style.fontSize = currentFontSize + "px";
        }}

        // Metni Sesli Okuma (Text-To-Speech)
        let isSpeaking = false;
        function toggleSpeech() {{
            const btn = document.getElementById("ttsBtn");
            if ('speechSynthesis' in window) {{
                if (isSpeaking) {{
                    window.speechSynthesis.cancel();
                    isSpeaking = false;
                    btn.innerText = "🔊 Sesli Dinle";
                }} else {{
                    const text = document.getElementById("article-body").innerText;
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'tr-TR';
                    utterance.onend = function() {{
                        isSpeaking = false;
                        btn.innerText = "🔊 Sesli Dinle";
                    }};
                    window.speechSynthesis.speak(utterance);
                    isSpeaking = true;
                    btn.innerText = "⏹️ Durdur";
                }}
            }} else {{
                alert("Tarayıcınız sesli okuma özelliğini desteklemiyor.");
            }}
        }}
    </script>
</body>
</html>'''
