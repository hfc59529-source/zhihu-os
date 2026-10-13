"""Read-only source audit; writes only adjacent audit outputs. Run from any directory."""
import csv, hashlib, json, collections, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
missing = {'', 'UNKNOWN', 'NA', 'N/A', 'NULL'}
records = []
for base in ('data', 'reports', 'runtime/logs'):
 for p in sorted((ROOT / base).rglob('*.csv')):
  with p.open(encoding='utf-8-sig', newline='') as f:
   reader = csv.DictReader(f); rows = list(reader); fields = reader.fieldnames or []
  records.append({'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'rows':len(rows), 'fields':fields, 'missing_by_field':{k:sum(str(r.get(k,'')).strip().upper() in missing for r in rows) for k in fields}, 'exact_duplicate_rows':len(rows)-len({json.dumps(r,sort_keys=True,ensure_ascii=False) for r in rows})})
def read(name):
 with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
spec=importlib.util.spec_from_file_location('audit_learning_loop',ROOT/'scripts/learning_loop.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
pubs=list(module.publications(ROOT)); l0=read('data/l0_content_assets.csv'); rev=read('data/revenue_observations.csv'); snaps=read('data/review_data_snapshots.csv')
keys=['revenue_window_start','revenue_window_end','content_title','content_type','published_date']
counts=collections.Counter(tuple(r[k] for k in keys) for r in rev)
summary={'audit_date':'2026-10-13 Africa/Nairobi','csv_inventory':records,'scripts':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'scripts').glob('*.py'))], 'publication_rows':len(pubs),'exact_publication_times':sum(t is not None for _,t in pubs),'l0_mapped':len({r['article_id'] for r in l0}&{p['article_id'] for p,_ in pubs}),'snapshot_unique_articles':len({r['article_id'] for r in snaps}),'task_status_counts':dict(collections.Counter(r['task_status'] for r in module.tasks(ROOT,module.timestamp('2026-10-13T00:00:00+03:00')))),'revenue_business_key_duplicate_excess':sum(v-1 for v in counts.values() if v>1),'revenue_batches':[dict(zip(['start','end','observation_time','rows'],(*k,v))) for k,v in sorted(collections.Counter((r['revenue_window_start'],r['revenue_window_end'],r['observation_time']) for r in rev).items())]}
(OUT/'inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['csv_inventory','scripts','revenue_batches']},ensure_ascii=False,indent=2))
print('CSV files:',len(records))
