"""Exact InChIKey membership using bounded-memory mmap buckets."""
from pathlib import Path
import mmap
from aizynthfinder.context.stock.queries import StockQueryMixin
from _runtime import load

class DiskInchiStock(StockQueryMixin):
    def __init__(self,path):
        self.path=Path(path);self.meta=load(self.path/'manifest.json')
        if self.meta['status']!='validated':raise ValueError('Unvalidated stock derivation')
        self.handles={};self.maps={};self.cache={}
        for p in self.path.glob('*.keys'):
            if p.stat().st_size:
                h=p.open('rb');self.handles[p.stem]=h;self.maps[p.stem]=mmap.mmap(h.fileno(),0,access=mmap.ACCESS_READ)
    def __len__(self):return self.meta['source_rows']
    def __contains__(self,mol):
        key=mol.inchi_key
        if key not in self.cache:
            bucket=self.maps.get(key[:1]);needle=key.encode('ascii')+b'\n'
            offset=bucket.find(needle) if bucket is not None else -1
            self.cache[key]=offset>=0 and offset%28==0
        return self.cache[key]
