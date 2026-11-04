"""Fixed source-coordinate crop analysis only; never alter source/camera/GLB inputs."""
from pathlib import Path
import hashlib, json
from PIL import Image
P=Path(__file__).resolve().parent
plan=json.loads((P/'PLAN.json').read_bytes());final=json.loads((P/'FINAL-GUARD.json').read_bytes())
assert final['status']=='ACTUAL_EXTERNAL_PAIR_RENDERED_UNREVIEWED'
box=tuple(plan['crop']);scale=plan['analysis_scale'];assert box==(1380,330,1500,420) and scale==8
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for label,p in [('source',Path(plan['inputs']['source_original']['path'])),('before',P/'before-bare-render.png'),('after',P/'after-bare-render.png')]:
 before=sha(p);assert not (P/(label+'-same-fixed-crop-8x.png')).exists()
 if label=='source':assert before==plan['expected']['source']
 else:
  art=next(r for r in final['results'] if r['label']==label)['artifacts']['bare_render'];assert before==art['sha256']
 with Image.open(p) as image:
  assert image.size==(1920,1042)
  crop=image.crop(box);out=P/(label+'-same-fixed-crop-8x.png');crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST).save(out)
 assert sha(p)==before
 rows.append({'label':label,'input':str(p),'input_sha256':before,'crop':box,'scale':scale,'resampling':'NEAREST fixed analysis crop; no fit, annotation, enhancement, or changed source','output':str(out),'output_sha256':sha(out)})
(P/'FIXED-ANALYSIS-CROPS.json').write_text(json.dumps({'analysis_only':True,'camera_source_unchanged':True,'images':rows},indent=2)+'\n')
print(json.dumps({'analysis_crops':3,'camera_or_grade_or_match_claim':False}))
