import openpyxl

data = [
    ["KOD", "PARTI_ADI", "YUZDE", "OY_SAYISI", "RENK"],
    ["CHP", "Cumhuriyet Halk Partisi", 33.8, 16900, "#e30613"],
    ["AKP", "AK Parti", 31.5, 15750, "#ff9900"],
    ["DEM", "DEM Parti", 9.2, 4600, "#800080"],
    ["MHP", "Milliyetçi Hareket Partisi", 7.1, 3550, "#b10000"],
    ["YRP", "Yeniden Refah Partisi", 6.4, 3200, "#006400"],
    ["İYİ", "İYİ Parti", 4.8, 2400, "#00a2e8"],
    ["ZAFER", "Zafer Partisi", 3.5, 1750, "#cc0000"],
    ["DİĞER", "Diğer Partiler", 3.7, 1850, "#7f7f7f"]
]

wb = openpyxl.Workbook()
ws = wb.active

for row in data:
    ws.append(row)

wb.save("secim-anketi/anket_verileri.xlsx")
print("✅ anket_verileri.xlsx otomatik olarak oluşturuldu.")
