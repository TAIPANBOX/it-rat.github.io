/* IT-RAT v2 - shared behaviors: stack registry, reveal, counters,
   command palette, directional page transitions. Vanilla, no deps. */
(function(){
"use strict";

/* ---- the stack registry: single source of truth for navigation ---- */
/* Order is the corridor: the rail, the left/right arrows, the dots and the
   palette all walk it. It opens on the money plane, then the control room you
   actually run and the memory underneath it, then the rest of the planes. The
   two iOS rooms come last together: neither is something you can run today. */
const STACK = [
  {id:"tokenfuse", name:"TokenFuse",  plane:"money",     color:"#F4B23E", what:"Runtime spend control and the in-line kill switch", href:"services/tokenfuse.html"},
  {id:"enterprise",name:"Genaryx",    plane:"control room", color:"#B48CFF", what:"The paid control room over all of it, in your browser on your own box", href:"enterprise.html", tier:"enterprise"},
  {id:"engram",    name:"Engram",     plane:"memory",    color:"#6C7BFF", what:"The SQLite of agent memory",                      href:"services/engram.html"},
  {id:"wardryx",   name:"Wardryx",    plane:"policy",    color:"#2DD4BF", what:"Policy decisions with a human in the loop",       href:"services/wardryx.html"},
  {id:"idryx",     name:"Idryx",      plane:"access",    color:"#34D399", what:"One identity graph for humans, keys and agents",  href:"services/idryx.html"},
  {id:"qryx",      name:"Qryx",       plane:"crypto",    color:"#B48CFF", what:"Cryptography inventory and post-quantum risk",    href:"services/qryx.html"},
  {id:"verdryx",   name:"Verdryx",    plane:"quality",   color:"#FF7AA2", what:"Cost per correctly resolved case, not per token", href:"services/verdryx.html"},
  {id:"mockryx",   name:"Mockryx",    plane:"pre-prod",  color:"#FF8A5B", what:"Fire drills that prove guardrails hold",          href:"services/mockryx.html"},
  {id:"platform",  name:"Platform",   plane:"contract",  color:"#93A8C4", what:"Agent Passport, shared contract, Terraform",      href:"services/platform.html"},
  {id:"pocket",    name:"TokenFuse Pocket", plane:"iOS · watchOS", color:"#22D3EE", what:"The kill switch on your wrist",          href:"services/pocket.html", tier:"exploration"},
  {id:"sphere",    name:"Sphere",     plane:"iOS",       color:"#A3E635", what:"Personal life intelligence, twelve agents",       href:"services/sphere.html", tier:"personal"},
];
window.STACK = STACK;

const here = (document.body.dataset.service||"").trim();
const idx = STACK.findIndex(s=>s.id===here);
const root = (document.body.dataset.root||"").trim(); // "" on home, "../" inside /services/

/* ---- directional cross-document transitions ---- */
function markDir(dir){ try{sessionStorage.setItem("nav-dir",dir);}catch(e){} }
document.addEventListener("click",e=>{
  const a = e.target.closest("a[data-dir]");
  if(a) markDir(a.dataset.dir);
});
(function applyDir(){
  let dir=null; try{dir=sessionStorage.getItem("nav-dir");sessionStorage.removeItem("nav-dir");}catch(e){}
  if(!dir) return;
  const cls = dir==="back" ? "slide-back" : "slide-fwd";
  document.documentElement.classList.add(cls);
  if("onpagereveal" in window){
    addEventListener("pagereveal",()=>setTimeout(()=>document.documentElement.classList.remove(cls),450),{once:true});
  } else setTimeout(()=>document.documentElement.classList.remove(cls),450);
})();

/* ---- edge prev/next + dots, injected on service pages ---- */
if(idx>=0){
  const prev = STACK[(idx-1+STACK.length)%STACK.length];
  const next = STACK[(idx+1)%STACK.length];
  const mountEdge = document.querySelector("[data-edge-nav]");
  if(mountEdge){
    mountEdge.classList.add("edge-nav");
    mountEdge.innerHTML =
      `<a class="edge prev" data-dir="back" href="${root}${prev.href}">
         <span class="arrow">&#8592;</span><span class="dir">previous</span>
         <span class="name" style="color:${prev.color}">${prev.name}</span>
         <span class="what">${prev.what}</span></a>
       <a class="edge next" data-dir="fwd" href="${root}${next.href}">
         <span class="arrow">&#8594;</span><span class="dir">next</span>
         <span class="name" style="color:${next.color}">${next.name}</span>
         <span class="what">${next.what}</span></a>`;
  }
  const dots = document.createElement("nav");
  dots.className="dots"; dots.setAttribute("aria-label","Stack");
  dots.innerHTML = STACK.map((s,i)=>
    `<a href="${root}${s.href}" title="${s.name}" ${i===idx?'class="on"':""} data-dir="${i>idx?"fwd":"back"}"></a>`).join("");
  document.body.appendChild(dots);

  /* keyboard: page left / page right through the stack */
  addEventListener("keydown",e=>{
    if(e.metaKey||e.ctrlKey||e.altKey) return;
    const tag=(document.activeElement&&document.activeElement.tagName)||"";
    if(/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    if(e.key==="ArrowRight"){markDir("fwd");location.href=root+next.href;}
    if(e.key==="ArrowLeft"){markDir("back");location.href=root+prev.href;}
  });
}

/* ---- reveal on scroll ---- */
const io = new IntersectionObserver(es=>{
  es.forEach(en=>{ if(en.isIntersecting){en.target.classList.add("in"); io.unobserve(en.target);} });
},{threshold:.12, rootMargin:"0px 0px -6% 0px"});
document.querySelectorAll(".rv").forEach(el=>io.observe(el));

/* ---- tick-up counters: <span data-count="176" data-decimals="0" data-prefix="" data-suffix=""> ---- */
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const cio = new IntersectionObserver(es=>{
  es.forEach(en=>{
    if(!en.isIntersecting) return; cio.unobserve(en.target);
    const el=en.target, target=parseFloat(el.dataset.count), dec=+(el.dataset.decimals||0);
    const pre=el.dataset.prefix||"", suf=el.dataset.suffix||"";
    if(reduce){el.textContent=pre+target.toFixed(dec)+suf;return;}
    const t0=performance.now(), dur=1200+Math.random()*500;
    (function tick(t){
      const p=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-p,3);
      el.textContent=pre+(target*e).toFixed(dec)+suf;
      if(p<1) requestAnimationFrame(tick);
    })(t0);
  });
},{threshold:.4});
document.querySelectorAll("[data-count]").forEach(el=>cio.observe(el));

/* ---- command palette ---- */
const k = document.createElement("div");
k.className="cmdk"; k.innerHTML =
  `<div class="cmdk-veil"></div>
   <div class="cmdk-box" role="dialog" aria-label="Jump to">
     <input type="text" placeholder="Jump to a service&#8230; (esc to close)" autocomplete="off" spellcheck="false">
     <div class="cmdk-list"></div>
   </div>`;
document.body.appendChild(k);
const kin = k.querySelector("input"), klist = k.querySelector(".cmdk-list");
/* Genaryx is a room in STACK now, so it needs no separate palette entry: it
   used to be appended here because the corridor did not hold it. */
const pages = [{id:"home",name:"Home",plane:"the stack",color:"#E9EFF6",what:"The whole control room",href:"index.html"}].concat(STACK);
let ksel=0, khits=pages;
function kOpen(){k.classList.add("open");kin.value="";ksel=0;kRender("");setTimeout(()=>kin.focus(),10);}
function kClose(){k.classList.remove("open");}
function kGo(p){ if(!p) return; markDir("fwd"); location.href=root+p.href; }
function kRender(q){
  const ql=q.trim().toLowerCase();
  khits = pages.filter(p=>!ql || (p.name+" "+p.plane+" "+p.what).toLowerCase().includes(ql));
  ksel=Math.min(ksel,Math.max(0,khits.length-1));
  klist.innerHTML = khits.length ? khits.map((p,i)=>
    `<div class="cmdk-item${i===ksel?" sel":""}" data-i="${i}">
       <span class="g" style="background:${p.color}"></span>
       <span class="nm">${p.name}</span><span class="ds">${p.what}</span></div>`).join("")
    : `<div class="cmdk-empty">Nothing in the stack matches that.</div>`;
}
function kSelect(i){ /* move selection without rebuilding the DOM */
  ksel=i;
  [...klist.querySelectorAll(".cmdk-item")].forEach((el,j)=>el.classList.toggle("sel",j===ksel));
}
/* delegated: hovering moves the selection, one click (or tap) navigates */
klist.addEventListener("pointermove",e=>{
  const it=e.target.closest(".cmdk-item");
  if(it && +it.dataset.i!==ksel) kSelect(+it.dataset.i);
});
klist.addEventListener("click",e=>{
  const it=e.target.closest(".cmdk-item");
  if(it) kGo(khits[+it.dataset.i]);
});
kin&&kin.addEventListener("input",()=>{ksel=0;kRender(kin.value);});
addEventListener("keydown",e=>{
  if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();k.classList.contains("open")?kClose():kOpen();}
  else if(e.key==="/" && !k.classList.contains("open")){
    const tag=(document.activeElement&&document.activeElement.tagName)||"";
    if(!/INPUT|TEXTAREA/.test(tag)){e.preventDefault();kOpen();}
  }
  else if(!k.classList.contains("open")) return;
  else if(e.key==="Escape") kClose();
  else if(e.key==="ArrowDown"){e.preventDefault();kSelect(Math.min(khits.length-1,ksel+1));}
  else if(e.key==="ArrowUp"){e.preventDefault();kSelect(Math.max(0,ksel-1));}
  else if(e.key==="Enter") kGo(khits[ksel]);
});
k.querySelector(".cmdk-veil").addEventListener("click",kClose);
document.querySelectorAll("[data-cmdk]").forEach(b=>b.addEventListener("click",kOpen));

/* ---- hero headline: split into words for the rise-in ---- */
(function(){
  if(reduce) return;
  const h1=document.querySelector(".svc-hero h1");
  if(!h1) return;
  h1.classList.remove("rv","d1","d2","d3");
  let wi=0;
  function split(node){
    [...node.childNodes].forEach(ch=>{
      if(ch.nodeType===3){
        const frag=document.createDocumentFragment();
        ch.textContent.split(/(\s+)/).forEach(part=>{
          if(!part) return;
          if(/^\s+$/.test(part)){frag.appendChild(document.createTextNode(part));return;}
          const s=document.createElement("span");
          s.className="w";s.style.setProperty("--wi",wi++);s.textContent=part;
          frag.appendChild(s);
        });
        node.replaceChild(frag,ch);
      }else if(ch.nodeType===1) split(ch);
    });
  }
  split(h1);
  /* insurance: snap words visible even if animation frames never run */
  setTimeout(()=>h1.classList.add("w-done"),2400);
})();

/* ---- card spotlight: track the cursor with an accent glow ---- */
document.addEventListener("pointermove",e=>{
  const c=e.target.closest&&e.target.closest(".card.hover");
  if(!c) return;
  const r=c.getBoundingClientRect();
  c.style.setProperty("--mx",(e.clientX-r.left)+"px");
  c.style.setProperty("--my",(e.clientY-r.top)+"px");
});

/* ---- reading progress hairline ---- */
(function(){
  const bar=document.createElement("div");
  bar.className="progress";bar.setAttribute("aria-hidden","true");
  document.body.appendChild(bar);
  let raf=null;
  function paint(){
    raf=null;
    const max=document.documentElement.scrollHeight-innerHeight;
    bar.style.width=(max>0?Math.min(100,scrollY/max*100):0)+"%";
  }
  addEventListener("scroll",()=>{if(!raf)raf=requestAnimationFrame(paint);},{passive:true});
  paint();
})();

/* ---- the Enterprise door opens onto two rooms ----
   The pager only runs paired to a Genaryx relay, so it is not a service anyone
   could adopt on its own: it belongs behind the same nav item, not beside the
   open stack. Progressive enhancement, so with no JS the link still goes to
   Genaryx exactly as before. */
(function(){
  const trigger = document.querySelector('.topbar a.tb-link[href$="enterprise.html"]');
  if(!trigger) return;
  const wrap = document.createElement("div");
  wrap.className = "tb-menu";
  trigger.parentNode.insertBefore(wrap, trigger);
  wrap.appendChild(trigger);
  trigger.insertAdjacentHTML("beforeend", '<span class="tb-caret" aria-hidden="true">&#9660;</span>');
  trigger.setAttribute("aria-haspopup", "true");
  trigger.setAttribute("aria-expanded", "false");

  const pop = document.createElement("div");
  pop.className = "tb-pop";
  pop.setAttribute("role", "menu");
  pop.innerHTML =
    `<a role="menuitem" href="${root}enterprise.html">Genaryx<span>the control room over the stack</span></a>
     <a role="menuitem" href="${root}services/pocket.html">TokenFuse Pocket<span>the same fleet on the phone and the wrist</span></a>`;
  wrap.appendChild(pop);

  const close = () => { wrap.classList.remove("open"); trigger.setAttribute("aria-expanded","false"); };
  trigger.addEventListener("click", e => {
    e.preventDefault();
    const open = !wrap.classList.contains("open");
    wrap.classList.toggle("open", open);
    trigger.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("click", e => { if(!wrap.contains(e.target)) close(); });
  document.addEventListener("keydown", e => { if(e.key === "Escape") close(); });
})();

/* ---- horizontal rail: wheel scrolls sideways ----
   The rail no longer snaps at all (see site.css): a snapping container re-snaps
   every programmatic scroll, so it lurched one card at a time, and suspending
   snapping only for the gesture just moved the jolt to the end of it, measured
   at a 163px jump the moment the tail of a swipe ran out. It now stops where it
   was left. */
document.querySelectorAll(".rail").forEach(r=>{
  r.addEventListener("wheel",e=>{
    const dx=Math.abs(e.deltaX), dy=Math.abs(e.deltaY);
    if(!dx && !dy) return;
    /* Both axes are driven here, on purpose. Handing sideways gestures back to
       the browser left them scrolling a snapping container, which resists a
       live trackpad swipe and reads as the rail braking under your fingers,
       while up-and-down felt free because it came through this path. Same path,
       same feel, either way you push it. Preventing the default also keeps a
       sideways swipe from being taken as the back gesture. */
    const before=r.scrollLeft;
    r.scrollLeft += dx>dy ? e.deltaX : e.deltaY;
    /* The gesture is only claimed if the rail actually moved. At either end it
       has nothing left to give, so the page gets the scroll instead of it being
       swallowed, and resting the cursor on a rail that has run out of travel no
       longer makes the page feel stuck. Comparing before and after beats
       comparing against 0 and the max: the container's own padding puts its
       resting start at 4px, not 0, so a threshold here would need a magic
       number and would drift the moment that padding changed. */
    if(r.scrollLeft!==before) e.preventDefault();
  },{passive:false});
});
})();
