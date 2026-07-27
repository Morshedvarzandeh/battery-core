(()=>{
"use strict";
const visual=document.getElementById("visual"),lane=document.getElementById("ion-lane"),electrolyteRegion=document.getElementById("electrolyte-region");
const modeButtons=[...document.querySelectorAll("[data-mode]")];
const inspectButtons=[...document.querySelectorAll("[data-inspect]")];
const parts=[...document.querySelectorAll("[data-part]")];
const motion=document.getElementById("motion");
const modeStatus=document.getElementById("mode-status");
const reduceMotion=matchMedia("(prefers-reduced-motion: reduce)");
// Single source of truth for the horizontal inset: CSS owns it, JS reads it.
const readInset=()=>(parseFloat(getComputedStyle(visual).getPropertyValue("--inset"))||7)/100;
const details={
"negative-electrode":{title:"Negative electrode — graphite",discharge:"During discharge, lithium stored in graphite is oxidized. Lithium ions enter the electrolyte and electrons enter the external circuit.",charge:"During charge, graphite is reduced. It accepts electrons from the charger and lithium ions return from the positive electrode."},
"positive-electrode":{title:"Positive electrode — lithium metal oxide",discharge:"During discharge, the positive electrode is reduced. It accepts electrons from the external circuit and lithium ions from the electrolyte.",charge:"During charge, the positive electrode is oxidized. It releases lithium ions into the electrolyte and electrons toward the charger."},
"electrolyte":{title:"Electrolyte",discharge:"The nonaqueous lithium-salt electrolyte conducts lithium ions inside the cell while blocking electronic current.",charge:"The electrolyte conducts lithium ions back toward the negative electrode while still blocking electrons."},
"separator":{title:"Separator",discharge:"The separator is electronically insulating and ionically permeable. It keeps the electrodes physically apart and reduces the risk of an internal short circuit.",charge:"Its function is unchanged during charge: keep the electrodes apart while allowing lithium-ion transport."},
"negative-collector":{title:"Negative current collector — copper",discharge:"The copper collector conducts electrons from the graphite coating to the negative terminal without being the active lithium-storage material.",charge:"It carries electrons from the external charger into the graphite electrode."},
"positive-collector":{title:"Positive current collector — aluminum",discharge:"The aluminum collector distributes electrons from the positive terminal into the positive-electrode coating.",charge:"It carries electrons away from the positive electrode toward the external charger."}
};
let mode="discharge",running=true,selected=null,animations=[];
function clearMotion(){animations.forEach(a=>a.cancel());animations=[];document.querySelectorAll(".particle").forEach(p=>p.remove())}
function makeParticle(cls,text,parent){const p=document.createElement("span");p.className="particle "+cls;p.textContent=text;p.setAttribute("aria-hidden","true");parent.appendChild(p);return p}
function electronMotion(){const w=visual.getBoundingClientRect().width,inset=readInset();
 const probe=makeParticle("electron","e−",visual),half=(probe.offsetWidth||19)/2;probe.remove();
 // 31.5 = centreline of the 3px wire top border; 162 = centre of a 34px terminal at top:145px.
 const left=w*inset-half,right=w*(1-inset)-half,top=31.5-half,y=162-half;
 const forward=[{transform:`translate(${left}px,${y}px)`},{transform:`translate(${left}px,${top}px)`},{transform:`translate(${right}px,${top}px)`},{transform:`translate(${right}px,${y}px)`}];
 const route=mode==="discharge"?forward:[...forward].reverse();
 for(let i=0;i<10;i++){const p=makeParticle("electron","e−",visual);animations.push(p.animate(route,{duration:5200,iterations:Infinity,delay:-i*520,easing:"linear"}))}
}
function ionMotion(){const w=lane.getBoundingClientRect().width,a=w*.18,b=w*.82;
 const route=mode==="discharge"?[{transform:`translate(${a}px,0)`},{transform:`translate(${b}px,0)`}]:[{transform:`translate(${b}px,0)`},{transform:`translate(${a}px,0)`}];
 for(let i=0;i<8;i++){const p=makeParticle("lithium","Li+",lane);p.style.top=(5+(i%2)*26)+"px";animations.push(p.animate(route,{duration:4300,iterations:Infinity,delay:-i*537.5,easing:"linear"}))}
}
function applyMotion(){animations.forEach(a=>running?a.play():a.pause());motion.textContent=running?"Pause motion":"Play motion";motion.setAttribute("aria-pressed",String(running))}
function rebuild(){clearMotion();const reduce=reduceMotion.matches;
 motion.hidden=reduce; // no animations exist under reduced motion, so the toggle would be inert
 if(!reduce){electronMotion();ionMotion();applyMotion()}}
function updateDetails(){
 parts.forEach(p=>{const on=p.dataset.part===selected;p.classList.toggle("selected",on);p.setAttribute("aria-pressed",String(on))});
 electrolyteRegion.classList.toggle("selected",selected==="electrolyte");
 inspectButtons.forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.inspect===selected)));
 const title=document.getElementById("detail-title"),text=document.getElementById("detail-text");
 if(!selected){title.textContent="Select a component";text.textContent="Choose a component above or click directly on the cell cross-section to see its role.";return}
 const d=details[selected];title.textContent=d.title;text.textContent=d[mode]}
function setMode(next){mode=next;const discharge=mode==="discharge";
 modeButtons.forEach(b=>{const active=b.dataset.mode===mode;b.setAttribute("aria-pressed",String(active));b.classList.toggle("active",active)});
 document.getElementById("device").textContent=discharge?"Load":"Charger";
 document.getElementById("electron-flow").textContent=discharge?"Electrons: negative electrode → load → positive electrode":"Electrons: positive electrode → charger → negative electrode";
 document.getElementById("neg-reaction").textContent=discharge?"Oxidation · releases Li+ and e−":"Reduction · accepts Li+ and e−";
 document.getElementById("pos-reaction").textContent=discharge?"Reduction · accepts Li+ and e−":"Oxidation · releases Li+ and e−";
 document.getElementById("ion-flow").textContent=discharge?"Li+ moves internally through the electrolyte toward the positive electrode. Electrons cannot cross the separator and must use the external circuit.":"Li+ moves internally through the electrolyte toward the negative electrode. The charger drives electrons through the external circuit.";
 document.getElementById("role-heading").textContent=discharge?"Reaction roles during discharge":"Reaction roles during charge";
 document.getElementById("anode").textContent=discharge?"Negative electrode, where oxidation occurs.":"Positive electrode, where oxidation occurs.";
 document.getElementById("cathode").textContent=discharge?"Positive electrode, where reduction occurs.":"Negative electrode, where reduction occurs.";
 modeStatus.textContent=discharge?"Discharge mode. Electrons move through the external circuit from the negative electrode to the positive electrode, while lithium ions move internally toward the positive electrode.":"Charge mode. The charger drives electrons toward the negative electrode, while lithium ions move internally toward the negative electrode.";
 updateDetails();rebuild()}
function choose(part){
 selected=selected===part?null:part;
 updateDetails();
 if(selected){
   document.getElementById("detail-title").scrollIntoView({behavior:reduceMotion.matches?"auto":"smooth",block:"nearest"});
 }
}
modeButtons.forEach(b=>b.addEventListener("click",()=>setMode(b.dataset.mode)));
motion.addEventListener("click",()=>{running=!running;applyMotion()});
inspectButtons.forEach(b=>b.addEventListener("click",()=>choose(b.dataset.inspect)));
parts.forEach(b=>b.addEventListener("click",()=>choose(b.dataset.part)));
reduceMotion.addEventListener("change",rebuild);
let timer;new ResizeObserver(()=>{clearTimeout(timer);timer=setTimeout(rebuild,100)}).observe(visual);
setMode("discharge");
})();
