(function(){
'use strict';
var d=document, w=window; d.documentElement.classList.add('js');
var RM=w.matchMedia('(prefers-reduced-motion: reduce)').matches;
var save=!!(navigator.connection&&(navigator.connection.saveData||/(^|[^4-9])[23]g/.test(navigator.connection.effectiveType||'')));
var PHONE=w.matchMedia('(max-width: 900px), (max-height: 500px)');
function $(s,c){return (c||d).querySelector(s)}function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
function clamp(v,a,b){return v<a?a:v>b?b:v}
function onScroll(fn){var t=false;w.addEventListener('scroll',function(){if(t)return;t=true;requestAnimationFrame(function(){t=false;fn()})},{passive:true})}
function cookie(name){var m=d.cookie.match(new RegExp('(?:^|; )'+name+'=([^;]*)'));return m?decodeURIComponent(m[1]):''}

/* ---------- click ids ride on every booking link ---------- */
(function(){
  var keys=['gclid','wbraid','gbraid','fbclid','msclkid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'];
  var q=new URLSearchParams(location.search), got={};
  keys.forEach(function(k){var v=q.get(k);if(v){got[k]=v;try{sessionStorage.setItem('cc_'+k,v)}catch(e){}}});
  keys.forEach(function(k){if(!got[k]){try{var v=sessionStorage.getItem('cc_'+k);if(v)got[k]=v}catch(e){}}});
  ['gclid','wbraid','gbraid'].forEach(function(k){if(!got[k]){var v=cookie(k);if(v)got[k]=v}});
  if(!got.gclid){var g=cookie('_gcl_aw');if(g){var p=g.split('.');if(p.length>=3)got.gclid=p.slice(2).join('.')}}
  var extra=Object.keys(got).map(function(k){return k+'='+encodeURIComponent(got[k])}).join('&');
  if(extra){$$('a[href^="https://book.campcookstown.com"]').forEach(function(a){a.href+=(a.href.indexOf('?')>-1?'&':'?')+extra})}
})();

/* ---------- header: clear over the hero, solid on the light sections ---------- */
var top=$('#top'), lastY=w.scrollY, heroEl=$('.hero-wrap')||$('.hero.short')||$('.nf'), heroH=0;
function measure(){heroH=heroEl?heroEl.offsetHeight:0}
measure();
function header(){
  var y=w.scrollY;
  if(top){
    top.classList.toggle('solid',y>Math.max(40,heroH-72));
    top.classList.toggle('hide',y>lastY&&y>160&&!d.body.classList.contains('menu-open'));
    if(!heroEl)top.classList.add('onlight');
  }
  lastY=y;
}
header();onScroll(header);w.addEventListener('resize',function(){measure();header()});
var drawer=$('#drawer'), lastFocus=null;
function menu(open){
  d.body.classList.toggle('menu-open',open);
  if(drawer){drawer.classList.toggle('open',open);drawer.setAttribute('aria-hidden',open?'false':'true')}
  $$('[data-menu]').forEach(function(b){b.setAttribute('aria-expanded',open?'true':'false')});
  ['main','#top','footer','#mcta'].forEach(function(s){var el=$(s);if(el){if(open)el.setAttribute('inert','');else el.removeAttribute('inert')}});
  d.documentElement.style.overflow=open?'hidden':'';
  if(open){lastFocus=d.activeElement;var x=$('#drawer .x');if(x)x.focus()}else if(lastFocus&&lastFocus.focus){lastFocus.focus()}
}
$$('[data-menu]').forEach(function(b){b.addEventListener('click',function(){menu(!drawer.classList.contains('open'))})});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&drawer&&drawer.classList.contains('open'))menu(false)});

/* ---------- reveal ---------- */
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -4% 0px',threshold:.02});
$$('.r').forEach(function(el){io.observe(el)});
$$('[data-stagger]').forEach(function(g){$$('.r',g).forEach(function(el,i){el.style.setProperty('--d',Math.min(i*0.08,0.32)+'s')})});

/* ---------- hero video ---------- */
(function(){
  var hero=$('.hero'); if(!hero) return;
  var v=$('video.hv',hero), inner=$('.inner',hero), cv=$('canvas.hbg',hero), pause=$('.pausebtn',hero);
  var mobile=PHONE.matches;
  if(v&&!RM&&!save){
    var src=v.getAttribute(mobile?'data-mobile':'data-desktop');
    var st=parseFloat(v.getAttribute('data-start')||'0');
    v.addEventListener('playing',function(){hero.classList.add('playing')},{once:true});
    if(st>0)v.addEventListener('loadedmetadata',function(){try{v.currentTime=st}catch(e){}},{once:true});
    v.src=src;v.load();var p=v.play();if(p&&p.catch)p.catch(function(){});
    if(pause){pause.hidden=false;pause.addEventListener('click',function(){var on=v.paused;if(on)v.play();else v.pause();pause.setAttribute('aria-pressed',on?'false':'true');pause.querySelector('span').textContent=on?'Pause':'Play'})}
    /* wide screens: the tall video sits in the frame and a blurred copy of the same frame fills the sides */
    if(cv&&!mobile){
      var ctx=cv.getContext('2d'),running=false;
      function paint(){if(!running)return;if(v.readyState>=2&&!v.paused){ctx.drawImage(v,0,0,cv.width,cv.height)}requestAnimationFrame(paint)}
      var vis=new IntersectionObserver(function(es){es.forEach(function(e){running=e.isIntersecting;if(running)paint()})});
      vis.observe(hero);
    }
  }else if(v){v.remove();if(cv)cv.remove();hero.classList.add('still')}
  if(RM||!inner) return;
  var stuck=hero.parentElement&&hero.parentElement.classList.contains('hero-wrap'),hh=hero.offsetHeight||1;
  w.addEventListener('resize',function(){hh=hero.offsetHeight||1});
  function par(){var y=w.scrollY,p=clamp(y/hh,0,1);if(y>hh)return;inner.style.transform='translate3d(0,'+(y*0.22)+'px,0)';inner.style.opacity=String(1-p*1.15)}
  if(stuck){par();onScroll(par)}
})();

/* ---------- photo bands: a slow drift, desktop only, no zoom ---------- */
if(!RM&&!PHONE.matches){var bands=$$('.band .par');if(bands.length){function drift(){var vh=w.innerHeight;bands.forEach(function(b){var r=b.parentElement.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var p=(r.top+r.height/2-vh/2)/vh;b.style.transform='translate3d(0,'+(p*-16)+'px,0)'})}drift();onScroll(drift)}}

/* ---------- the film: scrubbed by scroll on wide screens, a loop on phones ---------- */
(function(){
  var film=$('.film'); if(!film) return;
  var stage=$('.stage',film), cv=$('canvas',film), bar=$('.bar i',film), caps=$$('.cap .c',film), lv=$('video.loop',film);
  var n=parseInt(film.getAttribute('data-frames'),10), base=film.getAttribute('data-base');
  var mobile=PHONE.matches;
  function showCap(p){caps.forEach(function(c){var a=parseFloat(c.getAttribute('data-a')),b=parseFloat(c.getAttribute('data-b'));c.classList.toggle('on',p>=a&&(p<b||b>=1))})}
  if(RM||save||mobile){
    film.classList.add('static');
    if(cv)cv.remove();
    if(lv&&!RM&&!save){
      lv.src=lv.getAttribute('data-src');lv.load();
      var near=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var p=lv.play();if(p&&p.catch)p.catch(function(){})}else{lv.pause()}})},{rootMargin:'30% 0px'});
      near.observe(film);
      lv.addEventListener('playing',function(){film.classList.add('playing')},{once:true});
      lv.addEventListener('timeupdate',function(){if(lv.duration)showCap(lv.currentTime/lv.duration)});
      showCap(0);
    }else{if(lv)lv.remove();caps.forEach(function(c){c.classList.add('on')})}
    return;
  }
  if(lv)lv.remove();
  var frames=new Array(n), ctx=cv.getContext('2d'), cur=-1, pending=-1, started=false, cw=0, ch=0;
  function url(i){return base+'/d/'+String(i+1).padStart(3,'0')+'.webp'}
  function size(){var r=Math.min(w.devicePixelRatio||1,1.5),nw=Math.min(Math.round(stage.clientWidth*r),1400),nh=Math.round(nw*stage.clientHeight/stage.clientWidth);if(nw===cw&&nh===ch)return;cw=cv.width=nw;ch=cv.height=nh;cur=-1;draw(pending<0?0:pending)}
  function nearest(i){for(var k=0;k<n;k++){var a=frames[i-k],b=frames[i+k];if(a&&a.complete&&a.naturalWidth)return a;if(b&&b.complete&&b.naturalWidth)return b}return null}
  function draw(i){var im=frames[i];if(!im||!im.complete||!im.naturalWidth){pending=i;im=nearest(i);if(!im)return}else{pending=-1}
    if(i===cur)return;cur=i;
    var iw=im.naturalWidth,ih=im.naturalHeight,s=Math.max(cw/iw,ch/ih),dw=iw*s,dh=ih*s;
    ctx.drawImage(im,(cw-dw)/2,(ch-dh)/2,dw,dh);film.classList.add('drawn')}
  function load(){if(started)return;started=true;
    var i=0;function next(){if(i>=n)return;var k=i++;var im=new Image();im.decoding='async';im.onload=function(){if(pending===k||(pending<0&&k===0&&cur<0))draw(k);next()};im.onerror=next;im.src=url(k);frames[k]=im}
    next();next();next();}
  var near=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){load();near.disconnect()}})},{rootMargin:'60% 0px'});
  near.observe(film);
  function upd(){
    var r=film.getBoundingClientRect(), vh=d.documentElement.clientHeight, total=r.height-vh, p=clamp(-r.top/total,0,1);
    if(r.bottom<0||r.top>vh)return;
    draw(Math.min(n-1,Math.floor(p*(n-1)+0.0001)));
    if(bar)bar.style.transform='scaleX('+p+')';
    showCap(p);
  }
  onScroll(upd);w.addEventListener('resize',function(){size();upd()});
  size();upd();
})();

/* ---------- right now at camp (Ontario time) ---------- */
(function(){
  var figs=$$('.day figure[data-slot]'), clocks=$$('.clock'); if(!figs.length&&!clocks.length) return;
  function tick(){
    var now=new Date(), t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',hour:'numeric',minute:'2-digit',hour12:true}).format(now).toLowerCase().replace(/\./g,'').replace(/\s+/g,' ').trim();
    var h=parseInt(new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',hour:'numeric',hour12:false}).format(now),10);
    var slot=h<7?'night':h<9?'dropoff':h<12?'morning':h<14?'midday':h<17?'afternoon':h<19?'evening':'night';
    var label={night:'Lights out with the pack',dropoff:'Drop off',morning:'The big romp',midday:'Pools and shade',afternoon:'Barn naps',evening:'Dinner, one at a time'}[slot];
    figs.forEach(function(f){f.classList.toggle('now-on',f.getAttribute('data-slot')===slot)});
    clocks.forEach(function(c){c.innerHTML='<i></i>It is '+t+' at camp. '+label+'.'});
  }
  tick();setInterval(tick,60000);
})();

/* ---------- live prices from the booking system ---------- */
(function(){
  var els=$$('[data-item-price]'); if(!els.length) return;
  var ctl=('AbortController' in w)?new AbortController():null; if(ctl)setTimeout(function(){ctl.abort()},4000);
  fetch('https://book.campcookstown.com/pricing.json',{signal:ctl?ctl.signal:undefined}).then(function(r){return r.ok?r.json():{}}).then(function(j){
    if(!j)return;
    els.forEach(function(el){var k=el.getAttribute('data-item-price'),v=j[k];
      if(k==='day.perday'&&j['day.pack']&&/^\d+(\.\d+)?$/.test(String(j['day.pack'])))v=String(Math.round(parseFloat(j['day.pack'])/10));
      if(v&&/^\d+(\.\d+)?$/.test(String(v)))el.textContent='$'+String(v).replace(/\.0+$/,'')})
  }).catch(function(){});
})();

/* ---------- mobile floating book bar ---------- */
(function(){
  var m=$('#mcta'); if(!m||!w.matchMedia('(max-width: 999px)').matches) return;
  var hero=$('.hero')||$('.nf'), stop=$$('.cta,footer');
  function chk(){var vh=w.innerHeight, past=hero?hero.getBoundingClientRect().bottom<vh*0.35:w.scrollY>200;
    var over=stop.some(function(s){var r=s.getBoundingClientRect();return r.top<vh-80&&r.bottom>0});
    m.classList.toggle('on',past&&!over&&!d.body.classList.contains('menu-open'))}
  chk();onScroll(chk);w.addEventListener('resize',chk);
})();

/* ---------- review card tilt (pointer devices) ---------- */
if(!RM&&w.matchMedia('(hover:hover) and (pointer:fine)').matches){$$('.review').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateX('+(-y*6)+'deg) rotateY('+(x*8)+'deg) translateY(-3px)'});c.addEventListener('pointerleave',function(){c.style.transform=''})})}

/* ---------- youtube facade ---------- */
$$('.yt[data-id]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var f=d.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+a.getAttribute('data-id')+'?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='Camp Cookstown video';var box=d.createElement('div');box.className='yt';box.appendChild(f);a.replaceWith(box)})});
})();
