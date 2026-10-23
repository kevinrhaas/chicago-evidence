// Read-only, pinned import resolver. A single Node loader worker; no browser.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const HERE=path.dirname(fileURLToPath(import.meta.url));
const binding=JSON.parse(fs.readFileSync(path.join(HERE,'BINDING-RELEASED-FALSE.json'),'utf8'));
const vendor=pathToFileURL(binding.app_root+'/renderers/web/vendor/three-0.185.1/').href;
export async function resolve(s,c,next){
 if(s==='three')return{url:vendor+'three.module.js',shortCircuit:true};
 if(s.startsWith('three/addons/'))return{url:vendor+'addons/'+s.slice(13),shortCircuit:true};
 if(s.startsWith('./')&&c.parentURL?.startsWith(pathToFileURL(HERE+'/modules/').href)){
  const u=new URL(s,c.parentURL);if(!fs.existsSync(fileURLToPath(u)))return{url:new URL(s,pathToFileURL(binding.app_root+'/renderers/web/js/')).href,shortCircuit:true};
 }return next(s,c);
}
export async function load(url,context,next){
 if(url.startsWith('file:')){const p=fileURLToPath(url),pin=binding.inputs[p];if(!pin)throw Error('Unpinned module '+p);const b=fs.readFileSync(p);if(createHash('sha256').update(b).digest('hex')!==pin.sha256)throw Error('Module drift '+p);}
 return next(url,context);
}
