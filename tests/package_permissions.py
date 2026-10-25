"""Verify every shipped directory/file is accessible to the LG web runtime."""
import io,subprocess,tarfile,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
v=json.loads((r/'app/appinfo.json').read_text())
ipk=r/'dist'/f"{v['id']}_{v['version']}_all.ipk"
data=subprocess.check_output(['ar','p',str(ipk),'data.tar.gz'])
with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
    members=archive.getmembers()
    assert members
    for m in members:
        if m.isdir():assert m.mode&0o005==0o005,(m.name,oct(m.mode))
        elif m.isfile():assert m.mode&0o004,(m.name,oct(m.mode))
print('IPK directories traversable and files readable by unprivileged LG runtime')
