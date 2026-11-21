from pathlib import Path
import math
root=Path(__file__).resolve().parents[4]
d=root/"analyses/visualizer/accessibility-review/inputs"
rotations={"rot-x90":((1,0,0),(0,0,-1),(0,1,0)),"rot-y90":((0,0,1),(0,1,0),(-1,0,0))}
for name in ["route01-ethyl-4-nitrobenzoate-conf1.sdf","route05-p-aminobenzoic-acid-conf4.sdf"]:
 lines=(d/name).read_text(encoding="ascii").splitlines(); n=int(lines[3][:3]); xyz=[[float(lines[4+i][j:j+10]) for j in (0,10,20)] for i in range(n)]; c=[sum(x[k] for x in xyz)/n for k in range(3)]
 for label,m in rotations.items():
  out=lines.copy()
  for i,p in enumerate(xyz):
   q=[sum(m[a][b]*(p[b]-c[b]) for b in range(3))+c[a] for a in range(3)]; out[4+i]=f"{q[0]:10.4f}{q[1]:10.4f}{q[2]:10.4f}"+lines[4+i][30:]
  target=d/(Path(name).stem+"-"+label+".sdf"); target.write_text("\n".join(out)+"\n",encoding="ascii")
