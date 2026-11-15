"""Read-only tree/asset comparison against an explicitly supplied baseline."""
import argparse
import os
from pathlib import Path
from _runtime import ROOT,load,save,digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',required=True,type=Path,help='directory whose preservation is being audited')
    p.add_argument('--before-manifest',required=True,type=Path,help='JSON file-to-size/mtime mapping captured before work')
    p.add_argument('--asset-manifest',type=Path,help='optional JSON relative-path-to-SHA256 mapping')
    p.add_argument('--output',type=Path,default=ROOT/'validation'/'preservation-final.json')
    a=p.parse_args(); source=a.source_root.resolve(); before=load(a.before_manifest); current={}
    for folder,dirs,names in os.walk(source):
        for name in names:
            f=Path(folder)/name; st=f.stat(); current[f.relative_to(source).as_posix()]={'size':st.st_size,'mtime_ns':st.st_mtime_ns}
    changed=[n for n,v in before.items() if current.get(n)!=v]; added=sorted(set(current)-set(before)); missing=sorted(set(before)-set(current))
    assets=load(a.asset_manifest) if a.asset_manifest else {}; bad_assets=[n for n,sha in assets.items() if not (source/n).is_file() or digest(source/n)!=sha]
    save(a.output,{'status':'passed' if not changed and not added and not bad_assets else 'failed','source_root':str(source),'source_files_checked':len(before),'changed_or_missing':sorted(set(changed+missing)),'new_files_in_source_tree':added,'asset_hashes_checked':len(assets),'changed_asset_hashes':bad_assets,'scope':'Read-only tree size/mtime comparison and optional SHA256 checks'})
    print('Changed/missing:',len(set(changed+missing)),'new:',len(added),'asset hash mismatches:',len(bad_assets))
if __name__=='__main__': main()
