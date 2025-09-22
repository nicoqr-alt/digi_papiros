//Este documento hay que estudiarlo con cuidado. Establece una conexión entre la página WEB y la API llamada supabase. Este código crea un botón de inicio y cierre de sesión que se actualiza automáticamente cuando estamos en la página y también fabrica
//un recuadro de texto para llevar a cabo el registro.
// docs/auth.js
// Inicializar cliente con variables globales
//Pide datos al explorador para saber si hay un usuario registrado y con base en eso construye un botón que puede ser para iniciar sesión o para cerrarla (ifElse)
const sb = supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
//Helpers cortos
const $id = (id, root = document) => root.getElementById(id);
const $qs = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function ensureHeaderButton(){
    const headerInner = document.querySelector('.md-header__inner');
    if (!headerInner) return;
    if (! document.querySelector('#btn-auth')){
    const btn = document.createElement('button');
    btn.id = 'btn-auth';
    btn.className = 'md-button';
    btn.style.marginLeft = 'auto';
    btn.textContent = 'Ingresar / Registrarse';
    btn.style.color = "white";
    btn.style.fontWeight = "bold";
    btn.style.padding = "0.5em 1em"
    btn.addEventListener('click',onAuthButtonClick);
    headerInner.appendChild(btn);}
}
function setHeaderButton(session){
    const btn = document.querySelector('#btn-auth');
    if (btn) btn.textContent = session ? 'Salir' : 'Ingresar/Registrarse';
}

function injectAuthModal(){
    if (document.getElementById('auth-modal')) return;
    const div = document.createElement('div');
    div.id = 'auth-modal';
    //Estilizado del botón
     div.style.cssText = `
    position:fixed; inset:0; display:none; place-items:center;
    background: rgba(253, 253, 253, 0.45); z-index: 9999;
    `;
    div.innerHTML = `
    <div id="auth-dialog" style="
      background: var(--md-default-bg-color, #fff);
      color: var(--md-typeset-color, #fffdfdff);
      width: min(420px, 90vw);
      border-radius: 12px; padding: 16px 20px;
      box-shadow: 0 12px 40px rgba(0,0,0,.3);
    ">
      <h3 style="margin: 0 0 .5rem 0;">Acceder</h3>
      <form id="auth-form">
        <label>Email<br>
          <input type="email" id="auth-email" required style="width:100%;padding:.5rem;margin:.25rem 0 .75rem;">
        </label>
        <label>Contraseña<br>
          <input type="password" id="auth-pass" required style="width:100%;padding:.5rem;margin:.25rem 0 .75rem;">
        </label>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.25rem;">
          <button type="submit" id="btn-login" class="md-button">Iniciar sesión</button>
          <button type="button" id="btn-go-register" class="md-button">Crear cuenta</button>
          <button type="button" id="btn-close-auth" class="md-button">Cerrar</button>
        </div>
        <p id="auth-msg" style="opacity:.7;font-size:.9em;margin:.5rem 0 0;"></p>
      </form>
    </div>
    `;
    document.body.appendChild(div);
    //Eventos 
    const $ = (sel) => div.querySelector(sel);
    const form = $('#auth-form');
    const btnReg = $('#btn-go-register');
    const btnClose = $('#btn-close-auth');

    btnClose?.addEventListener('click', closeAuthModal);
    form?.addEventListener('submit', handleLogin);
    btnReg?.addEventListener('click', handleRegister);
    };
function openAuthModal(){
    const m = document.getElementById('auth-modal');
    if (!m) return;
    m.style.display = 'grid';
    const msg = m.querySelector('#auth-msg');
    const loginBtn = m.querySelector('#btn-login');
    const regBtn = m.querySelector('#btn-go-register');
    msg && (msg.textContent = '');
    loginBtn && (loginBtn.disabled = false);
    regBtn && (regBtn.disabled = false);
}
function closeAuthModal(){
    const m = document.getElementById('auth-modal');
    if (m) m.style.display = 'none';
}
//Handlers para login y para registro
async function handleLogin(ev) {
    ev?.preventDefault();
    const msg = document.getElementById('auth-msg');
    const mail = document.getElementById('auth-email')?.value.trim();
    const pass = document.getElementById('auth-pass').value;
    const btn = document.getElementById('btn-login');
    if (!mail||!pass) {msg && (msg.textContent='Completa email y contraseña.'); return;}
    try{
        btn && (btn.disabled =true);
        msg && (msg.textContent = 'Ingresando...');
        const {data, error} = await sb.auth.signInWithPassword({email: mail, password: pass});
        if (error) {msg && (msg.textContent = error.message); 
            return;}
        const res = await sb.auth.getSession();
        const session = res?.data?.session ??
        null;
        closeAuthModal?.();
        setAuthGating(session);}
    catch(e){
        console.error(e);
        msg && (msg.textContent = 'Error inesperado');}
    finally {btn && (btn.disabled = false);}
    }
async function handleRegister(ev){
    ev?.preventDefault?.();
    const msg = document.getElementById('auth-msg');
    const mail = document.getElementById('auth-email')?.value.trim();
    const pass =document.getElementById('auth-pass')?.value;
    const btn = document.getElementById('btn-go-register');

    if (!mail||!pass){ msg && (msg.textContent = 'Escribe email y contraseña'); return;}
    if (pass.length < 6) {msg && (msg.textContent = 'La contraseña debe tener 6+ caracteres.'); return;}
    try{
        btn && (btn.disabled = true);
        msg && (msg.textContent = 'Creando cuenta');
        const {error} = await sb.auth.signUp({email: mail, password: pass});
        if (error) {msg && (msg.textContent = error.message);
        return;
        }
        msg && (msg.textContent = 'Listo. Revisa tu correo para confirmar la cuenta');
    }
    catch(e){
        console.error(e);
        msg && (msg.textContent = 'Error inesperado');
    }
    finally{
        btn && (btn.disabled = false);
    }
}
function initAuthUI(){
    ensureHeaderButton();
    injectAuthModal?.();

    //Estado inicial
    sb.auth.getSession().then(({data: {session}}) => setAuthGating(session));

    //Cambios de sesión en caliente
    sb.auth.onAuthStateChange((_event, session) => {setAuthGating(session); if (session) closeAuthModal?.();});

    setupDownloadTracking();
}
function setAuthGating(session){
    const logged = !!session;
    ensureHeaderButton();
    const label = logged? 'Salir':'Ingresar/Registrarse'
    document.querySelectorAll('.require-auth').forEach(el => el.classList.toggle('hidden', !logged));
    document.querySelectorAll('.require-anon').forEach(el => el.classList.toggle('hidden', logged));
    //Texto del botón
    document.querySelectorAll('#btn-auth').forEach(btn => {btn.textContent = logged ? 'Salir' : 'Ingresar / Registrarse';});
}
function setupDownloadTracking(){

    document.querySelectorAll('.dowload-link').forEach(link => {link.addEventListener('click', async (ev) => {const {data : {session}} = await sb.auth.getSession(); if (!session) {ev.preventDefault(); openAuthModal(); return;} 
    const bookId = link.dataset.bookId || 'desconocido'; console.log('Descarga registrada ${bookId} por ${session.user.email}');});});
}
async function onAuthButtonClick(){
    const { data: {session} } = await sb.auth.getSession();
    if (session) {
        try{await sb.auth.signOut();}
        catch(e) {console.error('Error al cerrar sesión', e);}
        setAuthGating(null)
        const m = document.getElementById('auth-msg');
        if (m) m.textContent = '';
        return;
    } 
    injectAuthModal?.();
    openAuthModal?.();
}
(async () => {
const {data: {session}, error} = await sb.auth.getSession();
if (error) {
    console.error("Error al obtener sesión:", error.message);
}
else{
    console.log("Sesión actual:", session);
}
})();

(function(){
    const start = () => {try {initAuthUI();} catch(e){console.error(e);}};
    if (document.readyState === 'loading')
        document.addEventListener('DOMContentLoaded', async()=> {const{data:{session}} = await sb.auth.getSession(); setAuthGating(session);});
    else start();
    if(window.document$?.subscribe)
        window.document$.subscribe(start);
})();