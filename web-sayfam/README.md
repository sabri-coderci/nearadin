# web-sayfam — "Ne Aradın" (scaffold)

Bu klasör basit ama genişletilebilir bir web şablonu sunar. Amaç: "bir web sayfasında olabilecek her şeyi" destekleyecek şekilde başlayabileceğiniz bir iskelet.

İçerik:
- index.html — sayfanın ana şablonu (header, hero, galeri, blog, form, modal mount)
- css/styles.css — temel stil sistemi ve yardımcı sınıflar
- js/* — modüler JS: app.js başlangıç, components dizini içinde header/footer/modal/gallery
- manifest.json, sw.js — PWA desteği (örnek)

Genişletme önerileri:
- components dizinine yeni bileşenler ekleyin (carousel, accordion, tooltip)
- i18n: küçük bir çeviri loader ekleyin
- CMS: form gönderimlerini gerçek bir endpoint'e bağlayın
- image optim: yerel `assets` klasöründe ön-üretim görselleri ve responsive srcset kullanın

Kullanmadan önce:
- Repo ana dalı `main` olduğundan, dosyalar burada `web-sayfam/` altına yazıldı.
- PWA test etmek için sayfayı bir sunucuda çalıştırın (örn. `npx serve` veya GitHub Pages)

İsterseniz bu şablonu daha ileri götürebilirim: SSG entegrasyonu (11ty/Eleventy), React/Vue versiyonları, Tailwind/SCSS yapılandırması, form backend örneği veya bir admin arayüzü.
