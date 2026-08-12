(()=>{
  "use strict";

  const LEAD_ENDPOINT="https://wuwgvtjktppjueiykcww.supabase.co/functions/v1/website-lead-capture";
  const BUSINESS_PHONE="(864) 446-8911";
  const BUSINESS_PHONE_URL="tel:+18644468911";

  const ham=document.getElementById("ham");
  const mobileNav=document.getElementById("mobileNav");
  if(ham&&mobileNav){
    ham.addEventListener("click",()=>{
      mobileNav.classList.toggle("open");
      ham.setAttribute("aria-expanded",mobileNav.classList.contains("open")?"true":"false");
    });
    mobileNav.querySelectorAll("a").forEach(link=>{
      link.addEventListener("click",()=>{
        mobileNav.classList.remove("open");
        ham.setAttribute("aria-expanded","false");
      });
    });
  }

  document.querySelectorAll(".faq-q").forEach(question=>{
    question.addEventListener("click",()=>{
      const open=question.classList.toggle("open");
      const answer=question.nextElementSibling;
      if(answer)answer.classList.toggle("open",open);
      question.setAttribute("aria-expanded",open?"true":"false");
    });
  });

  function ensureHoneypot(form){
    if(form.querySelector('input[name="website"]'))return;
    const trap=document.createElement("input");
    trap.type="text";
    trap.name="website";
    trap.tabIndex=-1;
    trap.autocomplete="off";
    trap.setAttribute("aria-hidden","true");
    trap.style.position="absolute";
    trap.style.left="-9999px";
    trap.style.width="1px";
    trap.style.height="1px";
    trap.style.opacity="0";
    form.appendChild(trap);
  }

  function showFormError(form,message){
    let error=form.querySelector(".form-error");
    if(!error){
      error=document.createElement("div");
      error.className="form-error";
      error.setAttribute("role","alert");
      error.style.cssText="display:none;background:#fee2e2;border:1px solid #fca5a5;border-radius:6px;padding:.75rem .9rem;margin-bottom:.8rem;color:#7f1d1d;font-weight:600;font-size:.88rem";
      const success=form.querySelector(".form-success");
      if(success)success.insertAdjacentElement("afterend",error);
      else form.prepend(error);
    }
    error.textContent=message;
    error.style.display="block";
  }

  function clearFormError(form){
    const error=form.querySelector(".form-error");
    if(error)error.style.display="none";
  }

  document.querySelectorAll("form.lead-form").forEach(form=>{
    ensureHoneypot(form);

    form.addEventListener("submit",async event=>{
      event.preventDefault();
      if(form.dataset.submitting==="true")return;

      clearFormError(form);
      const success=form.querySelector(".form-success");
      if(success)success.classList.remove("show");

      const data=new FormData(form);
      const payload={
        name:String(data.get("name")||""),
        phone:String(data.get("phone")||""),
        email:String(data.get("email")||""),
        city:String(data.get("city")||""),
        service:String(data.get("service")||""),
        message:String(data.get("message")||""),
        website:String(data.get("website")||""),
        source_page:window.location.pathname||"/",
        form_id:form.id||"lead_form"
      };
      if(/^select/i.test(payload.service))payload.service="";
      if(!payload.service&&!payload.message)payload.message="Callback requested from website";

      const submitButton=form.querySelector('button[type="submit"]');
      const originalButtonText=submitButton?submitButton.textContent:"";
      form.dataset.submitting="true";
      if(submitButton){
        submitButton.disabled=true;
        submitButton.textContent="Sending…";
      }

      try{
        const response=await fetch(LEAD_ENDPOINT,{
          method:"POST",
          headers:{"Content-Type":"application/json"},
          body:JSON.stringify(payload)
        });
        let result={};
        try{result=await response.json();}catch(_error){}
        if(!response.ok||!result.ok){
          throw new Error(result.error||"Request could not be sent");
        }

        if(success){
          if(result.emergency){
            success.innerHTML='✅ Request received. This sounds urgent — please <a href="'+BUSINESS_PHONE_URL+'" style="color:var(--green-dk)">call '+BUSINESS_PHONE+' now</a> for the fastest response.';
          }
          success.classList.add("show");
        }
        form.querySelectorAll("input,select,textarea,button").forEach(control=>{control.disabled=true;});

        if(typeof gtag==="function"){
          gtag("event","generate_lead",{
            form_id:form.id||"lead_form",
            lead_source:"supabase_crm"
          });
        }
      }catch(error){
        console.error("[PP911 Lead Form]",error);
        showFormError(form,"We couldn't send your request. Please call "+BUSINESS_PHONE+" so we don't miss you.");
        form.dataset.submitting="false";
        if(submitButton){
          submitButton.disabled=false;
          submitButton.textContent=originalButtonText;
        }
        if(typeof gtag==="function"){
          gtag("event","lead_submit_error",{form_id:form.id||"lead_form"});
        }
      }
    });
  });

  document.querySelectorAll('a[href^="tel:"]').forEach(link=>{
    link.addEventListener("click",()=>{
      if(typeof gtag==="function"){
        gtag("event","phone_click",{
          phone:"864-446-8911",
          location:document.body.dataset.page||"site"
        });
      }
    });
  });
})();

(()=>{
  const CONFIG={
    priceMultiplier:1,
    discountPercent:10,
    serviceCallFee:null
  };
  window.PP911_PRICING_CONFIG=CONFIG;

  const path=(window.location.pathname||"/").replace(/\/+$/,"")||"/";

  function money(value){
    return "$"+Math.round(value).toLocaleString();
  }

  function addLakeAreaLinks(){
    if(path==="/service-areas"){
      const grid=document.querySelector("main .grid-4");
      if(grid&&!grid.querySelector('[href="/service-areas/iva-lake-secession-sc/"]')){
        grid.insertAdjacentHTML("afterbegin",'<a class="nav-card" href="/service-areas/iva-lake-secession-sc/"><h3>💧 Iva &amp; Lake Secession, SC</h3><p>Well pumps, lake homes &amp; rural plumbing.</p><span class="arrow">Iva &amp; Lake Secession plumber →</span></a><a class="nav-card" href="/service-areas/savannah-lakes-village-sc/"><h3>🏡 Savannah Lakes Village, SC</h3><p>Well pumps, lift pumps &amp; second-home plumbing.</p><span class="arrow">Savannah Lakes Village plumber →</span></a>');
      }
      const summary=document.querySelector(".page-header .speakable-summary");
      if(summary)summary.textContent="Serving Upstate South Carolina with extra focus on lake and rural communities where well pumps, pressure systems and second-home plumbing matter most.";
    }

    if(path==="/services/well-pump-repair"){
      const hero=document.querySelector(".service-hero");
      if(hero&&!document.getElementById("lake-area-well-pump-focus")){
        hero.insertAdjacentHTML("afterend",'<section id="lake-area-well-pump-focus" class="section" style="padding-top:34px;padding-bottom:34px"><div class="container"><div style="background:var(--blue-xlt);border:1.5px solid #90CAF9;border-radius:var(--r2);padding:26px"><span class="label">Priority Well-Pump Markets</span><h2 style="font-size:1.45rem;margin:6px 0 10px">Lake Secession, Iva, McCormick &amp; Savannah Lakes Village</h2><p style="color:var(--ink2);margin-bottom:16px">We are putting extra focus on lake and rural properties where a failed well pump or pressure system can shut the entire home down.</p><div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-blue btn-sm" href="/service-areas/iva-lake-secession-sc/">Iva &amp; Lake Secession →</a><a class="btn btn-blue btn-sm" href="/service-areas/savannah-lakes-village-sc/">Savannah Lakes Village →</a><a class="btn btn-blue btn-sm" href="/service-areas/mccormick-sc/">McCormick →</a></div></div></div></section>');
      }
    }
  }

  function updatePricingPageCopy(){
    if(path!=="/pricing")return;

    document.title="Upfront Plumbing Pricing & Price Estimator | Plumbing Paramedic 911";
    const meta=document.querySelector('meta[name="description"]');
    if(meta)meta.content="Upfront flat-rate plumbing pricing and a customizable price estimator from Plumbing Paramedic 911. Service-call charges and discounts are disclosed before booking; repair prices are approved before work starts.";
    ['meta[property="og:description"]','meta[name="twitter:description"]'].forEach(selector=>{
      const el=document.querySelector(selector);
      if(el)el.content=meta?meta.content:el.content;
    });

    const promiseParagraph=[...document.querySelectorAll("main p")].find(p=>p.textContent.includes("Every price includes labor and standard materials"));
    if(promiseParagraph)promiseParagraph.textContent="Our estimator gives you a useful starting point before you call. Repair pricing is flat-rate, a service/diagnostic charge applies to on-site visits and is disclosed before dispatch, and any additional work is priced before you authorize it.";

    const discountListItem=[...document.querySelectorAll(".check-list li")].find(li=>li.textContent.includes("Military"));
    if(discountListItem)discountListItem.textContent="10% military, veteran, senior and first-responder discount; discounts do not stack";

    const serviceCallFaq=[...document.querySelectorAll(".faq-item")].find(item=>{
      const q=item.querySelector(".faq-q");
      return q&&/service call|diagnostic fee/i.test(q.textContent);
    });
    if(serviceCallFaq){
      const answer=serviceCallFaq.querySelector(".faq-a");
      if(answer)answer.textContent="Yes. An on-site service/diagnostic charge applies and is disclosed before we dispatch. Repair and installation prices are then quoted upfront before work starts. We are updating the calculator to show the exact current service-call amount instead of treating it as $0.";
    }

    document.querySelectorAll("script[type='application/ld+json']").forEach(script=>{
      try{
        const data=JSON.parse(script.textContent);
        const nodes=data&&data['@graph'];
        if(!Array.isArray(nodes))return;
        nodes.forEach(node=>{
          if(node['@type']!=="FAQPage"||!Array.isArray(node.mainEntity))return;
          node.mainEntity.forEach(faq=>{
            if(/service call|diagnostic fee/i.test(faq.name||"")&&faq.acceptedAnswer){
              faq.acceptedAnswer.text="An on-site service/diagnostic charge applies and is disclosed before dispatch. Repair and installation prices are quoted upfront before work begins.";
            }
          });
        });
        script.textContent=JSON.stringify(data);
      }catch(_error){}
    });

    document.querySelectorAll(".option-radio").forEach(option=>{
      const name=option.querySelector(".option-radio-name");
      const price=option.querySelector(".option-radio-price");
      if(!name||!price)return;
      if(name.textContent.includes("Residential Home"))price.textContent="Service call applies";
      if(/Military|Senior Citizen|Police \/ Fire \/ EMS/.test(name.textContent))price.textContent="−10%";
    });

    const discountHeading=[...document.querySelectorAll(".calc-options div")].find(el=>el.textContent.trim()==="🎖️ Discount (if applicable)");
    if(discountHeading)discountHeading.textContent="🎖️ Discount — 10% if applicable (one discount per job)";

    const whButtons=[...document.querySelectorAll("#calc-water-heater .calc-service-btn")];
    const repair=whButtons.find(btn=>btn.textContent.includes("Water Heater Repair"));
    if(repair){
      const range=repair.querySelector(".range");
      if(range)range.textContent="From $149";
      repair.onclick=()=>window.selectService(repair,"Water Heater Repair",149,null);
    }
    const forty=whButtons.find(btn=>btn.textContent.includes("Replace 40-Gal Tank"));
    if(forty){
      const range=forty.querySelector(".range");
      if(range)range.textContent="From $1,699";
      forty.onclick=()=>window.selectService(forty,"Replace 40-Gal Tank",1699,null);
    }

    const resultLabel=document.querySelector(".calc-result-label");
    if(resultLabel)resultLabel.textContent="Your estimated repair / installation price";
    const totalLabel=document.querySelector("#bd-total")?.previousElementSibling;
    if(totalLabel)totalLabel.textContent="Estimated repair price";
    const baseRow=document.getElementById("bd-base")?.parentElement;
    if(baseRow&&!document.getElementById("bd-service-call")){
      baseRow.insertAdjacentHTML("afterend",'<div class="breakdown-row"><span>Service / diagnostic call</span><span id="bd-service-call">Confirmed before dispatch</span></div>');
    }
    const disclaimer=document.querySelector(".calc-disclaimer");
    if(disclaimer)disclaimer.textContent="* Repair/install estimate only. The current service/diagnostic charge is disclosed before dispatch and is not shown as $0. Final repair price is confirmed before work begins. Special materials, code-required upgrades or conditions outside normal scope are quoted before authorization.";
  }

  addLakeAreaLinks();
  updatePricingPageCopy();

  if(!document.querySelector(".calc-wrapper"))return;

  const state={serviceName:"Toilet Repair",low:89,high:149,property:"residential",propertyAdj:0,timing:"business",timingAdj:0,discount:"none",discountPercent:0};

  window.setCalcTab=(name,button)=>{
    document.querySelectorAll(".calc-tab").forEach(tab=>tab.classList.remove("active"));
    button.classList.add("active");
    document.querySelectorAll(".calc-tab-content").forEach(content=>{content.style.display="none";});
    const target=document.getElementById("calc-"+name);
    if(target)target.style.display="block";
  };

  window.selectService=(button,name,low,high)=>{
    document.querySelectorAll(".calc-service-btn").forEach(item=>item.classList.remove("selected"));
    button.classList.add("selected");
    state.serviceName=name;
    state.low=Number.isFinite(Number(low))?Number(low):null;
    state.high=high===null||high===undefined||high===""?null:Number(high);
    update();
  };

  window.selectOption=(button,type,value,adjustment)=>{
    button.parentElement.querySelectorAll(".option-radio").forEach(item=>item.classList.remove("selected"));
    button.classList.add("selected");
    if(type==="property"){
      state.property=value;
      state.propertyAdj=Number(adjustment)||0;
    }
    if(type==="discount"){
      state.discount=value;
      state.discountPercent=value==="none"?0:CONFIG.discountPercent;
    }
    update();
  };

  window.selectTiming=(button,value,adjustment)=>{
    document.querySelectorAll(".timing-btn").forEach(item=>item.classList.remove("active"));
    button.classList.add("active");
    state.timing=value;
    state.timingAdj=Number(adjustment)||0;
    update();
  };

  window.printEstimate=()=>window.print();

  const scaled=value=>value===null?null:Math.round(value*CONFIG.priceMultiplier);
  const rangeText=(low,high)=>{
    if(low===null)return "Call for current price";
    if(high===null||high===low)return "From "+money(low);
    return money(low)+" – "+money(high);
  };

  function update(){
    let low=scaled(state.low);
    let high=scaled(state.high);
    const propertyAdj=scaled(state.propertyAdj)||0;
    const timingAdj=scaled(state.timingAdj)||0;

    if(low!==null)low+=propertyAdj+timingAdj;
    if(high!==null)high+=propertyAdj+timingAdj;

    const discountLow=low!==null?Math.round(low*(state.discountPercent/100)):0;
    const discountHigh=high!==null?Math.round(high*(state.discountPercent/100)):0;
    if(low!==null)low=Math.max(49,low-discountLow);
    if(high!==null)high=Math.max(low||49,high-discountHigh);

    const display=document.getElementById("calcPriceDisplay");
    const sub=document.getElementById("calcPriceSub");
    if(display)display.textContent=rangeText(low,high);
    if(sub)sub.textContent=state.serviceName+" · "+(state.timing==="business"?"Business Hours":"After Hours / Emergency")+" · "+(state.property==="residential"?"Residential":"Commercial");

    const base=document.getElementById("bd-base");
    if(base)base.textContent=rangeText(scaled(state.low),scaled(state.high));
    const surcharge=document.getElementById("bd-surcharge");
    if(surcharge)surcharge.textContent=timingAdj?"+"+money(timingAdj):"$0";
    const commercial=document.getElementById("bd-commercial");
    if(commercial)commercial.textContent=propertyAdj?"+"+money(propertyAdj):"$0";
    const discount=document.getElementById("bd-discount");
    if(discount)discount.textContent=state.discountPercent?"−"+state.discountPercent+"%":"$0";
    const discountLabel=document.getElementById("bd-discount-label");
    if(discountLabel)discountLabel.textContent=state.discount==="none"?"Discount":"Discount ("+state.discount+")";
    const serviceCall=document.getElementById("bd-service-call");
    if(serviceCall)serviceCall.textContent=CONFIG.serviceCallFee===null?"Confirmed before dispatch":money(scaled(CONFIG.serviceCallFee));
    const total=document.getElementById("bd-total");
    if(total)total.textContent=rangeText(low,high);
  }

  update();
})();
