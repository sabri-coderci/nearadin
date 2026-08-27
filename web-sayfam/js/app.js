// web-sayfam/js/app.js
// Başlangıç uygulaması: bileşen kaydı, form, galeri, posts demo, PWA
import Header from './components/header.js'
import Footer from './components/footer.js'
import Modal from './components/modal.js'
import Gallery from './components/gallery.js'

// Register header/footer into the DOM by attribute `is` (simple component mount)
const mountComponents = () => {
  const headerEl = document.querySelector('[is="main-header"]')
  if(headerEl) Header(headerEl)

  const footerEl = document.querySelector('[is="main-footer"]')
  if(footerEl) Footer(footerEl)

  // Modal root
  Modal({root:document.getElementById('modal-root')})

  // Gallery
  const gallery = new Gallery({el:document.getElementById('gallery')})
  gallery.loadSample()

  // Demo posts
  const posts = document.getElementById('posts')
  if(posts){
    const sample = Array.from({length:3}).map((_,i)=>`<article class="card"><h3>Yazı başlığı ${i+1}</h3><p class="small">Özet içerik...</p></article>`)
    posts.innerHTML = sample.join('')
  }

  // Modal demo button
  const openDemo = document.getElementById('open-demo-modal')
  if(openDemo){
    openDemo.addEventListener('click',()=>{
      window.appModal && window.appModal.show('<h3>Önizleme</h3><p>Bu modal bileşeni kolayca yeniden kullanılabilir.</p>')
    })
  }

  // Contact form
  const form = document.getElementById('contact-form')
  if(form){
    const status = document.getElementById('form-status')
    form.addEventListener('submit', e=>{
      e.preventDefault()
      const fd = new FormData(form)
      const data = Object.fromEntries(fd.entries())
      // Basit doğrulama
      if(!data.name || !data.email || !data.message){
        status.textContent = 'Lütfen tüm alanları doldurunuz.'
        return
      }
      // Demo: localStorage'e kaydet
      const storage = JSON.parse(localStorage.getItem('nearadin-contacts')||'[]')
      storage.push({...data, created: new Date().toISOString()})
      localStorage.setItem('nearadin-contacts', JSON.stringify(storage))
      status.textContent = 'Mesajınız kaydedildi (demo).'
      form.reset()
    })
    document.getElementById('clear-form').addEventListener('click',()=>{form.reset();document.getElementById('form-status').textContent='';})
  }
}

// Register service worker for offline/PWA
if('serviceWorker' in navigator){
  window.addEventListener('load', async ()=>{
    try{ await navigator.serviceWorker.register('/web-sayfam/sw.js') }catch(e){console.warn('SW kaydı başarısız',e)}
  })
}

// Expose modal API for demos
window.appModal = null

document.addEventListener('DOMContentLoaded', ()=>{
  mountComponents()
})
