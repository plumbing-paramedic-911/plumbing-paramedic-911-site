/* Plumbing Paramedic 911 — shared site script */
(function(){
  'use strict';

  // Mobile nav toggle
  var ham = document.getElementById('ham');
  var mobileNav = document.getElementById('mobileNav');
  if(ham && mobileNav){
    ham.addEventListener('click', function(){
      mobileNav.classList.toggle('open');
      ham.setAttribute('aria-expanded', mobileNav.classList.contains('open') ? 'true' : 'false');
    });
    // close mobile nav on link click
    mobileNav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ mobileNav.classList.remove('open'); });
    });
  }

  // FAQ accordion (semantic: button.faq-q controls .faq-a sibling)
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click', function(){
      var open = q.classList.toggle('open');
      var a = q.nextElementSibling;
      if(a){ a.classList.toggle('open', open); }
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Generic contact form handler (front-end only — wire to email/CRM later)
  document.querySelectorAll('form.lead-form').forEach(function(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var msg = form.querySelector('.form-success');
      if(msg){ msg.classList.add('show'); }
      form.querySelectorAll('input,select,textarea,button').forEach(function(el){ el.disabled = true; });
      // GA4 event
      if(typeof gtag === 'function'){
        gtag('event','generate_lead',{form_id: form.id || 'lead_form'});
      }
    });
  });

  // Telephone click tracking (GA4)
  document.querySelectorAll('a[href^="tel:"]').forEach(function(a){
    a.addEventListener('click', function(){
      if(typeof gtag === 'function'){
        gtag('event','phone_click',{phone:'864-446-8911',location:document.body.dataset.page||'site'});
      }
    });
  });
})();

/* ──────────────────────────────────────────────────────────────
   Pricing Calculator (used only on /pricing/ page)
   ────────────────────────────────────────────────────────────── */
(function(){
  if(!document.querySelector('.calc-wrapper')) return;

  var state = {
    serviceName:'Toilet Repair', low:89, high:149,
    property:'residential', propertyAdj:0,
    timing:'business', timingAdj:0,
    discount:'none', discountAdj:0
  };

  window.setCalcTab = function(tab, btn){
    document.querySelectorAll('.calc-tab').forEach(function(t){ t.classList.remove('active'); });
    btn.classList.add('active');
    document.querySelectorAll('.calc-tab-content').forEach(function(c){ c.style.display='none'; });
    var el = document.getElementById('calc-'+tab);
    if(el) el.style.display='block';
  };

  window.selectService = function(btn, name, low, high){
    document.querySelectorAll('.calc-service-btn').forEach(function(b){ b.classList.remove('selected'); });
    btn.classList.add('selected');
    state.serviceName = name; state.low = low; state.high = high;
    render();
  };

  window.selectOption = function(el, group, value, adj){
    el.parentElement.querySelectorAll('.option-radio').forEach(function(r){ r.classList.remove('selected'); });
    el.classList.add('selected');
    if(group==='property'){ state.property = value; state.propertyAdj = adj; }
    if(group==='discount'){ state.discount = value; state.discountAdj = adj; }
    render();
  };

  window.selectTiming = function(btn, value, adj){
    document.querySelectorAll('.timing-btn').forEach(function(b){ b.classList.remove('active'); });
    btn.classList.add('active');
    state.timing = value; state.timingAdj = adj;
    render();
  };

  window.printEstimate = function(){ window.print(); };

  function fmt(n){ return '$'+n.toLocaleString(); }

  function render(){
    var low = state.low + state.propertyAdj + state.timingAdj + state.discountAdj;
    var high = state.high + state.propertyAdj + state.timingAdj + state.discountAdj;
    if(low < 49) low = 49; if(high < low) high = low;
    var disp = document.getElementById('calcPriceDisplay');
    var sub = document.getElementById('calcPriceSub');
    if(disp) disp.textContent = fmt(low)+' – '+fmt(high);
    if(sub) sub.textContent = state.serviceName+' · '+(state.timing==='business'?'Business Hours':'After Hours / Emergency')+' · '+(state.property==='residential'?'Residential':'Commercial');
    var s = document.getElementById('bd-surcharge'); if(s) s.textContent = state.timingAdj?'+$'+state.timingAdj:'$0';
    var c = document.getElementById('bd-commercial'); if(c) c.textContent = state.propertyAdj?'+$'+state.propertyAdj:'$0';
    var d = document.getElementById('bd-discount'); if(d) d.textContent = state.discountAdj?'−$'+Math.abs(state.discountAdj):'$0';
    var dl = document.getElementById('bd-discount-label'); if(dl) dl.textContent = state.discount==='none'?'Discount':'Discount ('+state.discount+')';
    var t = document.getElementById('bd-total'); if(t) t.textContent = fmt(low)+' – '+fmt(high);
  }

  render();
})();
