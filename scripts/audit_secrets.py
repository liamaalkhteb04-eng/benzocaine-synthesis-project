"""Scan files and actual Git-index blobs without printing secret values or matching lines."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
from _runtime import save

PATTERNS = {
 "github_token": rb"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,})\b",
 "upstage_token": rb"\bup_[A-Za-z0-9_-]{24,}\b",
 "aws_access_key": rb"\bAKIA[0-9A-Z]{16}\b",
 "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
}


def known_secrets(env_path):
    values=[]
    if env_path and env_path.is_file():
        for line in env_path.read_text(encoding="utf-8-sig").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                name,value=line.split("=",1);value=value.strip().strip("\"'")
                if re.search(r"KEY|TOKEN|SECRET|PASSWORD",name,re.I) and len(value)>=12:values.append(value.encode())
    for name,value in os.environ.items():
        if re.search(r"(?:API_KEY|ACCESS_TOKEN|SECRET_KEY)$",name) and len(value)>=12:values.append(value.encode())
    return list(set(values))


def inspect(data,label,secrets):
    findings=[]
    for value in secrets:
        if value in data:findings.append({"path":label,"category":"known_private_value"})
    for name,pattern in PATTERNS.items():
        if re.search(pattern,data):findings.append({"path":label,"category":name})
    # Quoted hardcoded values; environment lookups and empty/template placeholders are not secrets.
    assignment=rb'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)["']?\s*[:=]\s*["']([^"'\r\n]{20,})["']'''
    for match in re.finditer(assignment,data):
        value=match.group(1)
        if any(word in value.lower() for word in [b"example",b"your_",b"placeholder",b"os.environ",b"process.env",b"getenv",b"<token>"]):continue
        if b" " not in value and not value.startswith((b"$",b"http",b"path/")):
            findings.append({"path":label,"category":"possible_hardcoded_credential","line":data[:match.start()].count(b"\n")+1})
    return findings


def git_index(repo,secrets):
    top=subprocess.run(["git","-C",str(repo),"rev-parse","--show-toplevel"],capture_output=True)
    if top.returncode:return {"repository":str(repo),"is_git_repository":False,"tracked_files":0,"findings":[],"history_scanned":False}
    listing=subprocess.run(["git","-C",str(repo),"ls-files","--stage","-z"],capture_output=True,check=True).stdout
    entries=[]
    for line in listing.split(b"\0"):
        if not line:continue
        head,name=line.split(b"\t",1);mode,sha,stage=head.split()
        if mode==b"160000":continue
        entries.append((sha,name.decode("utf-8")))
    findings=[];total=0
    for start in range(0,len(entries),25):
        batch=entries[start:start+25]
        output=subprocess.run(["git","-C",str(repo),"cat-file","--batch"],input=b"\n".join(x[0] for x in batch)+b"\n",capture_output=True,check=True).stdout
        pos=0
        for _,name in batch:
            end=output.index(b"\n",pos);header=output[pos:end].split();size=int(header[-1]);pos=end+1
            data=output[pos:pos+size];pos+=size+1;total+=size
            findings.extend(inspect(data,name,secrets))
    return {"repository":str(repo),"is_git_repository":True,"tracked_files":len(entries),"indexed_bytes_scanned":total,"findings":findings,"history_scanned":False,"scope":"Actual current index blobs, including content differing from the working tree"}


def scan_tree(root,secrets):
    findings=[];count=0;size=0
    for directory,dirs,files in os.walk(root):
        dirs[:]=[d for d in dirs if d!=".git"]
        for name in files:
            path=Path(directory)/name;data=path.read_bytes();count+=1;size+=len(data)
            findings.extend(inspect(data,str(path.relative_to(root)),secrets))
            if name.endswith(".docx"):
                import zipfile
                with zipfile.ZipFile(path) as archive:
                    for part in archive.namelist():
                        if part.endswith(".xml"):findings.extend(inspect(archive.read(part),str(path.relative_to(root))+":"+part,secrets))
    return {"files_scanned":count,"bytes_scanned":size,"findings":findings}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--env-file",type=Path);p.add_argument("--tree",type=Path);p.add_argument("--git-repo",type=Path,action="append",default=[]);p.add_argument("--output",type=Path,required=True)
    args=p.parse_args();secrets=known_secrets(args.env_file)
    record={"known_private_values_available_for_exact_match":bool(secrets),"values_or_matching_lines_output":False}
    if args.tree:record["tree_scan"]=scan_tree(args.tree,secrets)
    record["git_index_scans"]=[git_index(repo,secrets) for repo in args.git_repo]
    groups=record["git_index_scans"]+([record["tree_scan"]] if "tree_scan" in record else [])
    count=sum(len(group["findings"]) for group in groups);record["status"]="passed" if not count else "findings_require_review"
    save(args.output,record)
    print(json.dumps({"status":record["status"],"finding_count":count,"git_tracked_counts":[g.get("tracked_files",0) for g in record["git_index_scans"]],"output":str(args.output)}))
    return 0 if not count else 2


if __name__=="__main__":raise SystemExit(main())
