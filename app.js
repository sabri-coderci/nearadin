document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedCategory = urlParams.get('kategori');

    const titleElement = document.getElementById("dynamic-category-title");
    const descElement = document.getElementById("dynamic-category-desc");
    const containerElement = document.getElementById("posts-container");

    fetch('data/posts.json')
        .then(response => response.json())
        .then(posts => {
            let filteredPosts = posts;

            if (selectedCategory) {
                filteredPosts = posts.filter(post => post.category === selectedCategory);
            }

            renderPosts(filteredPosts, containerElement);
        });
});

function renderPosts(posts, container) {
    if (posts.length === 0) {
        container.innerHTML = `<p>Bu kategoride içerik yok.</p>`;
        return;
    }

    container.innerHTML = posts.map(post => `
        <article class="post-card" style="margin-bottom: 25px; border-bottom: 1px solid #ddd; padding-bottom: 15px;">
            <span class="post-cat">${post.categoryName}</span>
            <h2 class="post-title">
                <!-- Tıklandığında Yorum Kısmını Aç/Kapat -->
                <a href="javascript:void(0)" onclick="toggleComments('${post.id}')">${post.title}</a>
            </h2>
            <p class="post-summary">${post.summary}</p>
            <div class="post-meta">
                <span>📅 ${post.date}</span>
                <button onclick="toggleComments('${post.id}')" style="margin-left: 10px; cursor: pointer;">💬 Yorumlar / Göster</button>
            </div>
            
            <!-- Gizli Yorum Alanı -->
            <div id="comments-${post.id}" class="comments-section" style="display: none; margin-top: 15px; padding: 10px; background: #f9f9f9;">
                <h3>Yorumlar</h3>
                <div class="giscus-container-${post.id}"></div>
            </div>
        </article>
    `).join('');
}

// Yorum Alanını Açma / Kapatma Fonksiyonu
function toggleComments(postId) {
    const commentBox = document.getElementById(`comments-${postId}`);
    if (commentBox.style.display === "none") {
        commentBox.style.display = "block";
        loadGiscus(postId); // Yorum servisini yükle
    } else {
        commentBox.style.display = "none";
    }
}

// GitHub Discussions Tabanlı Yorum Modülü (Giscus)
function loadGiscus(postId) {
    const container = document.querySelector(`.giscus-container-${postId}`);
    if (container.children.length > 0) return; // Zaten yüklendiyse tekrar yükleme

    const script = document.createElement("script");
    script.src = "https://giscus.app/client.js";
    script.setAttribute("data-repo", "KULLANICI_ADI/DEPO_ADI"); // GitHub kullanıcı adınız ve repo adınız
    script.setAttribute("data-repo-id", "REPO_ID_BURAYA");
    script.setAttribute("data-category", "Announcements");
    script.setAttribute("data-category-id", "KATEGORI_ID_BURAYA");
    script.setAttribute("data-mapping", "specific");
    script.setAttribute("data-term", `Post-${postId}`);
    script.setAttribute("data-strict", "0");
    script.setAttribute("data-reactions-enabled", "1");
    script.setAttribute("data-emit-metadata", "0");
    script.setAttribute("data-input-position", "bottom");
    script.setAttribute("data-theme", "light");
    script.setAttribute("data-lang", "tr");
    script.crossOrigin = "anonymous";
    script.async = true;

    container.appendChild(script);
}
