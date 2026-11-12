// Renderiza quadro a quadro (determinístico): node render.mjs  |  ONLY=1.5,9 node render.mjs (prévia de quadros)
import {createRequire} from 'node:module';import {mkdirSync} from 'node:fs';import {fileURLToPath} from 'node:url';import path from 'node:path';
const {chromium}=createRequire(import.meta.url)('playwright');
const dir=path.dirname(fileURLToPath(import.meta.url));const OUT=process.env.OUT||path.join(dir,'..','render','frames');mkdirSync(OUT,{recursive:true});
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1920,height:1080}});
pg.on('console',m=>{if(m.type()==='error')console.log('ERR',m.text())});pg.on('pageerror',e=>console.log('PAGEERR',e.message));
await pg.goto('file://'+path.join(dir,'index.html')+'?clean=1');await pg.waitForFunction('window.V&&window.V.ready',{timeout:60000});
const {DURATION,FPS}=await pg.evaluate(()=>({DURATION:window.V.DURATION,FPS:window.V.FPS}));
const only=process.env.ONLY?process.env.ONLY.split(',').map(Number):null;const total=Math.floor(DURATION*FPS);
const list=only?only.map(t=>Math.round(t*FPS)):[...Array(total).keys()];
for(const i of list){await pg.evaluate(t=>window.V.seek(t),i/FPS);
  await pg.locator('#c').screenshot({path:`${OUT}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});
  if(!only&&i%240===0)console.log(i,'/',total)}
await b.close();console.log('ok',list.length,'quadros');
