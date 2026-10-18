#!/usr/bin/env python3
"""Persistent evidence index implementation. Invoked through data/store.sh."""
import hashlib, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
INDEX=ROOT/'data'/'evidence'/'index.json'
def records(stream): return [json.loads(line) for line in stream if line.strip()]
def emit(rows):
    for row in rows: print(json.dumps(row,ensure_ascii=False,separators=(',',':')))
def save(db):
    INDEX.parent.mkdir(parents=True,exist_ok=True); INDEX.write_text(json.dumps(db,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def main(args):
    if not args: raise ValueError('Usage: store.py init|upsert RUN_DIR|list|get ITEM_ID [VERSION_ID]')
    op=args[0]
    if op=='init':
        if not INDEX.exists(): save({'items':{}})
        return
    if not INDEX.exists(): raise ValueError('Evidence store is not initialized')
    db=json.loads(INDEX.read_text(encoding='utf-8'))
    if op=='list': emit([entry['versions'][-1]['item'] for entry in db['items'].values()]); return
    if op=='get':
        if len(args)<2: raise ValueError('get ITEM_ID [VERSION_ID]')
        entry=db['items'].get(args[1]); versions=entry['versions'] if entry else []
        found=next((v for v in versions if len(args)<3 or v['item']['version_id']==args[2]),None)
        if not found: print('Item/version not found',file=sys.stderr); sys.exit(1)
        emit([found['item']]); return
    if op=='upsert':
        if len(args)<2: raise ValueError('upsert RUN_DIR required')
        changes=[]
        for item in records(sys.stdin):
            item=dict(item)
            if not item.get('version_id'):
                data={k:v for k,v in item.items() if k not in ('version_id','retrieved_at')}
                item['version_id']=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            entry=db['items'].setdefault(item['item_id'],{'versions':[]})
            previous=entry['versions'][-1]['item'] if entry['versions'] else None
            change='new' if previous is None else ('unchanged' if previous['version_id']==item['version_id'] else 'changed')
            if change!='unchanged': entry['versions'].append({'run_id':pathlib.Path(args[1]).name,'item':item})
            changes.append({'item_id':item['item_id'],'version_id':item['version_id'],'change':change})
        save(db); emit(changes); return
    raise ValueError('Unknown store command: '+op)
if __name__=='__main__':
    try: main(sys.argv[1:])
    except Exception as exc: print(f'ERROR: {exc}',file=sys.stderr); sys.exit(2)
