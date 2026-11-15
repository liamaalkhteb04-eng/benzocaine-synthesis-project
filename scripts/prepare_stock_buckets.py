"""Derive an exact disk stock from literal InChIKeys in the existing HDF pickle.

No unpickling a 17-million-string Python array. The validated literal count must
match the original row count; no subset/approximate stock is silently accepted.
"""
import argparse
from pathlib import Path
import re
import string
from _runtime import save,digest

def main():
    import tables
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=False)
    prefix=rb'(?:X\x1b\x00\x00\x00|\x8c\x1b|C\x1b|U\x1b|T\x1b\x00\x00\x00)'
    pattern=re.compile(prefix+rb'([A-Z]{14}-[A-Z]{10}-[A-Z])')
    handles={c:open(a.output_dir/(c+'.keys'),'xb',buffering=1024*1024) for c in string.ascii_uppercase}
    count=0;samples=[]
    try:
        with tables.open_file(str(a.source),mode='r') as f:
            expected=int(f.root.table.axis1.shape[0])
            # Read raw serialized bytes rather than VLArray's ObjectAtom.fromarray.
            raw=f.root.table.block0_values._read_array(0,1,1)[0]
            print('Raw serialized bytes:',raw.nbytes,'expected rows:',expected,flush=True)
            for match in pattern.finditer(memoryview(raw)):
                key=match.group(1);handles[chr(key[0])].write(key+b'\n');count+=1
                if count<=5:samples.append(key.decode())
                if count%2000000==0:print('Extracted real keys:',count,flush=True)
        if count!=expected:raise ValueError(f'Literal extraction completeness not proven: {count} != {expected}')
    finally:
        for h in handles.values():h.close()
    files={p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in a.output_dir.glob('*.keys')}
    assert sum(x['bytes'] for x in files.values())==28*count
    save(a.output_dir/'manifest.json',{'status':'validated','source_path':str(a.source.resolve()),'source_sha256':digest(a.source),'source_rows':expected,'extracted_rows':count,'record_bytes':28,'literal_pattern':pattern.pattern.decode('ascii'),'samples':samples,'files':files,'semantics':'Exact original InChIKey literals partitioned by first letter; no stock subset or Bloom approximation','tables_version':tables.__version__})
    print('Exact disk stock ready:',count,flush=True)

if __name__=='__main__':main()
