// web-sayfam/js/components/header.js
export default function Header(el){
  el.innerHTML = `
    <div class="container">
      <div class="brand">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="6" fill="#0b62ff"/><path d="M7 12h10" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>
        <span>Ne Aradın</span>
      </div>
      <nav aria-label="Ana gezinme">
        <ul>
          <li><a href="#hero">Ana</a></li>
          <li><a href="#gallery">Galeri</a></li>
          <li><a href="#contact">İletişim</a></li>
        </ul>
      </nav>
    </div>
  `
}
