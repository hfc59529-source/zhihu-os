"""Read-only account revenue analysis. Outputs JSON beside this script."""
import csv,json,hashlib
from collections import defaultdict
from decimal import Decimal as D
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
P='data/revenue_observations.csv'
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rows=[dict(r,source_line=i+2) for i,r in enumerate(read(P))]
key=lambda r:(r['content_title'],r['content_type'],r['published_date'])
windows=[('2026-07-01','2026-07-30'),('2026-08-16','2026-09-14'),('2026-09-09','2026-10-07')]
batches=[{key(r):r for r in rows if (r['revenue_window_start'],r['revenue_window_end'])==w} for w in windows]
rawpaths=['data/raw_exports/zhihu_income_export_2026-07-01_2026-07-30.csv','data/raw_exports/zhihu_knowledge_income_detail_20260914_recent30_browser.csv','data/raw_exports/zhihu_knowledge_income_detail_20261008_20260909_20261007_browser.csv']
reconciliation=[]
for b,p in zip(batches,rawpaths):
 raw=read(p); chinese='内容' in raw[0]
 src={((r['内容'],r['内容类型'],r['内容发布时间']) if chinese else key(r)):tuple(D(r[k]) for k in (['本期阅读/观看量','本期收益','累计阅读/观看量','累计收益'] if chinese else ['period_reads','period_revenue','cumulative_reads','cumulative_revenue'])) for r in raw}
 assert len(src)==len(raw)==len(b)
 assert all(tuple(D(r[k]) for k in ['period_reads','period_revenue','cumulative_reads','cumulative_revenue'])==src[k0] for k0,r in b.items())
 reconciliation.append(dict(path=p,rows=len(raw),status='PASS'))
def stats(b,w):
 rs=list(b.values());s=sum(D(r['period_revenue']) for r in rs);reads=sum(int(r['period_reads']) for r in rs)
 new=sum(D(r['period_revenue']) for r in rs if w[0]<=r['published_date']<=w[1]);old=sum(D(r['period_revenue']) for r in rs if r['published_date']<w[0])
 assert new+old==s
 return dict(window=list(w),days=(date.fromisoformat(w[1])-date.fromisoformat(w[0])).days+1,rows=len(rs),salt=str(s),reads=reads,new_salt=str(new),old_salt=str(old),read_earnings_alignment='UNKNOWN',account_total_reconciliation='UNKNOWN')
a,b=batches[:2];common=a.keys()&b.keys();before_only=a.keys()-b.keys();after_only=b.keys()-a.keys()
sum_s=lambda batch,ks:sum(D(batch[k]['period_revenue']) for k in ks)
bridge=dict(before_salt=str(sum_s(a,a)),after_salt=str(sum_s(b,b)),common_count=len(common),common_before_salt=str(sum_s(a,common)),common_after_salt=str(sum_s(b,common)),common_delta_salt=str(sum_s(b,common)-sum_s(a,common)),before_only_count=len(before_only),before_only_before_salt=str(sum_s(a,before_only)),after_only_count=len(after_only),after_only_after_salt=str(sum_s(b,after_only)),after_only_post_prior_window_salt=str(sum_s(b,[k for k in after_only if k[2]>windows[0][1]])),after_only_preexisting_salt=str(sum_s(b,[k for k in after_only if k[2]<=windows[0][1]])),interpretation='EXPORT_MEMBERSHIP_BRIDGE_NOT_TRUE_ENTRIES_OR_EXITS')
assert sum_s(b,b)-sum_s(a,a)==sum_s(b,common)-sum_s(a,common)+sum_s(b,after_only)-sum_s(a,before_only)
by=defaultdict(list)
for r in rows:by[key(r)].append(r)
latest=sorted(batches[2].values(),key=lambda r:D(r['period_revenue']),reverse=True)
latest_records=[]
for r in latest:
 history=sorted(by[key(r)],key=lambda x:(x['revenue_window_end'],x['revenue_window_start']))
 disjoint=[];last=None
 for h in history:
  if D(h['period_revenue'])>0 and (last is None or h['revenue_window_start']>last):
   disjoint.append([h['revenue_window_start'],h['revenue_window_end']]);last=h['revenue_window_end']
 latest_records.append(dict(title=r['content_title'],published_date=r['published_date'],source_line=r['source_line'],period_reads=r['period_reads'],period_salt=r['period_revenue'],read_earnings_alignment='UNKNOWN',quadrant='UNCLASSIFIED_ALIGNMENT_UNKNOWN',positive_disjoint_windows=disjoint,repeat_positive_evidence=len(disjoint)>=2,identity='TITLE_TYPE_DATE_CANDIDATE',history=[dict(window=[h['revenue_window_start'],h['revenue_window_end']],reads=h['period_reads'],salt=h['period_revenue'],source_line=h['source_line']) for h in history]))
changes=sorted([dict(title=k[0],published_date=k[2],before_salt=a[k]['period_revenue'],after_salt=b[k]['period_revenue'],delta_salt=str(D(b[k]['period_revenue'])-D(a[k]['period_revenue'])),before_reads=a[k]['period_reads'],after_reads=b[k]['period_reads']) for k in common],key=lambda x:D(x['delta_salt']))
result=dict(source_observations=len(rows),reconciliation=reconciliation,window_summaries=[stats(b,w) for b,w in zip(batches,windows)],bridge=bridge,common_content_changes=changes,latest_records=latest_records,latest_repeat_positive_count=sum(r['repeat_positive_evidence'] for r in latest_records),quadrant_counts={'UNCLASSIFIED_ALIGNMENT_UNKNOWN':len(latest)},hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [P,*rawpaths]})
(OUT/'account_evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['latest_records','hashes','common_content_changes']},ensure_ascii=False,indent=2))
