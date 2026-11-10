/** Exact official published-sheet transform binding, never a blanket SHA exception. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=file=>{const b=fs.readFileSync(file);return {path:file,bytes:b.length,sha256:hash(b)};};
function files(dir,rel=''){return fs.readdirSync(path.join(dir,rel),{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(dir,path.join(rel,e.name)):e.name.endsWith('.glb')?[path.join(rel,e.name)]:[]);}
export async function bindPublishedAsset(root,published,sourcePath,publishedPath,out){
 const source=binding(sourcePath),pub=binding(publishedPath);if(source.sha256===pub.sha256)return {mode:'EXACT_WEB_COPY',source,published:pub,sheets:[]};
 assert.equal(path.basename(sourcePath),'lake_house_construction__shell_1835.glb','unexpected transformed target requires its own exact publisher qualification');
 const tool=path.join(root,'tools/share_glb_sheets.mjs'),m=await import(pathToFileURL(tool).href),src=m.readGlb(fs.readFileSync(sourcePath)),dst=m.readGlb(fs.readFileSync(publishedPath));
 const images=m.movableImages(src.json,src.bin),sheets=[];
 for(const image of images){const view=dst.json.bufferViews[dst.json.images[image.index].bufferView],buffer=dst.json.buffers[view.buffer];if(!buffer.uri)continue;
  assert(buffer.uri.startsWith('sheets/')&&!buffer.uri.includes('..'));assert.equal(path.basename(buffer.uri),m.sheetName(image.bytes,image.mimeType));
  const p=path.resolve(path.dirname(publishedPath),buffer.uri),b=fs.readFileSync(p);assert(b.equals(image.bytes),'resolved texture bytes differ from original embedded WEB image');
  assert(src.json.images[image.index].name.startsWith('common_buff_common_6_'),'unexpected texture provenance');
  sheets.push({image_index:image.index,image_name:src.json.images[image.index].name,mimeType:image.mimeType,uri:buffer.uri,source_embedded_sha256:hash(image.bytes),published:binding(p)});
 }
 assert.equal(sheets.length,2,'this Lake publication must externalize exactly its two K03 maps');
 const needed=new Set(sheets.map(s=>s.source_embedded_sha256)),peers=[];
 for(const rel of files(path.join(root,'assets/web')).sort()){
  const p=path.join(root,'assets/web',rel);if(path.resolve(p)===path.resolve(sourcePath))continue;
  const bytes=fs.readFileSync(p),g=m.readGlb(bytes),held=m.movableImages(g.json,g.bin).filter(i=>needed.has(hash(i.bytes))).map(i=>hash(i.bytes));
  if(!held.length)continue;peers.push({rel,source:binding(p),shares:held});for(const sha of held)needed.delete(sha);if(!needed.size)break;
 }
 assert.equal(needed.size,0,'no real WEB peer establishes the official sharing decision');
 const temp=fs.mkdtempSync(path.join(out,'publisher-repro-')),sourceDir=path.join(temp,'sources'),site=path.join(temp,'site'),glbs=path.join(site,'data/gltf');fs.mkdirSync(sourceDir,{recursive:true});fs.mkdirSync(glbs,{recursive:true});
 const selected=[{rel:path.basename(sourcePath),source},...peers];
 for(const row of selected){for(const dir of [sourceDir,glbs]){const p=path.join(dir,row.rel);fs.mkdirSync(path.dirname(p),{recursive:true});fs.copyFileSync(row.source.path,p);}}
 const transformed=m.shareSheets(site),check=m.checkSheets(site,sourceDir);assert.deepEqual(check.problems,[],'official shared-sheet readback rejected actual source/peer reproduction');
 const generated=path.join(glbs,path.basename(sourcePath));assert(fs.readFileSync(generated).equals(fs.readFileSync(publishedPath)),'official exact selected-copy reproduction differs from actual published GLB');
 for(const sheet of sheets){const generatedSheet=path.join(glbs,sheet.uri);assert.equal(hash(fs.readFileSync(generatedSheet)),sheet.published.sha256);}
 const licenses=path.join(root,'assets/LICENSES.md'),license=path.join(root,'assets/textures/prairie_1904_brick/LICENSE.txt'),material=path.join(root,'assets/textures/prairie_1904_brick/panel/common_buff_common_6/material.json');
 const registry=fs.readFileSync(licenses,'utf8');assert(registry.includes('textures/prairie_1904_brick/**')&&registry.includes('Project-permissive, CC0-equivalent'));
 return {mode:'EXACT_OFFICIAL_SHARED_SHEETS_REPRODUCTION',source,published:pub,official_tool:binding(tool),reproduction:{directory:temp,result:transformed,check,generated:binding(generated),actual_source_peers:peers},sheets,
  textureLicense:{registry:binding(licenses),license:binding(license),material:binding(material),scope:'K03 common_buff_common_6 original procedural project maps, project-permissive CC0-equivalent; no confidence labels removed'},
  invariants:'Official checkSheets proves all placement-free JSON/material/confidence/accessor bindings, every geometry bufferView/meshopt byte and every resolved source image byte unchanged. Exact official output must additionally equal the published GLB byte for byte.'};
}
