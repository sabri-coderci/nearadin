import os
import sys
import datetime
import openpyxl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def generate_secim_anketi_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, "anket_verileri.xlsx")
    output_html_path = os.path.join(current_dir, "index.html")

    poll_results = []
    total_votes = 0

    # Excel dosyasından veri okuma
    if os.path.exists(excel_path):
        try:
            wb = openpyxl.load_workbook(excel_path)
            sheet = wb.active
            
            # 2. satırdan başlayarak tüm verileri oku (1. satır başlık)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row and row[0] is not None:
                    code = str(row[0]).strip()
                    name = str(row[1]).strip()
                    percent = float(row[2])
                    votes = int(row[3])
                    color = str(row[4]).strip()
                    
                    total_votes += votes
                    poll_results.append({
                        "code": code,
                        "name": name,
                        "percent": percent,
                        "votes": votes,
                        "color": color
                    })
        except Exception as e:
            print(f"⚠️ Excel dosyası okunurken hata oluştu: {e}")

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

    poll_bars_html = ""
    for party in poll_results:
        poll_bars_html += f'''
        <div style="margin-bottom: 12px; padding: 12px; border: 1px solid #e4e6eb; border-radius: 8px; background: #fff;">
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; margin-bottom: 6px;">
                <span>{party['name']} ({party['code']})</span>
                <span style="color: {party['color']};">%{party['percent']}</span>
            </div>
            <div style="background: #e4e6eb; height: 16px; border-radius: 8px; overflow: hidden;">
                <div style="background: {party['color']}; width: {party['percent']}%; height: 100%; border-radius: 8px;"></div>
            </div>
            <div style="font-size: 12px; color: #65676b; text-align: right; margin-top: 6px;">Oy Sayısı: {party['votes']:,}</div>
        </div>
        '''

    poll_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Son Seçim Anketi Sonuçları - nearadin.net</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 15px auto; padding: 0 12px; min-height: 70vh; }}
        .status-bar {{ background: #ffffff; border-radius: 8px; padding: 10px 14px; margin-bottom: 15px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px; font-size: 13px; color: #4b4f56; border: 1px solid #e4e6eb; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 15px; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 4px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin-bottom: 10px; }}
        h1 {{ font-size: 20px; margin-bottom: 12px; color: #050505; font-weight: 700; }}
        .total-box {{ background: #f7f8fa; border-left: 4px solid #1877f2; padding: 12px 15px; border-radius: 0 8px 8px 0; margin: 15px 0; font-size: 13px; color: #4b4f56; }}
        .btn-home {{ display: block; width: 100%; background: #1877f2; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 15px; text-align: center; }}
    </style>
</head>
<body>
    {admatic_code}
    {header_html}

    <div class="container">
        <div class="status-bar">
            <div>Veri Kaynağı: <strong>Excel Veri Tablosu</strong></div>
            <div>Son Güncelleme: <strong>{last_update}</strong></div>
        </div>

        <article class="card">
            <span class="badge">🔴 GÜNCEL ANKET VERİLERİ</span>
            <h1>Son Seçim Anketi Sonuçları ve Oy Dağılımı</h1>
            
            <div class="total-box">
                📊 <strong>Toplam Örneklem:</strong> <strong>{total_votes:,}</strong> oy değerlendirilmiştir.
            </div>

            {poll_bars_html if poll_bars_html else '<p>Anket verileri bulunamadı.</p>'}

            {admatic_code}

            <a href="/" class="btn-home">← Anasayfaya Dön</a>
        </article>

        {whos_amung_us_code}
    </div>

    {footer_html}
</body>
</html>'''

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(poll_html)
    print("✅ Excel verileriyle /secim-anketi/index.html başarıyla oluşturuldu.")

if __name__ == "__main__":
    header_html = ""
    footer_html = ""
    whos_amung_us_code = ""
    admatic_code = ""

    try:
        from fetch_news import get_header_html, footer_html, whos_amung_us_code, admatic_code
        header_html = get_header_html("nearadin.net - Seçim Anketi")
    except ImportError:
        header_html = '<header style="background:#1877f2;padding:16px;color:#ffffff;text-align:center;"><h2 style="color:#ffffff;margin:0;">nearadin.net</h2></header>'
        footer_html = '<footer style="text-align:center;padding:20px;color:#65676b;">© nearadin.net</footer>'

    generate_secim_anketi_page(header_html, footer_html, whos_amung_us_code, admatic_code)
