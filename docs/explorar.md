<div id="filtros">
<label>Coleccion: <select id="f-coleccion"><option value="">Todas</option></select> </label>
<label>Serie: <select id="f-serie"><option value="">Todas</option></select> </label>
<label>Año:<select id="f-anio"><option value ="">Todos</option></select></label>
<label>Autor: <input id="f-autor" type="text" placeholder ="Ej. Pérez"></label>
<label>Título: <input id="f-titulo" type="text" placeholder ="Buscar por título"></label>
<span id="contador" style="margin-left:.6rem;"></span>

<button id="btn-clear" type = "button" class = "md-button">Limpiar filtros</button>

</div>

<div id="resultados"></div>
<script>
    (async function() {
    const resp = await fetch('/data/catalogo.json');
    const libros = await resp.json();
    window.libros = libros;
    const $ = (sel) => document.querySelector(sel);
    const unique = (arr) => Array.from(new Set(arr.filter(Boolean)));
    const selColeccion = $('#f-coleccion');
    const selSerie = $('#f-serie');
    const selAnio = $('#f-anio');
    const inpAutor = $('#f-autor');
    const inpTitulo = $('#f-titulo');
    const contador = $('#contador');
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
        <div class="card">
        <h3><a href="/libros/${x.id}/"><p><strong><Autores:></strong>${(x.autores && x.autores.length ? x.autores.join(', ') : '_')}</p>
        <p>${[x.coleccion ? `Colección: ${x.coleccion}` : '', x.serie ? `Serie: ${x.serie}` : '', x.anio ? `Año: ${x.anio}` : ''].filter(Boolean).join(' . ')}</p>
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
        const out = libros.filter(x => (!c || x.coleccion === c) && (!s || x.serie === s) && (!a || String(x.anio) === String(a)) && coincideAutor(x, au) && coincideTitulo(x, ti)).sort((u,v) => String(u.titulo).localeCompare(String(v.titulo)));
        render(out);
    }
    selColeccion.addEventListener('change', filtrar);
    selSerie.addEventListener('change', filtrar);
    selAnio.addEventListener('change', filtrar);
    inpAutor.addEventListener('input', filtrar);
    inpTitulo.addEventListener('input', filtrar);
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
    })();

</script>

<style>
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
</style>
