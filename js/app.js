let L="ar",C={},F="all";const $=id=>document.getElementById(id),f=n=>n.toLocaleString("en-US");
try{C=JSON.parse(localStorage.getItem("mhdc")||"{}")}catch(e){}
function save(){try{localStorage.setItem("mhdc",JSON.stringify(C))}catch(e){}}
function cnt(){return Object.values(C).reduce((a,b)=>a+b,0)}
function sum(){return P.reduce((a,p)=>a+(C[p.id]||0)*p.price,0)}
function setQ(id,d){C[id]=Math.max(0,(C[id]||0)+d);if(!C[id])delete C[id];save();draw()}
function draw(){const t=T[L];
 const card=p=>{const q=C[p.id]||0;return `<article class="p"><div class="im ${p.fit}"><img src="${p.img}" alt="${p.n[L]}" loading="lazy"></div><div class="b"><h3>${p.n[L]}</h3>${p.d?`<p class="d">${p.d[L]}</p>`:`<p class="d"></p>`}<div class="price">${f(p.price)}<small>${t.cur}</small></div>${q?`<div class="qty"><button data-m="${p.id}" aria-label="-">−</button><span>${q}</span><button data-a="${p.id}" aria-label="+">+</button></div>`:`<button class="add" data-a="${p.id}">${t.add}</button>`}</div></article>`};
 const used=SEC.filter(s=>P.some(x=>x.cat===s.id));if(F!=="all"&&!used.some(s=>s.id===F))F="all";
 $("chips").innerHTML=[["all",t.all]].concat(used.map(s=>[s.id,s[L]])).map(x=>`<button class="chip" data-f="${x[0]}" aria-pressed="${F===x[0]}">${x[1]}</button>`).join("");
 $("grid").innerHTML=F==="all"?used.map(s=>`<h2 class="sh">${s[L]}</h2>`+P.filter(p=>p.cat===s.id).map(card).join("")).join(""):P.filter(p=>p.cat===F).map(card).join("");
 const n=cnt();$("bar").classList.toggle("on",n>0);$("bn").textContent=`${t.view} (${n})`;$("bt").textContent=`${f(sum())} ${t.cur}`;
 $("tv").textContent=`${f(sum())} ${t.cur}`;
 $("items").innerHTML=n?P.filter(p=>C[p.id]).map(p=>`<div class="it"><img src="${p.img}" alt=""><div class="n"><b>${p.n[L]}</b><span>${f(p.price*C[p.id])} ${t.cur}</span></div><div class="qty"><button data-m="${p.id}" aria-label="-">−</button><span>${C[p.id]}</span><button data-a="${p.id}" aria-label="+">+</button></div></div>`).join(""):`<p class="empty">${t.empty}</p>`;
 $("co").style.display=n?"block":"none";if(!n&&$("sheet").classList.contains("on"))null}
function setL(l){L=l;const d=T[l];document.documentElement.lang=l==="en"?"en":l;document.documentElement.dir=l==="en"?"ltr":"rtl";
 document.querySelectorAll("[data-k]").forEach(e=>e.textContent=d[e.dataset.k]);
 document.querySelectorAll(".lang button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===l));
 try{localStorage.setItem("mhdl",l)}catch(e){}draw()}
document.addEventListener("click",e=>{const fc=e.target.closest("[data-f]");if(fc){F=fc.dataset.f;draw();return}
 const a=e.target.closest("[data-a]"),m=e.target.closest("[data-m]");
 if(a)setQ(+a.dataset.a,1);else if(m)setQ(+m.dataset.m,-1)});
document.querySelectorAll(".lang button").forEach(b=>b.onclick=()=>setL(b.dataset.l));
$("openCart").onclick=()=>{$("sheet").classList.add("on");$("err").textContent=""};
$("close").onclick=()=>$("sheet").classList.remove("on");
$("sheet").onclick=e=>{if(e.target===$("sheet"))$("sheet").classList.remove("on")};
document.addEventListener("keydown",e=>{if(e.key==="Escape")$("sheet").classList.remove("on")});
$("send").onclick=()=>{const t=T[L],nm=$("nm").value.trim(),ph=$("ph").value.trim(),ad=$("ad").value.trim(),nt=$("nt").value.trim();
 if(!nm||!ph||!ad){$("err").textContent=t.need;return}
 if(!WA_NUMBER){$("err").textContent=t.nowa;return}
 const lines=P.filter(p=>C[p.id]).map(p=>`• ${p.n.ar} × ${C[p.id]} = ${f(p.price*C[p.id])} د.ع`);
 const msg=`طلب جديد من موقع ${SHOP_NAME}\n\n${lines.join("\n")}\n\nالمجموع: ${f(sum())} د.ع\n\nالاسم: ${nm}\nالهاتف: ${ph}\nالعنوان: ${ad}${nt?`\nملاحظات: ${nt}`:""}`;
 window.open(`https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`,"_blank","noopener")};
let s="ar";try{s=localStorage.getItem("mhdl")||"ar"}catch(e){}setL(T[s]?s:"ar");
