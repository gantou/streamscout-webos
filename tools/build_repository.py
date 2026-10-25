"""Generate a LAN-only Homebrew Channel catalog from the built IPK."""
import argparse, hashlib, json, shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--base-url',required=True);args=p.parse_args()
root=Path(__file__).resolve().parents[1];out=root/'dist/repository';out.mkdir(parents=True,exist_ok=True)
info=json.loads((root/'app/appinfo.json').read_text());name=f"{info['id']}_{info['version']}_all.ipk";ipk=root/'dist'/name
base=args.base_url.rstrip('/')
shutil.copy2(ipk,out/name);shutil.copy2(root/'app/largeIcon.png',out/'icon.png')
manifest={k:info[k] for k in ['id','version','type','title','appDescription']}
manifest.update(iconUri=base+'/icon.png',sourceUrl='https://github.com/gantou/streamscout-webos',rootRequired=False,ipkUrl=base+'/'+name,ipkSize=ipk.stat().st_size,ipkHash={'sha256':hashlib.sha256(ipk.read_bytes()).hexdigest()})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
catalog={'paging':{'page':1,'count':1,'maxPage':1,'itemsTotal':1,'prevUrl':None,'nextUrl':None},'packages':[{'id':info['id'],'title':info['title'],'iconUri':manifest['iconUri'],'manifestUrl':base+'/manifest.json','manifest':manifest,'pool':'main','shortDescription':'StreamScout TV client — first test build; physical G3 playback not yet verified.'}]}
(out/'repo.json').write_text(json.dumps(catalog,indent=2))
print(base+'/repo.json')
