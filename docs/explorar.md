<div id="filtros">
<label>Coleccion: <select id="f-coleccion"><option value="">Todas</option></select> </label>
<label>Serie: <select id="f-serie"><option value="">Todas</option></select> </label>
<label>Año:<select id="f-anio"><option value ="">Todos</option></select></label>
<label>Autor: <input id="f-autor" type="text" placeholder ="Ej. Pérez"></label>
<label>Título: <input id="f-titulo" type="text" placeholder ="Buscar por título"></label>
<span id="contador" style="margin-left:.6rem;"></span>
<button id="btn-clear" type = "button" class = "md-button">Limpiar filtros</button>

<label> Ordenar por:
    <select id="f-order">
        <option value="titulo-asc">Título (A -> Z)</option>
        <option value="titulo-desc">Título (Z-> A)</option>
        <option value="anio-asc">Año (asc)</option>
        <option value="anio-desc">Año (desc)</option>
    </select>
</label>
</div>

<div id="resultados"></div>
<script>

    (async function() {
    const { origin, hostname, pathname} = window.location;
    <!-- El cálculo de la base se hace de dos formas, una para ver si estamos en deployment o si estamos trabajando con MKDCOS -->
    let BASE = origin + "/";
    if (hostname.endsWith(".github.io")) {const segs = pathname.split("/").filter(Boolean); if (segs.length> 0) BASE = `${origin}/${segs[0]}/`;}
    console.log("base = ", BASE);
    const resp = await fetch(`${BASE}data/catalogo.json`);
    const libros = await resp.json();
    const $ = (sel) => document.querySelector(sel);
    const unique = (arr) => Array.from(new Set(arr.filter(Boolean)));
    const selColeccion = $('#f-coleccion');
    const selSerie = $('#f-serie');
    const selAnio = $('#f-anio');
    const inpAutor = $('#f-autor');
    const inpTitulo = $('#f-titulo');
    const contador = $('#contador');
    const selOrder = document.querySelector('#f-order')
    unique(libros.map(x=> x.coleccion)).sort().forEach(c => selColeccion.insertAdjacentHTML('beforeend',`<option>${c}</option>`));
    unique(libros.map(x=> x.serie)).sort().forEach(s => selSerie.insertAdjacentHTML('beforeend',`<option>${s}</option>`));
    unique(libros.map(x=> String(x.anio))).sort().forEach(a => selAnio.insertAdjacentHTML('beforeend',`<option>${a}</option>`))
    const cont = document.querySelector('#resultados');
    function render(lista){
        if(!Array.isArray(lista)) {
        cont.textContent = 'Error: datos inválidos';
        return;
    }
    if (!lista.length){
    cont.innerHTML = '<p><em>Sin resultados.</em></p>';
        return;
        }
    cont.innerHTML = lista.map(x => `
        <!-- <div class="card">
        <h3><a href="${BASE}/libros/${x.id}/"> <b>${x.titulo}</b> <br>
            <small class="meta"><strong><Autores:></strong>${(x.autores && x.autores.length ? x.autores.join(', ') : '_')}</small>
            <p>${[x.coleccion ? `Colección: ${x.coleccion}` : '', x.serie ? `Serie: ${x.serie}` : '', x.anio ? `Año: ${x.anio}` : ''].filter(Boolean).join(' | ')}</p>
            <img src="${BASE}/assets/covers/${x.id}.jpg" style="display: none" onload="this.style.display=''">
            <img src="${BASE}/assets/covers/${x.id}.png" style="display: none" onload="this.style.display=''">
        </div> -->
        <div class="card">
        <a href="${BASE}/libros/${x.id}/">
          <div class="libro-portada">
              <img src="${BASE}/assets/covers/${x.id}.jpg" style="display: none" onload="this.style.display=''">
              <img src="${BASE}/assets/covers/${x.id}.png" style="display: none" onload="this.style.display=''">
          </div>
          <div class="libro-datos">
            <h3>${x.titulo}<br>
            <div class="autores"><strong><Autores:></strong>${(x.autores && x.autores.length ? x.autores.join(', ') : '_')}</div>
            <div class="meta">${[x.coleccion ? `<b>Colección:</b> ${x.coleccion}` : '', x.serie ? `<b>Serie:</b> ${x.serie}` : '', x.anio ? `<b>Año:</b> ${x.anio}` : ''].filter(Boolean).join(' | ')}<br>
            <b>ISBN: </b>${x.isbn_libro}</div>
          </div>
        </div>        
        `).join('');
    }
    function coincideAutor(libro, needle){
        if(!needle) return true;
        const n = needle.toLowerCase();
        return (libro.autores || []).some(a => a.toLowerCase().includes(n));
        }
    function coincideTitulo(libro, needle){
        if(!needle) return true;
        return(libro.titulo || '').toLowerCase().includes(needle.toLowerCase());
    }
    function filtrar(){
        const c = selColeccion.value;
        const s = selSerie.value;
        const a = selAnio.value;
        const au = inpAutor.value.trim();
        const ti = inpTitulo.value.trim();
        const comparator = getComparator(selOrder.value || 'titulo-asc');
        const out = libros.filter(x=> (!c || x.coleccion === c) && (!s || String(x.serie || '') === String(s)) && (!a || String(x.anio) === String(a)) && coincideAutor(x, au) && coincideTitulo(x,ti)).sort(comparator);
        render(out);
    }
    selColeccion.addEventListener('change', filtrar);
    selSerie.addEventListener('change', filtrar);
    selAnio.addEventListener('change', filtrar);
    inpAutor.addEventListener('input', filtrar);
    inpTitulo.addEventListener('input', filtrar);
    selOrder.addEventListener('change',filtrar);
    render(libros);
        const btnClear = document.querySelector('#btn-clear');
    function limpiar(){
        selColeccion.value = '';
        selSerie.value = '';
        selAnio.value = '';
        inpAutor.value = '';
        inpTitulo.value = '';
        filtrar();
        inpTitulo.focus();
    }
    btnClear.addEventListener('click',limpiar);
    const yearNum = (val) => {
        const m = String (val ?? '').match(/\b(19|20)\d{2}\b/);
        return m ? Number(m[0]) : NaN;};
    const cmpTituloAsc = (a,b) => String(a.titulo).localeCompare(String(b.titulo));
    const cmpTituloDesc = (a,b) => -cmpTituloAsc(a,b);
    const cmpAnioAsc = (a,b) => {
        const A = yearNum(a.anio), B = yearNum(b.anio);
        if (isNaN(A) && isNaN(B)) return cmpTituloAsc(a,b);
        if (isNaN(A)) return 1;
        if (isNaN(B)) return -1;
        if (A !== B) return A-B;
        return cmpTituloAsc(a,b);
    };
    const cmpAnioDesc = (a,b) => {
        const A = yearNum(a.anio), B = yearNum(b.anio);
        if (isNaN(A) && isNaN(B)) return cmpTituloAsc(a,b);
        if (isNaN(A)) return 1;
        if (isNaN(B)) return -1;
        if (A !== B) return B-A;
        return cmpTituloAsc(a,b);
    };
    function getComparator(mode){
        switch(mode) {
            case 'titulo-asc': return cmpTituloAsc;
            case 'titulo-desc': return cmpTituloDesc;
            case 'anio-asc': return cmpAnioAsc;
            case 'anio-desc': return cmpAnioDesc;
            default: return cmpTituloAsc;
        }
    }
})();

</script>

<!-- <style>
    #resultados .card{
        padding:.9rem 1rem; 
        border:1px solid
        var(--md-default-fg-color--lightest);
        border-radius:.5rem; margin:.5rem 0;
    }
    #resultados h3 {margin:.2rem 0 .3rem;
    font-size:1.05rem;
    }
    #resultados p{
        margin:.1rem 0;
    }
</style> -->
