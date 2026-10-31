"""Inspect built IPK bytes/modes and synchronized TV/catalog release inputs.

Run after npm run build. --update-catalogs refreshes local release metadata only;
this script never uploads, installs, publishes, or contacts a server.
"""
import argparse
import hashlib
import io
import json
import subprocess
import tarfile
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update-catalogs', action='store_true')
    parser.add_argument('--backend', type=Path, default=Path('/opt/data/streamscout'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    info = json.loads((root / 'app/appinfo.json').read_text())
    version = info['version']
    assert version == json.loads((root / 'package.json').read_text())['version']
    assert version == json.loads((root / 'package-lock.json').read_text())['version']
    assert version == json.loads((root / 'package-lock.json').read_text())['packages']['']['version']
    assert "set('build','" + version + "')" in (root / 'app/config.js').read_text()
    ipk = root / 'dist' / f"{info['id']}_{version}_all.ipk"
    raw = ipk.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    payload = subprocess.check_output(['ar', 'p', str(ipk), 'data.tar.gz'])
    prefix = 'usr/palm/applications/' + info['id'] + '/'
    with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        assert len(names) == len(set(names)), 'Duplicate archive members'
        packed = {m.name: m for m in members}
        for member in members:
            assert member.isdir() or member.isfile(), member.name
            assert member.mode == (0o755 if member.isdir() else 0o644), (member.name, oct(member.mode))
        app_files = [p for p in (root / 'app').rglob('*') if p.is_file()]
        for path in app_files:
            name = prefix + path.relative_to(root / 'app').as_posix()
            stream = archive.extractfile(packed[name])
            assert stream is not None, name
            assert stream.read() == path.read_bytes(), 'Stale packed bytes: ' + name
        packed_tv = {name[len(prefix + 'tv/'):] for name, member in packed.items() if member.isfile() and name.startswith(prefix + 'tv/')}
    source_tv = args.backend / 'streamscout/static/tv'
    backend_files = {p.relative_to(source_tv).as_posix(): p.read_bytes() for p in source_tv.rglob('*') if p.is_file()}
    webos_tv = root / 'app/tv'
    webos_files = {p.relative_to(webos_tv).as_posix(): p.read_bytes() for p in webos_tv.rglob('*') if p.is_file()}
    assert backend_files == webos_files, 'Backend/webOS TV files differ'
    assert packed_tv == set(webos_files), 'Packed TV file set differs'
    assert 'v=' + version in (webos_tv / 'index.html').read_text()
    assert 'v=0.4.14' not in (webos_tv / 'index.html').read_text()
    artwork = json.loads(webos_files['assets/manifest.json'])
    assert len(artwork) == 39
    assert {a['filename'] for a in artwork} == {p.name for p in (webos_tv / 'assets').glob('*.jpg')}
    for art in artwork:
        pixels = webos_files['assets/' + art['filename']]
        assert len(pixels) == art['bytes'] <= 300000
        assert hashlib.sha256(pixels).hexdigest() == art['sha256'], art['filename']
    manifest_path = root / 'homebrew/manifest.json'
    repo_path = root / 'homebrew/repo.json'
    manifest = json.loads(manifest_path.read_text())
    catalog = json.loads(repo_path.read_text())
    if args.update_catalogs:
        manifest.update(version=version, rootRequired=False,
                        ipkUrl=f"https://github.com/gantou/streamscout-webos/releases/download/v{version}/{ipk.name}",
                        ipkSize=len(raw), ipkHash={'sha256': digest})
        catalog['packages'][0]['manifest'] = manifest
        catalog['packages'][0]['shortDescription'] = '39 credited sports photos, varied ambient shuffle and bounded TV shelves. Physical LG unverified.'
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
        repo_path.write_text(json.dumps(catalog, indent=2) + '\n')
        (root / 'index.html').write_bytes(repo_path.read_bytes())
    # Always read back exact targets, including the store's bare-root catalog.
    manifest = json.loads(manifest_path.read_text())
    catalog = json.loads(repo_path.read_text())
    assert (root / 'index.html').read_bytes() == repo_path.read_bytes()
    assert catalog['packages'][0]['manifest'] == manifest
    assert manifest['version'] == version and manifest['rootRequired'] is False
    assert manifest['ipkSize'] == len(raw) and manifest['ipkHash']['sha256'] == digest
    assert manifest['ipkUrl'].endswith(f'/v{version}/{ipk.name}')
    assert (root / f'docs/release-{version}.md').is_file()
    old_release = subprocess.check_output(['git', 'show', 'HEAD:docs/release-0.4.14.md'], cwd=root)
    assert (root / 'docs/release-0.4.14.md').read_bytes() == old_release, 'Previous release notes changed'
    print(json.dumps({'verified': True, 'artifact': str(ipk), 'version': version,
                      'bytes': len(raw), 'sha256': digest, 'packedAppFiles': len(app_files),
                      'packedTvFiles': len(packed_tv), 'photos': len(artwork),
                      'eligiblePhotos': sum(a['actionSuitable'] for a in artwork),
                      'payloadModes': dict(Counter(oct(m.mode) for m in members)),
                      'catalogs': ['homebrew/manifest.json', 'homebrew/repo.json', 'index.html'],
                      'previousReleaseUnchanged': True}, indent=2))


if __name__ == '__main__':
    main()
