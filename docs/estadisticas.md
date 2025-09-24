#Estadisticas de descargas

> Esta página mostrará los conteos por libro

## Top libros

<table id = "top-books" class = "md-typeset">
    <thead>
        <tr>
            <th> Título </th>
            <th>Descargas (total) </th>
        </tr>
    </thead>
    <tbody>
        <tr><td colspan = "2" style = "opacity: .7"> Aún sin datos (falta conectar a SupaBase) </td></tr>
    </tbody>
</table>

<script>
function renderStats() {
  const tbody = document.querySelector('#top-books tbody');
  if (!tbody) return;

  // evitar doble ejecución
  if (tbody.dataset.bound === '1') return;
  tbody.dataset.bound = '1';

  tbody.innerHTML = `<tr><td colspan="2" style="opacity:.7">Cargando…</td></tr>`;

  fetch('/data/catalogo.json').then(r=> r.json()).catch(()=> []).then(catalogo => {
    const titleById = Object.fromEntries((catalogo || []).map(b=> [b.id, b.titulo || b.title || b.nombre || b.id])); 
    return sb.from('v_downloads_by_book').select('book_id, total').order('total', {ascending : false}).limit(50).then(({data, error})=> {if (error) throw error; if (!data || data.length ===0){tbody.innerHTML = `<tr><td colspan="2" style="opacity:.7">Sin datos aún</td></tr>`; return;

    } 
    tbody.innerHTML = data.map(r => {const titulo = titleById[r.book_id] ?? r.book_id; return `<tr><td>${titulo}</td><td>${r.total}</td></tr>`;}).join('');});
  }).catch(e=> {console.error(e); tbody.innerHTML = `<tr><td colspan="2" style="color:#c00;">Error al cargar datos</td></tr>`;
        return;});
}

// 1) Ejecutar cuando cargue todo el sitio
window.addEventListener('load', renderStats);

// 2) Ejecutar también en cada navegación interna de MkDocs Material
if (window.document$ && window.document$.subscribe) {
  window.document$.subscribe(renderStats);
}
</script>
