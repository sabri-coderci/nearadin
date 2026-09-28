import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import os
import html
import json
import time
import hashlib
import shutil
from email.utils import parsedate_to_datetime

def slugify(text):
    text = text.lower()
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c',
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text


# ============================================================
#  AYARLAR
# ============================================================
SITE_URL = "https://nearadin.net"
DEFAULT_IMAGE = SITE_URL + "/1789249176325.png"

# True  -> haber detay sayfaları Google'a açık (index, follow)
INDEX_ARTICLE_PAGES = True

# Kaç günden eski haber sayfaları silinsin? None = hiç silme.
RETENTION_DAYS = 60

# Spam / sahte yayın siteleri (RSS <source> alan adı veya kaynak adı)
BLOCKED_SOURCES = {"jcyl.es"}

_SPAM_PATTERNS = [
    r"[\U0001D400-\U0001D7FF]",
    r"\$#\s*[=→>]",
    r"\[%!",
    r"CANLI-YAYIN\]",
    r"TRT1-CANLI\+",
    r"sel[cç]uk\s*sports",
]
SPAM_RE = re.compile("|".join(_SPAM_PATTERNS), re.IGNORECASE)

TWEET_TIME_FILE = "tweet_last.txt"


# ============================================================
#  YARDIMCI VE SEO FONKSİYONLARI
# ============================================================
def esc(text):
    return html.escape(text or "", quote=True)


def is_spam(title, source_name="", source_url=""):
    host = urllib.parse.urlparse(source_url or "").netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    name = (source_name or "").strip().lower()
    for blocked in BLOCKED_SOURCES:
        if blocked in (host, name) or (host and host.endswith("." + blocked)):
            return True
    return bool(SPAM_RE.search(title or ""))


def fetch_full_article_content(url):
    """
    Hedef haber linkine giderek HTML içerikten ana paragraf ve resim bilgilerini çeker.
    Google botlarının indekslemesi için zenginleştirilmiş içerik sağlar.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }
    paragraphs = []
    image_url = DEFAULT_IMAGE
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html_content = resp.read().decode('utf-8', errors='ignore')
            
            # Görsel çekme (og:image kontrolü)
            og_img = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_content, re.I)
            if not og_img:
                og_img = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html_content, re.I)
            if og_img:
                image_url = og_img.group(1)

            # Metin temizleme (p etiketlerini topla)
            raw_p = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.I)
            for p in raw_p:
                clean_p = re.sub(r'<[^>]+>', '', p)
                clean_p = html.unescape(clean_p).strip()
                if len(clean_p) > 60 and not any(x in clean_p.lower() for x in ["tıklayınız", "abone ol", "çerez", "copyright"]):
                    paragraphs.append(clean_p)
                if len(paragraphs) >= 4:
                    break
    except Exception:
        pass

    return paragraphs, image_url


def rewrite_text_for_seo(title, paragraphs, source, category, date_str):
    """
    Çekilen paragraf verilerini SEO uyumlu, anahtar kelime destekli metne dönüştürür.
    """
    if paragraphs:
        main_body = " ".join(paragraphs)
    else:
        main_body = f"{title} ile ilgili öne çıkan tüm detaylar ve son gelişmeler kamuoyunun ilgisine sunuldu."

    intro = f"<strong>{title}</strong> gelişmesi, {category} alanında son dakika haberleri arasında yer aldı. {source} kaynaklarına göre edinilen bilgi doğrultusunda, {date_str} tarihi itibarıyla konuyla ilgili öne çıkan detaylar netleşmeye başladı."
    
    body = f"<p>{intro}</p><p>{main_body}</p>"
    
    closing = f"<p>Güncel {category} haberleri ve son dakika gelişmeleri için sitemizi takip etmeye devam edebilir, konu hakkındaki düşüncelerinizi yorum kısmından iletebilirsiniz.</p>"
    
    return body + closing


def make_keywords(news):
    words = re.findall(r"[A-Za-zÇĞİıÖŞÜçğıöşü]{4,}", news['title'])
    seen, out = set(), []
    for w in words:
        lw = w.lower()
        if lw not in seen:
            seen.add(lw)
            out.append(w)
        if len(out) >= 6:
            break
    out.append(news['category_name'])
    out.append("son dakika")
    out.append("güncel haberler")
    return ", ".join(out)


def make_meta_desc(news):
    desc = news.get("clean_body_text", news['title'])
    clean = re.sub(r'<[^>]+>', '', desc)
    if len(clean) < 60:
        clean = f"{news['title']} — {news['source']} kaynaklı {news['category_name']} haberinin detayları ve tüm gelişmeler."
    return clean[:160].replace('"', '')


def json_ld(data):
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'    <script type="application/ld+json">{payload}</script>\n'


def seo_head(title, description, canonical, og_type="website",
             robots="index, follow, max-image-preview:large", image=DEFAULT_IMAGE):
    t = esc(title)
    d = esc(description)
    c = esc(canonical)
    img = esc(image)
    return f'''    <meta name="description" content="{d}" />
    <meta name="robots" content="{robots}" />
    <link rel="canonical" href="{c}" />
    <meta property="og:site_name" content="nearadin.net" />
    <meta property="og:locale" content="tr_TR" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:title" content="{t}" />
    <meta property="og:description" content="{d}" />
    <meta property="og:url" content="{c}" />
    <meta property="og:image" content="{img}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{t}" />
    <meta name="twitter:description" content="{d}" />
    <meta name="twitter:site" content="@nearadin2026" />
    <meta name="twitter:image" content="{img}" />
'''


def normalize_entry(item):
    for key in ("internal_link", "category_link", "full_url", "canonical_url"):
        if isinstance(item.get(key), str):
            item[key] = re.sub(r"\s+/", "/", item[key])
    if isinstance(item.get("category_slug"), str):
        item["category_slug"] = item["category_slug"].strip()
    return item


def _sm_url(loc, lastmod=None):
    safe_loc = html.escape(urllib.parse.quote(loc, safe=":/%?=&-._~"), quote=False)
    out = f"  <url>\n    <loc>{safe_loc}</loc>\n"
    if lastmod:
        out += f"    <lastmod>{lastmod}</lastmod>\n"
    return out + "  </url>\n"


def _write_urlset(path, entries):
    body = "".join(_sm_url(loc, lm) for loc, lm in entries)
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + body + '</urlset>\n')


def write_sitemaps(static_entries, article_entries, now_iso):
    index_items = []
    _write_urlset("sitemap-pages.xml", static_entries)
    index_items.append(("sitemap-pages.xml", now_iso))

    by_month = {}
    for loc, lastmod in article_entries.items():
        m = re.search(r"/(\d{4})/(\d{2})/\d{2}/", loc)
        key = f"{m.group(1)}-{m.group(2)}" if m else "diger"
        by_month.setdefault(key, []).append((loc, lastmod))

    for key in sorted(by_month):
        items = sorted(by_month[key])
        for part, start in enumerate(range(0, len(items), 40000), start=1):
            name = f"sitemap-{key}.xml" if part == 1 else f"sitemap-{key}-{part}.xml"
            chunk = items[start:start + 40000]
            _write_urlset(name, chunk)
            index_items.append((name, max(lm for _, lm in chunk)))

    body = "".join(
        f"  <sitemap>\n    <loc>{SITE_URL}/{name}</loc>\n    <lastmod>{lm}</lastmod>\n  </sitemap>\n"
        for name, lm in index_items
    )
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + body + '</sitemapindex>\n')


def ensure_robots_txt():
    sitemap_lines = f"Sitemap: {SITE_URL}/sitemap.xml\nSitemap: {SITE_URL}/news-sitemap.xml\n"
    if not os.path.exists("robots.txt"):
        with open("robots.txt", "w", encoding="utf-8") as f:
            f.write("User-agent: *\nAllow: /\n\n" + sitemap_lines)
        return
    with open("robots.txt", "r", encoding="utf-8") as f:
        content = f.read()
    if "sitemap:" not in content.lower():
        with open("robots.txt", "a", encoding="utf-8") as f:
            f.write(("" if content.endswith("\n") else "\n") + "\n" + sitemap_lines)


def get_header_html(title_text="nearadin.net - SON DAKİKA"):
    return f'''
    <header style="background-color: #0056b3; color: white; padding: 12px 20px; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
        <a href="/" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">{title_text}</a>
    </header>
    '''


def get_footer_html():
    return '''
    <footer style="background-color: #1c1e21; color: #90949c; padding: 30px 15px; margin-top: 40px; font-size: 13px; line-height: 1.6;">
        <div style="max-width: 680px; margin: 0 auto; text-align: center;">
            <p>© 2026 nearadin.net - Tüm Hakları Saklıdır.</p>
        </div>
    </footer>
    '''


# ============================================================
#  ANA HABER TOPLAMA VE SAYFA ÜRETİM MOTORU
# ============================================================
def fetch_and_generate():
    RAW_CATEGORIES = {
        "gundem": {"name": "Gündem", "url": "https://news.google.com/rss/search?q=g%C3%BCndem&hl=tr&gl=TR&ceid=TR:tr"},
        "dunya": {"name": "Dünya", "url": "https://news.google.com/rss/search?q=d%C3%BCnya&hl=tr&gl=TR&ceid=TR:tr"},
        "ekonomi": {"name": "Ekonomi", "url": "https://news.google.com/rss/search?q=ekonomi&hl=tr&gl=TR&ceid=TR:tr"},
        "teknoloji": {"name": "Teknoloji", "url": "https://news.google.com/rss/search?q=teknoloji&hl=tr&gl=TR&ceid=TR:tr"},
        "spor": {"name": "Spor", "url": "https://news.google.com/rss/search?q=spor&hl=tr&gl=TR&ceid=TR:tr"},
        "saglik": {"name": "Sağlık", "url": "https://news.google.com/rss/search?q=sa%C4%9Fl%C4%B1k&hl=tr&gl=TR&ceid=TR:tr"},
        "deprem": {"name": "Deprem", "url": "https://news.google.com/rss/search?q=deprem&hl=tr&gl=TR&ceid=TR:tr"},
        "bilim": {"name": "Bilim", "url": "https://news.google.com/rss/search?q=bilim&hl=tr&gl=TR&ceid=TR:tr"},
        "istanbul-haber": {"name": "İstanbul Haber", "url": "https://news.google.com/rss/search?q=istanbul+haber&hl=tr&gl=TR&ceid=TR:tr"},
        "ankara-haber": {"name": "Ankara Haber", "url": "https://news.google.com/rss/search?q=ankara+haber&hl=tr&gl=TR&ceid=TR:tr"},
        "izmir-haber": {"name": "İzmir Haber", "url": "https://news.google.com/rss/search?q=izmir+haber&hl=tr&gl=TR&ceid=TR:tr"},
        "son-dakika": {"name": "Son Dakika", "url": "https://news.google.com/rss/search?q=son+dakika&hl=tr&gl=TR&ceid=TR:tr"}
    }

    # Kategori adlarındaki boşluk hatalarını temizle
    CATEGORIES = {k.strip(): v for k, v in RAW_CATEGORIES.items()}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(datetime.timezone.utc)
    
    last_update_iso = datetime.datetime.now(tz_tr).strftime("%Y-%m-%dT%H:%M:%S+03:00")
    footer_html = get_footer_html()
    header_html = get_header_html()

    parsed_items = []

    for cat_slug, cat_info in CATEGORIES.items():
        try:
            req = urllib.request.Request(cat_info["url"], headers=headers)
            response = urllib.request.urlopen(req, timeout=15)
            root = ET.fromstring(response.read())

            for item in root.findall('./channel/item'):
                _t = item.find('title')
                _raw_title = html.unescape(_t.text) if (_t is not None and _t.text) else ''
                _s = item.find('source')
                _src_name = (_s.text or '') if _s is not None else _raw_title.rsplit(' - ', 1)[-1]
                _src_url = _s.get('url', '') if _s is not None else ''

                if is_spam(_raw_title, _src_name, _src_url):
                    continue

                pub_date_raw = item.find('pubDate').text if item.find('pubDate') is not None else ''
                pub_datetime = now
                if pub_date_raw:
                    try:
                        pub_datetime = parsedate_to_datetime(pub_date_raw)
                    except Exception:
                        pass

                # Son 24 saatin haberleri
                if (now - pub_datetime.astimezone(datetime.timezone.utc)).total_seconds() <= 86400:
                    parsed_items.append({
                        'item': item,
                        'pub_datetime': pub_datetime,
                        'category_slug': cat_slug,
                        'category_name': cat_info["name"]
                    })
        except Exception as e:
            print(f"Hata ({cat_info['name']}): {e}")
            continue

    parsed_items.sort(key=lambda x: x['pub_datetime'], reverse=True)
    parsed_items = parsed_items[:100]  # Performans ve indeks hızı için sınır

    news_list = []
    seen_titles = {}

    for idx, entry in enumerate(parsed_items):
        item = entry['item']
        pub_datetime = entry['pub_datetime']
        cat_slug = entry['category_slug']
        cat_name = entry['category_name']

        title = item.find('title').text if item.find('title') is not None else ''
        original_link = item.find('link').text if item.find('link') is not None else '#'
        clean_title = html.unescape(title)

        source_name = "Haber Merkezi"
        if " - " in clean_title:
            parts = clean_title.rsplit(" - ", 1)
            clean_title = parts[0]
            source_name = parts[1]

        dt_tr = pub_datetime.astimezone(tz_tr)
        date_folder = dt_tr.strftime("%Y/%m/%d")
        date_str = dt_tr.strftime("%d.%m.%Y")
        time_str = dt_tr.strftime("%H:%M")
        
        os.makedirs(f"{cat_slug}/{date_folder}", exist_ok=True)

        # 1. ORİJİNAL İÇERİĞİ ÇEK VE ÖZGÜNLEŞTİR (Scraping + Content Enrichment)
        paragraphs, image_url = fetch_full_article_content(original_link)
        content_html = rewrite_text_for_seo(clean_title, paragraphs, source_name, cat_name, date_str)

        slug = slugify(clean_title[:60]) or hashlib.md5(original_link.encode('utf-8')).hexdigest()[:10]
        page_name = f"{slug}.html"
        internal_link = f"/{cat_slug}/{date_folder}/{page_name}"
        category_link = f"/{cat_slug}/{date_folder}/"
        full_url = f"{SITE_URL}{internal_link}"

        _tkey = slugify(clean_title)
        canonical_url = seen_titles.get(_tkey, full_url)
        seen_titles[_tkey] = canonical_url

        news_data = {
            "idx": idx,
            "title": clean_title,
            "original_link": original_link,
            "content_html": content_html,
            "image_url": image_url,
            "source": source_name,
            "time": time_str,
            "date_str": date_str,
            "date_folder": date_folder,
            "page_name": page_name,
            "internal_link": internal_link,
            "category_link": category_link,
            "full_url": full_url,
            "canonical_url": canonical_url,
            "iso_date": dt_tr.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "category_slug": cat_slug,
            "category_name": cat_name
        }

        news_data["keywords"] = make_keywords(news_data)
        news_data["meta_desc"] = make_meta_desc(news_data)
        news_list.append(news_data)

    # PAGE & ARTICLE HTML GENERATION
    for news in news_list:
        article_head = seo_head(f"{news['title']} - nearadin.net", news['meta_desc'],
                                news['canonical_url'], og_type="article", image=news['image_url'])
        
        # Schema - NewsArticle
        article_head += json_ld({
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": news['title'][:110],
            "description": news['meta_desc'],
            "image": [news['image_url']],
            "datePublished": news['iso_date'],
            "dateModified": news['iso_date'],
            "inLanguage": "tr",
            "articleSection": news['category_name'],
            "keywords": news['keywords'],
            "mainEntityOfPage": {"@type": "WebPage", "@id": news['canonical_url']},
            "author": {"@type": "Organization", "name": news['source']},
            "publisher": {"@type": "Organization", "name": "nearadin.net", "logo": {"@type": "ImageObject", "url": DEFAULT_IMAGE}},
        })

        detail_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(news['title'])} - nearadin.net</title>
{article_head}
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; margin:0; padding:0; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; }}
        .article-card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; }}
        h1 {{ font-size: 22px; margin-bottom: 15px; color: #050505; }}
        .meta-info {{ font-size: 13px; color: #65676b; margin-bottom: 12px; }}
        .btn {{ display: inline-block; padding: 10px 15px; background: #1877f2; color: white; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
    </style>
</head>
<body>
    {header_html}
    <div class="container">
        <article class="article-card">
            <div class="meta-info">Kategori: <strong>{news['category_name']}</strong> | Kaynak: <strong>{esc(news['source'])}</strong></div>
            <h1>{esc(news['title'])}</h1>
            <img src="{news['image_url']}" alt="{esc(news['title'])}" style="width:100%; border-radius:8px; margin-bottom:15px;" />
            <div>{news['content_html']}</div>
            <a href="{news['original_link']}" target="_blank" rel="nofollow noopener" class="btn">Kaynaktan Orijinal İçeriği Göre Oku ↗</a>
        </article>
    </div>
    {footer_html}
</body>
</html>'''

        file_path = f"{news['category_slug']}/{news['date_folder']}/{news['page_name']}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(detail_html)

    # --- GOOGLE NEWS SITEMAP GENERATION (Son 48 saat kuralına uygun) ---
    news_sitemap_items = ""
    for news in news_list:
        if news.get('canonical_url', news['full_url']) != news['full_url']:
            continue
        safe_title = html.escape(news['title'])
        news_sitemap_items += f'''  <url>
    <loc>{news['full_url']}</loc>
    <news:news>
      <news:publication>
        <news:name>nearadin.net</news:name>
        <news:language>tr</news:language>
      </news:publication>
      <news:publication_date>{news['iso_date']}</news:publication_date>
      <news:title>{safe_title}</news:title>
    </news:news>
  </url>\n'''

    news_sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{news_sitemap_items}</urlset>'''

    with open("news-sitemap.xml", "w", encoding="utf-8") as f:
        f.write(news_sitemap_content)

    # Sitemaps ve Robots Güncelleme
    static_entries = [(SITE_URL + "/", last_update_iso)]
    article_entries = {n['full_url']: n['iso_date'] for n in news_list}
    write_sitemaps(static_entries, article_entries, last_update_iso)
    ensure_robots_txt()

    print("Google SEO için Tam Optimize Edilmiş İçerik ve Sitemapler Başarıyla Oluşturuldu.")

if __name__ == "__main__":
    fetch_and_generate()
