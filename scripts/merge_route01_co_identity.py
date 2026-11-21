"""Apply a verified Solar route-01 CO identity block without retaining its stale conflicting sentence."""
import argparse, hashlib, json
from pathlib import Path

START = "BEGIN_ROUTE01_CO_IDENTITY_SENTENCE"
END = "END_ROUTE01_CO_IDENTITY_SENTENCE"
OLD = "`CCO`\uB294 \uC5D0\uD0C4\uC62C \uAD6C\uC870 \uD1A0\uD070\uC774\uACE0, `CO`\uB294 \uC77C\uC0B0\uD654\uD0C4\uC18C \uAD6C\uC870 \uD1A0\uD070\uC774\uB2E4."
CORRECT_ANCHOR = "`solvent1=CO`\uB294 \uB2E8\uC77C \uAD6C\uC870 \uD1A0\uD070\uC774\uBA70, \uAC80\uC99D\uB41C \uAD6C\uC870 \uD574\uC11D\uC740 \uBA54\uD0C4\uC62C"

def sha(data): return hashlib.sha256(data).hexdigest()
def extract(text):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Solar identity block markers are not unique")
    block = text.split(START, 1)[1].split(END, 1)[0].strip()
    if not block.startswith(CORRECT_ANCHOR) or "[D12]" not in block:
        raise ValueError("Saved Solar block is not the validated CO-to-methanol identity block")
    return block

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', required=True, type=Path)
    ap.add_argument('--solar-response', required=True, type=Path)
    ap.add_argument('--preserved-blocks', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--manifest', required=True, type=Path)
    a=ap.parse_args()
    source_bytes=a.source.read_bytes(); source=source_bytes.decode('utf-8-sig')
    response_bytes=a.solar_response.read_bytes(); response=json.loads(response_bytes.decode('utf-8-sig'))
    preserved=json.loads(a.preserved_blocks.read_text(encoding='utf-8-sig'))
    record=next(x for x in preserved['blocks'] if x.get('block_id')=='ROUTE01_CO_IDENTITY_SENTENCE')
    expected_response_hash=record['source_response_sha256']
    if sha(response_bytes)!=expected_response_hash:
        raise SystemExit('Solar response hash does not match preserved-block provenance')
    exact=record['exact_text']
    if sha(exact.encode('utf-8'))!=record['text_sha256']:
        raise SystemExit('Preserved Solar block hash mismatch')
    saved=extract(exact)
    solar_text=response['choices'][0]['message']['content']
    if extract(solar_text)!=saved:
        raise SystemExit('Preserved block differs from original Solar response')
    # Locate exactly one route-01 explanatory paragraph and replace/remove only the stale conflicting sentence.
    paragraphs=source.split('\n\n')
    candidates=[i for i,p in enumerate(paragraphs) if OLD in p and CORRECT_ANCHOR in p]
    if len(candidates)!=1:
        raise SystemExit(f'Expected one route-01 paragraph containing both correction and stale sentence; found {len(candidates)}')
    i=candidates[0]; before=paragraphs[i]
    if before.count(OLD)!=1 or before.count(saved)!=1:
        raise SystemExit('Expected one stale sentence and one verified Solar block in route-01 paragraph')
    after=before.replace(OLD,'',1)
    if after.count(saved)!=1:
        raise SystemExit('Corrected Solar block was lost or duplicated')
    paragraphs[i]=after
    merged='\n\n'.join(paragraphs)
    if OLD in merged:
        raise SystemExit('Stale CO=carbon monoxide sentence remains in report')
    if merged.count(saved)!=source.count(saved):
        raise SystemExit('Verified Solar sentence occurrence count changed unexpectedly')
    if a.output.exists(): raise SystemExit('Output exists; refusing overwrite')
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(merged,encoding='utf-8',newline='\n')
    manifest={'status':'passed','change':'removed stale CO=carbon monoxide sentence because the same paragraph already contains the verified Solar CO=methanol block','source_report_path':str(a.source.resolve()),'source_report_sha256':sha(source_bytes),'solar_response_path':str(a.solar_response.resolve()),'solar_response_sha256':sha(response_bytes),'preserved_blocks_path':str(a.preserved_blocks.resolve()),'preserved_block_id':record['block_id'],'preserved_block_sha256':record['text_sha256'],'old_sentence_count_before':source.count(OLD),'old_sentence_count_after':merged.count(OLD),'correct_solar_block_count_before':source.count(saved),'correct_solar_block_count_after':merged.count(saved),'changed_paragraphs':1,'all_other_markdown_text_unchanged':source.replace(before,after,1)==merged,'solar_text_rewritten':False,'new_scientific_text_authored':False,'merged_report_sha256':sha(merged.encode('utf-8'))}
    a.manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=True,indent=2))
if __name__=='__main__': main()