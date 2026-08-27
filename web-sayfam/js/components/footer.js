// web-sayfam/js/components/footer.js
export default function Footer(el){
  const year = new Date().getFullYear()
  el.innerHTML = `
    <div class="footer-inner">
      <div class="small">© ${year} Ne Aradın</div>
      <div class="small">Built with ❤️ — extensible template</div>
    </div>
  `
}
