"""Initialize empty project directories and check model configuration prerequisites."""
import argparse
from pathlib import Path
import json
import os
import re
from _runtime import ROOT

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-root',type=Path,default=ROOT)
    a=p.parse_args(); root=a.project_root.resolve()
    for name in ('skill','inputs','configs','results','reports','validation','plans','tests','analyses'):
        (root/name).mkdir(parents=True,exist_ok=True)
    required=[root/'skill'/'synthesis_report_skill.md',root/'inputs'/'input-template.json',root/'configs'/'runtime.json']
    missing=[str(x) for x in required if not x.is_file()]
    unresolved=set()
    pattern=re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
    def scan(value):
        if isinstance(value,str):
            for name in pattern.findall(value):
                if name != 'PROJECT_ROOT' and not os.environ.get(name): unresolved.add(name)
        elif isinstance(value,dict):
            for child in value.values(): scan(child)
        elif isinstance(value,list):
            for child in value: scan(child)
    config_dir=root/'configs'
    for config_path in sorted(config_dir.glob('*.json')):
        try: scan(json.loads(config_path.read_text(encoding='utf-8')))
        except (OSError,json.JSONDecodeError): continue
    print(json.dumps({'project_root':str(root),'directories_initialized':True,'missing_required_files':missing,'runtime_placeholders_need_environment_or_config':sorted(unresolved),'external_project_read':False},ensure_ascii=False,indent=2))
    return 1 if missing else 0
if __name__=='__main__': raise SystemExit(main())
