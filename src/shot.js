const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
 const p=await b.newPage({viewport:{width:1100,height:900},deviceScaleFactor:2});
 const html=require('fs').readFileSync(process.argv[2],'utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:20000}).catch(e=>console.log('load',e.message));
 const figs=await p.$$('figure');
 for(let i=0;i<figs.length;i++){const id=await figs[i].getAttribute('id'); await figs[i].screenshot({path:'png/'+id+'.png'});}
 await p.screenshot({path:'full.png',fullPage:true});
 await b.close();})();
