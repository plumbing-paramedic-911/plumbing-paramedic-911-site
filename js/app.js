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
  if(!document.querySelector(".calc-wrapper"))return;
  const state={serviceName:"Toilet Repair",low:89,high:149,property:"residential",propertyAdj:0,timing:"business",timingAdj:0,discount:"none",discountAdj:0};
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
    state.low=low;
    state.high=high;
    update();
  };
  window.selectOption=(button,type,value,adjustment)=>{
    button.parentElement.querySelectorAll(".option-radio").forEach(item=>item.classList.remove("selected"));
    button.classList.add("selected");
    if(type==="property"){
      state.property=value;
      state.propertyAdj=adjustment;
    }
    if(type==="discount"){
      state.discount=value;
      state.discountAdj=adjustment;
    }
    update();
  };
  window.selectTiming=(button,value,adjustment)=>{
    document.querySelectorAll(".timing-btn").forEach(item=>item.classList.remove("active"));
    button.classList.add("active");
    state.timing=value;
    state.timingAdj=adjustment;
    update();
  };
  window.printEstimate=()=>window.print();
  const money=value=>"$"+value.toLocaleString();
  function update(){
    let low=state.low+state.propertyAdj+state.timingAdj+state.discountAdj;
    let high=state.high+state.propertyAdj+state.timingAdj+state.discountAdj;
    if(low<49)low=49;
    if(high<low)high=low;
    const display=document.getElementById("calcPriceDisplay");
    const sub=document.getElementById("calcPriceSub");
    if(display)display.textContent=money(low)+" – "+money(high);
    if(sub)sub.textContent=state.serviceName+" · "+(state.timing==="business"?"Business Hours":"After Hours / Emergency")+" · "+(state.property==="residential"?"Residential":"Commercial");
    const surcharge=document.getElementById("bd-surcharge");
    if(surcharge)surcharge.textContent=state.timingAdj?"+$"+state.timingAdj:"$0";
    const commercial=document.getElementById("bd-commercial");
    if(commercial)commercial.textContent=state.propertyAdj?"+$"+state.propertyAdj:"$0";
    const discount=document.getElementById("bd-discount");
    if(discount)discount.textContent=state.discountAdj?"−$"+Math.abs(state.discountAdj):"$0";
    const discountLabel=document.getElementById("bd-discount-label");
    if(discountLabel)discountLabel.textContent=state.discount==="none"?"Discount":"Discount ("+state.discount+")";
    const total=document.getElementById("bd-total");
    if(total)total.textContent=money(low)+" – "+money(high);
  }
  update();
})();