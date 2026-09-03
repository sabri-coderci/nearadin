# 🔍 Google Search Console Kurulum Rehberi

## ⚡ ACIL YAPILACAKLAR (Bugün Yap!)

### 1. Domain'i Google Search Console'a Ekle
```
1. https://search.google.com/search-console/ adresine git
2. "Mülkiyet Ekle" butonuna tıkla
3. nearadin.net yaz
4. "URL öneki" seçeneğini seç
5. Doğrula
```

#### Doğrulama Seçenekleri:
- **DNS TXT Kaydı (ÖNERİLİ):**
  - Hosting paneline git
  - DNS ayarlarına gir
  - TXT kaydı ekle (Google tarafından sağlanan kod)
  - Kontrol et

- **HTML Dosyası (Alternatif):**
  - google-site-verification.html dosyası root'a yükle ✅ (Zaten var)
  - Kontrol et

---

### 2. Sitemaps'i Gönder
```
1. Google Search Console'da nearadin.net'i seç
2. Sol menüden "Sitemaps" tıkla
3. Aşağıdaki linkleri ekle (tek tek):
   - https://nearadin.net/sitemap.xml
   - https://nearadin.net/news-sitemap.xml
   - https://nearadin.net/sitemap-index.xml
4. Gönder
```

---

### 3. URL'leri Indexlemeye Sor
```
1. Search Console'da "URL Denetçisi" aç
2. Anasayfanın URL'sini gir: https://nearadin.net/
3. "Indexlemesini İste" butonuna tıkla
4. Haber detay sayfalarında da tekrarla
```

---

## 📊 Önemli Ayarlar

### Tercih Edilen Alan
```
Search Console → Ayarlar → Tercih Edilen Alan
→ nearadin.net seç (www olmadan)
```

### İşaretler
```
Search Console → Ayarlar → İşaretler
→ Türkçe seç
→ "Türkiye" seç
```

---

## 🏃 Keyword Tracking

Su başlıklar Google arama sonuçlarında çıkması için optimize edilmiştir:
- **son dakika haberleri** ← Anasayfa Title
- **sondakika** ← Meta description
- **haberler** ← H1 etiketleri
- **güncel haberler** ← İçerikte tekrarlanan
- **canlı haber** ← Header metaları

**Durumu Kontrol Et:**
1. Search Console → Performans
2. Sorgularını filtrele
3. "son dakika" arayarak CTR kontrol et

---

## 📱 Mobil Uyumluluk Doğrula

```
Search Console → Mobil Kullanılabilirlik
→ Sorun yok mu diye kontrol et
```

---

## 🔗 İç Bağlantı Yapısı (Kontrol)

✅ **Zaten Yapılmış:**
- Anasayfadan tüm kategorilere linkler
- Her haber detayında ilişkili haberler
- Arşiv sayfalarında tarih bazlı linkler

---

## 📈 İlk Haftada Beklenenler

| Gün | Beklenti |
|-----|----------|
| 1-2 | Google crawl başlar |
| 3-5 | İlk sayfalar index olur |
| 7-14 | Arama sonuçlarında görünür |
| 14-30 | Ranking başlar |
| 30+ | Sabit ranking |

---

## ✅ Son Kontrol Listesi

- [ ] Domain'i Google Search Console'a ekledim
- [ ] DNS veya HTML dosyası doğruladım
- [ ] Tüm sitemaps'i gönderdim
- [ ] Anasayfa URL'sini indexlemeye istedim
- [ ] robots.txt kontrol ettim
- [ ] Meta descriptions tümünde var
- [ ] Title etiketleri benzersiz
- [ ] İç linkler düzgün
- [ ] Mobil uyumluluk sorunsu yok
- [ ] Google News Publisher Center'a başvuru yaptım (opsiyonel)

---

## 🚀 Google News'e Başvuru (İsteğe Bağlı)

Haberler daha hızlı index olsun diye:

```
1. https://news.google.com/news/publication/add
2. nearadin.net ekle
3. Form doldur
4. Bekle (2-4 hafta)
```

---

## 📞 Sorun Giderme

### "404 Hatası: Bulunamadı"
- robots.txt kontrol et
- URL'nin gerçekten var mı kontrol et
- DNS yayılmasını bekle (24 saat)

### "Meta Etiketleri Yok"
- fetch_news.py'yi çalıştır
- HTML dosyaları yeniden oluştur

### "Sitemaps Kabul Edilmiyor"
- XML formatını kontrol et
- Encoding UTF-8 mi kontrol et
- Sitemap yeniden oluştur

---

## 💡 İpuçları

1. **Düzenli Güncelleme:** Her gün yeni haberler ekle
2. **Sosyal Medya:** Twitter'da paylaş (@nearadin2026)
3. **Hız:** Sayfa hızını test et (PageSpeed Insights)
4. **Backlinks:** Diğer sitelere link iste
5. **Analytics:** Google Analytics ekle

---

**Son Güncelleme:** 2026-09-03
**Sonraki Kontrol:** 1 hafta sonra