document.addEventListener("DOMContentLoaded", () => {
    // 1. URL'deki kategori parametresini yakala
    const urlParams = new URLSearchParams(window.location.search);
    const selectedCategory = urlParams.get('kategori');

    // 2. DOM Elemanları
    const titleElement = document.getElementById("dynamic-category-title");
    const descElement = document.getElementById("dynamic-category-desc");
    const containerElement = document.getElementById("posts-container");
    const pageTitleElement = document.getElementById("page-title");

    // Kategori Tanımları & Açıklamaları
    const categoryInfo = {
        "teknoloji": { title: "Teknoloji Konuları", desc: "Teknoloji, yazılım ve dijital dünyadan en son başlıklar." },
        "genel": { title: "Genel Tartışma", desc: "Soru-cevap, fikir alışverişi ve genel sohbetler." },
        "all": { title: "Tüm Konular", desc: "Topluluğumuzdaki tüm içerik ve paylaşımları inceleyin." }
    };

    // 3. JSON Verisini Çek ve Filtrele
    fetch('data/posts.json')
        .then(response => {
            if (!response.ok) throw new Error("Veri yüklenemedi.");
            return response.json();
        })
        .then(posts => {
            let filteredPosts = posts;
            let currentCatKey = "all";

            if (selectedCategory && categoryInfo[selectedCategory]) {
                currentCatKey = selectedCategory;
                filteredPosts = posts.filter(post => post.category === selectedCategory);
            }

            // Başlıkları ve Sayfa Unvanını Güncelle
            const info = categoryInfo[currentCatKey];
            titleElement.textContent = info.title;
            descElement.textContent = info.desc;
            pageTitleElement.textContent = `${info.title} - Ne Aradın`;

            // Aktif Navigasyon Butonunu Vurgula
            document.querySelectorAll(".nav-btn").forEach(btn => {
                const cat = btn.getAttribute("data-cat");
                if ((selectedCategory && cat === selectedCategory) || (!selectedCategory && cat === "all")) {
                    btn.classList.add("active");
                }
            });

            // İçerikleri Oluştur
            renderPosts(filteredPosts, containerElement);
        })
        .catch(err => {
            console.error("Hata:", err);
            containerElement.innerHTML = `<p class="error">İçerikler yüklenirken bir hata oluştu.</p>`;
        });
});

function renderPosts(posts, container) {
    if (posts.length === 0) {
        container.innerHTML = `<p class="no-data">Bu kategoride henüz yayınlanan bir içerik bulunmuyor.</p>`;
        return;
    }

    container.innerHTML = posts.map(post => `
        <article class="post-card">
            <span class="post-cat">${post.categoryName}</span>
            <h2 class="post-title"><a href="#${post.slug}">${post.title}</a></h2>
            <p class="post-summary">${post.summary}</p>
            <div class="post-meta">
                <span class="post-date">📅 ${post.date}</span>
            </div>
        </article>
    `).join('');
}

