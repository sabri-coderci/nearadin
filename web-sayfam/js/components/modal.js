// web-sayfam/js/components/modal.js
export default function Modal({root}){
  if(!root) return
  const container = document.createElement('div')
  container.className = 'modal-container hidden'
  container.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true">
      <div class="modal-body"></div>
      <div class="modal-actions"><button class="btn close">Kapat</button></div>
    </div>
  `
  root.appendChild(container)
  const body = container.querySelector('.modal-body')
  const btn = container.querySelector('.close')
  btn.addEventListener('click', ()=>container.classList.add('hidden'))

  const api = {
    show(html){ body.innerHTML = html; container.classList.remove('hidden') }
  }
  // expose to global for quick use
  window.appModal = api
  return api
}
