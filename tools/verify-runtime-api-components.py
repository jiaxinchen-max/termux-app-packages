#!/usr/bin/env python3
"""Verify APK-matched external API companion catalogs, archives and historical deb identity."""
from pathlib import Path
import argparse,hashlib,json,zipfile,stat,tarfile
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'repository/android-api'
def sha(data): return hashlib.sha256(data).hexdigest()
def require(ok,message):
    if not ok: raise ValueError(message)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,required=True);a=p.parse_args()
    data=(BASE/'runtime-api-components.json').read_bytes();catalog=json.loads(data)
    lock=json.loads((BASE/'source-lock.json').read_text());previous=json.loads((ROOT/'repository/embedded-termux-api-0.60.0-r1.json').read_text())
    require(catalog['schema']==1 and catalog['contract']=='embedded-v1','Catalog schema/contract mismatch')
    require(sha(data)==lock['catalog_sha256'] and lock['components']==catalog['components'],'Source lock mismatch')
    require((a.assets/'runtime-api-components.json').read_bytes()==data,'Published catalog mismatch')
    expected_abis={'arm64-v8a':'aarch64','armeabi-v7a':'arm','x86':'i686','x86_64':'x86_64'}
    require(set(catalog['components'])==set(expected_abis),'Unexpected ABI inventory')
    for abi,entry in catalog['components'].items():
        require(entry['abi']==abi and entry['contract']=='embedded-v1','Component contract mismatch')
        require(entry['url']=='https://github.com/jiaxinchen-max/termux-app-packages/releases/download/'+catalog['release']+'/'+entry['asset'],'Unexpected URL')
        payload=(a.assets/entry['asset']).read_bytes()
        require(len(payload)==entry['size'] and sha(payload)==entry['sha256'],'Archive identity mismatch: '+abi)
        with zipfile.ZipFile(a.assets/entry['asset']) as z:
            infos=z.infolist();require(len(infos)==len(entry['files']) and set(i.filename for i in infos)==set(entry['files']),'Duplicate or unexpected archive entries')
            for i in infos:
                require(not i.is_dir() and not i.filename.startswith('/') and '..' not in Path(i.filename).parts,'Unsafe archive path')
                require(stat.S_ISREG(i.external_attr>>16),'Non-regular archive member')
                file=z.read(i);expected=entry['files'][i.filename]
                require(len(file)==expected['size'] and sha(file)==expected['sha256'],'File identity mismatch')
            deb=z.read('share/embedded-api/termux-api.deb')
            old=next(e for e in previous['assets'] if e['name'].startswith('termux-api_') and e['name'].endswith('_'+expected_abis[abi]+'.deb'))
            require(sha(deb)==old['sha256'],'Public r1 deb differs: '+abi)
    for name in ['source-lock.json','validation.json','README.md']:require((a.assets/name).read_bytes()==(BASE/name).read_bytes(),'Published metadata mismatch: '+name)
    source=lock['source_overlay'];path=a.assets/source['asset'];data=path.read_bytes()
    require(len(data)==source['size'] and sha(data)==source['sha256'],'Source overlay mismatch')
    with tarfile.open(path) as t:
        members=t.getmembers();require(all(m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts for m in members),'Unsafe source entry')
        require(len(members)==len(lock['source_overlay_files_sha256']),'Source count mismatch')
        require({m.name:sha(t.extractfile(m).read()) for m in members}==lock['source_overlay_files_sha256'],'Source file hash mismatch')
    for line in (a.assets/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);require(Path(name).name==name,'Unsafe checksum name');require(sha((a.assets/name).read_bytes())==digest,'Checksum mismatch: '+name)
    print('External API catalog, four ABI companions, source overlay and fixed r1 debs verified.')
if __name__=='__main__':main()
