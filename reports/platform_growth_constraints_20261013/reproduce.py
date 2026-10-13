import csv,json,hashlib
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
paths=['data/revenue_observations.csv','data/l0_content_assets.csv','data/production_article_map.csv','data/article_reasoning_features.csv']
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rev,l0,pubs,features=map(read,paths)
b=[dict(r,source_line=i+2) for i,r in enumerate(rev) if (r['revenue_window_start'],r['revenue_window_end'])==('2026-09-09','2026-10-07')]; b.sort(key=lambda r:D(r['period_revenue']),reverse=True)
def stats(rows):
 e=sum(D(r['period_revenue']) for r in rows);v=sum(int(r['period_reads']) for r in rows)
 return dict(rows=len(rows),reads=v,salt=str(e),reported_yuan=str(e/100),reported_yuan_per_1000_reads=str(e*10/v) if v else 'UNKNOWN')
joins=[]
for i,r in enumerate(b):
 matches=[a for a in l0 if a['title']==r['content_title'] and a['content_type']==r['content_type']]
 aid=matches[0]['article_id'] if len(matches)==1 else 'UNKNOWN'
 joins.append(dict(rank=i+1,source_line=r['source_line'],title=r['content_title'],published_date=r['published_date'],candidate_article_id=aid,match_status='UNIQUE_TITLE_TYPE_CANDIDATE_NOT_VERIFIED_ID' if len(matches)==1 else 'UNRESOLVED',l0_published_display=matches[0]['published_at'] if len(matches)==1 else 'UNKNOWN',mapped_production_id=next((p['production_id'] for p in pubs if p['article_id']==aid),'UNKNOWN'),audited_structure_available=any(f['article_id']==aid for f in features)))
with (OUT/'candidate_content_links.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(joins[0]));w.writeheader();w.writerows(joins)
result={'scope':'PLATFORM_CONTENT_REVENUE_ONLY','window':['2026-09-09','2026-10-07'],'all':stats(b),'top10':stats(b[:10]),'remaining37':stats(b[10:]),'title_type_candidate_links':sum(x['candidate_article_id']!='UNKNOWN' for x in joins),'top10_audited_structure_links':sum(x['audited_structure_available'] for x in joins[:10]),'top10_mapped_production_links':sum(x['mapped_production_id']!='UNKNOWN' for x in joins[:10]),'source_hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
assert result['all']['rows']==47 and result['all']['salt']=='3695'
(OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
