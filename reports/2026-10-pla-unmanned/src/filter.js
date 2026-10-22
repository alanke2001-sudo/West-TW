// 條目篩選：依關鍵字與類別隱藏卡片，並同步隱藏沒有可見卡片的小節標題
(function(){
  var q=document.getElementById('q'), cnt=document.getElementById('cnt');
  var cards=[].slice.call(document.querySelectorAll('.card')), btns=[].slice.call(document.querySelectorAll('.chiprow button'));
  var heads=[].slice.call(document.querySelectorAll('h3.sub')), ch='';
  function run(){
    var terms=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean), n=0;
    cards.forEach(function(c){
      var ok=(!ch||c.dataset.ch===ch)&&terms.every(function(t){return c.dataset.s.indexOf(t)>=0||c.textContent.toLowerCase().indexOf(t)>=0});
      c.hidden=!ok; if(ok)n++;
    });
    heads.forEach(function(h){
      var el=h.nextElementSibling, any=false;
      while(el&&el.classList.contains('card')){ if(!el.hidden)any=true; el=el.nextElementSibling; }
      h.hidden=!any;
    });
    cnt.textContent='顯示 '+n+' / '+cards.length+' 筆條目';
  }
  btns.forEach(function(b){b.addEventListener('click',function(){
    ch=b.dataset.ch; btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')}); run();
  })});
  q.addEventListener('input',run); run();
})();
