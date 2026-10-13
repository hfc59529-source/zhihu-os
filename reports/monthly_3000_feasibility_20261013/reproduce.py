"""Read local observations, reconcile latest export, write only this audit directory."""
import csv, json, hashlib
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
source=ROOT/'data/revenue_observations.csv'
with source.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
rows=[dict(r,source_line=i+2) for i,r in enumerate(rows) if (r['revenue_window_start'],r['revenue_window_end'])==('2026-09-09','2026-10-07')]
raw=ROOT/'data/raw_exports/zhihu_knowledge_income_detail_20261008_20260909_20261007_browser.csv'
with raw.open(encoding='utf-8-sig',newline='') as f: original=list(csv.DictReader(f))
def key(r): return r['content_title'],r['content_type'],r['published_date']
assert len(rows)==47 and len({key(r) for r in rows})==47
expected={(r['内容'],r['内容类型'],r['内容发布时间']):(Decimal(r['本期阅读/观看量']),Decimal(r['本期收益']),Decimal(r['累计阅读/观看量']),Decimal(r['累计收益'])) for r in original}
assert len(original)==47 and len(expected)==47
for r in rows:
 assert tuple(Decimal(r[k]) for k in ('period_reads','period_revenue','cumulative_reads','cumulative_revenue'))==expected[key(r)]
rows.sort(key=lambda r:Decimal(r['period_revenue']),reverse=True)
total=sum(Decimal(r['period_revenue']) for r in rows)
with (OUT/'revenue_contribution.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['rank','source_line','content_title','content_type','published_date','period_reads','period_revenue_salt','reported_yuan','share_percent','publication_cohort','identity_status']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for i,r in enumerate(rows):
  w.writerow(dict(rank=i+1,source_line=r['source_line'],content_title=r['content_title'],content_type=r['content_type'],published_date=r['published_date'],period_reads=r['period_reads'],period_revenue_salt=r['period_revenue'],reported_yuan=Decimal(r['period_revenue'])/100,share_percent=round(Decimal(r['period_revenue'])/total*100,4),publication_cohort='BEFORE_WINDOW' if r['published_date']<'2026-09-09' else 'WITHIN_WINDOW',identity_status='SOURCE_TITLE_TYPE_DATE_ONLY'))
summary={'window':['2026-09-09','2026-10-07'],'inclusive_calendar_days':29,'rows':len(rows),'positive_rows':sum(Decimal(r['period_revenue'])>0 for r in rows),'total_salt':str(total),'reported_yuan':str(total/100),'reads':sum(int(r['period_reads']) for r in rows),'top_n_share_percent':{str(n):str(round(sum(Decimal(r['period_revenue']) for r in rows[:n])/total*100,4)) for n in (1,2,5,10)},'before_window_rows':sum(r['published_date']<'2026-09-09' for r in rows),'before_window_salt':str(sum(Decimal(r['period_revenue']) for r in rows if r['published_date']<'2026-09-09')),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,raw)},'raw_reconciliation':'47/47 PASS','target_yuan_scenario':3000,'baseline_calendar_month_reported_yuan':'49.09','target_to_baseline_ratio':str(round(Decimal(3000)/Decimal('49.09'),4)),'cash_cost':'UNKNOWN','labor_hours':'UNKNOWN','net_profit':'UNKNOWN','repeatability':'UNKNOWN'}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
