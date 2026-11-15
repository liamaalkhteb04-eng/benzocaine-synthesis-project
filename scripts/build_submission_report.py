"""Explicit future authoring or genuine-response document rebuild, never automatic."""
import argparse
from pathlib import Path
import subprocess
import sys
from _runtime import ROOT,load,save
from validate_report_content import check_content

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--attempt-id');g.add_argument('--reuse-attempt-dir',type=Path)
    p.add_argument('--execute-solar',action='store_true');a=p.parse_args();plan=load(ROOT/'configs/report-plan.json')
    if a.attempt_id and not plan['report_generation_authorized']:p.error('Fresh report generation is not authorized in the current phase')
    if a.output_dir.exists():p.error('Preserve previous output; choose a new directory')
    def invoke(cmd):subprocess.run(list(map(str,cmd)),cwd=ROOT,check=True)
    if a.attempt_id:
        if not a.execute_solar:p.error('Fresh authoring requires --execute-solar')
        invoke([sys.executable,'-B',ROOT/'scripts/generate_report.py','--run-dir',a.run_dir,'--attempt-id',a.attempt_id,'--execute-solar']);attempt=a.run_dir/'solar-attempts'/a.attempt_id
    else:attempt=a.reuse_attempt_dir
    status=load(attempt/'solar-status.json');raw=load(attempt/'solar-response.raw.json')
    assert status['status']=='success' and raw['model'].startswith('solar-pro4')
    text=raw['choices'][0]['message']['content'];check=check_content(text,load(a.run_dir/'report-evidence.json'));assert not check['errors'],check['errors']
    a.output_dir.mkdir(parents=True);md=a.output_dir/'report.md';md.write_bytes(text.encode('utf-8'));save(a.output_dir/'content-validation.json',check)
    invoke([sys.executable,ROOT/'scripts/export_report_docx.py','--run-dir',a.run_dir,'--markdown',md,'--solar-status',attempt/'solar-status.json'])
    invoke(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'scripts/convert_docx_to_pdf.ps1','-DocxPath',md.with_suffix('.docx'),'-PdfPath',md.with_suffix('.pdf'),'-MetadataPath',a.output_dir/'word-export.json'])
    invoke([sys.executable,ROOT/'scripts/validate_report_documents.py','--report-dir',a.output_dir,'--attempt-dir',attempt,'--run-dir',a.run_dir])

if __name__=='__main__':main()
