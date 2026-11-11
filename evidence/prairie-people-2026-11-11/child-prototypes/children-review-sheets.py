"""Review sheets from unmodified source photos and actual town screenshots.
No approval or photographic verdict is assigned by this script.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import hashlib,json,sys,textwrap
shots=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
refs=Path('/workspace/chicago-evidence/evidence/prairie-people-2026-11-11')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=ImageFont.truetype(font,20); H=ImageFont.truetype(font,28); S=ImageFont.truetype(font,16)
configs=[
 ('child_boy_1904','Boy — Arthur M. Walker, age 8','roosevelt-sons-1904.jpg',(.64,.45,.89,.95),'Archibald Roosevelt, age 9, right; Hewitt / NY Tribune, 29 May 1904. Knee trousers, stockings, jacket.'),
 ('child_girl_1904','Girl — Margaret Shortall, age 8','children-tea-1904.jpg',(.29,.34,.46,.69),'Girl at left, identity unconfirmed; Snyder, Oxford, Ohio, August 1904. Sleeved, waisted frock; kneeling pose hides hem length.'),
 ('child_toddler_1904','Toddler — John Glessner, age 2','children-tea-1904.jpg',(.29,.34,.46,.69),'Older child, not a toddler: Snyder, August 1904. The toddler frock extrapolates this silhouette; no same-age reference located.'),
 ('teen_boy_1904','Teen boy — Marcel Longini, age 14','roosevelt-sons-1904.jpg',(.11,.33,.34,.92),'Kermit Roosevelt, age 14, left; Hewitt / NY Tribune, 29 May 1904. Jacket and long trousers.'),
 ('teen_girl_1904','Teen girl — Elizabeth S. Cunningham, age 15','roosevelt-family-1903.jpg',(.14,.22,.315,.94),'Ethel Roosevelt, age 11, left; Pach Brothers, 12 July 1903, LOC 2009631485. Younger comparison: long sleeves and skirt. Added after construction; not an individual likeness.')]
report={'source_sha':json.loads((shots/'town-preview.json').read_text())['source_sha'],'status':'unreviewed','scope':'New 1904 clothes on actual exported child/teen models, staged in published town with temporary review overlays. References show other people. No owner approval, photographic acceptance or production activation claimed. Screenshots are resized only. Source crops are identified in normalized coordinates.','sheets':[]}
for role,title,ref,crop,caption in configs:
 raw=Image.open(refs/ref).convert('RGB'); region=raw.crop(tuple(round(v*(raw.width if i%2==0 else raw.height)) for i,v in enumerate(crop)))
 for band in ['near','far']:
  canvas=Image.new('RGB',(1600,1050),(241,242,244)); d=ImageDraw.Draw(canvas)
  d.text((20,14),title,fill='#17212e',font=H)
  d.text((20,55),f'{3 if band=="near" else 10} m / street eye 1.68 m / 1904-07-01, 10:00 / reconstructed appearance',fill='#334155',font=F)
  d.text((20,92),'Period clothing reference',fill='#17212e',font=F)
  d.text((510,92),'Desktop — actual town renderer',fill='#17212e',font=F)
  d.text((1180,92),'Phone',fill='#17212e',font=F)
  ri=ImageOps.contain(region,(470,780));canvas.paste(ri,(20+(470-ri.width)//2,125))
  desk=Image.open(shots/f'{role}-{band}-desktop.png').convert('RGB');desk=ImageOps.contain(desk,(640,780));canvas.paste(desk,(510,125))
  phone=Image.open(shots/f'{role}-{band}-phone.png').convert('RGB');phone=ImageOps.contain(phone,(390,780));canvas.paste(phone,(1180,125))
  y=930
  for line in textwrap.wrap(caption,145):d.text((20,y),line,fill='#334155',font=S);y+=22
  d.text((20,1018),'Review prototype: clothes, face and colours reconstructed. Staging location is not a residence claim.',fill='#334155',font=S)
  name=f'{role}-{band}-comparison.jpg';canvas.save(out/name,quality=92)
  report['sheets'].append({'role':role,'band':band,'file':name,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),'reference':ref,'reference_sha256':hashlib.sha256((refs/ref).read_bytes()).hexdigest(),'crop_normalized':crop,'caption':caption})
 motion=Image.new('RGB',(1600,300),(241,242,244));d=ImageDraw.Draw(motion);d.text((12,10),title+' — five-second walk samples',font=H,fill='#17212e')
 for i in range(5):
  im=Image.open(shots/f'{role}-walk-{i}-desktop.png').convert('RGB');im=ImageOps.contain(im,(320,200));motion.paste(im,(i*320,60));d.text((i*320+8,267),f'{i*1.25:g} s',font=S,fill='#334155')
 motion.save(out/f'{role}-motion.jpg',quality=92)
(out/'review-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
