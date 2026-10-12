
(function(){
  try{
    if(window.top!==window.self) return;              // never redirect an embedded preview (try.html result frame)
    var UARE=/^\/ukr(\/|$)/;
    // Remember an explicit language choice so IP detection never overrides it.
    document.addEventListener('click',function(e){
      var a=e.target&&e.target.closest&&e.target.closest('.lang-switch a, a.lang-other, a.lang-current');
      if(!a)return;
      var href=a.getAttribute('href')||'';
      var selected=a.getAttribute('hreflang')||(UARE.test(href)?'uk':'en');
      try{localStorage.setItem('oo_lang',selected);}catch(_){}
    },true);
    var ua=navigator.userAgent||'';
    // Bots: leave both language trees crawlable — no auto-redirect.
    if(/bot|crawl|spider|slurp|mediapartners|bingpreview|facebookexternalhit|embedly|quora|pinterest|slack|twitter|whatsapp|telegram|discord|yandex|baidu|duckduck|applebot|petalbot|semrush|ahrefs/i.test(ua))return;
    var path=location.pathname||'/';
    if(/^\/(es|pt|de|fr|it|da|sv|nb|fi)(\/|$)/.test(path))return;    // explicit translated URLs always win
    if(/^\/en(\/|$)/.test(path))return;               // legacy /en/ redirect stubs run their own redirect to root
    var pageLang=UARE.test(path)?'uk':'en';
    // Track first real interaction so a slow async lookup never discards typed
    // input (e.g. the /try.html plan form) by navigating out from under the user.
    var touched=false,mark=function(){touched=true;};
    ['keydown','pointerdown','input','touchstart'].forEach(function(ev){
      try{window.addEventListener(ev,mark,{once:true,passive:true,capture:true});}catch(_){try{window.addEventListener(ev,mark,true);}catch(__){}}
    });
    function mirror(){
      var p=UARE.test(path)?(path.replace(/^\/ukr/,'')||'/'):('/ukr'+(path==='/'?'/':path));
      return p+(location.search||'')+(location.hash||'');
    }
    function go(lang){
      if(lang===pageLang)return;
      var alternate=document.querySelector('link[rel="alternate"][hreflang="'+lang+'"]');
      if(!alternate)return;                         // never guess a missing translated page
      var target=alternate.href+(location.search||'')+(location.hash||'');
      var key='oo_lr:'+path+'>'+target;                // one hop per session guards against mirror-mapping loops
      try{if(sessionStorage.getItem(key))return;sessionStorage.setItem(key,'1');}catch(_){}
      location.replace(target);
    }
    function want(cc){return cc==='UA'?'uk':'en';}
    // 1) explicit choice wins
    var pref=null;try{pref=localStorage.getItem('oo_lang');}catch(_){}
    if(/^(es|pt|de|fr|it|da|sv|nb|fi)$/.test(pref||''))return;
    if(pref==='uk'||pref==='en'){go(pref);return;}
    // 2) cached IP-country (7 days) → decide synchronously, no flash on repeat visits
    var cc=null;
    try{var raw=localStorage.getItem('oo_geo');if(raw){var o=JSON.parse(raw);if(o&&o.cc&&o.t&&(Date.now()-o.t)<6048e5)cc=o.cc;}}catch(_){}
    if(cc){go(want(cc));return;}
    // 3) look up country by IP. Third-party surface kept minimal for a medical
    //    site: GeoJS first (keyless, CORS, states no logging), ipapi.co as the
    //    only fallback; both HTTPS + no-referrer. Any failure stays English.
    var eps=[
      ['https://get.geojs.io/v1/ip/country.json',function(j){return j&&j.country;}],
      ['https://ipapi.co/json/',function(j){return j&&(j.country_code||j.country);}]
    ];
    (function tryEp(i){
      if(i>=eps.length)return;                          // all endpoints failed → English default
      var ctl=('AbortController'in window)?new AbortController():null;
      var to=ctl?setTimeout(function(){ctl.abort();},1500):null;
      fetch(eps[i][0],{signal:ctl?ctl.signal:undefined,referrerPolicy:'no-referrer'})
        .then(function(r){return r.ok?r.json():Promise.reject();})
        .then(function(j){
          if(to)clearTimeout(to);
          var code=((eps[i][1](j))||'').toString().toUpperCase();
          if(/^[A-Z]{2}$/.test(code)){
            try{localStorage.setItem('oo_geo',JSON.stringify({cc:code,t:Date.now()}));}catch(_){}
            if(!touched)go(want(code));                 // don't yank a visitor who has started interacting
          }else{tryEp(i+1);}
        })
        .catch(function(){if(to)clearTimeout(to);tryEp(i+1);});
    })(0);
  }catch(_){}
})();
