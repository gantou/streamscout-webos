"""Build LG IPK and normalize all payload permissions for WebAppMgr."""
import io,json,os,subprocess,tarfile,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
subprocess.run(['ares-package','app','-o','dist'],cwd=root,check=True)
info=json.loads((root/'app/appinfo.json').read_text())
ipk=root/'dist'/f"{info['id']}_{info['version']}_all.ipk"
raw=subprocess.check_output(['ar','p',str(ipk),'data.tar.gz'])
with tempfile.TemporaryDirectory(dir=os.getenv('TMPDIR',str(root/'dist'))) as tmp:
    output=Path(tmp)/'data.tar.gz'
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as source,tarfile.open(output,mode='w:gz') as target:
        for member in source.getmembers():
            member.mode=0o755 if member.isdir() else 0o644
            member.uid=member.gid=0;member.uname=member.gname='root'
            prefix=f"usr/palm/applications/{info['id']}/"
            original=root/'app'/member.name[len(prefix):] if member.name.startswith(prefix) else None
            # LG's packager minifies JS by default. Preserve audited source bytes
            # in the payload so the hosted and packaged TV frontend are identical.
            if member.isfile() and original is not None and original.is_file():
                data=original.read_bytes();member.size=len(data)
                target.addfile(member,io.BytesIO(data))
            else:
                target.addfile(member,source.extractfile(member) if member.isfile() else None)
    subprocess.run(['ar','r',str(ipk),str(output)],check=True)
subprocess.run(['python3','tests/package_permissions.py'],cwd=root,check=True)
