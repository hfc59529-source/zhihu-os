"""Historical revenue-unit evidence, never extrapolate observed maxima as a ceiling."""
import csv,json,calendar,hashlib
from datetime import date
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
P='data/revenue_observations.csv'
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rs=[dict(r,source_line=i+2) for i,r in enumerate(read(P))]
key=lambda r:(r['content_title'],r['content_type'],r['published_date'])
def days(r):return (date.fromisoformat(r['revenue_window_end'])-date.fromisoformat(r['revenue_window_start'])).days+1
def month(r):
 s,e=date.fromisoformat(r['revenue_window_start']),date.fromisoformat(r['revenue_window_end'])
 return s.day==1 and s.year==e.year and s.month==e.month and e.day==calendar.monthrange(e.year,e.month)[1]
monthly=[r for r in rs if month(r)]; thirty=[r for r in rs if days(r)==30]
rawfiles=['data/raw_exports/zhihu_income_export_2026-06-01_2026-06-30.csv','data/raw_exports/zhihu_income_export_2026-07-01_2026-07-30.csv','data/raw_exports/zhihu_income_export_30d.csv','data/raw_exports/zhihu_knowledge_income_detail_20260914_recent30_browser.csv']
checks=[]
for p in rawfiles:
 raw=read(p);chinese='内容' in raw[0]
 target=[r for r in rs if r['source_file']==Path(p).name]
 if not target:
  window={'zhihu_income_export_30d.csv':('2026-07-12','2026-08-10'),'zhihu_knowledge_income_detail_20260914_recent30_browser.csv':('2026-08-16','2026-09-14')}[Path(p).name]
  target=[r for r in rs if (r['revenue_window_start'],r['revenue_window_end'])==window]
 source={((r['内容'],r['内容类型'],r['内容发布时间']) if chinese else key(r)):tuple(D(r[k]) for k in (['本期阅读/观看量','本期收益','累计阅读/观看量','累计收益'] if chinese else ['period_reads','period_revenue','cumulative_reads','cumulative_revenue'])) for r in raw}
 assert len(source)==len(raw)==len(target)
 assert all(tuple(D(r[k]) for k in ['period_reads','period_revenue','cumulative_reads','cumulative_revenue'])==source[key(r)] for r in target)
 checks.append(dict(path=p,rows=len(raw),status='PASS'))
best={}
for r in thirty:
 if key(r) not in best or D(r['period_revenue'])>D(best[key(r)]['period_revenue']):best[key(r)]=r
ordered=sorted(best.values(),key=lambda r:D(r['period_revenue']),reverse=True)
def disjoint(rows):
 chosen=[];end=None
 for r in sorted(rows,key=lambda r:(r['revenue_window_end'],r['revenue_window_start'])):
  if end is None or r['revenue_window_start']>end:chosen.append(r);end=r['revenue_window_end']
 return chosen
thresholds=[]
for yuan in [1,5,10,30,100]:
 ks={key(r) for r in thirty if D(r['period_revenue'])>=yuan*100}
 repeats=[k for k in ks if len(disjoint([r for r in thirty if key(r)==k and D(r['period_revenue'])>=yuan*100]))>=2]
 thresholds.append(dict(yuan=yuan,calendar_month_content_count=len({key(r) for r in monthly if D(r['period_revenue'])>=yuan*100}),thirty_day_content_count=len(ks),two_disjoint_thirty_day_content_count=len(repeats),repeat_titles=[k[0] for k in sorted(repeats)]))
units=[]
for r in ordered[:5]:
 history=sorted([x for x in rs if key(x)==key(r)],key=lambda x:(x['revenue_window_end'],x['revenue_window_start']))
 units.append(dict(title=r['content_title'],published_date=r['published_date'],highest_thirty_day_yuan=str(D(r['period_revenue'])/100),highest_window=[r['revenue_window_start'],r['revenue_window_end']],history=[dict(window=[x['revenue_window_start'],x['revenue_window_end']],days=days(x),is_calendar_month=month(x),reads=x['period_reads'],salt=x['period_revenue'],source_line=x['source_line']) for x in history]))
out=dict(observations=len(rs),calendar_windows=sorted({(r['revenue_window_start'],r['revenue_window_end']) for r in monthly}),calendar_observed_max=max(monthly,key=lambda r:D(r['period_revenue'])),thirty_day_unique_content_count=len(best),thresholds=thresholds,top_units=units,raw_reconciliation=checks,source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [P,*rawfiles]})
assert out['calendar_observed_max']['period_revenue']=='12647'
(OUT/'revenue_units_evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['top_units','source_hashes','calendar_observed_max']},ensure_ascii=False,indent=2))
