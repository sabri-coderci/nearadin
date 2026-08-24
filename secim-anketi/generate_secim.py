import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def generate_secim_anketi_page(header_html, footer_html, whos_amung_us_code, admatic_code):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_html_path = os.path.join(current_dir, "index.html")

    tz_tr = datetime.timezone(datetime.timedelta(hours=3))
    last_update = datetime.datetime.now(tz_tr).strftime("%d.%m.%Y %H:%M")

    poll_html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canlı Seçim Anketi - Oy Kullan ve Sonuçları Gör - nearadin.net</title>
    <meta name="description" content="Canlı seçim anketi! Oyunu kullan, partilerin anlık oy oranlarını ve seçim sonuçlarını canlı takip et." />
    <link rel="canonical" href="https://nearadin.net/secim-anketi/" />

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; line-height: 1.6; }}
        .container {{ max-width: 680px; margin: 20px auto; padding: 0 12px; min-height: 70vh; }}
        
        .card {{ background: white; border-radius: 10px; padding: 20px; border: 1px solid #e4e6eb; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 15px; }}
        .status-bar {{ background: white; border-radius: 8px; padding: 10px 15px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #65676b; border: 1px solid #e4e6eb; }}
        .badge {{ background: #ffebe9; color: #d93025; font-weight: bold; padding: 3px 8px; border-radius: 4px; font-size: 11px; display: inline-block; margin-bottom: 10px; }}
        
        h1 {{ font-size: 22px; margin-bottom: 12px; color: #050505; line-height: 1.3; }}
        h2 {{ font-size: 17px; margin: 18px 0 10px 0; color: #0056b3; border-bottom: 2px solid #e4e6eb; padding-bottom: 5px; }}
        p {{ font-size: 14px; color: #333; margin-bottom: 12px; line-height: 1.6; }}
        
        .total-box {{ background: #f7f8fa; border-left: 4px solid #1877f2; padding: 12px 15px; border-radius: 0 8px 8px 0; margin: 15px 0; font-size: 13px; color: #4b4f56; }}
        
        .party-item {{ margin-bottom: 15px; padding: 10px; border: 1px solid #e4e6eb; border-radius: 8px; background: #fff; }}
        .party-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-weight: bold; font-size: 14px; }}
        .progress-bg {{ background: #e4e6eb; height: 18px; border-radius: 9px; overflow: hidden; position: relative; }}
        .progress-bar {{ height: 100%; border-radius: 9px; transition: width 0.5s ease; width: 0%; }}
        .party-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 6px; font-size: 12px; color: #65676b; }}
        
        .vote-btn {{ background: #1877f2; color: white; border: none; padding: 6px 14px; border-radius: 6px; font-weight: bold; font-size: 12px; cursor: pointer; transition: 0.2s; }}
        .vote-btn:hover {{ background: #166fe5; }}
        .vote-btn:disabled {{ background: #bcc0c4; cursor: not-allowed; }}
        
        .btn-home {{ display: inline-block; background: #1877f2; color: white; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 15px; text-align: center; }}
        #voted-alert {{ display: none; background: #e7f3ff; color: #1877f2; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 13px; font-weight: bold; text-align: center; }}
    </style>

    <!-- Firebase SDK Entegrasyonu -->
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-database-compat.js"></script>
</head>
<body>
    
    {admatic_code}
    {header_html}

    <div class="container">
        <div class="status-bar">
            <span>Veri Kaynağı: <strong>Canlı Kullanıcı Oylaması</strong></span>
            <span>Güncelleme: <strong>{last_update}</strong></span>
        </div>

        <article class="card">
            <span class="badge">🔴 INTERAKTİF CANLI ANKET</span>
            <h1>Seçim Anketi: Oyunu Kullan, Anlık Sonuçları Gör</h1>
            
            <p>Aşağıdaki listeden desteklediğiniz siyasi partiye oy vererek canlı anket sonuçlarına anında katkıda bulunabilirsiniz.</p>

            <div id="voted-alert">✅ Oyunuz başarıyla kaydedildi! Teşekkür ederiz.</div>

            <div class="total-box">
                📊 <strong>Toplam Kullanılan Oy:</strong> <span id="total-votes-count">Yükleniyor...</span>
            </div>

            <h2>🗳️ Parti Bazlı Canlı Oy Dağılımı</h2>
            
            <div id="poll-container">
                <!-- Partiler JS ile canlı yüklenecek -->
                <p style="text-align:center; padding: 20px;">Anket verileri yükleniyor...</p>
            </div>

            {admatic_code}

            <a href="/" class="btn-home">← Anasayfaya Dön</a>
        </article>

        {whos_amung_us_code}
    </div>

    {footer_html}

    <script>
        // Firebase Yapılandırması (Ücretsiz Firebase Realtime DB)
        const firebaseConfig = {{
            databaseURL: "https://nearadin-poll-default-rtdb.firebaseio.com/"
        }};
        
        firebase.initializeApp(firebaseConfig);
        const db = firebase.database().ref("secim_anketi");

        const parties = [
            {{ id: "chp", name: "Cumhuriyet Halk Partisi (CHP)", color: "#e30613" }},
            {{ id: "akp", name: "AK Parti (AKP)", color: "#ff9900" }},
            {{ id: "dem", name: "DEM Parti", color: "#800080" }},
            {{ id: "mhp", name: "Milliyetçi Hareket Partisi (MHP)", color: "#b10000" }},
            {{ id: "yrp", name: "Yeniden Refah Partisi (YRP)", color: "#006400" }},
            {{ id: "iyi", name: "İYİ Parti", color: "#00a2e8" }},
            {{ id: "zafer", name: "Zafer Partisi", color: "#cc0000" }},
            {{ id: "diger", name: "Diğer Partiler", color: "#7f7f7f" }}
        ];

        let hasVoted = localStorage.getItem("nearadin_voted");

        if (hasVoted) {{
            document.getElementById("voted-alert").style.display = "block";
        }}

        // Veritabanından Canlı Dinleme ve Grafik Güncelleme
        db.on("value", (snapshot) => {{
            const data = snapshot.val() || {{}};
            let totalVotes = 0;

            parties.forEach(p => {{
                totalVotes += (data[p.id] || 0);
            }});

            document.getElementById("total-votes-count").innerText = totalVotes.toLocaleString("tr-TR");

            let html = "";
            parties.forEach(p => {{
                const votes = data[p.id] || 0;
                const percent = totalVotes > 0 ? ((votes / totalVotes) * 100).toFixed(1) : 0;

                html += `
                <div class="party-item">
                    <div class="party-header">
                        <span>${{p.name}}</span>
                        <span style="color:${{p.color}}">%${{percent}}</span>
                    </div>
                    <div class="progress-bg">
                        <div class="progress-bar" style="background:${{p.color}}; width:${{percent}}%;"></div>
                    </div>
                    <div class="party-footer">
                        <span>Oy Sayısı: ${{votes.toLocaleString("tr-TR")}}</span>
                        <button class="vote-btn" onclick="castVote('${{p.id}}')" ${{hasVoted ? 'disabled' : ''}}>
                            ${{hasVoted ? 'Oy Kullanıldı' : 'Oy Ver'}}
                        </button>
                    </div>
                </div>
                `;
            }});

            document.getElementById("poll-container").innerHTML = html;
        }});

        // Oy Kullanma Fonksiyonu
        function castVote(partyId) {{
            if (localStorage.getItem("nearadin_voted")) {{
                alert("Zaten oy kullandınız!");
                return;
            }}

            db.child(partyId).transaction((currentVotes) => {{
                return (currentVotes || 0) + 1;
            }}, (error, committed) => {{
                if (committed) {{
                    localStorage.setItem("nearadin_voted", partyId);
                    hasVoted = true;
                    document.getElementById("voted-alert").style.display = "block";
                }}
            }});
        }}
    </script>
</body>
</html>'''

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(poll_html)
    print("✅ Interaktif /secim-anketi/index.html oluşturuldu.")

if __name__ == "__main__":
    header_html = ""
    footer_html = ""
    whos_amung_us_code = ""
    admatic_code = ""

    try:
        from fetch_news import get_header_html, footer_html, whos_amung_us_code, admatic_code
        header_html = get_header_html("nearadin.net - Seçim Anketi")
    except ImportError:
        header_html = '<header style="background:#1877f2;padding:15px;color:white;text-align:center;"><h2>nearadin.net</h2></header>'
        footer_html = '<footer style="text-align:center;padding:20px;color:#65676b;">© nearadin.net</footer>'

    generate_secim_anketi_page(
        header_html=header_html,
        footer_html=footer_html,
        whos_amung_us_code=whos_amung_us_code,
        admatic_code=admatic_code
    )
