from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[4]
src=root/"analyses/visualizer/inputs"
out=root/"analyses/visualizer/accessibility-review/inputs"
spec={
 "ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf":{1:"route01-ethyl-4-nitrobenzoate-conf1.sdf",2:"route01-ethyl-4-nitrobenzoate-conf2.sdf"},
 "benzocaine-mopac-pm7-conformers.sdf":{1:"route01-benzocaine-product-conf1.sdf"},
 "p-aminobenzoic-acid-mopac-pm7-conformers.sdf":{4:"route05-p-aminobenzoic-acid-conf4.sdf"},
 "ethanol-mopac-pm7-conformers.sdf":{2:"route05-ethanol-conf2.sdf"},
}
for file,selected in spec.items():
 data=(src/file).read_bytes(); records=[r for r in data.split(b"$$$$") if r.strip()]
 for i,name in selected.items():
  rec=records[i-1].strip()+b"\n$$$$\n"; target=out/name; target.write_bytes(rec)
  print(name,hashlib.sha256(rec).hexdigest())
