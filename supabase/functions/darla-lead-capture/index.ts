import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import {createClient} from "npm:@supabase/supabase-js@2.57.4";
const reply=(v:unknown,status=200)=>Response.json(v,{status});
const clean=(v:unknown,n=200)=>typeof v==="string"?v.trim().slice(0,n):"";
const hash=async(v:string)=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(v)))).map(x=>x.toString(16).padStart(2,"0")).join("");
Deno.serve(async(req:Request)=>{
 if(req.method==="GET")return reply({ok:true,service:"darla-lead-capture",version:1});
 if(req.method!=="POST")return reply({ok:false,error:"Method not allowed"},405);
 const token=(req.headers.get("authorization")||"").replace(/^Bearer\s+/i,"").trim();
 if(!token)return reply({ok:false,error:"Unauthorized"},401);
 const key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")||JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS")||"{}").default;
 if(!key)return reply({ok:false,error:"Service unavailable"},503);
 const sb=createClient(Deno.env.get("SUPABASE_URL")!,key,{auth:{persistSession:false,autoRefreshToken:false}});
 const {data:credential,error:authError}=await sb.from("integration_credentials").select("id").eq("provider","vapi").eq("token_hash",await hash(token)).eq("active",true).maybeSingle();
 if(authError||!credential)return reply({ok:false,error:"Unauthorized"},401);
 try{
 const raw=await req.text();if(raw.length>16000)return reply({ok:false,error:"Request too large"},413);
 let b;try{b=JSON.parse(raw)}catch{return reply({ok:false,error:"Invalid JSON"},400)}
 let digits=clean(b.phone).replace(/\D/g,"");if(digits.length===11&&digits[0]==="1")digits=digits.slice(1);
 if(digits.length!==10)return reply({ok:false,error:"A valid US callback number is required"},400);
 const phone="+1"+digits, message=clean(b.message,3000),service=clean(b.service,100),name=clean(b.name,120)||"Unknown Caller";
 if(!message)return reply({ok:false,error:"Issue summary is required"},400);
 const address=clean(b.address,300),city=clean(b.city),issue=[service,message].filter(Boolean).join(" — ");
 const urgent=b.urgency==="emergency"||/emergency|flood|burst|sewage|sewer backup|gas (smell|leak)|smell gas|no water|gushing/i.test(issue);
 const {data:org,error:oe}=await sb.from("organizations").select("id").eq("slug","plumbing-paramedic-911").eq("active",true).single();if(oe||!org)throw Error("Company unavailable");
 const requestKey=await hash("darla|"+org.id+"|"+phone+"|"+issue+"|"+address+"|"+Math.floor(Date.now()/600000));
 const {data:session,error:se}=await sb.from("call_sessions").upsert({organization_id:org.id,external_call_id:"darla-intake:"+requestKey,provider:"vapi",direction:"inbound",status:"in_progress",caller_phone:phone,caller_name:name,ai_summary:issue,emergency:urgent,raw_payload:{source:"darla-lead-capture"}},{onConflict:"external_call_id"}).select("id").single();if(se)throw se;
 let {data:intake,error:ie}=await sb.from("receptionist_intake").select("id").eq("request_key",requestKey).maybeSingle();if(ie)throw ie;
 if(!intake){
 const {data,error}=await sb.from("receptionist_intake").insert({organization_id:org.id,call_session_id:session.id,request_key:requestKey,caller_name:name,phone,address_line1:address||null,city:city||null,state:"SC",issue_summary:issue,urgency:urgent?"emergency":"routine",processing_status:"needs_review",booked:false,access_notes:"Darla voice intake; schedule and dispatch require separate confirmation."}).select("id").single();
 if(error&&error.code!=="23505")throw error;
 if(error){const r=await sb.from("receptionist_intake").select("id").eq("request_key",requestKey).single();if(r.error)throw r.error;intake=r.data;}else intake=data;
 }
 const {data:crm,error:ce}=await sb.rpc("process_receptionist_intake",{p_intake_id:intake!.id});
 if(ce){console.error("Darla processing failed",ce.code);return reply({ok:false,intake_saved:true,request_id:intake!.id,crm_processed:false,error:"Intake saved but CRM processing needs office review"},503);}
 return reply({ok:true,saved:true,request_id:intake!.id,crm_processed:true,lead_id:crm?.lead_id,appointment_confirmed:false,notification_sent:false});
 }catch(e){console.error("Darla lead capture",e instanceof Error?e.message:"error");return reply({ok:false,error:"Could not complete intake. Do not claim it was saved."},500);}
});