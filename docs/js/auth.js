// docs/auth.js
// Inicializar cliente con variables globales
//Pide datos al explorador para saber si hay un usuario registrado y con base en eso construye un botón que puede ser para iniciar sesión o para cerrarla (ifElse)
const sb = supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
//Helpers cortos
const $id = (id, root = document) => root.getElementById(id);
const $qs = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function ensureHeaderButton(){
    if (document.querySelector('#btn-auth'))
        return;
    const headerInner = document.querySelector('.md-header__inner');
    if (!headerInner) return;

    const btn = document.createElement('button');
    btn.id = 'btn-auth';
    btn.className = 'md-button';
    btn.style.marginleft = 'auto';
    btn.textContent = 'Ingresar / Registrarse';
    btn.style.color = "white";
    btn.style.fontWeight = "bold";
    btn.style.padding = "0.5em 1em"
    btn.addEventListener('click',onAuthButtonClick);
    headerInner.appendChild(btn);
}
function setHeaderButton(session){
    const btn = document.querySelector('#btn-auth');
    if (btn) btn.textContent = session ? 'Salir' : 'Ingresar/Registrarse';
}
async function onAuthButtonClick(){
    const { data: {session} } = await sb.auth.getSession();
    if (session) {
        console.log('Hay sesión; luego hacemos logout');
        return;
    } 
    injectAuthModal?.();
    openAuthModal?.();
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
    const btnLogin = $('#btn-login');
    const btnReg = $('#btn-go-register');
    const btnClose = $('#btn-close-auth');

    btnClose?.addEventListener('click', closeAuthModal);
    form?.addEventListener('submit', handleLogin);
    btnReg?.addEventListener('click', handleRegister);

    //Opcional, para evitar dobles clicks rápidos
    btnLogin?.addEventListener('click', () => btnLogin.disabled = true, {once: true});
    btnReg ?.addEventListener('click', () => btnReg.disabled = true, {once: true});
    };
function openAuthModal(){
    const m = document.getElementById('auth-modal');
    if (m) m.style.display = 'grid';
}
function closeAuthModal(){
    const m = document.getElementById('auth-modal');
    if (m) m.style.display = 'none';
}
//Handlers para login y para registro
async function handleLogin(ev) {
    ev?.preventDefault?.();
    const msg = $id('auth-msg');
    const mail = $('auth-email')?.value.trim();
    const pass = $('auth-pass')?.value;

    if(!mail || !pass){msg.textContent = 'Completa email y contraseña.'; return;}
    msg.textContent = 'Ingresando...';
    const{data, error} = await sb.auth.signInWithPassword({email : mail, password : pass});
    if(error) {msg.textContent = error.message; return;}
    closeAuthModal?.();
    setAuthGating(data.session);
}
async function handleRegister(ev){
    ev?.preventDefault?.();
    const msg = $id('auth-msg');
    const mail = $id('auth-email')?.value.trim();
    const pass = $id('auth-pass')?.value;

    if (!mail||!pass){msg.textContent = 'Escribe email y contraseña'; return;}
    if (pass.length < 6) {msg.textContent = 'La contraseña debe tener 6+ caracteres.'; return;}
    
    msg.textContent = 'Creando cuenta...';
    const{data, error} = await sb.auth.signUp({email: mail, password: pass});
    if (error) {msg.textContent = error.message; return;}

    msg.textContent = 'Listo. Revisa tu correo para confirmar la cuenta';
}
function initAuthUI(){
    ensureHeaderButton();
    injectAuthModal?.();

    sb.auth.getSession().then(({data:{session}}) => setHeaderButton(session));
    sb.auth.onAuthStateChange((_event, session) => setHeaderButton(session));
}
function setAuthGating(session){
    const logged = !!session;
    $$('.require-auth').forEach(el => el?.classList.toggle('hidden', !logged));
    $$('.require-anon').forEach(el => el?.classList.toggle('hidden',logged));
    setHeaderButton(session);
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

(async () => {
ensureHeaderButton();
const{data : {session}} = await sb.auth.getSession();
setHeaderButton(session);
sb.auth.onAuthStateChange((_event, session) => setHeaderButton(session));})();//Creamos el MODAL para poder iniciar sesión o registrarse

if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initAuthUI);
}
else{
    initAuthUI();
}