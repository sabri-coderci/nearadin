// web-sayfam/js/components/gallery.js
export default class Gallery{
  constructor({el}){this.el = el}
  loadSample(){
    if(!this.el) return
    const items = Array.from({length:9}).map((_,i)=>({id:i+1,src:`https://picsum.photos/seed/nearadin${i+1}/600/400`,title:`Resim ${i+1}`}))
    this.el.innerHTML = items.map(it=>`<figure class="card"><img loading="lazy" src="${it.src}" alt="${it.title}" width="600" height="400"><figcaption>${it.title}</figcaption></figure>`).join('')
  }
}
