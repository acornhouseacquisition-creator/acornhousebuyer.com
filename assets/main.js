// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
})();

// Close form look. Only styling changes here: fields and submission still come from Close.
var CLOSE_FORM_CSS = `
.form{padding:0;font-family:var(--font);color:var(--ink)}
.form .form-row{margin-bottom:0}
.form .label{font-size:.9rem;font-weight:700;color:var(--ink)}
.form .input{font:inherit;font-size:16px;font-weight:400;padding:12px 13px;border:1.5px solid #cfc8bb;border-radius:9px;background:#fff;color:var(--ink);box-shadow:none}
.form .input:focus,.form .input:focus-within{border-color:var(--green);outline:none;box-shadow:0 0 0 3px rgba(31,77,58,.18)}
.form .phone-input input{font:inherit;font-size:16px}
.form .checkbox-input{accent-color:var(--green);width:18px;height:18px;flex:none}
.form .checkbox-message{font-size:.78rem;font-weight:400;line-height:1.45;color:var(--muted)}
.form .checkbox-message a{color:var(--green)}
.form .button{width:100%;font:inherit;font-size:1.08rem;font-weight:800;padding:14px 24px;border:0;border-radius:10px;background:var(--acorn);color:#fff;cursor:pointer;transition:background .15s}
.form .button:hover{background:var(--acorn-d)}
`;
if (window.customElements && 'adoptedStyleSheets' in Document.prototype) {
  customElements.whenDefined('close-form').then(function () {
    var sheet = new CSSStyleSheet();
    sheet.replaceSync(CLOSE_FORM_CSS);
    document.querySelectorAll('close-form').forEach(function (el) {
      (function apply(tries) {
        if (el.shadowRoot) el.shadowRoot.adoptedStyleSheets = el.shadowRoot.adoptedStyleSheets.concat(sheet);
        else if (tries) setTimeout(apply, 100, tries - 1);
      })(50);
    });
  });
}
