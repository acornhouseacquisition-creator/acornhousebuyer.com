// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
})();

// Lead forms: POST to data-endpoint when set; otherwise open a pre-filled email.
document.querySelectorAll('.lead-form').forEach(function (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var status = form.querySelector('.form-status');
    var bad = null;
    form.querySelectorAll('[required]').forEach(function (el) {
      var empty = !el.value.trim();
      el.classList.toggle('invalid', empty);
      if (empty && !bad) bad = el;
    });
    var phone = form.querySelector('[name=phone]');
    if (!bad && phone.value.replace(/\D/g, '').length < 10) { bad = phone; phone.classList.add('invalid'); }
    if (bad) {
      status.className = 'form-status err';
      status.textContent = 'Please add your property address, name and a valid phone number.';
      bad.focus();
      return;
    }
    if (form.company.value) return; // bot filled the hidden field

    var data = {};
    new FormData(form).forEach(function (v, k) { if (k !== 'company') data[k] = v; });
    data.page = location.pathname;
    var endpoint = form.dataset.endpoint;

    if (endpoint) {
      var b = form.querySelector('button'); b.disabled = true; b.textContent = 'Sending...';
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw 0; location.href = '/thank-you/'; })
        .catch(function () {
          b.disabled = false; b.textContent = 'Get My Cash Offer';
          status.className = 'form-status err';
          status.textContent = 'Something went wrong. Please call or text us instead.';
        });
    } else {
      var body = Object.keys(data).map(function (k) { return k + ': ' + data[k]; }).join('\n');
      location.href = 'mailto:' + form.dataset.email + '?subject=' + encodeURIComponent('Cash offer request: ' + data.address) + '&body=' + encodeURIComponent(body);
      status.className = 'form-status ok';
      status.textContent = 'Your email app should open with your details. Just press send, or call us if it does not open.';
    }
    if (window.gtag) gtag('event', 'generate_lead', { page_path: location.pathname });
  });
});
